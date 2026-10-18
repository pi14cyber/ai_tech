#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка полноты внешнего исследования.

Зачем: запрос уходит наружу десятками вопросов, ответ приходит прозой. Без
машинной сверки невозможно понять, на что ответили, а что тихо пропустили.

Основание приёмов: сверка декларации и исполнителя в обе стороны и контракт
кодов возврата 0/1/2 — netresearch/agent-harness-skill, verify-harness.sh:336-362,
:788-794.

Как устроено:

- В запросе каждый вопрос помечен идентификатором вида Q1.1.
- Ответ приходит файлом <имя запроса>.answer.md с блоками по тем же идентификаторам.
- Скрипт сверяет три вещи: все ли идентификаторы из запроса есть в ответе; нет ли
  лишних идентификаторов; в каждом блоке ответа есть ссылка или пометка белого пятна.

Коды возврата: 0 — всё сходится или ответов ещё нет; 1 — расхождения в ответе;
2 — сломан запрос: идентификаторов не найдено.
"""

import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ_DIR = os.path.join(ROOT, "internal", "draft", "requests")
RESP_DIR = os.path.join(ROOT, "internal", "draft", "responses")

ID_RE = re.compile(r"^(?:#{2,6}\s*|\*\*)?(Q\d+\.\d+)\b", re.MULTILINE)
ANY_ID_RE = re.compile(r"\bQ\d+\.\d+\b")
SECTIONS = ("Факты за", "Факты против", "Белые пятна")
WHITE_MARK = "не удалось"


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def find_response(name):
    if not os.path.isdir(RESP_DIR):
        return None
    for candidate in sorted(os.listdir(RESP_DIR)):
        if candidate.startswith(name) and candidate.endswith(".md"):
            return os.path.join(RESP_DIR, candidate)
    return None


def blocks(text, ids):
    """Нарезает текст ответа на блоки по идентификаторам."""
    positions = []
    for m in ANY_ID_RE.finditer(text):
        positions.append((m.start(), m.group(0)))
    out = {}
    for i, (pos, qid) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        out.setdefault(qid, text[pos:end])
    return out


def main():
    broken = []
    problems = []
    waiting = []
    total_q = 0
    answered = 0

    if not os.path.isdir(REQ_DIR):
        broken.append("нет папки запросов: %s" % REQ_DIR)
    else:
        requests = [f for f in sorted(os.listdir(REQ_DIR)) if f.endswith(".md")]
        if not requests:
            broken.append("в папке запросов нет ни одного файла")
        for name in requests:
            req_path = os.path.join(REQ_DIR, name)
            req_text = read(req_path)
            req_ids = [m.group(1) for m in ID_RE.finditer(req_text)]
            if not req_ids:
                broken.append("в запросе %s не найдено ни одного идентификатора Qn.n" % name)
                continue
            req_ids = list(dict.fromkeys(req_ids))
            total_q += len(req_ids)

            base = name[:-3]
            resp_path = find_response(base)
            if not resp_path:
                waiting.append("%s: вопросов %d, ответа нет" % (name, len(req_ids)))
                continue

            resp_text = read(resp_path)
            resp_ids = list(dict.fromkeys(ANY_ID_RE.findall(resp_text)))
            bl = blocks(resp_text, resp_ids)

            missing = [q for q in req_ids if q not in resp_ids]
            extra = [q for q in resp_ids if q not in req_ids]
            answered += len([q for q in req_ids if q in resp_ids])

            if missing:
                problems.append(
                    "%s: не отвечено на %d вопросов: %s"
                    % (os.path.basename(resp_path), len(missing), ", ".join(missing))
                )
            if extra:
                problems.append(
                    "%s: идентификаторы без вопроса в запросе: %s"
                    % (os.path.basename(resp_path), ", ".join(extra))
                )
            for section in SECTIONS:
                if section not in resp_text:
                    problems.append(
                        "%s: нет обязательного раздела «%s»" % (os.path.basename(resp_path), section)
                    )
            for qid in [q for q in req_ids if q in resp_ids]:
                body = bl.get(qid, "")
                if "http" not in body and WHITE_MARK not in body.lower():
                    problems.append(
                        "%s, блок %s: нет ни ссылки, ни пометки белого пятна"
                        % (os.path.basename(resp_path), qid)
                    )

            print(
                "%s → %s: вопросов %d, отвечено %d, ссылок %d"
                % (name, os.path.basename(resp_path), len(req_ids),
                   len([q for q in req_ids if q in resp_ids]), resp_text.count("http"))
            )

    print("")
    for line in waiting:
        print("ОЖИДАЕТ: %s" % line)
    for line in broken:
        print("ДЕКЛАРАЦИЯ: %s" % line)
    for line in problems:
        print("РАСХОЖДЕНИЕ: %s" % line)

    if total_q:
        print("\nвсего вопросов в запросах: %d, отвечено: %d" % (total_q, answered))

    if broken:
        print("\nИТОГ: 2 — сломан запрос, проверять нечего")
        return 2
    if problems:
        print("\nИТОГ: 1 — ответ неполный, вопросы уходят обратно в очередь")
        return 1
    if waiting:
        print("\nИТОГ: 0 — запросы отправлены, ответов пока нет")
        return 0
    print("\nИТОГ: 0 — все ответы полные")
    return 0


if __name__ == "__main__":
    sys.exit(main())
