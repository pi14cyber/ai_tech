#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка согласованности чисел и форм.

Зачем: аудит 20.10.2026 нашёл 165 замечаний при зелёных десяти проверках.
Часть из них — расхождение чисел между файлами и таблицы шаблонов с разным
числом колонок в заголовке и строках. Эти два класса ловятся машинно.

Что проверяет:

1. Число шаблонов: на диске, в `templates/README.md` и в `METHODOLOGY.md`.
2. Число навыков: папки со `SKILL.md` против строк реестра `skills/INDEX.md`.
3. Число проверок: `len(CHECKS)` в `verify.py` против фразы «внутри N» в `AGENTS.md`.
4. Таблицы: в каждом шаблоне число `|` в строке-разделителе и в строках данных
   совпадает с заголовком. Расхождение — сломанная таблица.
5. Обязательные блоки шаблона состояния: контур, статусы проверки, цикл HADI,
   сборка артефакта, режим. Без них статусы и таймбокс некуда писать.
6. Обещанные скрипты: упоминание `scripts/<имя>.py` в публичных файлах
   должно вести к существующему файлу.

Чего не проверяет: смысл правил, качество формулировок, лимиты по смыслу
(только их наличие). Смысловые расхождения остаются за «судьёй не автором».

Коды: 0 — сходится; 1 — расхождения; 2 — нечего проверять (нет папки шаблонов).
"""

import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "templates")
SKILLS = os.path.join(ROOT, "skills")
STATE_BLOCKS = ("Режим и контур", "Статусы проверки", "Цикл HADI", "Сборка артефакта", "Шаг пайплайна")


def table_problems(path):
    problems = []
    lines = open(path, encoding="utf-8").read().splitlines()
    block = []
    for number, line in enumerate(lines + [""], 1):
        if line.strip().startswith("|"):
            block.append((number, line.count("|")))
            continue
        if block:
            widths = {count for _n, count in block}
            if len(widths) > 1:
                problems.append("%s:%d — в таблице разное число колонок: %s"
                                % (os.path.relpath(path, ROOT), block[0][0], sorted(widths)))
            block = []
    return problems


def main():
    if not os.path.isdir(TEMPLATES):
        print("ИТОГ: 2 — нет папки шаблонов")
        return 2

    problems = []
    templates = sorted(f for f in os.listdir(TEMPLATES) if f.endswith(".md") and f != "README.md")
    count = len(templates)

    readme = os.path.join(TEMPLATES, "README.md")
    if os.path.exists(readme):
        text = open(readme, encoding="utf-8").read()
        match = re.search(r"Сколько их:\*\*\s*(\d+)\s*шаблон", text)
        if not match:
            problems.append("templates/README.md — нет строки «Сколько их: N шаблонов»")
        elif int(match.group(1)) != count:
            problems.append("templates/README.md — заявлено %s шаблонов, на диске %d"
                            % (match.group(1), count))
        listed = len(re.findall(r"^\|\s*`[^`]+\.md`", text, re.MULTILINE))
        if listed != count:
            problems.append("templates/README.md — в таблице %d шаблонов, на диске %d"
                            % (listed, count))

    methodology = os.path.join(ROOT, "METHODOLOGY.md")
    if os.path.exists(methodology):
        found = re.findall(r"(\d+)\s+шаблон", open(methodology, encoding="utf-8").read())
        if found and int(found[-1]) != count:
            problems.append("METHODOLOGY.md — заявлено %s шаблонов, на диске %d" % (found[-1], count))

    skill_dirs = [d for d in os.listdir(SKILLS)
                  if os.path.isdir(os.path.join(SKILLS, d))
                  and os.path.exists(os.path.join(SKILLS, d, "SKILL.md"))]
    index = os.path.join(SKILLS, "INDEX.md")
    if os.path.exists(index):
        rows = re.findall(r"^\|\s*`([a-z0-9-]+)`", open(index, encoding="utf-8").read(), re.MULTILINE)
        if len(rows) != len(skill_dirs):
            problems.append("skills/INDEX.md — записей %d, папок навыков %d" % (len(rows), len(skill_dirs)))
        missing = sorted(set(skill_dirs) - set(rows))
        if missing:
            problems.append("skills/INDEX.md — нет в реестре: %s" % ", ".join(missing))

    verify = os.path.join(ROOT, "scripts", "verify.py")
    agents = os.path.join(ROOT, "AGENTS.md")
    if os.path.exists(verify) and os.path.exists(agents):
        checks = len(re.findall(r'^\s*\("', open(verify, encoding="utf-8").read(), re.MULTILINE))
        text = open(agents, encoding="utf-8").read()
        claimed = re.search(r"внутри (\w+):", text)
        words = {"девять": 9, "десять": 10, "одиннадцать": 11, "двенадцать": 12,
                 "тринадцать": 13, "четырнадцать": 14}
        claimed_value = None
        if claimed:
            token = claimed.group(1)
            claimed_value = int(token) if token.isdigit() else words.get(token)
        if claimed_value is not None and claimed_value != checks:
            problems.append("AGENTS.md — заявлено %s проверок, в verify.py %d"
                            % (claimed.group(1), checks))

    agents_text = open(agents, encoding="utf-8").read() if os.path.exists(agents) else ""
    if agents_text and "любое из шести" not in agents_text:
        problems.append("AGENTS.md — нет формулировки «любое из шести» в стоп-условиях")
    public_texts = []
    for name in ("AGENTS.md", "START.md", "METHODOLOGY.md", "GLOSSARY.md"):
        path = os.path.join(ROOT, name)
        if os.path.exists(path):
            public_texts.append((name, open(path, encoding="utf-8").read()))
    public_texts += [(os.path.join("skills", d, "SKILL.md"), open(os.path.join(SKILLS, d, "SKILL.md"), encoding="utf-8").read())
                     for d in skill_dirs]
    for name, content in public_texts:
        for wrong in ("любое из четырёх", "любое из пяти", "из четырёх ниже"):
            if wrong in content:
                problems.append("%s — старая версия числа стоп-условий: «%s»" % (name, wrong))

    for template in templates:
        problems.extend(table_problems(os.path.join(TEMPLATES, template)))

    state = os.path.join(TEMPLATES, "state.md")
    if os.path.exists(state):
        content = open(state, encoding="utf-8").read()
        for block in STATE_BLOCKS:
            if block not in content:
                problems.append("templates/state.md — нет блока «%s»" % block)

    public = [os.path.join(ROOT, n) for n in ("AGENTS.md", "START.md", "METHODOLOGY.md",
                                              "GLOSSARY.md", "README.md")]
    public += [os.path.join(SKILLS, d, "SKILL.md") for d in skill_dirs]
    for path in public:
        if not os.path.exists(path):
            continue
        for script in re.findall(r"scripts/([a-z_]+\.py)", open(path, encoding="utf-8").read()):
            if not os.path.exists(os.path.join(ROOT, "scripts", script)):
                problems.append("%s — обещан скрипт scripts/%s, а его нет"
                                % (os.path.relpath(path, ROOT), script))

    # правило «исследование только через внешние сервисы, на 100%»
    agents_path = os.path.join(ROOT, "AGENTS.md")
    rule = "только через внешние сервисы, на 100%"
    if os.path.exists(agents_path) and rule not in open(agents_path, encoding="utf-8").read():
        problems.append("AGENTS.md — нет правила «исследование %s»" % rule)
    skill03 = os.path.join(SKILLS, "03-prevalidation", "SKILL.md")
    if os.path.exists(skill03) and "только внешний сервис" not in open(skill03, encoding="utf-8").read():
        problems.append("skills/03-prevalidation — нет правила «канал — только внешний сервис»")
    for name in ("request-short.md", "request-full.md"):
        path = os.path.join(TEMPLATES, name)
        if os.path.exists(path) and "**Внешний сервис:**" not in open(path, encoding="utf-8").read():
            problems.append("templates/%s — нет поля «Внешний сервис»" % name)

    print("шаблонов: %d, навыков: %d, файлов проверено: %d" % (count, len(skill_dirs), len(public)))
    for line in problems:
        print("РАСХОЖДЕНИЕ: %s" % line)
    if problems:
        print("\nИТОГ: 1 — числа и формы расходятся (%d)" % len(problems))
        return 1
    print("\nИТОГ: 0 — числа и формы сходятся")
    return 0


if __name__ == "__main__":
    sys.exit(main())
