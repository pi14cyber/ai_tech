#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Синхронизация песочницы runs/self-01 с публичным слоем репозитория.

Зачем: `verify_sandbox.py` требует, чтобы копия совпадала с репозиторием. После
каждой правки публичного слоя копию нужно пересобрать; вручную это делать
долго и легко забыть, поэтому — один скрипт.

Что копирует: `rules/`, `skills/`, `templates/`, `scripts/`, `knowledge/` и
корневые документы. Служебное (`__pycache__`, `_selftest*`, `.git`) не копируется.

Чего не делает: не трогает `runs/self-01/workspace/` — данные прогона остаются.
"""

import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN = os.path.join(ROOT, "runs", "self-01")
DIRS = ("rules", "skills", "templates", "scripts", "knowledge")
FILES = ("README.md", "AGENTS.md", "START.md", "GLOSSARY.md", "METHODOLOGY.md",
         "CHANGELOG.md", "LICENSE")
SKIP = ("__pycache__", "_selftest", ".pyc")


def skip(name):
    return any(part in name for part in SKIP)


def main():
    if not os.path.isdir(os.path.join(ROOT, "internal", "draft")):
        print("ИТОГ: 0 — режим пользователя: песочница не нужна")
        return 0
    if not os.path.isdir(RUN):
        print("ИТОГ: 2 — папки runs/self-01 нет: создавать копию некуда")
        return 2
    for directory in DIRS:
        src = os.path.join(ROOT, directory)
        dst = os.path.join(RUN, directory)
        if not os.path.isdir(src):
            continue
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*SKIP))
    for name in FILES:
        src = os.path.join(ROOT, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(RUN, name))
    print("ИТОГ: 0 — песочница синхронизирована")
    return 0


if __name__ == "__main__":
    sys.exit(main())
