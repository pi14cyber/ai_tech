#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка канона: числа, статусы, запрещённые формулировки и целостность проверок.

Зачем: четыре круга аудита показали один и тот же корень — правило живёт в
нескольких файлах и расходится при каждой правке. Канон `rules/canon.json` —
единственный источник чисел и словарей. Этот скрипт не переписывает файлы,
а сверяет их с каноном: расхождение — код 1, то есть тот, кто правил
в одном месте и забыл остальные, узнаёт об этом сразу.

Что проверяет:
 1. **Целостность канона.** Обязательные ключи: версия, счётчики, все ключи
    статусов, все десять правил `canon_rules`, все шесть групп запретов
    (непустые), все пять порогов внешней проверки, обязательные пределы и
    каждый ключ `limits`/`limits_where`/`limits_patterns` на своём месте.
    Канон, из которого ключ вычищен, — код 2 «канон очищен», а не 0.
 2. **Манифест хешей `kit/rules/check_hashes.json`.** Для каждого файла проверки из
    `canon.checks_expected` и для `kit/scripts/verify.py` записана sha256 его тела.
    Расхождение — код 1 «тело проверки изменено без обновления манифеста»;
    нет манифеста или в нём нет ключа — код 2. Обновление манифеста (после
    осознанной правки проверки): `python kit/scripts/verify_canon.py --write-hashes`,
    затем `python kit/scripts/sync_sandbox.py` — песочница должна совпасть.
    Все пути в каноне и манифесте записаны от корня репозитория, с префиксом `kit/`.
 3. Числа: навыки, шаблоны, проверки, стоп-условия — диск против канона.
    Контекстные значения пределов (`limits_values`) сверяются во всех вхождениях,
    а не только фактом присутствия: «три часа» внутри правила при каноне «четыре» —
    расхождение (p2 круга 9), а не «слово рядом есть».
 4. Запрещённые синонимы: «провалилось», старые числа стоп-условий,
    предзаполненные человеческие решения, ложный 16+ «встреча с датой».
 5. Статусы: словари артефакта, проверки, обязательств, находок, судьи,
    классов доказательств и вердиктов присутствуют в тех файлах, где работают.
 6. Ключевые правила: сеть только через человека, агент в сеть не ходит,
    одно правило BUILD, пакеты с Q1.1, канон стоп-условий, контур, подпись,
    версия результата, внешняя проверка, источники без кода.

Чего не проверяет: смысл формулировок, логику маршрута, содержимое workspace,
совпадение текста правил с живой практикой (сеть запрещена). Манифест хешей
ловит подмену тела проверки только до тех пор, пока его не переписали тем же
флагом `--write-hashes`: он фиксирует факт правки, а не право её делать.

Коды: 0 — канон сходится; 1 — расхождения; 2 — нет канона, он битый, канон
очищен или манифест хешей неполон.
"""

import hashlib
import json
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
CANON = os.path.join(KIT, "rules", "canon.json")
HASHES = os.path.join(KIT, "rules", "check_hashes.json")

# Обязательные ключи канона: удаление любого — код 2, а не «проверять нечего».
REQUIRED_COUNTS = ("skills", "templates", "checks", "stop_conditions")
REQUIRED_RULES = ("research", "network_agent", "gate_single", "packets", "stop_canon",
                  "escalation", "sources", "contour", "signature", "version")
REQUIRED_STATUSES = ("outcomes", "artifact", "check", "obligation", "finding", "judge",
                     "evidence_classes", "verdicts", "assumption", "contour")
REQUIRED_BANNED = ("outcome_synonyms", "old_stop_counts", "false_stop_words",
                   "prefilled_human", "false_sixteen", "exception_rules")
REQUIRED_ESCALATION = ("attempts_without_progress", "repeated_blocker_rounds",
                       "regressions_limit", "unknowns_without_source", "unresolved_hours")
REQUIRED_LIMITS = ("questions_first_session", "questions_later", "questions_per_packet",
                   "short_request_min", "short_request_max", "full_request_max",
                   "answer_words_short", "answer_words_full", "timebox_hours", "reworks",
                   "message_words", "touches_per_week", "silence_hours",
                   "contacts_per_sprint", "measure_days", "cycle_weeks", "question_length",
                   "list_people_min", "list_people_max")
# Токен числа в шаблонах limits_values: цифры и числительные в падежах, которые
# встречаются в текстах. Место подстановки в шаблоне канона — NUM.
NUMBER_TOKEN = (r"\d+|один|одного|два|двух|три|трёх|трех|четыре|четырёх|четырех|"
                r"пять|пяти|шесть|шести|семь|семи|восемь|восьми|девять|девяти|"
                r"десять|десяти|одиннадцать|одиннадцати|двенадцать|двенадцати|"
                r"тринадцать|тринадцати|четырнадцать|четырнадцати|пятнадцать|пятнадцати")
NUMBER_WORDS = {"один": 1, "одного": 1, "два": 2, "двух": 2, "три": 3, "трёх": 3,
                "трех": 3, "четыре": 4, "четырёх": 4, "четырех": 4, "пять": 5,
                "пяти": 5, "шесть": 6, "шести": 6, "семь": 7, "семи": 7, "восемь": 8,
                "восьми": 8, "девять": 9, "девяти": 9, "десять": 10, "десяти": 10,
                "одиннадцать": 11, "одиннадцати": 11, "двенадцать": 12,
                "двенадцати": 12, "тринадцать": 13, "тринадцати": 13,
                "четырнадцать": 14, "четырнадцати": 14, "пятнадцать": 15,
                "пятнадцати": 15}


def read(rel):
    """Читает файл по пути от корня репозитория: `kit/AGENTS.md`, `README.md`."""
    path = os.path.join(ROOT, *rel.split("/"))
    if not os.path.exists(path):
        return ""
    return open(path, encoding="utf-8").read()


WORDS = {1: "одно", 2: "два", 3: "три", 4: "четыре", 5: "пять", 6: "шесть",
         7: "семь", 8: "восемь", 9: "девять", 10: "десять", 11: "одиннадцать",
         12: "двенадцать", 13: "тринадцать", 14: "четырнадцать"}


def numbers_ok(content, value):
    """Число ищется как значение: цифрой или словом, но не подстрокой («4» не «14»)."""
    text = str(value)
    if text.isdigit():
        number = int(text)
        if re.search(r"(?<!\d)" + text + r"(?!\d)", content):
            return True
        word = WORDS.get(number)
        return bool(word and word in content)
    return text in content


def number_value(token):
    """Число из цифры или числительного; None, если токен не распознан."""
    token = (token or "").strip().lower()
    if token.isdigit():
        return int(token)
    return NUMBER_WORDS.get(token)


def declaration_errors(canon):
    """Обязательные ключи канона. Пустой список — канон цел, иначе код 2."""
    errors = []

    def need_block(container, name):
        if not isinstance(container, dict):
            errors.append("блока «%s»" % name)
            return None
        return container

    version = canon.get("version")
    if not isinstance(version, str) or not version.strip():
        errors.append("version")
    elif not re.match(r"^\d+\.\d+$", version.strip()):
        errors.append("version (не вида N.N)")

    counts = need_block(canon.get("counts"), "counts")
    if counts is not None:
        for key in REQUIRED_COUNTS:
            value = counts.get(key)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                errors.append("counts.%s" % key)

    rules = need_block(canon.get("canon_rules"), "canon_rules")
    if rules is not None:
        for key in REQUIRED_RULES:
            value = rules.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append("canon_rules.%s" % key)

    statuses = need_block(canon.get("statuses"), "statuses")
    if statuses is not None:
        for key in REQUIRED_STATUSES:
            value = statuses.get(key)
            if not isinstance(value, list) or not [v for v in value if str(v).strip()]:
                errors.append("statuses.%s" % key)

    banned = need_block(canon.get("banned"), "banned")
    if banned is not None:
        for key in REQUIRED_BANNED:
            value = banned.get(key)
            if not isinstance(value, list) or not [v for v in value if str(v).strip()]:
                errors.append("banned.%s" % key)

    escalation = need_block(canon.get("escalation"), "escalation")
    if escalation is not None:
        for key in REQUIRED_ESCALATION:
            value = escalation.get(key)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                errors.append("escalation.%s" % key)

    limits = need_block(canon.get("limits"), "limits")
    limits_where = need_block(canon.get("limits_where"), "limits_where")
    limits_required = canon.get("limits_required")
    patterns = canon.get("limits_patterns")
    if not isinstance(limits_required, list) or not [v for v in limits_required if str(v).strip()]:
        errors.append("limits_required (пустой список: ни один предел не обязателен)")
        limits_required = []
    if patterns is not None and not isinstance(patterns, dict):
        errors.append("limits_patterns (не словарь)")
        patterns = {}
    for key in REQUIRED_LIMITS:
        if limits is not None and key not in limits:
            errors.append("limits.%s" % key)
        if limits_where is not None and key not in limits_where:
            errors.append("limits_where.%s" % key)
        if key not in limits_required:
            errors.append("limits_required.%s" % key)
    if limits is not None and limits_where is not None:
        for key in limits:
            if key not in limits_where:
                errors.append("limits_where.%s" % key)
        for key in limits_where:
            if key not in limits:
                errors.append("limits.%s" % key)
    if limits_where is not None:
        for key, where in limits_where.items():
            if not isinstance(where, list) or not [w for w in where if str(w).strip()]:
                errors.append("limits_where.%s (пустой список файлов)" % key)
    if patterns:
        for key, pattern in patterns.items():
            if limits is not None and key not in limits:
                errors.append("limits_patterns.%s (предела нет в limits)" % key)
                continue
            if not isinstance(pattern, str) or not pattern.strip():
                errors.append("limits_patterns.%s (пустой шаблон)" % key)
                continue
            try:
                re.compile(pattern)
            except re.error:
                errors.append("limits_patterns.%s (шаблон не компилируется)" % key)

    values = canon.get("limits_values")
    if not isinstance(values, dict) or not values:
        errors.append("limits_values (нет контекстных шаблонов значений пределов)")
    else:
        for key, pattern in values.items():
            if limits is not None and key not in limits:
                errors.append("limits_values.%s (предела нет в limits)" % key)
                continue
            if not isinstance(pattern, str) or not pattern.strip():
                errors.append("limits_values.%s (пустой шаблон)" % key)
                continue
            try:
                compiled = re.compile(pattern.replace("NUM", NUMBER_TOKEN), re.IGNORECASE)
            except re.error:
                errors.append("limits_values.%s (шаблон не компилируется)" % key)
                continue
            if "num" not in compiled.groupindex:
                errors.append("limits_values.%s (нет группы num для значения)" % key)

    checks_expected = canon.get("checks_expected")
    if not isinstance(checks_expected, list) or not checks_expected:
        errors.append("checks_expected (пустой список проверок)")
    elif counts is not None and counts.get("checks") != len(checks_expected):
        errors.append("checks_expected (длина не равна counts.checks)")
    else:
        for entry in checks_expected:
            if not isinstance(entry, (list, tuple)) or len(entry) < 2 \
                    or not str(entry[1]).strip().endswith(".py"):
                errors.append("checks_expected (запись без имени скрипта .py)")

    return errors


def hash_targets(canon):
    """Файлы, чьё тело обязано быть зафиксировано: проверки из канона + вход.

    Пути — от корня репозитория (`kit/scripts/...`), как и весь канон.
    """
    targets = ["kit/scripts/verify.py"]
    for entry in canon.get("checks_expected") or []:
        if isinstance(entry, (list, tuple)) and len(entry) >= 2:
            target = str(entry[1]).strip()
            if target not in targets:
                targets.append(target)
    return targets


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_hashes(canon):
    """Записать манифест хешей: фиксирует текущее тело проверок."""
    targets = hash_targets(canon)
    if len(targets) < 2:
        print("ИТОГ: 2 — канон очищен: нет обязательного ключа «checks_expected»")
        return 2
    missing = [t for t in targets if not os.path.isfile(os.path.join(ROOT, *t.split("/")))]
    if missing:
        print("ИТОГ: 2 — нечего хешировать: нет файла %s" % missing[0])
        return 2
    data = {
        "about": "sha256 тела каждой машинной проверки. Меняешь проверку — осознанно "
                 "запусти python kit/scripts/verify_canon.py --write-hashes и синхронизируй песочницу.",
        "algorithm": "sha256",
        "files": {target: sha256_of(os.path.join(ROOT, *target.split("/"))) for target in targets},
    }
    with open(HASHES, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print("манифест хешей записан: kit/rules/check_hashes.json, файлов %d" % len(targets))
    print("ИТОГ: 0 — тело проверок зафиксировано; теперь python kit/scripts/sync_sandbox.py")
    return 0


def manifest_errors(canon):
    """Проверка манифеста. Возвращает (ошибки декларации — код 2, расхождения — код 1)."""
    declared, problems = [], []
    if not os.path.exists(HASHES):
        declared.append("нет манифеста kit/rules/check_hashes.json — тело проверок не "
                        "зафиксировано (создай: python kit/scripts/verify_canon.py --write-hashes)")
        return declared, problems
    try:
        data = json.load(open(HASHES, encoding="utf-8"))
    except Exception as error:
        declared.append("манифест kit/rules/check_hashes.json не читается: %s" % error)
        return declared, problems
    if data.get("algorithm") not in (None, "sha256"):
        declared.append("манифест kit/rules/check_hashes.json: алгоритм «%s» вместо sha256"
                        % data.get("algorithm"))
        return declared, problems
    files = data.get("files")
    if not isinstance(files, dict) or not files:
        declared.append("манифест kit/rules/check_hashes.json пуст: нет карты «files»")
        return declared, problems
    targets = hash_targets(canon)
    for target in targets:
        if target not in files:
            declared.append("в манифесте нет ключа «%s»: проверка не зафиксирована" % target)
    for key in files:
        if key not in targets:
            declared.append("в манифесте лишний ключ «%s»: такой проверки нет в verify.py" % key)
    if declared:
        return declared, problems
    for target in targets:
        path = os.path.join(ROOT, *target.split("/"))
        if not os.path.isfile(path):
            continue  # отсутствие файла ловится отдельно и другим кодом
        actual = sha256_of(path)
        if actual != str(files[target]).strip().lower():
            problems.append("тело проверки изменено без обновления манифеста: %s "
                            "(обнови: python kit/scripts/verify_canon.py --write-hashes, затем sync_sandbox.py)"
                            % target)
    return declared, problems


def main():
    global ROOT, KIT, CANON, HASHES
    argv = sys.argv[1:]
    write_mode = False
    if __name__ == "__main__" and "--root" in argv:
        index = argv.index("--root")
        if index + 1 >= len(argv):
            print("ИТОГ: 2 — параметр --root без значения")
            return 2
        ROOT = os.path.abspath(argv[index + 1])
        KIT = os.path.join(ROOT, "kit")
        CANON = os.path.join(KIT, "rules", "canon.json")
        HASHES = os.path.join(KIT, "rules", "check_hashes.json")
    if __name__ == "__main__" and "--write-hashes" in argv:
        write_mode = True
    if not os.path.exists(CANON):
        print("ИТОГ: 2 — нет канона kit/rules/canon.json")
        return 2
    try:
        canon = json.load(open(CANON, encoding="utf-8"))
    except Exception as error:
        print("ИТОГ: 2 — канон не читается: %s" % error)
        return 2
    if not isinstance(canon, dict):
        print("ИТОГ: 2 — канон не словарь: проверять нечего")
        return 2

    declared = declaration_errors(canon)
    if write_mode:
        if declared:
            print("ИТОГ: 2 — канон очищен: нет обязательного ключа «%s» (манифест не записан)"
                  % declared[0])
            return 2
        return write_hashes(canon)
    if declared:
        for key in declared:
            print("КАНОН ОЧИЩЕН: нет обязательного ключа «%s»" % key)
        print("\nИТОГ: 2 — канон очищен: нет обязательного ключа «%s» (%d)"
              % (declared[0], len(declared)))
        return 2

    problems = []
    counts = canon["counts"]

    skills = [d for d in os.listdir(os.path.join(KIT, "skills"))
              if os.path.isdir(os.path.join(KIT, "skills", d))
              and os.path.exists(os.path.join(KIT, "skills", d, "SKILL.md"))]
    if len(skills) != counts["skills"]:
        problems.append("навыков %d, канон говорит %d" % (len(skills), counts["skills"]))

    templates_dir = os.path.join(KIT, "templates")
    templates = [f for f in os.listdir(templates_dir) if f.endswith(".md") and f != "README.md"]
    if len(templates) != counts["templates"]:
        problems.append("шаблонов %d, канон говорит %d" % (len(templates), counts["templates"]))

    verify = read("kit/scripts/verify.py")
    found = re.findall(r'^\s*\("([^"]+)",\s*"([^"]+\.py)"\)', verify, re.MULTILINE)
    checks = len(found)
    expected = [tuple(pair) for pair in canon["checks_expected"]]
    if checks != counts["checks"]:
        problems.append("проверок в verify.py %d, канон говорит %d" % (checks, counts["checks"]))
    if expected and found != expected:
        problems.append("список проверок в verify.py не совпадает с каноном: %d против %d"
                        % (len(found), len(expected)))

    hash_declared, hash_problems = manifest_errors(canon)
    if hash_declared:
        for line in hash_declared:
            print("МАНИФЕСТ: %s" % line)
        print("\nИТОГ: 2 — манифест хешей неполон: %s" % hash_declared[0])
        return 2
    problems.extend(hash_problems)

    bodies = {}
    for name, script in found:
        path = os.path.join(ROOT, *script.split("/"))
        if not os.path.exists(path):
            problems.append("verify.py обещает проверку %s, а её нет" % script)
            continue
        body = open(path, encoding="utf-8", errors="replace").read()
        markers = sum(1 for marker in ("sys.exit(", "def main", "open(", "read(", "problems.append")
                      if marker in body)
        if len(body) < 1500 or "ИТОГ:" not in body or markers < 3:
            problems.append("%s — похоже на заглушку вместо проверки (короткое тело без логики и вердикта «ИТОГ:»)" % script)
        key = hash(body)
        if key in bodies and bodies[key] != script:
            problems.append("%s и %s — одинаковое тело: одна проверка выдаёт себя за другую"
                            % (bodies[key], script))
        bodies[key] = script

    agents = read("kit/AGENTS.md")
    words = {1: "одно", 2: "два", 3: "трёх", 4: "четырёх", 5: "пяти", 6: "шести",
             7: "семи", 8: "восьми", 9: "девяти", 10: "десяти", 11: "одиннадцати",
             12: "двенадцати", 13: "тринадцати", 14: "четырнадцати"}
    expected = words[counts["stop_conditions"]]
    if ("любое из %s" % expected) not in agents:
        problems.append("AGENTS.md — нет «любое из %s» в стоп-условиях" % expected)

    changelog = read("kit/CHANGELOG.md")
    version = canon["version"].strip()
    if not re.search(r"(?<![\d.])" + re.escape(version) + r"(?![\d.])", changelog):
        problems.append("Канон — версия «%s» не названа ни в одном выпуске kit/CHANGELOG.md: "
                        "версию канона не с чем сверить" % version)

    public = {
        "kit/AGENTS.md": agents,
        "kit/START.md": read("kit/START.md"),
        "kit/METHODOLOGY.md": read("kit/METHODOLOGY.md"),
        "kit/GLOSSARY.md": read("kit/GLOSSARY.md"),
        "README.md": read("README.md"),
    }
    public.update({("kit/skills/%s/SKILL.md" % d): read("kit/skills/%s/SKILL.md" % d) for d in skills})
    public.update({("kit/templates/%s" % f): read("kit/templates/%s" % f) for f in templates})
    public["kit/templates/README.md"] = read("kit/templates/README.md")
    public["kit/skills/INDEX.md"] = read("kit/skills/INDEX.md")
    for dirpath, _dirnames, filenames in os.walk(os.path.join(KIT, "knowledge")):
        for filename in filenames:
            if filename.endswith(".md"):
                rel = os.path.relpath(os.path.join(dirpath, filename), ROOT).replace("\\", "/")
                public[rel] = read(rel)

    for group, phrases in canon["banned"].items():
        if not phrases:
            problems.append("Канон — пустая группа запретов «%s»: проверять нечего" % group)
        for phrase in phrases:
            pattern = re.compile(r"(?<![а-яёa-z])" + re.escape(phrase) + r"(?![а-яёa-z])", re.IGNORECASE)
            for name, content in public.items():
                if pattern.search(content):
                    problems.append("%s — запрещённая каноном формулировка «%s» (%s)" % (name, phrase, group))

    def require(name, phrase):
        if not re.search(phrase, public.get(name, ""), re.IGNORECASE):
            problems.append("%s — нет обязательной формулировки «%s»" % (name, phrase))

    rules = canon["canon_rules"]
    require("kit/AGENTS.md", rules["research"])
    require("kit/skills/03-prevalidation/SKILL.md", rules["network_agent"])
    require("kit/skills/05-validation-gate/SKILL.md", rules["gate_single"])
    require("kit/skills/03-prevalidation/SKILL.md", rules["packets"])
    require("kit/skills/00-onboarding-interview/SKILL.md", rules["stop_canon"])
    require("kit/AGENTS.md", rules["escalation"])
    require("kit/AGENTS.md", rules["sources"])
    require("kit/AGENTS.md", rules["contour"])
    require("kit/AGENTS.md", rules["signature"])
    require("kit/AGENTS.md", rules["version"])
    require("kit/GLOSSARY.md", "канон — `kit/AGENTS.md`")
    require("kit/templates/state.md", "Версия результата")

    outcomes = canon["statuses"]["outcomes"]
    for name in ("kit/skills/03-prevalidation/SKILL.md", "kit/skills/04-mvp-artifact/SKILL.md",
                 "kit/templates/prevalidation-report.md", "kit/templates/artifact.md",
                 "kit/templates/state.md"):
        content = public.get(name, "")
        missing = [o for o in outcomes if o not in content]
        if missing:
            problems.append("%s — нет исходов: %s" % (name, ", ".join(missing)))

    for name, key in (("kit/templates/audit-log.md", "finding"), ("kit/skills/09-audit/SKILL.md", "finding"),
                      ("kit/templates/audit-log.md", "evidence_classes"), ("kit/skills/09-audit/SKILL.md", "evidence_classes"),
                      ("kit/templates/judge-report.md", "judge"), ("kit/skills/m3-judge/SKILL.md", "judge"),
                      ("kit/templates/state.md", "artifact"), ("kit/templates/state.md", "check"),
                      ("kit/templates/hadi-tracker.md", "obligation"), ("kit/skills/05-validation-gate/SKILL.md", "verdicts")):
        content = public.get(name, "")
        missing = [s for s in canon["statuses"][key] if s not in content]
        if missing:
            problems.append("%s — нет статусов %s: %s" % (name, key, ", ".join(missing)))

    for value, where in ((canon["limits"]["questions_first_session"], ["kit/AGENTS.md"]),
                         (canon["limits"]["timebox_hours"], ["kit/AGENTS.md", "kit/skills/04-mvp-artifact/SKILL.md"]),
                         (canon["limits"]["message_words"], ["kit/skills/04-mvp-artifact/SKILL.md"]),
                         (canon["limits"]["silence_hours"], ["kit/skills/06-access/SKILL.md", "kit/templates/access-log.md"])):
        for name in where:
            if not numbers_ok(public.get(name, ""), value):
                problems.append("%s — нет предела %s" % (name, value))

    for key, where in canon["limits_where"].items():
        value = canon["limits"].get(key)
        if value is None:
            problems.append("Канон — предел «%s» объявлен в limits_where, но не описан в limits" % key)
            continue
        pattern = canon["limits_patterns"].get(key)
        for name in where:
            content = public.get(name, "")
            if pattern is not None:
                if not re.search(pattern, content, re.IGNORECASE):
                    problems.append("%s — не назван предел «%s» в правильном контексте (%s)"
                                    % (name, key, pattern))
            elif not numbers_ok(content, value):
                problems.append("%s — не назван предел «%s» = %s" % (name, key, value))

    # Значение предела сверяется во всех вхождениях шаблона, а не только фактом
    # присутствия: «три часа» внутри правила при каноне «четыре» — расхождение.
    for key, pattern in canon["limits_values"].items():
        canonical = canon["limits"].get(key)
        if isinstance(canonical, str):
            continue  # предел записан диапазоном — сравнивать не с чем
        regex = re.compile(pattern.replace("NUM", NUMBER_TOKEN), re.IGNORECASE)
        for name in canon["limits_where"].get(key, []):
            content = public.get(name, "")
            for match in regex.finditer(content):
                got = number_value(match.group("num"))
                if got is None:
                    problems.append("%s — не удалось прочитать число предела «%s»: %r"
                                    % (name, key, " ".join(match.group(0).split())))
                elif got != canonical:
                    problems.append("%s — предел «%s» назван как %s, канон говорит %s (%s)"
                                    % (name, key, got, canonical,
                                       " ".join(match.group(0).split())[:70]))

    for key in canon["limits_required"]:
        if key not in canon["limits"] or key not in canon["limits_where"]:
            problems.append("Канон — обязательный предел «%s» удалён из limits или limits_where: правило нельзя проверить" % key)

    for path, fields in canon.get("required", {}).items():
        content = public.get(path)
        if content is None:
            content = read(path)
        for needed in fields:
            if needed not in content:
                problems.append("%s — нет обязательного поля или раздела «%s»" % (path, needed))

    for script in re.findall(r'^\s*\("[^"]+",\s*"([^"]+\.py)"\)', verify, re.MULTILINE):
        if not os.path.exists(os.path.join(ROOT, *script.split("/"))):
            problems.append("verify.py обещает проверку %s, а её нет" % script)

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
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as error:
        print("ИТОГ: 2 — канон сломан или проверка упала: %s" % error)
        sys.exit(2)
