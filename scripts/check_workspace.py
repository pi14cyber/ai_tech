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
WS = os.path.join(ROOT, "workspace")
OUTCOMES = ("прошло", "не прошло", "заблокировано", "не запускалось")
JUDGE = ("показывать", "не показывать")
CLASSES = ("A", "B", "C", "D")
FINDING = ("найдено", "предложено", "внедрено", "отклонено", "проверено")
STEP_VOCAB = ("онбординг", "замер", "выбор поля", "гипотеза", "предвалидация",
              "артефакт", "доступ", "разговор", "решение")
MODE_VOCAB = ("обычный", "только локально")
CONTOUR_VOCAB = ("внешний", "внутренний")
READY_VOCAB = ("да", "нет")
LIMITS = {"first": 5, "later": 3}


def load_limits():
    path = os.path.join(ROOT, "rules", "canon.json")
    if not os.path.exists(path):
        return LIMITS
    try:
        canon = json.load(open(path, encoding="utf-8"))
        limits = canon.get("limits", {})
        return {"first": limits.get("questions_first_session", 5),
                "later": limits.get("questions_later", 3)}
    except Exception:
        return LIMITS


def read(path):
    return open(path, encoding="utf-8", errors="replace").read()


def field(content, key):
    match = re.search(r"%s[^\n:]*:\s*(.+)" % re.escape(key), content)
    if not match:
        return None
    value = match.group(1).strip().strip("*` ")
    if not value:
        return None
    lowered = value.lower()
    if value.startswith("(") or "____" in value or "вписать" in lowered or "заполняет" in lowered:
        return None
    return value


def main():
    if "--root" in sys.argv:
        index = sys.argv.index("--root")
        if index + 1 >= len(sys.argv):
            print("ИТОГ: 2 — параметр --root без значения: проверять нечего")
            return 2
        if not os.path.isdir(WS):
            print("ИТОГ: 2 — корень %s не найден: проверять нечего" % ROOT)
            return 2
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
        for key in ("Текущий шаг", "Режим", "Задано вопросов", "Номер сессии"):
            if field(content, key) is None:
                problems.append("state.md — не заполнено поле «%s» (подсказка не считается ответом)" % key)
        step = field(content, "Текущий шаг") or ""
        if not any(v in step.lower() for v in STEP_VOCAB):
            problems.append("state.md — текущий шаг «%s» не из словаря" % step)
        marker = os.path.exists(os.path.join(WS, "LOCAL-ONLY"))
        mode = (field(content, "Режим") or "").lower()
        if marker and "локально" not in mode:
            problems.append("state.md — файл LOCAL-ONLY есть, а режим «%s»: расхождение" % mode)
        if not marker and "локально" in mode:
            problems.append("state.md — режим «только локально», а файла LOCAL-ONLY нет")
        if mode and not any(m in mode for m in MODE_VOCAB):
            problems.append("state.md — режим «%s» не из словаря" % mode)
        contour = field(content, "Контур")
        if contour and not any(c in contour.lower() for c in CONTOUR_VOCAB):
            problems.append("state.md — контур «%s» не из словаря" % contour)
        session = field(content, "Номер сессии")
        counter = field(content, "Задано вопросов")
        limits = load_limits()
        if session is not None and not session.strip().isdigit():
            problems.append("state.md — номер сессии «%s» не число" % session)
        if counter is not None and not counter.strip().isdigit():
            problems.append("state.md — счётчик вопросов «%s» не число" % counter)
        if session is not None and session.strip().isdigit() and counter is not None and counter.strip().isdigit():
            allowed = limits["first"] if int(session.strip()) <= 1 else limits["later"]
            if int(counter.strip()) > allowed:
                problems.append("state.md — задано вопросов %s при пределе %d" % (counter.strip(), allowed))
        gate = field(content, "Исход ворот")
        if gate is not None:
            head = gate.strip().split()[0].strip(".,:;—-").lower()
            if head not in OUTCOMES:
                problems.append("state.md — исход ворот «%s» не из словаря" % gate)
        ready = field(content, "Готов к показу")
        if ready is not None:
            head = ready.strip().split()[0].strip(".,:;—-").lower()
            if head not in READY_VOCAB:
                problems.append("state.md — «готов к показу» = «%s» не из да/нет" % ready)
            if head == "да":
                decision = field(content, "Решение судьи")
                normalized = (decision or "").lower()
                if "не показывать" in normalized:
                    problems.append("state.md — «готов к показу», но судья сказал «не показывать»")
                elif not normalized.strip(" .").startswith("показывать"):
                    problems.append("state.md — «готов к показу», но строгого решения судьи «показывать» нет")

    profile_path = os.path.join(WS, "profile.md")
    if os.path.exists(profile_path):
        checked += 1
        content = read(profile_path)
        consent = field(content, "Уровень готовности делиться")
        if consent is None:
            problems.append("profile.md — не заполнен уровень готовности делиться данными (вопрос шага 0)")
        elif not any(v in consent.lower() for v in ("файлы", "метаданные", "ответы", "локально")):
            problems.append("profile.md — уровень готовности «%s» не из четырёх вариантов" % consent)

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
                if not responses:
                    problems.append("%s — исход «прошло», но ни одного файла ответа нет: ворота не пройдены" % name)
                if "дип" in content and len(responses) < 2:
                    problems.append("%s — полный запрос, а файлов ответов %d (нужно два)" % (name, len(responses)))
        if "Пакет" not in content:
            problems.append("%s — нет поля «Пакет: N из M»" % name)

    for report in sorted(glob.glob(os.path.join(WS, "judge-report-*.md"))):
        checked += 1
        name = os.path.basename(report)
        content = read(report)
        decision_raw = field(content, "Решение судьи")
        normalized = (decision_raw or "").lower().strip(" .")
        if "не показывать" in normalized:
            pass
        elif not normalized.startswith("показывать"):
            problems.append("%s — нет строгого решения судьи «показывать» или «не показывать»" % name)
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
            if cells[5] == "проверено":
                who = cells[7].strip() if len(cells) > 7 else ""
                if not who:
                    problems.append("audit-log.md:%d — статус «проверено» без того, кто проверил" % number)

    decisions_path = os.path.join(WS, "memory", "decisions.md")
    if os.path.exists(decisions_path):
        checked += 1
        for number, line in enumerate(read(decisions_path).splitlines(), 1):
            if not line.strip().startswith("|") or "---" in line:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 8 or cells[0] in ("", "Дата"):
                continue
            who = cells[6]
            quote = cells[3]
            if who and not quote:
                problems.append("decisions.md:%d — решение записано, а дословной цитаты решения нет" % number)

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


def self_test():
    """Самопроверка: на корректном артефакте код 0, на испорченном — 1."""
    import shutil
    import subprocess

    base = os.path.join(ROOT, "scripts", "_selftest_ws")
    ok_root = os.path.join(base, "ok")
    bad_root = os.path.join(base, "bad")
    for root in (ok_root, bad_root):
        os.makedirs(os.path.join(root, "workspace", "research"))
        os.makedirs(os.path.join(root, "workspace", "responses"))
        open(os.path.join(root, "workspace", "responses", "req_01.answer.md"), "w",
             encoding="utf-8").write("# Ответ\n\nQ1.1: факт\n")
    state = (
        "# Состояние\n\n"
        "- **Текущий шаг:** артефакт\n- **Что дальше (один шаг):** ворота\n"
        "- **Режим:** обычный\n- **Задано вопросов в сессии:** 4\n"
        "- **Номер сессии:** 1\n"
        "- **Контур:** внешний\n- **Исход ворот:** прошло\n"
    )
    report = (
        "# Отчёт предвалидации\n\n- **Исход ворот — вписать одно значение:** прошло\n"
        "- **Пакет:** 1 из 1\n\n"
        "| Q | Вопрос | Ссылок |\n|---|---|---|\n"
        "| Q1.1 | вопрос | https://a.example/1 01.10.2026 |\n"
        "| Q1.2 | вопрос | https://b.example/2 02.10.2026 |\n"
    )
    for root in (ok_root, bad_root):
        open(os.path.join(root, "workspace", "state.md"), "w", encoding="utf-8").write(state)
        open(os.path.join(root, "workspace", "research", "prevalidation-2026-10-20.md"),
             "w", encoding="utf-8").write(report)
    bad_report = os.path.join(bad_root, "workspace", "research", "prevalidation-2026-10-20.md")
    content = open(bad_report, encoding="utf-8").read().replace(":** прошло", ":** ____", 1)
    open(bad_report, "w", encoding="utf-8").write(content)

    ok_code = subprocess.run([sys.executable, __file__, "--root", ok_root],
                             capture_output=True).returncode
    bad_code = subprocess.run([sys.executable, __file__, "--root", bad_root],
                              capture_output=True).returncode
    print("корректный артефакт: код %d (ожидался 0)" % ok_code)
    print("испорченный артефакт: код %d (ожидался 1)" % bad_code)
    shutil.rmtree(base, ignore_errors=True)
    if ok_code == 0 and bad_code == 1:
        print("\nИТОГ: 0 — самопроверка пройдена")
        return 0
    print("\nИТОГ: 2 — самопроверка не пройдена")
    return 2


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
