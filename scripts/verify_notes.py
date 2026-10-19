#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ссылки в заметках о клонах: путь и строка сверяются с диском.

Зачем: заметки в `internal/draft/research-notes/` пишут агенты, а ссылка в них —
это `путь/к/файлу:строка`. Публичная проверка путей (`verify_docs.py`) внутреннюю
папку пропускает намеренно, поэтому ссылки заметок не проверял никто: ошибка в
пути или в номере строки выглядела как честная ссылка.

Что проверяет: цели markdown-ссылок и инлайн-код, которые указывают на файлы
проекта: `internal/research/…`, `internal/draft/…`, `internal/docs/…`,
`scripts/*.py`, `skills/<наш навык>/…`, `knowledge/…`, `templates/…` и файлы
корня. Пути внутри чужих репозиториев (например `skills/mom-test/SKILL.md`
в заметке о клоне) не проверяются: они относительны корня клона.

Для файлов дополнительно проверяется, что номер строки не больше числа строк.

Если папка клонов `internal/research/` отсутствует, ссылки на клоны
пропускаются, и проверка говорит об этом прямо — вместо тихого нуля.

Коды возврата: 0 — ссылки сходятся или проверка честно пропущена; 1 — есть
отсутствующие пути или строки; 2 — нет папки заметок.
"""

import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES_DIR = os.path.join(ROOT, "internal", "draft", "research-notes")
CLONES_DIR = os.path.join(ROOT, "internal", "research")
SKILLS_DIR = os.path.join(ROOT, "skills")

LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
LINK_ALL_RE = re.compile(r"\[[^\]]*\]\([^)]*\)")
CODE_RE = re.compile(r"`([^`\n]+)`")
ROOT_FILES = ()
INTERNAL_PREFIXES = ("internal/research/", "internal/draft/", "internal/docs/")
PLACEHOLDER_RE = re.compile(r"<|\.\.\.|XX|YYYY|\*")


def project_ref(path):
    """Относится ли путь к проекту однозначно.

    Берём только то, что не спутать с путём внутри чужого клона: заметки пишут
    и относительные пути клона (`skills/mom-test/SKILL.md`), и пути проекта.
    Абсолютно надёжны только `internal/…` и канон `knowledge/…`; `skills/`
    проверяем по списку наших навыков. Голые `README.md`, `scripts/`,
    `templates/`, `workspace/` не проверяются: они бывают и там, и там.
    """
    if path.startswith(INTERNAL_PREFIXES):
        return True
    if path.startswith("knowledge/"):
        return True
    if path.startswith("skills/"):
        parts = path.split("/")
        return len(parts) > 2 and os.path.isdir(os.path.join(SKILLS_DIR, parts[1]))
    return False


def clean_token(token):
    """Делит ссылку на путь и номер строки: `a/b.py:12, 40-46` → (`a/b.py`, 12)."""
    token = token.rstrip(".,;:")
    if "#L" in token:
        path, _, anchor = token.partition("#L")
        number = re.match(r"(\d+)", anchor)
        return path, int(number.group(1)) if number else None
    match = re.match(r"^(.*?)(?::(\d+).*)?$", token)
    if not match:
        return token, None
    path = match.group(1)
    number = match.group(2)
    return path, int(number) if number else None


def refs_of(line):
    targets = LINK_RE.findall(line)
    without_links = LINK_ALL_RE.sub(" ", line)
    targets += CODE_RE.findall(without_links)
    out = []
    for raw in targets:
        if PLACEHOLDER_RE.search(raw):
            continue
        path, number = clean_token(raw)
        if path and project_ref(path):
            out.append((path, number))
    return out


def line_count(path):
    try:
        with open(path, "rb") as f:
            return f.read().decode("utf-8", errors="replace").count("\n") + 1
    except OSError:
        return None


def main():
    if not os.path.isdir(os.path.join(ROOT, "internal")):
        print("РЕЖИМ ПОЛЬЗОВАТЕЛЯ: папки internal/ нет — заметки о клонах не проверяются")
        print("\nИТОГ: 0 — проверять нечего")
        return 0

    if not os.path.isdir(NOTES_DIR):
        print("ИТОГ: 2 — нет папки заметок: %s" % NOTES_DIR)
        return 2

    notes = sorted(f for f in os.listdir(NOTES_DIR) if f.endswith(".md"))
    if not notes:
        print("ИТОГ: 2 — в папке заметок нет ни одного файла")
        return 2

    clones_present = os.path.isdir(CLONES_DIR)
    missing = []
    checked = 0
    skipped = 0

    for name in notes:
        with open(os.path.join(NOTES_DIR, name), "r", encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
        for number, line in enumerate(lines, 1):
            for path, source_line in refs_of(line):
                if path.startswith("internal/research/") and not clones_present:
                    skipped += 1
                    continue
                full = os.path.join(ROOT, *path.split("/"))
                checked += 1
                if not os.path.exists(full):
                    missing.append("%s:%d → %s (нет такого пути)" % (name, number, path))
                elif source_line is not None and os.path.isfile(full):
                    total = line_count(full)
                    if total is not None and source_line > total:
                        missing.append(
                            "%s:%d → %s:%d (в файле %d строк)"
                            % (name, number, path, source_line, total)
                        )

    unique = sorted(set(missing))
    print("файлов заметок: %d, ссылок проверено: %d, пропущено из-за клонов: %d"
          % (len(notes), checked, skipped))
    for line in unique:
        print("НЕТ ССЫЛКИ: %s" % line)
    if not clones_present:
        print("ВНИМАНИЕ: папки internal/research/ нет — ссылки на клоны не проверялись")

    if unique:
        print("\nИТОГ: 1 — %d ссылок не сходятся с диском" % len(unique))
        return 1
    print("\nИТОГ: 0 — ссылки в заметках сходятся с диском")
    return 0


if __name__ == "__main__":
    sys.exit(main())
