#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка карты структуры: STRUCTURE.md описывает все публичные файлы и не врёт.

Зачем: структура репозитория должна быть описана в одном месте. Если появился
новый навык, шаблон или скрипт, а в карте его нет — он невидим; если файл
удалён, а строка осталась — карта врёт. Обе ситуации ловятся здесь.

Что проверяет:
 1. `kit/STRUCTURE.md` существует.
 2. Каждый публичный файл корня, файл набора, папка, навык, шаблон и скрипт
    упомянуты в карте.
 3. Каждый путь вида `kit/scripts/x.py`, `kit/skills/x/SKILL.md`,
    `kit/templates/x.md`, `kit/rules/canon.json`, `kit/knowledge/INDEX.md`
    из карты существует на диске (пути считаются от корня репозитория).

Чего не проверяет: смысл описаний и порядок разделов. Папку `inbox/` не требует:
это зона человека, карта описывает публичный набор.

Коды: 0 — карта полная и без устаревших путей; 1 — расхождения; 2 — нет карты.
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
MAP = os.path.join(KIT, "STRUCTURE.md")
ROOT_FILES = ("README.md", "LICENSE")
KIT_FILES = ("START.md", "AGENTS.md", "METHODOLOGY.md", "GLOSSARY.md",
             "CHANGELOG.md", "STRUCTURE.md")
ROOT_DIRS = ("kit", "workspace", "runs", ".dsh", ".claude", ".agents", "gtm-cofounder")
KIT_DIRS = ("rules", "skills", "templates", "knowledge", "scripts", "internal")
TOKEN_RE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:py|md|json))`")
KIT_PREFIXES = ("kit/",)
LEGACY_PREFIXES = ("scripts/", "skills/", "templates/", "rules/", "knowledge/")


def read(path):
    return open(path, encoding="utf-8", errors="replace").read()


def main():
    if not os.path.exists(MAP):
        print("ИТОГ: 2 — нет kit/STRUCTURE.md: структура не описана")
        return 2
    text = read(MAP)
    problems = []

    for name in ROOT_FILES:
        if os.path.exists(os.path.join(ROOT, name)) and name not in text:
            problems.append("STRUCTURE.md — не описан корневой файл %s" % name)

    for name in KIT_FILES:
        if os.path.exists(os.path.join(KIT, name)) and name not in text:
            problems.append("STRUCTURE.md — не описан файл набора kit/%s" % name)

    for directory in ROOT_DIRS:
        if os.path.isdir(os.path.join(ROOT, directory)) and directory not in text:
            problems.append("STRUCTURE.md — не описана папка %s/" % directory)

    for directory in KIT_DIRS:
        if os.path.isdir(os.path.join(KIT, directory)) and directory not in text:
            problems.append("STRUCTURE.md — не описана папка kit/%s/" % directory)

    skill_dirs = sorted(os.listdir(os.path.join(KIT, "skills")))
    for skill in skill_dirs:
        skill_file = os.path.join(KIT, "skills", skill, "SKILL.md")
        if os.path.isfile(skill_file) and skill not in text:
            problems.append("STRUCTURE.md — не описан навык kit/skills/%s" % skill)

    templates = sorted(os.listdir(os.path.join(KIT, "templates")))
    for template in templates:
        if template.endswith(".md") and template != "README.md" and template not in text:
            problems.append("STRUCTURE.md — не описан шаблон kit/templates/%s" % template)

    scripts = sorted(p for p in os.listdir(os.path.join(KIT, "scripts")) if p.endswith(".py"))
    for script in scripts:
        if script not in text:
            problems.append("STRUCTURE.md — не описан скрипт kit/scripts/%s" % script)

    for token in set(TOKEN_RE.findall(text)):
        if token.startswith(LEGACY_PREFIXES):
            base = KIT
        elif token.startswith(KIT_PREFIXES):
            base = ROOT
        else:
            continue
        if not os.path.exists(os.path.join(base, *token.split("/"))):
            problems.append("STRUCTURE.md — запись «%s» указывает на несуществующий файл" % token)

    print("корневых файлов: %d, папок: %d, навыков: %d, шаблонов: %d, скриптов: %d"
          % (len(ROOT_FILES) + len(KIT_FILES), len(ROOT_DIRS) + len(KIT_DIRS),
             len([1 for s in skill_dirs
                  if os.path.isfile(os.path.join(KIT, "skills", s, "SKILL.md"))]),
             len([t for t in templates if t.endswith(".md") and t != "README.md"]),
             len(scripts)))
    for line in problems:
        print("РАСХОЖДЕНИЕ: %s" % line)
    if problems:
        print("\nИТОГ: 1 — карта структуры разошлась с диском (%d)" % len(problems))
        return 1
    print("\nИТОГ: 0 — карта структуры полная и без устаревших путей")
    return 0


if __name__ == "__main__":
    sys.exit(main())
