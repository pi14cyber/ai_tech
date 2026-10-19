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
5. Запрос с пометкой `**Статус:** неактуален` снимается с работы и уходит в архив
   без ответа: тема закрыта или поглощена другим запросом.

Коды возврата: 0 — состояние сходится; 1 — расхождения; 2 — нечего проверять.

Проверка самого проверяльщика: `--self-test` прогоняет обе процедуры архива
(отвеченная пара и снятый запрос) на временной папке.
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
OBSOLETE_RE = re.compile(r"^\*\*Статус:\*\*\s*неактуален", re.MULTILINE)
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


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    write_mode = "--write" in args
    move_mode = "--move" in args

    if not os.path.isdir(os.path.join(ROOT, "internal")):
        print("РЕЖИМ ПОЛЬЗОВАТЕЛЯ: папки internal/ нет — состояние запросов проекта не проверяется")
        print("\nИТОГ: 0 — проверять нечего")
        return 0

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
        obsolete = bool(OBSOLETE_RE.search(req_text))
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
            if obsolete:
                note = "в архиве, снят как неактуальный"
            elif not complete:
                problems.append("%s: лежит в архиве, но полного ответа нет — вернуть в работу" % name)
                note = "в архиве, ответ рядом: `%s`" % (os.path.basename(resp_path) if resp_path else "нет")
            else:
                note = "в архиве, ответ рядом: `%s`" % (os.path.basename(resp_path) if resp_path else "нет")
        elif obsolete:
            note = "неактуален, перенос в архив: `python scripts/verify_state.py --move`"
            to_move.append((req_path, None, name))
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
            total = len(list(dict.fromkeys(Q_HEAD.findall(text))))
            if OBSOLETE_RE.search(text):
                note = "в архиве, снят как неактуальный"
                answered = 0
            else:
                note = "в архиве, ответ рядом: `%s`" % (os.path.basename(resp_path) if resp_path else "нет")
                answer_text = read(os.path.join(ARCH_ANSWERS, os.path.basename(resp_path))) if resp_path else ""
                req_qids = list(dict.fromkeys(Q_HEAD.findall(text)))
                answer_qids = set(Q_HEAD.findall(answer_text))
                answered = len([q for q in req_qids if q in answer_qids])
            with open(target_req, "w", encoding="utf-8", newline="\n") as f:
                f.write(STATE_LINE.sub(state_line(answered, total, note), text, count=1))
            print("в архив: %s" % name)

    remaining = [p for p in problems if not ((write_mode or move_mode) and "устарела" in p)]
    if remaining and not write_mode:
        print("")
        for line in remaining:
            print("СОСТОЯНИЕ: %s" % line)
        print("\nИТОГ: 1 — состояние расходится; запусти с --write, чтобы обновить строки")
        return 1
    print("\nзапросов в работе: %d, в архиве: %d" % (len(pairs()) - archived, archived))
    print("ИТОГ: 0 — состояние сходится с диском")
    return 0


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def self_test():
    """Проверка самого проверяльщика: обе процедуры архива на временной папке.

    A. Отвеченный запрос: полный ответ по всем идентификаторам → пара уходит
       в архив, ответ лежит рядом, строка состояния говорит «ответ рядом».
    B. Снятый запрос: пометка «Статус: неактуален», ответа нет → уходит в архив
       со строкой «снят как неактуальный», а не «вернуть в работу».
    """
    global REQ_DIR, ARCH_DIR, ARCH_ANSWERS, RESP_DIR, RESP_DIRS
    saved = (REQ_DIR, ARCH_DIR, ARCH_ANSWERS, RESP_DIR, RESP_DIRS)
    tmp = os.path.join(ROOT, "scripts", "_selftest_state")
    failures = []

    def check(condition, message):
        if not condition:
            failures.append(message)

    try:
        shutil.rmtree(tmp, ignore_errors=True)
        REQ_DIR = os.path.join(tmp, "requests")
        ARCH_DIR = os.path.join(REQ_DIR, "archive")
        ARCH_ANSWERS = os.path.join(ARCH_DIR, "answers")
        RESP_DIR = os.path.join(tmp, "responses")
        RESP_DIRS = (RESP_DIR, ARCH_ANSWERS)
        os.makedirs(ARCH_ANSWERS)
        os.makedirs(RESP_DIR)

        answered_req = os.path.join(REQ_DIR, "req_test_answered.md")
        write(answered_req,
              "# Запрос\n\n**Состояние:** устарело\n\n## 2. Вопросы\n\n"
              "### Q1.1. Первый\n\n### Q1.2. Второй\n")
        write(os.path.join(RESP_DIR, "req_test_answered.answer.md"),
              "### Q1.1. Первый\n\n- **Факты за:** x\n\n"
              "### Q1.2. Второй\n\n- **Факты за:** y\n")

        obsolete_req = os.path.join(REQ_DIR, "req_test_obsolete.md")
        write(obsolete_req,
              "# Запрос\n\n**Состояние:** отвечено 0 из 2 — ответа нет\n"
              "**Статус:** неактуален — тест\n\n## 2. Вопросы\n\n"
              "### Q1.1. Первый\n\n### Q1.2. Второй\n")

        check(main(["--write"]) == 0, "после --write состояние должно сходиться")
        check(main(["--move"]) == 0, "перенос в архив должен проходить без ошибок")

        archived_answered = os.path.join(ARCH_DIR, "req_test_answered.md")
        archived_answer = os.path.join(ARCH_ANSWERS, "req_test_answered.answer.md")
        archived_obsolete = os.path.join(ARCH_DIR, "req_test_obsolete.md")

        check(os.path.exists(archived_answered), "отвеченный запрос должен уйти в архив")
        check(os.path.exists(archived_answer), "ответ должен лежать рядом, в archive/answers")
        check(not os.path.exists(answered_req), "отвеченного запроса не должно остаться в работе")
        check("в архиве, ответ рядом" in read(archived_answered),
              "строка состояния отвеченного запроса должна указывать на ответ")

        check(os.path.exists(archived_obsolete), "снятый запрос должен уйти в архив")
        check(not os.path.exists(obsolete_req), "снятого запроса не должно остаться в работе")
        check("снят как неактуальный" in read(archived_obsolete),
              "снятый запрос должен помечаться как неактуальный")
        check(not os.path.exists(os.path.join(ARCH_ANSWERS, "req_test_obsolete.answer.md")),
              "у снятого запроса не должно появляться ответа")

        check(main([]) == 0, "финальная сверка архива должна сходиться")
    finally:
        REQ_DIR, ARCH_DIR, ARCH_ANSWERS, RESP_DIR, RESP_DIRS = saved
        shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        print("")
        for message in failures:
            print("САМОПРОВЕРКА: %s" % message)
        print("\nИТОГ: 1 — самопроверка провалена")
        return 1
    print("\nСАМОПРОВЕРКА ПРОЙДЕНА: отвеченные пары и снятые запросы уходят в архив по своим правилам")
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
