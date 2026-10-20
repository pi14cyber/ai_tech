#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка базы знаний.

Зачем: база легко превращается в свалку. Без машинной сверки агент не знает,
какие карточки протухли и что не зарегистрировано в индексе.

Проверяет четыре вещи:

1. Паспорт карточки: обязательные поля во фронтматтере.
2. Срок годности: если `date_verified` плюс `freshness_ttl` истёк — карточка
   считается протухшей и требует нового запроса исследователю.
3. Сверка с индексом в обе стороны: карточка без строки в индексе и строка
   индекса без карточки — обе ошибки.
4. Объём: карточка длиннее 250 строк считается неатомарной.

Коды возврата: 0 — всё сходится; 1 — расхождения; 2 — сломан паспорт.

Приём сверки декларации и исполнителя и контракт кодов взят из
netresearch/agent-harness-skill, verify-harness.sh:336-362, :788-794.
"""

import datetime
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
KB = os.path.join(KIT, "knowledge")
INDEX = os.path.join(KB, "INDEX.md")
REQUIRED = ("id", "type", "evidence_level", "source_url", "date_verified",
            "used_in_skills", "freshness_ttl")
ZONES = ("01_canon", "02_external", "03_practices", "04_artifacts")
PATH_RE = re.compile(r"(%s)/[\w\-.]+\.md" % "|".join(ZONES))
MAX_LINES = 250


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    block = text[3:end]
    data = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def ttl_months(value):
    value = (value or "").strip().lower()
    if value in ("forever", "вечно", ""):
        return None
    m = re.match(r"^(\d+)\s*m$", value)
    if m:
        return int(m.group(1))
    m = re.match(r"^(\d+)\s*d$", value)
    if m:
        return max(1, int(m.group(1)) // 30)
    return "unknown"


def main():
    broken = []
    problems = []

    if not os.path.isdir(KB):
        broken.append("нет папки базы знаний: %s" % KB)
        print("\nИТОГ: 2 — база знаний не найдена")
        return 2

    cards = []
    for zone in ZONES:
        zone_dir = os.path.join(KB, zone)
        if not os.path.isdir(zone_dir):
            problems.append("нет зоны %s" % zone)
            continue
        for name in sorted(os.listdir(zone_dir)):
            if name.endswith(".md") and name != "README.md":
                cards.append("%s/%s" % (zone, name))

    today = datetime.date.today()
    for rel in cards:
        path = os.path.join(KB, *rel.split("/"))
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        lines = text.count("\n") + 1
        meta = parse_frontmatter(text)
        if meta is None:
            broken.append("%s: нет фронтматтера" % rel)
            continue
        missing = [k for k in REQUIRED if k not in meta]
        if missing:
            broken.append("%s: в паспорте нет полей %s" % (rel, ", ".join(missing)))
            continue
        ttl = ttl_months(meta.get("freshness_ttl"))
        if ttl == "unknown":
            broken.append("%s: непонятный freshness_ttl «%s»" % (rel, meta.get("freshness_ttl")))
            continue
        if ttl is not None:
            try:
                verified = datetime.date.fromisoformat(meta["date_verified"])
            except ValueError:
                broken.append("%s: дата проверки не в формате ГГГГ-ММ-ДД" % rel)
                continue
            months = (today.year - verified.year) * 12 + (today.month - verified.month)
            if months > ttl:
                problems.append(
                    "%s: карточка протухла (%d мес. при сроке %d), нужен новый запрос исследователю"
                    % (rel, months, ttl)
                )
        if lines > MAX_LINES:
            problems.append("%s: %d строк, карточка неатомарна (лимит %d)" % (rel, lines, MAX_LINES))
        print("%s: строк %d, уровень %s, годность %s" % (rel, lines, meta.get("evidence_level"), meta.get("freshness_ttl")))

    if os.path.exists(INDEX):
        with open(INDEX, "r", encoding="utf-8", errors="replace") as f:
            index_text = f.read()
        router = index_text.split("## План пополнения")[0]
        listed = set(PATH_RE.findall(router))
        declared = set()
        for m in re.finditer(r"(%s)/[\w\-.]+\.md" % "|".join(ZONES), router):
            declared.add(m.group(0))
        actual = set(cards)
        for rel in sorted(actual - declared):
            problems.append("%s: карточки нет в индексе" % rel)
        for rel in sorted(declared - actual):
            problems.append("%s: строка индекса без карточки" % rel)
        print("\nв индексе объявлено карточек: %d, найдено файлов: %d" % (len(declared), len(actual)))
    else:
        broken.append("нет файла индекса: %s" % INDEX)

    print("")
    for line in broken:
        print("ПАСПОРТ: %s" % line)
    for line in problems:
        print("РАСХОЖДЕНИЕ: %s" % line)

    if broken:
        print("\nИТОГ: 2 — сломан паспорт, база не принимается")
        return 2
    if problems:
        print("\nИТОГ: 1 — расхождения, нужно чинить")
        return 1
    print("\nИТОГ: 0 — база сходится")
    return 0


if __name__ == "__main__":
    sys.exit(main())
