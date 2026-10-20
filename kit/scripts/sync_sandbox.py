#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Синхронизация песочницы runs/self-01 с публичным слоем репозитория.

Зачем: `verify_sandbox.py` требует, чтобы копия совпадала с репозиторием. После
каждой правки публичного слоя копию нужно пересобрать; вручную это делать
долго и легко забыть, поэтому — один скрипт.

Раскладка v3.0: машинная часть набора живёт в `kit/`, в корне — только вход для
человека (`README.md`, `LICENSE`) и зоны данных (`workspace/`, `inbox/`, `runs/`).
Поэтому копирует скрипт `kit/` целиком (без `kit/internal/` — внутренняя кухня
проекта в набор пользователя не входит) и корневые `README.md`, `LICENSE`.

Служебное (`__pycache__`, `_selftest*`, `.pyc`) не копируется. Старая раскладка
в песочнице (`AGENTS.md`, `skills/` и прочее в корне копии) удаляется: двух
расходящихся версий одного текста быть не должно.

Чего не делает: не трогает `runs/self-01/workspace/` — данные прогона остаются.
Каталоги оболочек (`.dsh`, `.claude`, `.agents`) в копии удаляются: ссылки в них
ведут на старые пути и пересоздаются `make_skill_adapters.py` в самой песочнице.
"""

import os
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
ROOT = os.path.dirname(KIT)
RUN = os.path.join(ROOT, "runs", "self-01")
KIT_DIRS = ("rules", "skills", "templates", "knowledge", "scripts")
KIT_FILES = ("AGENTS.md", "START.md", "GLOSSARY.md", "METHODOLOGY.md",
             "CHANGELOG.md", "STRUCTURE.md")
ROOT_FILES = ("README.md", "LICENSE")
OLD_ROOT_ENTRIES = ("AGENTS.md", "START.md", "GLOSSARY.md", "METHODOLOGY.md",
                    "CHANGELOG.md", "STRUCTURE.md", "rules", "skills", "templates",
                    "knowledge", "scripts", ".dsh", ".claude", ".agents")
SKIP = ("__pycache__", "_selftest", ".pyc")


def skip(name):
    return any(part in name for part in SKIP)


def main():
    if not os.path.isdir(os.path.join(KIT, "internal")):
        print("ИТОГ: 0 — режим пользователя: песочница не нужна")
        return 0
    if not os.path.isdir(RUN):
        print("ИТОГ: 2 — папки runs/self-01 нет: создавать копию некуда")
        return 2

    # Старая раскладка: публичные файлы лежали прямо в корне копии.
    for name in OLD_ROOT_ENTRIES:
        stale = os.path.join(RUN, name)
        if os.path.isdir(stale) and not os.path.islink(stale):
            shutil.rmtree(stale)
        elif os.path.exists(stale) or os.path.islink(stale):
            os.remove(stale)

    kit_copy = os.path.join(RUN, "kit")
    if os.path.isdir(kit_copy):
        shutil.rmtree(kit_copy)
    os.makedirs(kit_copy)
    for directory in KIT_DIRS:
        src = os.path.join(KIT, directory)
        if not os.path.isdir(src):
            continue
        shutil.copytree(src, os.path.join(kit_copy, directory),
                        ignore=shutil.ignore_patterns(*SKIP))
    for name in KIT_FILES:
        src = os.path.join(KIT, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(kit_copy, name))
    for name in ROOT_FILES:
        src = os.path.join(ROOT, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(RUN, name))
    print("ИТОГ: 0 — песочница синхронизирована: kit/ (без internal) + README.md, LICENSE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
