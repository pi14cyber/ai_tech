#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка артефактов в workspace: барьеры существуют только если читают файлы.

Зачем: четыре круга аудита показали, что все барьеры обходятся, потому что
ни одна проверка не читает `workspace/`. Здесь проверяются сами артефакты:
отчёт ворот, отчёт судьи, журнал находок, состояние.

Что проверяет (только если файлы есть):
 1. `workspace/state.md` — есть блок шага, режим, счётчик вопросов, решение судьи,
    версия результата, исход ворот.
 2. Отчёты ворот `workspace/research/prevalidation-*.md` — исход ровно из четырёх,
    не меньше двух строк `Q` с адресом и датой, для «дип» — два файла ответов,
    при исходе «прошло» остальные требования выполнены.
 3. Отчёты судьи `workspace/judge-report-*.md` — заполнено решение (показывать или
    не показывать), заполнена версия результата, есть результат проверок.
 4. `workspace/audit-log.md` — у каждой строки класс A/B/C/D и допустимый статус.
 5. `workspace/artifact.md` — если статус «показан человеку», отчёт судьи с решением
    «показывать» обязан существовать.

Чего не проверяет: качество содержания, правдивость цитат, ход разговора.

Коды: 0 — нарушения нет или проверять нечего; 1 — артефакт нарушает правило;
2 — workspace есть, но не читается.
"""

import glob
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
WS = os.path.join(ROOT, "workspace")
OUTCOMES = ("прошло", "не прошло", "заблокировано", "не запускалось")
JUDGE = ("показывать", "не показывать")
CLASSES = ("A", "B", "C", "D")
FINDING = ("найдено", "предложено", "внедрено", "отклонено", "проверено")


def read(path):
    return open(path, encoding="utf-8", errors="replace").read()


def field(content, key):
    match = re.search(r"%s[^\n:]*:\s*(.+)" % re.escape(key), content)
    if not match:
        return None
    value = match.group(1).strip()
    return value if value else None


def main():
    if not os.path.isdir(WS):
        print("workspace/ нет — проверять нечего (режим пользователя)")
        print("\nИТОГ: 0 — артефактов нет")
        return 0

    problems = []
    checked = 0

    state_path = os.path.join(WS, "state.md")
    if os.path.exists(state_path):
        checked += 1
        content = read(state_path)
        for key in ("Текущий шаг", "Режим", "Задано вопросов", "Контур"):
            if field(content, key) is None and key != "Контур":
                problems.append("state.md — не заполнено поле «%s»" % key)
        gate = field(content, "Исход ворот")
        if gate is not None and not any(o in gate for o in OUTCOMES):
            problems.append("state.md — исход ворот «%s» не из словаря" % gate)

    responses = glob.glob(os.path.join(WS, "responses", "*.md"))
    for report in sorted(glob.glob(os.path.join(WS, "research", "prevalidation-*.md"))):
        checked += 1
        name = os.path.basename(report)
        content = read(report)
        outcome = field(content, "Исход ворот")
        if outcome is None:
            problems.append("%s — не заполнен исход ворот" % name)
        else:
            matched = [o for o in OUTCOMES if o in outcome]
            if not matched:
                problems.append("%s — исход «%s» не из словаря" % (name, outcome))
            elif "не прошло" not in outcome and "заблокировано" not in outcome and "не запускалось" not in outcome \
                    and "прошло" not in outcome:
                problems.append("%s — исход не распознан" % name)
            if "прошло" in outcome and "не прошло" not in outcome and "не запускалось" not in outcome:
                q_lines = re.findall(r"Q\d+\.\d+[^\n]*https?://[^\s)]+[^\n]*\d{2}\.\d{2}\.\d{4}", content)
                if len(q_lines) < 2:
                    problems.append("%s — при исходе «прошло» нужно не меньше двух строк Q с адресом и датой (найдено %d)"
                                    % (name, len(q_lines)))
                if "дип" in content and len(responses) < 2:
                    problems.append("%s — полный запрос, а файлов ответов %d (нужно два)" % (name, len(responses)))
        if "Пакет" not in content:
            problems.append("%s — нет поля «Пакет: N из M»" % name)

    for report in sorted(glob.glob(os.path.join(WS, "judge-report-*.md"))):
        checked += 1
        name = os.path.basename(report)
        content = read(report)
        decision = field(content, "Решение судьи")
        if decision is None or not any(j in decision for j in JUDGE):
            problems.append("%s — нет решения судьи (показывать / не показывать)" % name)
        version = field(content, "Версия результата")
        if version is None:
            problems.append("%s — нет привязки к версии результата" % name)

    audit_path = os.path.join(WS, "audit-log.md")
    if os.path.exists(audit_path):
        checked += 1
        for number, line in enumerate(read(audit_path).splitlines(), 1):
            if not line.strip().startswith("|") or "---" in line:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 6 or cells[0].startswith("#"):
                continue
            if cells[0] in ("", "№") or not any(cells):
                continue
            if cells[3] not in CLASSES:
                problems.append("audit-log.md:%d — класс «%s» не из A/B/C/D" % (number, cells[3]))
            if cells[5] not in FINDING:
                problems.append("audit-log.md:%d — статус «%s» не из словаря" % (number, cells[5]))

    artifact_path = os.path.join(WS, "artifact.md")
    if os.path.exists(artifact_path):
        checked += 1
        content = read(artifact_path)
        if "показан человеку" in content:
            judges = glob.glob(os.path.join(WS, "judge-report-*.md"))
            ok = False
            for judge in judges:
                decision = field(read(judge), "Решение судьи")
                if decision and "показывать" in decision and "не показывать" not in decision:
                    ok = True
            if not ok:
                problems.append("artifact.md — статус «показан человеку», но нет отчёта судьи с решением «показывать»")

    print("файлов проверено: %d" % checked)
    for line in problems:
        print("НАРУШЕНИЕ: %s" % line)
    if problems:
        print("\nИТОГ: 1 — артефакты нарушают правила (%d)" % len(problems))
        return 1
    print("\nИТОГ: 0 — артефакты сходятся с правилами")
    return 0


if __name__ == "__main__":
    sys.exit(main())
