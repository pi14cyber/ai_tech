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
"""

import importlib.util
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = (
    ("Заметки по источникам", "verify_harness.py"),
    ("База знаний", "verify_knowledge.py"),
    ("Внешнее исследование", "verify_research.py"),
    ("Структура запросов", "verify_requests.py"),
    ("Состояние запросов", "verify_state.py"),
    ("Навыки: шапка и имена", "verify_skills.py"),
    ("Документация и пути", "verify_docs.py"),
    ("Разделение слоёв", "verify_layers.py"),
    ("Ссылки в заметках", "verify_notes.py"),
    ("Адаптеры навыков", "verify_adapters.py"),
    ("Числа и формы", "verify_consistency.py"),
    ("Канон: числа и статусы", "verify_canon.py"),
    ("Артефакты workspace", "check_workspace.py"),
    ("Песочница", "verify_sandbox.py"),
)


def load(name, filename):
    path = os.path.join(HERE, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    codes = []
    crashed = set()
    for index, (title, filename) in enumerate(CHECKS):
        print("=" * 60)
        print("ПРОВЕРКА: %s" % title)
        print("=" * 60)
        try:
            module = load(filename[:-3], filename)
            code = module.main()
        except Exception as error:  # сломанный проверяльщик — это код 2, не 0
            print("ПРОВЕРЯЛЬЩИК УПАЛ: %s" % error)
            crashed.add(index)
            code = 2
        codes.append(code)
        print("")

    worst = max(codes)
    marker = os.path.join(os.path.dirname(HERE), "workspace", "LOCAL-ONLY")
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
