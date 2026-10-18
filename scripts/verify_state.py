#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Статус запросов: что отвечено, что нет, где лежит ответ.

Зачем: ответы копились в отдельной папке, и по запросу нельзя было понять,
пришёл ли ответ. Теперь каждый запрос несёт строку состояния, которая
сверяется с диском, а отработанные запросы переносятся в архив.

Что делает:

1. Читает все запросы проекта и их ответы.
2. Сверяет строку `**Состояние:**` в запросе с тем, что лежит на диске.
3. Проверяет, что блоки `### Q1.N` в запросе и в ответе совпадают.
4. В режиме `--write` переписывает строку состояния во всех запросах.
5. В режиме `--move` переносит пары «запрос + ответ» в `archive/`,
   когда строка состояния помечена как `отвечено`.

Коды возврата: 0 — состояние сходится; 1 — расхождения; 2 — нечего проверять.
"""

import os
import re
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ_DIR = os.path.join(ROOT, "internal", "draft", "requests")
RESP_DIR = os.path.join(ROOT, "internal", "draft", "responses")
ARCH_DIR = os.path.join(REQ_DIR, "archive")
STATE_LINE = re.compile(r"^\*\*Состояние:\*\*.*$", re.MULTILINE)
Q_HEAD = re.compile(r"^### (Q1\.\d+)\.", re.MULTILINE)


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def answer_for(name):
    base = name[:-3]
    if not os.path.isdir(RESP_DIR):
        return None
    for candidate in sorted(os.listdir(RESP_DIR)):
        if candidate.startswith(base) and candidate.endswith(".md"):
            return os.path.join(RESP_DIR, candidate)
    return None


def state_text(total, answered, note):
    return "**Состояние:** отвечено %d из %d — %s" % (total, answered, note)


def main():
    write_mode = "--write" in sys.argv
    move_mode = "--move" in sys.argv

    if not os.path.isdir(REQ_DIR):
        print("ИТОГ: 2 — нет папки запросов: %s" % REQ_DIR)
        return 2

    problems = []
    moved = []
    actions = []

    for name in sorted(f for f in os.listdir(REQ_DIR) if f.endswith(".md") and f != "README.md"):
        req_path = os.path.join(REQ_DIR, name)
        req_text = read(req_path)
        req_ids = list(dict.fromkeys(Q_HEAD.findall(req_text)))
        total = len(req_ids)
        resp_path = answer_for(name)

        answered = 0
        note = "ответа нет"
        if resp_path:
            resp_text = read(resp_path)
            resp_ids = list(dict.fromkeys(Q_HEAD.findall(resp_text)))
            answered = len([q for q in req_ids if q in resp_ids])
            missing = [q for q in req_ids if q not in resp_ids]
            extra = [q for q in resp_ids if q not in req_ids]
            if missing:
                note = "нет ответа по %s" % ", ".join(missing)
                problems.append("%s: в ответе нет блоков %s" % (name, ", ".join(missing)))
            elif extra:
                note = "в ответе лишние блоки %s" % ", ".join(extra)
                problems.append("%s: в ответе лишние блоки %s" % (name, ", ".join(extra)))
            else:
                note = "архивировать: `%s`" % os.path.relpath(resp_path, ROOT).replace("\\", "/")

        expected = state_text(total, answered, note)
        current = STATE_LINE.search(req_text)
        if not current:
            problems.append("%s: нет строки «**Состояние:**»" % name)
            actions.append((req_path, req_text, expected))
        elif current.group(0).strip() != expected.strip():
            problems.append("%s: строка состояния устарела" % name)
            actions.append((req_path, req_text, expected))

        print("%s: отвечено %d из %d — %s" % (name, answered, total, note))

        if move_mode and resp_path and resp_path and answered == total and not problems:
            os.makedirs(ARCH_DIR, exist_ok=True)
            shutil.move(req_path, os.path.join(ARCH_DIR, name))
            os.makedirs(os.path.join(ARCH_DIR, "answers"), exist_ok=True)
            shutil.move(resp_path, os.path.join(ARCH_DIR, "answers", os.path.basename(resp_path)))
            moved.append(name)

    if write_mode and actions:
        for path, text, expected in actions:
            new_text = STATE_LINE.sub(expected, text, count=1)
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_text)
        print("\nстрок состояния обновлено: %d" % len(actions))

    if moved:
        print("перенесено в архив: %s" % ", ".join(moved))

    if problems and not write_mode:
        print("")
        for line in problems:
            print("СОСТОЯНИЕ: %s" % line)
        print("\nИТОГ: 1 — состояние расходится; запусти с --write, чтобы обновить строки")
        return 1
    print("\nИТОГ: 0 — состояние запросов сходится с диском")
    return 0


if __name__ == "__main__":
    sys.exit(main())
