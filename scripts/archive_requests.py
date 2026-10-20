#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Архивация закрытых запросов: запрос и ответ уезжают в архив одной операцией.

Правило набора: **закрытый запрос обязан уехать в архив**. Закрытым считается
запрос, у ответа которого в шапке стоит «Статус обработки: принят» или
«отклонён». Пока статус «в очереди», запрос остаётся в работе.

Что делает, в двух слоях:
 1. Проект: `internal/draft/requests/` + `internal/draft/responses/` (или `responses/inbox/`).
 2. Человек: `workspace/requests/` + `workspace/responses/` (или `responses/inbox/`), если папки есть.
 3. Если ответ закрыт — переносит запрос в `<requests>/archive/`, ответ в
    `<requests>/archive/answers/<id>.answer.md`. Для слоя человека архив лежит
    внутри `workspace/` и не публикуется.
 4. Печатает, что перенесено и что осталось в работе.

Чего не делает: не решает, закрыт ли запрос по смыслу — статус ставит агент
после разбора. Не удаляет данные человека: закрытые пары человека переносит
только внутрь `workspace/`.

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


def read(path):
    return open(path, encoding="utf-8", errors="replace").read()


def answer_for(resp_dir, request_id):
    candidates = []
    candidates += glob.glob(os.path.join(resp_dir, request_id + "*.answer.md"))
    candidates += glob.glob(os.path.join(resp_dir, "inbox", request_id + "*.answer.md"))
    return sorted(candidates)


def status_of(text):
    match = re.search(r"\*\*Статус обработки:\*\*\s*([^\n]*)", text)
    return match.group(1).strip().lower() if match else ""


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
        answer = answers[0]
        state = status_of(read(answer))
        if state.startswith("принят") or state.startswith("отклон"):
            shutil.move(path, os.path.join(arch_dir, name))
            target = os.path.join(answers_dir, request_id + ".answer.md")
            if os.path.exists(target):
                os.remove(target)
            shutil.move(answer, target)
            closed.append((request_id, state))
        else:
            waiting.append((request_id, "статус: %s" % (state or "не указан")))

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
