#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Заготовки ответов: пустые файлы по каждому активному запросу.

Зачем: внешняя модель отвечает длинным текстом, и копировать его в правильные
блоки по идентификаторам легче в готовый каркас. Скрипт делает каркас на каждый
активный запрос: `<имя запроса>.md` в `internal/draft/responses/inbox/`.

Правила:

1. Заголовки вопросов берутся из самого запроса, чтобы каркас не расходился
   с вопросами.
2. Существующий файл не перезаписывается: заполненный ответ дороже каркаса.
3. Снятые запросы (`**Статус:** неактуален`) пропускаются.
4. Архив не трогается.

Запуск:

    python scripts/make_answer_blanks.py

Коды возврата: 0 — каркасы готовы; 2 — нет папки запросов.
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
INBOX_DIR = os.path.join(ROOT, "internal", "draft", "responses", "inbox")

OBSOLETE_RE = re.compile(r"^\*\*Статус:\*\*\s*неактуален", re.MULTILINE)
QUESTIONS_RE = re.compile(r"##\s*2\.\s*Вопросы(.*?)##\s*3\.", re.S)
HEAD_RE = re.compile(r"^###\s*(Q1\.\d+)\.\s*(.+)$", re.MULTILINE)
CATEGORY_RE = re.compile(r"^\*\*Категория:\*\*\s*`([^`]+)`", re.MULTILINE)

BLANK_BODY = """# Ответ: {title}

**Запрос:** `{name}` · **Вопросов:** {total}
**Категория:** `{category}` — {mode}
**Дата получения:**
**Канал:**

> Это заготовка. Копируй ответ в блоки ниже как есть, не переписывай и не сокращай.
> Если по вопросу данных нет — оставь пустым блок «Белые пятна» с пометкой, где искали:
> так проверка поймёт, что вопрос закрыт поиском, а не пропущен.

{questions}
"""

BLANK_BLOCK = """### {qid}. {title}

**Факты за:**

-

**Факты против:**

-

**Белые пятна:**

-
"""


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def questions_of(text):
    section = QUESTIONS_RE.search(text)
    body = section.group(1) if section else text
    return HEAD_RE.findall(body)


def title_of(text):
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            for prefix in ("Запрос:", "Задание:"):
                if title.startswith(prefix):
                    title = title[len(prefix):].strip()
            return title
    return "ответ"


def plural_questions(n):
    if n % 10 == 1 and n % 100 != 11:
        return "%d вопрос" % n
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return "%d вопроса" % n
    return "%d вопросов" % n


def main():
    if not os.path.isdir(REQ_DIR):
        print("ИТОГ: 2 — нет папки запросов: %s" % REQ_DIR)
        return 2
    os.makedirs(INBOX_DIR, exist_ok=True)

    created = 0
    skipped_existing = 0
    skipped_obsolete = 0

    for name in sorted(os.listdir(REQ_DIR)):
        if not name.endswith(".md") or name == "README.md":
            continue
        path = os.path.join(REQ_DIR, name)
        if not os.path.isfile(path):
            continue
        text = read(path)
        if OBSOLETE_RE.search(text):
            skipped_obsolete += 1
            continue

        questions = questions_of(text)
        if not questions:
            print("ПРОПУСК: %s — не нашёл вопросов Q1.N" % name)
            continue

        base = name[:-3]
        target = os.path.join(INBOX_DIR, name)
        if os.path.exists(target):
            skipped_existing += 1
            continue

        blocks = "\n".join(
            BLANK_BLOCK.format(qid=qid, title=title)
            for qid, title in questions
        ).rstrip() + "\n"
        category_match = CATEGORY_RE.search(text)
        category = category_match.group(1) if category_match else "быстрая"
        mode = ("короткий объём, один канал" if category == "быстрая"
                else "полный объём, два и более канала")
        content = BLANK_BODY.format(
            title=title_of(text),
            name=base,
            total=plural_questions(len(questions)),
            category=category,
            mode=mode,
            questions=blocks,
        )
        with open(target, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        created += 1
        print("заготовка: %s (%s)" % (name, plural_questions(len(questions))))

    print("")
    print("создано: %d, уже были: %d, снятых пропущено: %d"
          % (created, skipped_existing, skipped_obsolete))
    print("ИТОГ: 0 — заготовки в %s" % os.path.relpath(INBOX_DIR, ROOT).replace("\\", "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
