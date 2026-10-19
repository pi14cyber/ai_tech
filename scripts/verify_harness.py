#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка целостности артефактов репозитория.

Зачем: 18.10.2026 два агента записали заметки не по выданным путям и затёрли
заметки другого источника. Правило в тексте от этого не спасает, нужна проверка.

Основание приёмов:
- сверка декларации и исполнителя в обе стороны — netresearch/agent-harness-skill,
  verify-harness.sh:336-362;
- коды возврата 0/1/2, где сломанная декларация это 2 и никогда 0 — там же :788-794;
- блокировка до выполнения, а не разбор после — enforcement-mechanisms.md:579-628.

Что проверяется:

1. Каждая заметка в internal/draft/extracts/notes объявляет источник в первой строке,
   и объявленный источник совпадает с префиксом имени файла.
   Именно это ловит наш сбой: файл от другого источника под чужим именем.
2. Диапазоны строк каждого источника идут подряд, без пропусков и наложений,
   начиная с первой строки и до конца файла источника.
   Это ловит второй сбой: неполное чтение книги.

Коды возврата:
  0 — всё сходится;
  1 — расхождение в фактах (пропуск, наложение, не тот источник);
  2 — сломана декларация: нет папки, файл назван не по шаблону, неизвестный источник.
"""

import os
import re
import sys

try:  # чтобы вердикт читался в консоли Windows без кракозябр
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES_DIR = os.path.join(ROOT, "internal", "draft", "extracts", "notes")
BIBLIO_DIR = os.path.join(ROOT, "internal", "docs", "biblio")

# префикс имени файла -> (файл источника, обязательная подстрока в первой строке)
SOURCES = {
    "thiel": ("Ot-nulya-k-edynytse.md", "Тиль"),
    "blank": ("b81d33ce-aa5a-41d3-a554-5360b50c053f.md", "Четыре шага"),
    "blankdorf": ("Blank-S.-Dorf-B.-StartUp.-Nastolnaya-kniga-osnovatelya.md", "Бланк и Дорф"),
    "momtest": ("Sprosi_mamu-_The_Mom_Test-_RU (2).md", "Спроси маму"),
}

NAME_RE = re.compile(r"^([a-z0-9]+)-(\d+)-(\d+)\.md$")


def source_lines(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return f.read().decode("utf-8", errors="replace").count("\n")


def main():
    broken = []   # код 2: декларация
    problems = []  # код 1: расхождения

    if not os.path.isdir(os.path.join(ROOT, "internal")) and "--self-test" not in sys.argv:
        print("РЕЖИМ ПОЛЬЗОВАТЕЛЯ: папки internal/ нет — заметки по источникам не проверяются")
        print("\nИТОГ: 0 — проверять нечего")
        return 0

    if not os.path.isdir(NOTES_DIR):
        broken.append("нет папки заметок: %s" % NOTES_DIR)
    else:
        seen = {}
        for name in sorted(os.listdir(NOTES_DIR)):
            full = os.path.join(NOTES_DIR, name)
            if not os.path.isfile(full) or not name.endswith(".md"):
                continue
            m = NAME_RE.match(name)
            if not m:
                broken.append("имя не по шаблону «источник-от-до.md»: %s" % name)
                continue
            slug, start, end = m.group(1), int(m.group(2)), int(m.group(3))

            if slug not in SOURCES:
                broken.append("неизвестный источник «%s» в файле %s" % (slug, name))
                continue
            if start > end:
                broken.append("перевёрнутый диапазон в %s: %d-%d" % (name, start, end))
                continue

            with open(full, "r", encoding="utf-8", errors="replace") as f:
                first = f.readline().strip()
            if not first:
                broken.append("пустая первая строка в %s: декларации нет" % name)
                continue
            expected = SOURCES[slug][1]
            if expected not in first:
                problems.append(
                    "чужой источник: %s объявляет «%s», ожидалось вхождение «%s»"
                    % (name, first[:80], expected)
                )

            seen.setdefault(slug, []).append((start, end, name))

        for slug, (src_file, _) in sorted(SOURCES.items()):
            ranges = sorted(seen.get(slug, []))
            src_path = os.path.join(BIBLIO_DIR, src_file)
            total = source_lines(src_path)
            if total is None:
                broken.append("не найден файл источника для «%s»: %s" % (slug, src_file))
                continue
            if not ranges:
                problems.append("нет ни одной заметки для источника «%s»" % slug)
                continue
            if ranges[0][0] != 1:
                problems.append(
                    "источник «%s»: покрытие начинается с %d, а не с 1"
                    % (slug, ranges[0][0])
                )
            for prev, cur in zip(ranges, ranges[1:]):
                if cur[0] <= prev[1]:
                    problems.append(
                        "источник «%s»: наложение %s и %s" % (slug, prev[2], cur[2])
                    )
                elif cur[0] != prev[1] + 1:
                    problems.append(
                        "источник «%s»: пропуск строк %d-%d между %s и %s"
                        % (slug, prev[1] + 1, cur[0] - 1, prev[2], cur[2])
                    )
            last_end = ranges[-1][1]
            if last_end < total - 1:
                problems.append(
                    "источник «%s»: покрытие кончается на %d, в файле %d строк"
                    % (slug, last_end, total)
                )
            print(
                "источник «%s»: заметок %d, покрытие 1-%d, строк в файле %d"
                % (slug, len(ranges), last_end, total)
            )

    print("")
    for line in broken:
        print("ДЕКЛАРАЦИЯ: %s" % line)
    for line in problems:
        print("РАСХОЖДЕНИЕ: %s" % line)

    if broken:
        print("\nИТОГ: 2 — сломана декларация, работу принимать нельзя")
        return 2
    if problems:
        print("\nИТОГ: 1 — расхождения, нужно чинить")
        return 1
    print("\nИТОГ: 0 — всё сходится")
    return 0


def self_test():
    """Проверка самого проверяльщика: он обязан произнести вердикт всегда.

    Приём взят из netresearch/agent-harness-skill, tests/verify-harness-runs.sh:43-65:
    важно не сообщение, а факт, что проверка вообще высказалась.
    """
    global NOTES_DIR, BIBLIO_DIR
    saved_notes, saved_biblio = NOTES_DIR, BIBLIO_DIR
    NOTES_DIR = os.path.join(ROOT, "scripts", "_selftest_empty_notes")
    BIBLIO_DIR = os.path.join(ROOT, "scripts", "_selftest_empty_biblio")
    os.makedirs(NOTES_DIR, exist_ok=True)
    os.makedirs(BIBLIO_DIR, exist_ok=True)
    code = main()
    NOTES_DIR, BIBLIO_DIR = saved_notes, saved_biblio
    for d in (NOTES_DIR, BIBLIO_DIR):
        pass
    empty_notes = os.path.join(ROOT, "scripts", "_selftest_empty_notes")
    empty_biblio = os.path.join(ROOT, "scripts", "_selftest_empty_biblio")
    for d in (empty_notes, empty_biblio):
        try:
            os.rmdir(d)
        except OSError:
            pass
    if code != 2:
        print("САМОПРОВЕРКА ПРОВАЛЕНА: на пустом каталоге ожидался код 2, получен %d" % code)
        return 1
    print("САМОПРОВЕРКА ПРОЙДЕНА: на пустом каталоге вердикт произнесён, код 2")
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
