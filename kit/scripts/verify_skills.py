#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка навыков: шапка, имя, размер.

Зачем: агент находит навык по полям `name` и `description` из шапки, а мы ссылаемся
на навык путём к папке. Когда имя папки и имя навыка расходятся, ссылки живут сами
по себе, а активация — сама по себе, и разобраться в этом глазами нельзя.

Что проверяет каждый `skills/*/SKILL.md`:

1. Есть шапка с полями `name` и `description`.
2. `name` из строчных латинских букв, цифр и одиночных дефисов, до 64 символов.
3. `name` совпадает с именем папки — наше правило, введено ради ссылок.
4. `description` есть и не длиннее 1024 символов.
5. Тело навыка не длиннее 20 000 символов (ориентир — до 5 000 токенов).

Внешняя спецификация навыков (`agentskills.io/specification`) на момент проверки
была недоступна из окружения, поэтому её требования здесь не выдаются за источник:
правила 3 и 5 введены нами.

Коды возврата: 0 — навыки в порядке; 1 — есть отступления; 2 — нечего проверять.
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
SKILLS_DIR = os.path.join(KIT, "skills")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESC = 1024
MAX_BODY = 20000


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    block = text[3:end]
    body = text[end + 4:]
    data = {}
    for line in block.splitlines():
        if ":" in line and not line.strip().startswith("#"):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data, body


def main():
    if not os.path.isdir(SKILLS_DIR):
        print("ИТОГ: 2 — нет папки навыков: %s" % SKILLS_DIR)
        return 2

    folders = [d for d in sorted(os.listdir(SKILLS_DIR)) if os.path.isdir(os.path.join(SKILLS_DIR, d))]
    if not folders:
        print("ИТОГ: 2 — в папке навыков нет ни одной папки")
        return 2

    problems = []
    for folder in folders:
        path = os.path.join(SKILLS_DIR, folder, "SKILL.md")
        if not os.path.exists(path):
            problems.append("%s: нет файла SKILL.md" % folder)
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        meta, body = parse_frontmatter(text)
        if meta is None:
            problems.append("%s: нет шапки с полями" % folder)
            continue
        name = meta.get("name", "")
        desc = meta.get("description", "")
        if not name:
            problems.append("%s: нет поля name" % folder)
        else:
            if len(name) > MAX_NAME:
                problems.append("%s: name длиной %d, предел %d" % (folder, len(name), MAX_NAME))
            if not NAME_RE.match(name):
                problems.append("%s: name «%s» не из строчных букв, цифр и одиночных дефисов" % (folder, name))
            if name != folder:
                problems.append("%s: name «%s» не совпадает с именем папки" % (folder, name))
        if not desc:
            problems.append("%s: нет поля description" % folder)
        elif len(desc) > MAX_DESC:
            problems.append("%s: description длиной %d, предел %d" % (folder, len(desc), MAX_DESC))
        if len(body) > MAX_BODY:
            problems.append("%s: тело %d символов, ориентир — до %d" % (folder, len(body), MAX_BODY))

    print("проверено навыков: %d" % len(folders))
    for line in problems:
        print("НАВЫК: %s" % line)

    if problems:
        print("\nИТОГ: 1 — %d отступлений" % len(problems))
        return 1
    print("\nИТОГ: 0 — шапки и имена навыков в порядке")
    return 0


if __name__ == "__main__":
    sys.exit(main())
