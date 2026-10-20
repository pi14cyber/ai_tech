#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Архивация закрытых запросов: запрос и ответ уезжают в архив одной операцией.

Правило набора: **закрытый запрос обязан уехать в архив**. Закрытым считается
запрос, у ответа которого в шапке стоит «Статус обработки: принят» или
«отклонён». Пока статус «в очереди», запрос остаётся в работе.

Что делает:
 1. Находит в `internal/draft/requests/` запросы с ответом в
    `internal/draft/responses/` (или `responses/inbox/`).
 2. Если ответ закрыт — переносит запрос в `requests/archive/`, ответ в
    `requests/archive/answers/<id>.answer.md`.
 3. Печатает, что перенесено и что осталось в работе.

Чего не делает: не решает, закрыт ли запрос по смыслу — статус ставит агент
после разбора. Не трогает `workspace/` (данные человека).

Коды: 0 — архивация выполнена или архивировать нечего; 2 — нет папок.
"""

import glob
import os
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ_DIR = os.path.join(ROOT, "internal", "draft", "requests")
ARCH_DIR = os.path.join(REQ_DIR, "archive")
ANSW_DIR = os.path.join(ARCH_DIR, "answers")
RESP_DIR = os.path.join(ROOT, "internal", "draft", "responses")
ACTION = os.path.join(RESP_DIR, "inbox") + " (входящие)"


def read(path):
    return open(path, encoding="utf-8", errors="replace").read()


def answer_for(request_id):
    candidates = []
    candidates += glob.glob(os.path.join(RESP_DIR, request_id + "*.answer.md"))
    candidates += glob.glob(os.path.join(RESP_DIR, "inbox", request_id + "*.answer.md"))
    return sorted(candidates)


def status_of(text):
    match = __import__("re").search(r"\*\*Статус обработки:\*\*\s*([^\n]*)", text)
    return match.group(1).strip().lower() if match else ""


def main():
    if not os.path.isdir(os.path.join(ROOT, "internal")):
        print("РЕЖИМ ПОЛЬЗОВАТЕЛЯ: internal/ нет — архивировать нечего")
        print("\nИТОГ: 0 — проверять нечего")
        return 0
    if not (os.path.isdir(REQ_DIR) and os.path.isdir(RESP_DIR)):
        print("ИТОГ: 2 — нет папок requests/ или responses/")
        return 2
    os.makedirs(ANSW_DIR, exist_ok=True)

    closed, waiting = [], []
    for path in sorted(glob.glob(os.path.join(REQ_DIR, "*.md"))):
        name = os.path.basename(path)
        if name == "README.md":
            continue
        request_id = name[:-3]
        answers = answer_for(request_id)
        if not answers:
            waiting.append((request_id, "ответа нет"))
            continue
        answer = answers[0]
        state = status_of(read(answer))
        if state.startswith("принят") or state.startswith("отклон"):
            shutil.move(path, os.path.join(ARCH_DIR, name))
            target = os.path.join(ANSW_DIR, request_id + ".answer.md")
            if os.path.exists(target):
                os.remove(target)
            shutil.move(answer, target)
            closed.append((request_id, state))
        else:
            waiting.append((request_id, "статус: %s" % (state or "не указан")))

    for request_id, state in closed:
        print("В АРХИВ: %s (%s)" % (request_id, state))
    for request_id, reason in waiting:
        print("В РАБОТЕ: %s (%s)" % (request_id, reason))
    if not closed:
        print("Архивировать нечего: закрытых запросов нет.")
    print("\nИТОГ: 0 — архивация выполнена; состояние обнови: python scripts/verify_state.py --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
