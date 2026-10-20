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

Два слоя: проект — `kit/internal/draft/requests|responses`; человек —
`workspace/requests|responses`. Слой человека проверяется теми же правилами, в том
числе когда папки `kit/internal/` нет (основной режим набора). Папка `inbox/` в
корне — входящие файлы человека, к слою запросов она не относится. Если папок
запросов нет ни в одном слое — «проверять нечего» с кодом 0.

Коды возврата: 0 — всё сходится или ответов ещё нет; 1 — расхождения в ответе;
2 — сломан запрос: идентификаторов не найдено или нет папки запросов проекта.

Чего не проверяет: смысл вопросов и качество фактов (только наличие блока, ссылки
или честного белого пятна); что человек действительно отправил запрос — это
внешний факт, доступный только человеку.
"""

import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
ROOT = os.path.dirname(KIT)
INTERNAL = os.path.join(KIT, "internal")
LAYERS = (
    ("проект", os.path.join(INTERNAL, "draft", "requests"), os.path.join(INTERNAL, "draft", "responses")),
    ("человек", os.path.join(ROOT, "workspace", "requests"), os.path.join(ROOT, "workspace", "responses")),
)

ID_RE = re.compile(r"^(?:#{1,6}\s*)?(?:\*\*)?(?:Вопрос\s*)?(?:`)?(Q\d+\.\d+)\b", re.MULTILINE)
ANY_ID_RE = re.compile(r"\bQ\d+\.\d+\b")
OBSOLETE_RE = re.compile(r"^\*\*Статус:\*\*\s*неактуален", re.MULTILINE)
SECTIONS = ("Факты за", "Факты против", "Белые пятна")
ALT_SECTIONS = ("Источники", "Алгоритм словами", "Белые пятна")
WHITE_MARK = "не удалось"
MAX_QUESTIONS = 6


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def find_responses(name, resp_dirs):
    found = []
    for directory in resp_dirs:
        if not os.path.isdir(directory):
            continue
        for candidate in sorted(os.listdir(directory)):
            if candidate == name + ".answer.md" or candidate.startswith(name + "."):
                if candidate.endswith(".md"):
                    found.append(os.path.join(directory, candidate))
    return found


def blocks(text, ids):
    """Нарезает текст ответа на блоки по заголовкам идентификаторов.

    Считаются только заголовки (начало строки), а не упоминания в шапке файла:
    иначе перечисление идентификаторов в списке «вопросы пакета» выглядит как
    отвеченный блок.
    """
    positions = []
    for m in ID_RE.finditer(text):
        positions.append((m.start(), m.group(1)))
    out = {}
    for i, (pos, qid) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        out.setdefault(qid, text[pos:end])
    return out


def check_layer(label, req_dir, resp_dir, strict, problems, waiting, obsolete, broken):
    """Проверяет один слой. Возвращает (вопросов, отвечено) или None, если слоя нет."""
    prefix = "" if label == "проект" else "[человек] "
    if not os.path.isdir(req_dir):
        return None
    arch_dir = os.path.join(req_dir, "archive")
    resp_dirs = (resp_dir, os.path.join(arch_dir, "answers"))
    inbox_dir = os.path.join(resp_dir, "inbox")

    pairs = [(req_dir, f) for f in sorted(os.listdir(req_dir))
             if f.endswith(".md") and f != "README.md"]
    if os.path.isdir(arch_dir):
        pairs += [(arch_dir, f) for f in sorted(os.listdir(arch_dir))
                  if f.endswith(".md") and f != "README.md"]
    if not pairs:
        if strict:
            broken.append("%sнет ни одного файла запросов: %s" % (prefix, req_dir))
            return None
        return None

    total_q = 0
    answered = 0
    for folder, name in pairs:
        in_archive = folder == arch_dir
        req_path = os.path.join(folder, name)
        req_text = read(req_path)
        if OBSOLETE_RE.search(req_text):
            obsolete.append(prefix + name)
            continue
        req_ids = [m.group(1) for m in ID_RE.finditer(req_text)]
        if not req_ids:
            broken.append("%sв запросе %s не найдено ни одного идентификатора Qn.n" % (prefix, name))
            continue
        req_ids = list(dict.fromkeys(req_ids))
        total_q += len(req_ids)

        if len(req_ids) > MAX_QUESTIONS:
            problems.append(
                "%s%s: %d вопросов, предел пакета %d — нарежь на пакеты, иначе внешняя модель срежет ответ"
                % (prefix, name, len(req_ids), MAX_QUESTIONS)
            )

        base = name[:-3]
        resp_paths = find_responses(base, resp_dirs)
        if not resp_paths:
            waiting.append("%s%s: вопросов %d, ответа нет" % (prefix, name, len(req_ids)))
            continue
        if "быстрая" in req_text and len(req_ids) > 5 and not in_archive:
            problems.append("%s%s: категория «быстрая», а вопросов %d — короткий предел пять"
                            % (prefix, name, len(req_ids)))
        if "дип" in req_text and len(resp_paths) < 2:
            if in_archive:
                waiting.append("%s%s: «дип» с одним файлом ответа — старый формат, второй канал не подтверждён"
                               % (prefix, name))
            else:
                problems.append("%s%s: категория «дип», а файлов ответов %d — нужно два независимых канала"
                                % (prefix, name, len(resp_paths)))
        resp_path = resp_paths[0]

        resp_text = read(resp_path)
        resp_ids = list(dict.fromkeys([m.group(1) for m in ID_RE.finditer(resp_text)]))
        bl = blocks(resp_text, resp_ids)

        missing = [q for q in req_ids if q not in resp_ids]
        extra = [q for q in resp_ids if q not in req_ids]
        answered += len([q for q in req_ids if q in resp_ids])

        if missing:
            problems.append(
                "%s%s: не отвечено на %d вопросов: %s"
                % (prefix, os.path.basename(resp_path), len(missing), ", ".join(missing))
            )
        if extra:
            problems.append(
                "%s%s: идентификаторы без вопроса в запросе: %s"
                % (prefix, os.path.basename(resp_path), ", ".join(extra))
            )
        has_classic = all(section in resp_text for section in SECTIONS)
        has_alt = all(section in resp_text for section in ALT_SECTIONS)
        if not (has_classic or has_alt):
            problems.append(
                "%s%s: нет ни классических разделов (Факты за / против / Белые пятна), "
                "ни новых (Источники / Алгоритм словами / Белые пятна)"
                % (prefix, os.path.basename(resp_path))
            )
        for qid in [q for q in req_ids if q in resp_ids]:
            body = bl.get(qid, "")
            if "http" not in body and WHITE_MARK not in body.lower():
                problems.append(
                    "%s%s, блок %s: нет ни ссылки, ни пометки белого пятна"
                    % (prefix, os.path.basename(resp_path), qid)
                )

        print(
            "%s%s → %s: вопросов %d, отвечено %d, ссылок %d"
            % (prefix, name, os.path.basename(resp_path), len(req_ids),
               len([q for q in req_ids if q in resp_ids]), resp_text.count("http"))
        )

    incoming = []
    if os.path.isdir(inbox_dir):
        incoming = sorted(f for f in os.listdir(inbox_dir) if not f.startswith("README"))
    if incoming:
        print("\nВХОДЯЩИЕ (%s, responses/inbox): %d файл(ов) — заготовки и ответы"
              % (label, len(incoming)))
        for entry in incoming:
            print("  входящий: %s" % entry)
    elif label == "проект":
        print("\nвходящих ответов нет")
    return total_q, answered


def main():
    broken, problems, waiting, obsolete = [], [], [], []
    checked = []
    total_q = 0
    answered = 0
    internal = os.path.isdir(INTERNAL)
    if not internal:
        print("РЕЖИМ ПОЛЬЗОВАТЕЛЯ: папки kit/internal/ нет — запросы проекта не проверяются.")
        print("Проверяется слой человека: workspace/requests и workspace/responses.")
    for label, req_dir, resp_dir in LAYERS:
        if label == "проект" and not internal:
            continue
        if label == "проект" and not os.path.isdir(req_dir):
            broken.append("нет папки запросов: %s" % req_dir)
            continue
        result = check_layer(label, req_dir, resp_dir, label == "проект",
                             problems, waiting, obsolete, broken)
        if result is None:
            continue
        checked.append(label)
        total_q += result[0]
        answered += result[1]

    print("")
    if obsolete:
        print("СНЯТО С РАБОТЫ: %d запросов в архиве, ответа не ждут" % len(obsolete))
    for line in waiting:
        print("ОЖИДАЕТ: %s" % line)
    for line in broken:
        print("ДЕКЛАРАЦИЯ: %s" % line)
    for line in problems:
        print("РАСХОЖДЕНИЕ: %s" % line)

    if total_q:
        print("\nвсего вопросов в запросах: %d, отвечено: %d" % (total_q, answered))

    if not checked and not broken and not problems and not waiting:
        print("\nИТОГ: 0 — проверять нечего: ни у проекта, ни у человека нет папок запросов")
        return 0
    if not checked and not broken and not problems:
        print("\nИТОГ: 0 — запросы отправлены, ответов пока нет")
        return 0

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
    try:
        sys.exit(main())
    except Exception as error:
        print("ИТОГ: 2 — проверка не смогла выполниться: %s" % error)
        sys.exit(2)
