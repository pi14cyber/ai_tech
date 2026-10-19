#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка адаптеров навыков: в каталогах оболочек должны быть только ссылки.

Зачем: адаптер наполняет `.dsh/skills`, `.claude/skills` и `.agents/skills` ссылками
на наши папки навыков. Если кто-то положит туда копию, появятся две версии одного
навыка, и агент прочитает устаревшую. Правило запрещает копии, проверка это ловит.

Что проверяет для каждого существующего каталога:

1. на каждый наш навык есть запись;
2. запись — ссылка, а не папка-копия;
3. ссылка указывает на существующую папку навыка с файлом `SKILL.md`;
4. лишних записей нет.

Отсутствие каталога ошибкой не считается: адаптеры необязательны, каждая оболочка
заводит свой. Об этом проверка сообщает прямо, а не молчит.

Коды возврата: 0 — ссылки сходятся или каталогов нет; 1 — есть копии, лишние записи
или недостающие навыки; 2 — нет папки навыков.
"""

import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT, "skills")
TARGETS = (".dsh/skills", ".claude/skills", ".agents/skills")


def is_link(path):
    if os.path.islink(path):
        return True
    checker = getattr(os.path, "isjunction", None)
    return bool(checker and checker(path))


def skills():
    out = []
    if not os.path.isdir(SKILLS_DIR):
        return out
    for name in sorted(os.listdir(SKILLS_DIR)):
        folder = os.path.join(SKILLS_DIR, name)
        if os.path.isdir(folder) and os.path.exists(os.path.join(folder, "SKILL.md")):
            out.append(name)
    return out


def main():
    names = skills()
    if not names:
        print("ИТОГ: 2 — нет папки навыков: %s" % SKILLS_DIR)
        return 2

    problems = []
    present = 0
    checked = 0
    for rel in TARGETS:
        base = os.path.join(ROOT, *rel.split("/"))
        if not os.path.isdir(base):
            print("%s: каталога нет — адаптер не создан (это допустимо)" % rel)
            continue
        present += 1
        entries = sorted(os.listdir(base))
        for name in names:
            path = os.path.join(base, name)
            if not os.path.exists(path):
                problems.append("%s: нет навыка %s" % (rel, name))
                continue
            checked += 1
            if not is_link(path):
                problems.append("%s: %s — копия, а не ссылка" % (rel, name))
                continue
            if not os.path.exists(os.path.join(path, "SKILL.md")):
                problems.append("%s: ссылка %s не ведёт к SKILL.md" % (rel, name))
        for entry in entries:
            if entry not in names:
                problems.append("%s: лишняя запись %s" % (rel, entry))

    print("каталогов найдено: %d, ссылок проверено: %d, навыков в наборе: %d"
          % (present, checked, len(names)))
    for line in problems:
        print("АДАПТЕР: %s" % line)
    if problems:
        print("\nИТОГ: 1 — в адаптерах есть копии или лишние записи")
        return 1
    if not present:
        print("ВНИМАНИЕ: ни одного каталога адаптера нет — ссылки не проверялись")
    print("\nИТОГ: 0 — адаптеры ссылаются на наши навыки")
    return 0


if __name__ == "__main__":
    sys.exit(main())
