#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Статус запросов: что отвечено, что нет, где лежит ответ.

Зачем: ответы копились в отдельной папке, и по запросу нельзя было понять,
пришёл ли ответ. Теперь каждый запрос несёт строку состояния, она сверяется
с диском, а отработанные пары переносятся в архив.

Что делает:

1. Читает запросы активной папки и архива, находит ответы к каждому.
2. Сверяет блоки `### Q1.N` запроса и ответа.
3. Сверяет строку `**Состояние:**` с тем, что лежит на диске.
4. `--write` переписывает строки состояния, `--move` переносит полные пары в архив.

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
ARCH_DIR = os.path.join(REQ_DIR, "archive")
ARCH_ANSWERS = os.path.join(ARCH_DIR, "answers")
RESP_DIR = os.path.join(ROOT, "internal", "draft", "responses")
RESP_DIRS = (RESP_DIR, ARCH_ANSWERS)
STATE_LINE = re.compile(r"^\*\*Состояние:\*\*.*$", re.MULTILINE)
Q_HEAD = re.compile(r"^### (Q1\.\d+)\.", re.MULTILINE)


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def answer_for(base):
    for directory in RESP_DIRS:
        if not os.path.isdir(directory):
            continue
        for candidate in sorted(os.listdir(directory)):
            if candidate.startswith(base) and candidate.endswith(".md"):
                return os.path.join(directory, candidate)
    return None


def state_line(answered, total, note):
    return "**Состояние:** отвечено %d из %d — %s" % (answered, total, note)


def pairs():
    out = []
    for folder in (REQ_DIR, ARCH_DIR):
        if not os.path.isdir(folder):
            continue
        for name in sorted(f for f in os.listdir(folder) if f.endswith(".md") and f != "README.md"):
            out.append((folder, name))
    return out


def main():
    write_mode = "--write" in sys.argv
    move_mode = "--move" in sys.argv

    if not os.path.isdir(REQ_DIR):
        print("ИТОГ: 2 — нет папки запросов: %s" % REQ_DIR)
        return 2

    problems = []
    updates = []
    to_move = []
    archived = 0

    for folder, name in pairs():
        in_archive = folder == ARCH_DIR
        req_path = os.path.join(folder, name)
        req_text = read(req_path)
        req_ids = list(dict.fromkeys(Q_HEAD.findall(req_text)))
        total = len(req_ids)
        base = name[:-3]
        resp_path = answer_for(base)

        answered = 0
        if resp_path:
            resp_ids = list(dict.fromkeys(Q_HEAD.findall(read(resp_path))))
            answered = len([q for q in req_ids if q in resp_ids])
            missing = [q for q in req_ids if q not in resp_ids]
            extra = [q for q in resp_ids if q not in req_ids]
            if missing:
                problems.append("%s: в ответе нет блоков %s" % (name, ", ".join(missing)))
            if extra:
                problems.append("%s: в ответе лишние блоки %s" % (name, ", ".join(extra)))
            complete = not missing and not extra and total > 0
        else:
            complete = False

        if in_archive:
            archived += 1
            if not complete:
                problems.append("%s: лежит в архиве, но полного ответа нет — вернуть в работу" % name)
            note = "в архиве, ответ рядом: `%s`" % (os.path.basename(resp_path) if resp_path else "нет")
        elif complete:
            note = "ответ полный, перенос в архив: `python scripts/verify_state.py --move`"
            to_move.append((req_path, resp_path, name))
        elif resp_path:
            note = "частичный ответ, запрос остаётся в работе"
        else:
            note = "ответа нет"

        expected = state_line(answered, total, note)
        current = STATE_LINE.search(req_text)
        if not current:
            problems.append("%s: нет строки «**Состояние:**»" % name)
            updates.append((req_path, req_text, expected))
        elif current.group(0).strip() != expected:
            problems.append("%s: строка состояния устарела" % name)
            updates.append((req_path, req_text, expected))

        print("%s%s: отвечено %d из %d — %s" % ("[архив] " if in_archive else "", name, answered, total, note))

    if write_mode and updates:
        for path, text, expected in updates:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(STATE_LINE.sub(expected, text, count=1))
        print("\nстрок состояния обновлено: %d" % len(updates))

    if move_mode and to_move:
        os.makedirs(ARCH_ANSWERS, exist_ok=True)
        for req_path, resp_path, name in to_move:
            target_req = os.path.join(ARCH_DIR, name)
            shutil.move(req_path, target_req)
            if resp_path:
                shutil.move(resp_path, os.path.join(ARCH_ANSWERS, os.path.basename(resp_path)))
            text = read(target_req)
            note = "в архиве, ответ рядом: `%s`" % (os.path.basename(resp_path) if resp_path else "нет")
            answer_text = read(os.path.join(ARCH_ANSWERS, os.path.basename(resp_path))) if resp_path else ""
            answered = len([q for q in Q_HEAD.findall(text) if q in Q_HEAD.findall(answer_text)])
            with open(target_req, "w", encoding="utf-8", newline="\n") as f:
                f.write(STATE_LINE.sub(state_line(answered, len(Q_HEAD.findall(text)), note), text, count=1))
            print("в архив: %s" % name)

    remaining = [p for p in problems if not (write_mode and "устарела" in p)]
    if remaining and not write_mode:
        print("")
        for line in remaining:
            print("СОСТОЯНИЕ: %s" % line)
        print("\nИТОГ: 1 — состояние расходится; запусти с --write, чтобы обновить строки")
        return 1
    print("\nзапросов в работе: %d, в архиве: %d" % (len(pairs()) - archived, archived))
    print("ИТОГ: 0 — состояние сходится с диском")
    return 0


if __name__ == "__main__":
    sys.exit(main())
