#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка канона: числа, статусы и запрещённые формулировки в публичных файлах.

Зачем: четыре круга аудита показали один и тот же корень — правило живёт в
нескольких файлах и расходится при каждой правке. Канон `rules/canon.json` —
единственный источник чисел и словарей. Этот скрипт не переписывает файлы,
а сверяет их с каноном: расхождение — код 1, то есть тот, кто правил
в одном месте и забыл остальные, узнаёт об этом сразу.

Что проверяет:
 1. Числа: навыки, шаблоны, проверки, стоп-условия — диск против канона.
 2. Запрещённые синонимы: «провалилось», старые числа стоп-условий,
    предзаполненные человеческие решения, ложный 16+ «встреча с датой».
 3. Статусы: словари артефакта, проверки, обязательства, находок, судьи,
    классов доказательств и вердиктов присутствуют в тех файлах, где работают.
 4. Ключевые правила: сеть только через человека, агент в сеть не ходит,
    одно правило BUILD, пакеты с Q1.1, канон стоп-условий.

Чего не проверяет: смысл формулировок, логику маршрута, содержимое workspace.

Коды: 0 — канон сходится; 1 — расхождения; 2 — нет канона или он битый.
"""

import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if "--root" in sys.argv:
    index = sys.argv.index("--root")
    if index + 1 < len(sys.argv):
        ROOT = os.path.abspath(sys.argv[index + 1])
CANON = os.path.join(ROOT, "rules", "canon.json")


def read(rel):
    path = os.path.join(ROOT, *rel.split("/"))
    if not os.path.exists(path):
        return ""
    return open(path, encoding="utf-8").read()


def main():
    if not os.path.exists(CANON):
        print("ИТОГ: 2 — нет канона rules/canon.json")
        return 2
    try:
        canon = json.load(open(CANON, encoding="utf-8"))
    except Exception as error:
        print("ИТОГ: 2 — канон не читается: %s" % error)
        return 2

    problems = []
    counts = canon["counts"]

    skills = [d for d in os.listdir(os.path.join(ROOT, "skills"))
              if os.path.isdir(os.path.join(ROOT, "skills", d))
              and os.path.exists(os.path.join(ROOT, "skills", d, "SKILL.md"))]
    if len(skills) != counts["skills"]:
        problems.append("навыков %d, канон говорит %d" % (len(skills), counts["skills"]))

    templates_dir = os.path.join(ROOT, "templates")
    templates = [f for f in os.listdir(templates_dir) if f.endswith(".md") and f != "README.md"]
    if len(templates) != counts["templates"]:
        problems.append("шаблонов %d, канон говорит %d" % (len(templates), counts["templates"]))

    verify = read("scripts/verify.py")
    checks = len(re.findall(r'^\s*\("', verify, re.MULTILINE))
    if checks != counts["checks"]:
        problems.append("проверок в verify.py %d, канон говорит %d" % (checks, counts["checks"]))

    agents = read("AGENTS.md")
    words = {1: "одно", 2: "два", 3: "трёх", 4: "четырёх", 5: "пяти", 6: "шести",
             7: "семи", 8: "восьми", 9: "девяти", 10: "десяти", 11: "одиннадцати",
             12: "двенадцати", 13: "тринадцати", 14: "четырнадцати"}
    expected = words[counts["stop_conditions"]]
    if ("любое из %s" % expected) not in agents:
        problems.append("AGENTS.md — нет «любое из %s» в стоп-условиях" % expected)

    public = {
        "AGENTS.md": agents,
        "START.md": read("START.md"),
        "METHODOLOGY.md": read("METHODOLOGY.md"),
        "GLOSSARY.md": read("GLOSSARY.md"),
        "README.md": read("README.md"),
    }
    public.update({("skills/%s/SKILL.md" % d): read("skills/%s/SKILL.md" % d) for d in skills})
    public.update({("templates/%s" % f): read("templates/%s" % f) for f in templates})
    public["templates/README.md"] = read("templates/README.md")

    for group, phrases in canon["banned"].items():
        for phrase in phrases:
            pattern = re.compile(r"(?<![а-яёa-z])" + re.escape(phrase) + r"(?![а-яёa-z])", re.IGNORECASE)
            for name, content in public.items():
                if pattern.search(content):
                    problems.append("%s — запрещённая каноном формулировка «%s» (%s)" % (name, phrase, group))

    def require(name, phrase):
        if phrase not in public.get(name, ""):
            problems.append("%s — нет обязательной формулировки «%s»" % (name, phrase))

    rules = canon["canon_rules"]
    require("AGENTS.md", rules["research"])
    require("skills/03-prevalidation/SKILL.md", rules["network_agent"])
    require("skills/05-validation-gate/SKILL.md", rules["gate_single"])
    require("skills/03-prevalidation/SKILL.md", rules["packets"])
    require("skills/00-onboarding-interview/SKILL.md", rules["stop_canon"])

    outcomes = canon["statuses"]["outcomes"]
    for name in ("skills/03-prevalidation/SKILL.md", "skills/04-mvp-artifact/SKILL.md",
                 "templates/prevalidation-report.md", "templates/artifact.md", "templates/state.md"):
        content = public.get(name, "")
        missing = [o for o in outcomes if o not in content]
        if missing:
            problems.append("%s — нет исходов: %s" % (name, ", ".join(missing)))

    for name, key in (("templates/audit-log.md", "finding"), ("skills/09-audit/SKILL.md", "finding"),
                      ("templates/audit-log.md", "evidence_classes"), ("skills/09-audit/SKILL.md", "evidence_classes"),
                      ("templates/judge-report.md", "judge"), ("skills/m3-judge/SKILL.md", "judge"),
                      ("templates/state.md", "artifact"), ("templates/state.md", "check"),
                      ("templates/hadi-tracker.md", "obligation"), ("skills/05-validation-gate/SKILL.md", "verdicts")):
        content = public.get(name, "")
        missing = [s for s in canon["statuses"][key] if s not in content]
        if missing:
            problems.append("%s — нет статусов %s: %s" % (name, key, ", ".join(missing)))

    for value, where in ((canon["limits"]["questions_first_session"], ["AGENTS.md"]),
                         (canon["limits"]["timebox_hours"], ["AGENTS.md", "skills/04-mvp-artifact/SKILL.md"]),
                         (canon["limits"]["message_words"], ["skills/04-mvp-artifact/SKILL.md"]),
                         (canon["limits"]["silence_hours"], ["skills/06-access/SKILL.md", "templates/access-log.md"])):
        for name in where:
            if str(value) not in public.get(name, ""):
                problems.append("%s — нет предела %s" % (name, value))

    for path, fields in canon.get("required", {}).items():
        content = public.get(path)
        if content is None:
            content = read(path)
        for needed in fields:
            if needed not in content:
                problems.append("%s — нет обязательного поля или раздела «%s»" % (path, needed))

    for script in re.findall(r'^\s*\("[^"]+",\s*"([^"]+\.py)"\)', verify, re.MULTILINE):
        if not os.path.exists(os.path.join(ROOT, "scripts", script)):
            problems.append("verify.py обещает проверку scripts/%s, а её нет" % script)

    print("канон: версия %s; навыков %d, шаблонов %d, проверок %d, стоп-условий %d"
          % (canon.get("version"), len(skills), len(templates), checks, counts["stop_conditions"]))
    for line in problems:
        print("РАСХОЖДЕНИЕ: %s" % line)
    if problems:
        print("\nИТОГ: 1 — файлы разошлись с каноном (%d)" % len(problems))
        return 1
    print("\nИТОГ: 0 — файлы сходятся с каноном")
    return 0


if __name__ == "__main__":
    sys.exit(main())
