#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка карты структуры: STRUCTURE.md описывает все публичные файлы и не врёт.

Зачем: структура репозитория должна быть описана в одном месте. Если появился
новый навык, шаблон или скрипт, а в карте его нет — он невидим; если файл
удалён, а строка осталась — карта врёт. Обе ситуации ловятся здесь.

Что проверяет:
 1. `STRUCTURE.md` существует.
 2. Каждый корневой публичный файл, папка, навык, шаблон и скрипт упомянуты в карте.
 3. Каждый путь вида `scripts/x.py`, `skills/x/SKILL.md`, `templates/x.md`,
    `rules/canon.json`, `knowledge/INDEX.md` из карты существует на диске.

Чего не проверяет: смысл описаний и порядок разделов.

Коды: 0 — карта полная и без устаревших путей; 1 — расхождения; 2 — нет карты.
"""

import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, "STRUCTURE.md")
ROOT_FILES = ("README.md", "START.md", "AGENTS.md", "METHODOLOGY.md", "GLOSSARY.md",
              "CHANGELOG.md", "LICENSE", "STRUCTURE.md")
DIRS = ("rules", "skills", "templates", "knowledge", "scripts", "workspace",
        "internal", "runs", ".dsh", ".claude", ".agents")


def read(path):
    return open(path, encoding="utf-8", errors="replace").read()


def main():
    if not os.path.exists(MAP):
        print("ИТОГ: 2 — нет STRUCTURE.md: структура не описана")
        return 2
    text = read(MAP)
    problems = []

    for name in ROOT_FILES:
        if os.path.exists(os.path.join(ROOT, name)) and name not in text:
            problems.append("STRUCTURE.md — не описан корневой файл %s" % name)

    for directory in DIRS:
        if os.path.isdir(os.path.join(ROOT, directory)) and directory not in text:
            problems.append("STRUCTURE.md — не описана папка %s/" % directory)

    for skill in sorted(os.listdir(os.path.join(ROOT, "skills"))):
        skill_file = os.path.join(ROOT, "skills", skill, "SKILL.md")
        if os.path.isfile(skill_file) and skill not in text:
            problems.append("STRUCTURE.md — не описан навык skills/%s" % skill)

    for template in sorted(os.listdir(os.path.join(ROOT, "templates"))):
        if template.endswith(".md") and template != "README.md" and template not in text:
            problems.append("STRUCTURE.md — не описан шаблон templates/%s" % template)

    for script in sorted(os.listdir(os.path.join(ROOT, "scripts"))):
        if script.endswith(".py") and script not in text:
            problems.append("STRUCTURE.md — не описан скрипт scripts/%s" % script)

    for token in set(re.findall(r"`([A-Za-z0-9_./-]+\.(?:py|md|json))`", text)):
        if token.startswith(("scripts/", "skills/", "templates/", "rules/", "knowledge/")):
            if not os.path.exists(os.path.join(ROOT, *token.split("/"))):
                problems.append("STRUCTURE.md — запись «%s» указывает на несуществующий файл" % token)

    print("корневых файлов: %d, папок: %d, навыков: %d, шаблонов: %d, скриптов: %d"
          % (len(ROOT_FILES), len(DIRS),
             len([1 for s in os.listdir(os.path.join(ROOT, "skills"))
                  if os.path.isfile(os.path.join(ROOT, "skills", s, "SKILL.md"))]),
             len([t for t in os.listdir(os.path.join(ROOT, "templates")) if t.endswith(".md") and t != "README.md"]),
             len([p for p in os.listdir(os.path.join(ROOT, "scripts")) if p.endswith(".py")])))
    for line in problems:
        print("РАСХОЖДЕНИЕ: %s" % line)
    if problems:
        print("\nИТОГ: 1 — карта структуры разошлась с диском (%d)" % len(problems))
        return 1
    print("\nИТОГ: 0 — карта структуры полная и без устаревших путей")
    return 0


if __name__ == "__main__":
    sys.exit(main())
