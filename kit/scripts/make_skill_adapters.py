#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Адаптер навыков: ссылки из наших папок в каталоги, которые читают агенты.

Зачем: наш `kit/skills/` — раскладка набора, и оболочки её сами не видят. У каждой
оболочки свой каталог: DSH читает `<корень>/.dsh/skills`, Claude Code — `.claude/skills`,
агентская раскладка — `.agents/skills`. Адаптер наполняет эти каталоги ССЫЛКАМИ на
наши папки навыков.

Почему только ссылки: копия порождает вторую версию навыка, а две версии одного
текста запрещены правилами репозитория. Если в целевом каталоге лежит копия
(обычная папка), скрипт её не трогает и говорит об этом.

Что делает:

1. Читает список навыков из `kit/skills/*/SKILL.md`.
2. В каждом целевом каталоге создаёт ссылку на папку навыка, если ссылки ещё нет.
3. Найденные копии и лишние записи перечисляет и оставляет как есть.
4. `--remove` удаляет только ссылки, созданные адаптером; копии не трогает.

Коды возврата: 0 — ссылки готовы; 1 — есть копии или лишние записи; 2 — нет папки навыков.
"""

import os
import re
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
ROOT = os.path.dirname(KIT)
SKILLS_DIR = os.path.join(KIT, "skills")
NAME_RE = re.compile(r"^---\s*\n(?:.*\n)*?name:\s*([a-z0-9-]+)\s*\n", re.MULTILINE)

# каталог -> как называется источник (для отчёта)
TARGETS = (
    (".dsh/skills", "DSH: project-dsh"),
    (".claude/skills", "Claude Code"),
    (".agents/skills", "агентская раскладка"),
)


def skills():
    out = []
    for name in sorted(os.listdir(SKILLS_DIR)):
        folder = os.path.join(SKILLS_DIR, name)
        if not os.path.isdir(folder):
            continue
        path = os.path.join(folder, "SKILL.md")
        if not os.path.exists(path):
            continue
        out.append(name)
    return out


def is_link(path):
    return os.path.islink(path) or os.path.isjunction(path) if hasattr(os.path, "isjunction") else os.path.islink(path)


def make_link(target, source):
    if os.name == "nt":
        os.system('cmd /c mklink /J "%s" "%s" >nul' % (target, source))
        return os.path.islink(target) or (hasattr(os.path, "isjunction") and os.path.isjunction(target))
    os.symlink(source, target, target_is_directory=True)
    return os.path.islink(target)


def main():
    if not os.path.isdir(SKILLS_DIR):
        print("ИТОГ: 2 — нет папки навыков: %s" % SKILLS_DIR)
        return 2
    remove = "--remove" in sys.argv
    names = skills()
    if not names:
        print("ИТОГ: 2 — в папке навыков нет ни одной папки с SKILL.md")
        return 2

    created = removed = 0
    notes = []
    for rel, source_note in TARGETS:
        base = os.path.join(ROOT, *rel.split("/"))
        if remove:
            if not os.path.isdir(base):
                continue
            for entry in sorted(os.listdir(base)):
                path = os.path.join(base, entry)
                if is_link(path):
                    os.remove(path)
                    removed += 1
            try:
                if not os.listdir(base):
                    os.rmdir(base)
            except OSError:
                pass
            continue
        os.makedirs(base, exist_ok=True)
        for name in names:
            target = os.path.join(base, name)
            if os.path.exists(target) or is_link(target):
                if not is_link(target):
                    notes.append("%s: %s — копия, не ссылка (не трогаю)" % (rel, name))
                continue
            if not make_link(target, os.path.join(SKILLS_DIR, name)):
                notes.append("%s: %s — ссылку создать не удалось" % (rel, name))
                continue
            created += 1
        extra = [e for e in sorted(os.listdir(base)) if e not in names and not e.startswith(".")]
        for entry in extra:
            path = os.path.join(base, entry)
            if is_link(path):
                notes.append("%s: лишняя ссылка %s" % (rel, entry))
            else:
                notes.append("%s: лишняя запись %s" % (rel, entry))
        print("%s (%s): навыков %d" % (rel, source_note, len(names)))

    print("")
    if remove:
        print("удалено ссылок: %d" % removed)
    else:
        print("создано ссылок: %d" % created)
    for note in notes:
        print("ЗАМЕЧАНИЕ: %s" % note)
    if notes and not remove:
        print("\nИТОГ: 1 — есть копии или лишние записи, разбери их руками")
        return 1
    print("\nИТОГ: 0 — адаптеры готовы")
    return 0


if __name__ == "__main__":
    sys.exit(main())
