#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка документации: все пути, названные в публичных файлах, существуют.

Зачем: сегодняшний разбор «Судья не автор» нашёл четыре расхождения в путях,
которые человек ловит только вручную. Машина ловит их за секунду.

Что проверяет: каждый упомянутый в публичном файле путь, заканчивающийся на
`.md`, `.py`, `.template` или `/`, должен существовать на диске от корня
репозитория (публичные пути пишутся с префиксом `kit/`).

Где проверяет (публичное лицо и правила):
  kit/AGENTS.md, kit/METHODOLOGY.md, kit/START.md, kit/GLOSSARY.md, README.md,
  kit/skills/**/SKILL.md, kit/templates/*.md, kit/knowledge/**/*.md

Чего не проверяет:
  - пути, начинающиеся с `workspace/` — это данные человека, их может не быть;
  - пути, начинающиеся с `inbox/` — входящие файлы человека, папки может не быть;
  - пути, начинающиеся с `kit/internal/` — внутренняя папка проекта, у пользователя её нет;
  - разделы-планы (`## План пополнения`): всё, что ниже такого заголовка, — будущие файлы,
    поэтому остаток файла после него не проверяется;
  - строки, где встречаются слова «взят», «чужой», «образец», «цитат»: там описываются
    чужие материалы, а не наши пути;
  - примеры с заглушками: `<...>`, `...`, `XX`, `YYYY`.

Коды возврата: 0 — все пути на месте; 1 — есть отсутствующие; 2 — нечего проверять.
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
TARGETS = ["kit/AGENTS.md", "kit/METHODOLOGY.md", "README.md", "kit/START.md",
           "kit/GLOSSARY.md", "kit/skills/INDEX.md", "kit/templates/README.md"]
SKIP_PREFIXES = ("workspace/", "inbox/", "internal/", "kit/internal/", "http", "mailto:")
TOKEN_RE = re.compile(r"`([^`\n]+)`")
PATH_END_RE = re.compile(r"(\.md|\.py|\.template|/)$")
PLACEHOLDER_RE = re.compile(r"<|\.\.\.|XX|YYYY|/\*|\*")


def collect_files():
    files = []
    for name in TARGETS:
        path = os.path.join(ROOT, *name.split("/"))
        if os.path.exists(path):
            files.append(path)
    for sub, pattern in (("skills", "SKILL.md"), ("templates", ".md"), ("knowledge", ".md")):
        base = os.path.join(KIT, sub)
        for dirpath, _dirnames, filenames in os.walk(base):
            for filename in filenames:
                if filename == pattern or (pattern == ".md" and filename.endswith(".md")):
                    files.append(os.path.join(dirpath, filename))
    return sorted(set(files))


def main():
    files = collect_files()
    if not files:
        print("ИТОГ: 2 — не найдено ни одного публичного файла для проверки")
        return 2

    missing = []
    checked = 0
    for path in files:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
        plan = False
        for number, line in enumerate(lines, 1):
            if line.startswith("## План"):
                plan = True
            if plan:
                continue
            for token in TOKEN_RE.findall(line):
                token = token.strip()
                if not token or not PATH_END_RE.search(token):
                    continue
                if " " in token:
                    continue  # это команда, а не путь
                if token.startswith(SKIP_PREFIXES) or PLACEHOLDER_RE.search(token):
                    continue
                if any(marker in line.lower() for marker in ("чужой", "взят", "образец", "цитат")):
                    continue  # это ссылка на чужой репозиторий или цитата, а не наш путь
                if ":" in token.split("/")[-1] and not token.endswith("/"):
                    continue
                checked += 1
                clean = token.rstrip("/")
                candidates = [
                    os.path.join(ROOT, *clean.split("/")),
                    os.path.join(os.path.dirname(path), *clean.split("/")),
                ]
                if not any(os.path.exists(c) for c in candidates):
                    missing.append("%s:%d → %s" % (os.path.relpath(path, ROOT).replace("\\", "/"), number, token))

    print("проверено ссылок: %d в %d файлах" % (checked, len(files)))
    for line in missing:
        print("НЕТ ПУТИ: %s" % line)

    if missing:
        print("\nИТОГ: 1 — %d названных путей не существует" % len(missing))
        return 1
    print("\nИТОГ: 0 — все названные пути на месте")
    return 0


if __name__ == "__main__":
    sys.exit(main())
