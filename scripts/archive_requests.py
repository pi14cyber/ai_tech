#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Архивация закрытых запросов: запрос и ответ уезжают в архив одной операцией.

Правило набора: **закрытый запрос обязан уехать в архив**. Закрытым считается
запрос, у ответа которого в шапке стоит «Статус обработки: принят» или
«отклонён» — независимо от того, обёрнуто поле в `**` или нет: предикат тот же,
что в `verify_requests.py` и `verify_state.py`. Пока статус «в очереди», запрос
остаётся в работе.

Что делает, в двух слоях:
 1. Проект: `internal/draft/requests/` + `internal/draft/responses/` (или `responses/inbox/`).
 2. Человек: `workspace/requests/` + `workspace/responses/` (или `responses/inbox/`), если папки есть.
 3. Ответ ищется по `<id>*.answer.md` и `<id>*.resp.md`.
 4. Переносит только полную пару: в ответе есть все блоки `### Q1.N`, которые
    объявлены в запросе. Неполный ответ не архивируется — перенос спрятал бы
    недостающие вопросы в архив.
 5. Если ответ закрыт и полон — переносит запрос в `<requests>/archive/`, ответ в
    `<requests>/archive/answers/`. Для слоя человека архив лежит внутри
    `workspace/` и не публикуется. Печатает, что перенесено и что осталось в работе.

Чего не делает: не решает, закрыт ли запрос по смыслу — статус ставит агент
после разбора. Не удаляет данные человека: закрытые пары человека переносит
только внутрь `workspace/`. Не чинит неполные ответы.

Коды: 0 — архивация выполнена или архивировать нечего; 2 — сломана декларация
(нет папок проекта при живом internal/).
"""

import glob
import os
import re
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERNAL = os.path.join(ROOT, "internal")
LAYERS = (
    ("проект", os.path.join(INTERNAL, "draft", "requests"), os.path.join(INTERNAL, "draft", "responses")),
    ("человек", os.path.join(ROOT, "workspace", "requests"), os.path.join(ROOT, "workspace", "responses")),
)
# Один предикат «запрос закрыт» на все проверки и на архиватор: звёздочки,
# двоеточие и регистр не должны решать, уедет запрос в архив или нет.
STATUS_RE = re.compile(r"Статус обработки:?[ \t]*\**\s*([^\n]*)")
ANSWER_PATTERNS = ("{id}*.answer.md", "{id}*.resp.md")
CLOSED_WORDS = ("принят", "отклон")
Q_HEAD = re.compile(r"^### (Q1\.\d+)\.", re.MULTILINE)


def read(path):
    return open(path, encoding="utf-8", errors="replace").read()


def status_of(text):
    match = STATUS_RE.search(text)
    if not match:
        return ""
    return re.sub(r"[*`_]", "", match.group(1)).strip().lower()


def is_closed(text):
    state = status_of(text)
    return any(state.startswith(word) for word in CLOSED_WORDS)


def answer_for(resp_dir, request_id):
    candidates = []
    for pattern in ANSWER_PATTERNS:
        candidates += glob.glob(os.path.join(resp_dir, pattern.format(id=request_id)))
        candidates += glob.glob(os.path.join(resp_dir, "inbox", pattern.format(id=request_id)))
    return sorted(set(candidates))


def answer_gaps(request_text, answer_text):
    """Каких блоков Q1.N не хватает в ответе. Пустой список — ответ полный."""
    request_ids = list(dict.fromkeys(Q_HEAD.findall(request_text)))
    answer_ids = set(Q_HEAD.findall(answer_text))
    return [qid for qid in request_ids if qid not in answer_ids]


def archive_layer(label, req_dir, resp_dir):
    arch_dir = os.path.join(req_dir, "archive")
    answers_dir = os.path.join(arch_dir, "answers")
    os.makedirs(answers_dir, exist_ok=True)

    closed, waiting = [], []
    for path in sorted(glob.glob(os.path.join(req_dir, "*.md"))):
        name = os.path.basename(path)
        if name == "README.md":
            continue
        request_id = name[:-3]
        answers = answer_for(resp_dir, request_id)
        if not answers:
            waiting.append((request_id, "ответа нет"))
            continue
        request_text = read(path)
        closed_answer = None
        for candidate in answers:
            if is_closed(read(candidate)):
                closed_answer = candidate
                break
        if closed_answer is None:
            waiting.append((request_id, "статус: %s" % (status_of(read(answers[0])) or "не указан")))
            continue
        gaps = answer_gaps(request_text, read(closed_answer))
        if gaps:
            # Неполный ответ — не закрытый запрос: перенос спрятал бы недостающие
            # вопросы в архив. Сначала ответ, потом архив.
            waiting.append((request_id, "ответ неполный, нет блоков %s — архив запрещён"
                            % ", ".join(gaps[:6])))
            continue
        shutil.move(path, os.path.join(arch_dir, name))
        target = os.path.join(answers_dir, os.path.basename(closed_answer))
        if os.path.exists(target):
            os.remove(target)
        shutil.move(closed_answer, target)
        closed.append((request_id, status_of(read(target))))
    for request_id, state in closed:
        print("[%s] В АРХИВ: %s (%s)" % (label, request_id, state))
    for request_id, reason in waiting:
        print("[%s] В РАБОТЕ: %s (%s)" % (label, request_id, reason))
    if not closed:
        print("[%s] Архивировать нечего: закрытых запросов нет." % label)
    return len(closed)


def main():
    moved = 0
    checked = 0
    for label, req_dir, resp_dir in LAYERS:
        if not os.path.isdir(req_dir) or not os.path.isdir(resp_dir):
            if label == "проект" and os.path.isdir(INTERNAL):
                print("ИТОГ: 2 — нет папок requests/ или responses/ проекта")
                return 2
            continue
        checked += 1
        moved += archive_layer(label, req_dir, resp_dir)

    if not checked:
        print("ИТОГ: 0 — проверять нечего: ни у проекта, ни у человека нет папок запросов")
        return 0
    print("\nИТОГ: 0 — архивация выполнена; состояние обнови: python scripts/verify_state.py --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
