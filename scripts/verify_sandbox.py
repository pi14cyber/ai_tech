#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка песочницы: копия публичного слоя должна совпадать с репозиторием.

Зачем: аудит 20.10.2026 нашёл, что `runs/self-01` отстал на восемь файлов, и
ни одна проверка этого не видела. Песочница — вторая версия публичного слоя,
а правило репозитория запрещает две расходящиеся версии одного текста.

Что проверяет: наличие песочницы `runs/self-01`, совпадение по содержимому
публичных файлов и папок: корневые документы, `rules/`, `skills/`, `templates/`,
`scripts/`, `knowledge/`. Служебные и сгенерированные файлы (`__pycache__`,
самотесты, `*.pyc`, ссылки оболочек) не сравниваются.

Чего не проверяет: данных `workspace/` человека — их в песочнице может не быть;
истории git; клонов.

Коды: 0 — песочницы нет или она совпадает; 1 — расхождения; 2 — песочница есть,
но не читается.
"""

import filecmp
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN = os.path.join(ROOT, "runs", "self-01")
PUBLIC_FILES = ("README.md", "AGENTS.md", "START.md", "GLOSSARY.md",
                "METHODOLOGY.md", "CHANGELOG.md", "LICENSE")
PUBLIC_DIRS = ("rules", "skills", "templates", "scripts", "knowledge")
SKIP_PARTS = ("__pycache__", "_selftest", ".pyc")


def skip(path):
    return any(part in path for part in SKIP_PARTS)


def walk_public(base):
    seen = set()
    for name in PUBLIC_FILES:
        if os.path.exists(os.path.join(base, name)):
            seen.add(name)
    for directory in PUBLIC_DIRS:
        top = os.path.join(base, directory)
        if not os.path.isdir(top):
            continue
        for dirpath, _dirnames, filenames in os.walk(top):
            for filename in filenames:
                full = os.path.join(dirpath, filename)
                rel = os.path.relpath(full, base).replace("\\", "/")
                if not skip(rel):
                    seen.add(rel)
    return seen


def main():
    if os.path.islink(RUN) or os.path.realpath(RUN) == os.path.realpath(ROOT):
        print("ИТОГ: 2 — runs/self-01 является ссылкой на репозиторий: сверка с самой собой невозможна")
        return 2
    if not os.path.isdir(RUN):
        if os.path.isdir(os.path.join(ROOT, "runs")):
            print("ИТОГ: 2 — каталог runs/ есть, а песочницы self-01 нет: копия не сверена")
            return 2
        print("песочницы runs/self-01 нет — проверять нечего")
        print("\nИТОГ: 0 — копии нет")
        return 0
    try:
        repo = walk_public(ROOT)
        sandbox = walk_public(RUN)
    except Exception as error:
        print("ИТОГ: 2 — песочница не читается: %s" % error)
        return 2

    problems = []
    for rel in sorted(repo - sandbox):
        problems.append("runs/self-01 — нет файла %s" % rel)
    for rel in sorted(sandbox - repo):
        problems.append("runs/self-01 — лишний файл %s" % rel)
    for rel in sorted(repo & sandbox):
        if not filecmp.cmp(os.path.join(ROOT, rel), os.path.join(RUN, rel), shallow=False):
            problems.append("runs/self-01 — %s расходится с репозиторием" % rel)

    print("файлов в репозитории: %d, в песочнице: %d" % (len(repo), len(sandbox)))
    for line in problems:
        print("РАСХОЖДЕНИЕ: %s" % line)
    if problems:
        print("\nИТОГ: 1 — песочница расходится с репозиторием (%d)" % len(problems))
        return 1
    print("\nИТОГ: 0 — песочница совпадает с репозиторием")
    return 0


if __name__ == "__main__":
    sys.exit(main())
