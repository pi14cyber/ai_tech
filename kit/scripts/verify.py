#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Единый вход проверок репозитория.

Запускает проверки по очереди и возвращает худший из кодов:
0 — в перечисленных проверках расхождений нет, 1 — расхождения,
2 — сломана декларация или упал сам проверяльщик.

Зачем один вход: много команд забываются, а одна запоминается. Агент обязан
прогнать её перед тем, как объявить работу законченной (AGENTS.md, раздел 13).

Ноль означает «в проверенном расхождений нет», а не «всё проверено»: у каждой
проверки свой список того, что она не ловит, и он записан в её шапке.

Раскладка: скрипты лежат в `kit/scripts/`, поэтому `KIT` — папка набора,
`ROOT` — корень репозитория (там `workspace/` человека, `runs/`, `README.md`).
Пути к проверкам в CHECKS записаны от `ROOT` — так их видит канон.
"""

import importlib.util
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
ROOT = os.path.dirname(KIT)
CHECKS = (
    ("Заметки по источникам", "kit/scripts/verify_harness.py"),
    ("База знаний", "kit/scripts/verify_knowledge.py"),
    ("Внешнее исследование", "kit/scripts/verify_research.py"),
    ("Структура запросов", "kit/scripts/verify_requests.py"),
    ("Состояние запросов", "kit/scripts/verify_state.py"),
    ("Навыки: шапка и имена", "kit/scripts/verify_skills.py"),
    ("Документация и пути", "kit/scripts/verify_docs.py"),
    ("Разделение слоёв", "kit/scripts/verify_layers.py"),
    ("Ссылки в заметках", "kit/scripts/verify_notes.py"),
    ("Адаптеры навыков", "kit/scripts/verify_adapters.py"),
    ("Числа и формы", "kit/scripts/verify_consistency.py"),
    ("Канон: числа и статусы", "kit/scripts/verify_canon.py"),
    ("Артефакты workspace", "kit/scripts/check_workspace.py"),
    ("Песочница", "kit/scripts/verify_sandbox.py"),
    ("Структура описана", "kit/scripts/verify_structure.py"),
)


def load(name, filename):
    path = os.path.join(ROOT, *filename.split("/"))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    if len(sys.argv) > 1:
        print("ИТОГ: 2 — verify.py не принимает аргументов; --root есть только у отдельных проверок "
              "(check_workspace.py, verify_canon.py)")
        return 2
    codes = []
    crashed = set()
    for index, (title, filename) in enumerate(CHECKS):
        print("=" * 60)
        print("ПРОВЕРКА: %s" % title)
        print("=" * 60)
        try:
            module = load(os.path.basename(filename)[:-3], filename)
            code = module.main()
        except Exception as error:  # сломанный проверяльщик — это код 2, не 0
            print("ПРОВЕРЯЛЬЩИК УПАЛ: %s" % error)
            crashed.add(index)
            code = 2
        codes.append(code)
        print("")

    worst = max(codes)
    marker = os.path.join(ROOT, "workspace", "LOCAL-ONLY")
    mode = "только локально" if os.path.exists(marker) else "обычный (внешние запросы разрешены)"
    print("=" * 60)
    print("РЕЖИМ: %s" % mode)
    if os.path.exists(marker):
        print("  Файл workspace/LOCAL-ONLY на месте: запросы наружу не отправляются,")
        print("  предвалидация помечается [допущение], задания копятся в очереди.")
    print("=" * 60)
    print("ИТОГ ПО ВСЕМ ПРОВЕРКАМ: %d" % worst)
    print("=" * 60)
    for index, ((title, _), code) in enumerate(zip(CHECKS, codes)):
        if index in crashed:
            state = "проверяльщик упал"
        else:
            state = {0: "сходится", 1: "расхождения", 2: "сломана декларация"}.get(code, "?")
        print("  %-24s %d (%s)" % (title, code, state))
    return worst


if __name__ == "__main__":
    sys.exit(main())
