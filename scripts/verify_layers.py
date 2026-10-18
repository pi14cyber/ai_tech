#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка разделения слоёв: универсалии не зависят от конкретики.

Зачем: набор состоит из двух слоёв. Универсалии — метод, навыки, шаблоны,
проверки. Конкретика — данные человека и материалы этого проекта.

Правило: то, что выдаётся пользователю (навыки и шаблоны), не должно ссылаться
на внутреннюю папку проекта. Иначе чужой агент пойдёт читать наши черновики,
и набор перестанет быть переносимым.

Что проверяет: в `skills/**` и `templates/**` нет упоминаний `internal/`.

Чего не проверяет: правила и методику — им положено объяснять, где какой слой
живёт, поэтому упоминание `internal/` там законно.

Коды возврата: 0 — слои разделены; 1 — есть смешение; 2 — нечего проверять.
"""

import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNIVERSAL_DIRS = ("skills", "templates")
FORBIDDEN = re.compile(r"internal/")


def main():
    files = []
    for sub in UNIVERSAL_DIRS:
        for dirpath, _dirnames, filenames in os.walk(os.path.join(ROOT, sub)):
            for filename in filenames:
                if filename.endswith(".md"):
                    files.append(os.path.join(dirpath, filename))

    if not files:
        print("ИТОГ: 2 — не найдено файлов навыков и шаблонов")
        return 2

    violations = []
    for path in sorted(files):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for number, line in enumerate(f, 1):
                if FORBIDDEN.search(line):
                    rel = os.path.relpath(path, ROOT).replace("\\", "/")
                    violations.append("%s:%d → %s" % (rel, number, line.strip()[:90]))

    print("проверено файлов: %d" % len(files))
    for line in violations:
        print("СМЕШЕНИЕ СЛОЁВ: %s" % line)

    if violations:
        print("\nИТОГ: 1 — %d мест, где универсалии ссылаются на конкретику" % len(violations))
        return 1
    print("\nИТОГ: 0 — навыки и шаблоны не зависят от внутренней папки проекта")
    return 0


if __name__ == "__main__":
    sys.exit(main())
