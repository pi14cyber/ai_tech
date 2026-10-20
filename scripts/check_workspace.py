#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка артефактов в workspace: барьеры существуют только если читают файлы.

Зачем: четыре круга аудита показали, что все барьеры обходятся, потому что
ни одна проверка не читает `workspace/`. Здесь проверяются сами артефакты:
отчёт ворот, отчёт судьи, журнал находок, состояние.

Что проверяет (только если файлы есть):
 1. `workspace/state.md` — есть блок шага, режим, счётчик вопросов, решение судьи,
    версия результата, исход ворот. Версия читается и как число, и как фраза
    «N — пояснение» (формы пишут именно фразу). Строка «Показ состоялся» —
    событие показа, а не подпись.
 2. Отчёты ворот `workspace/research/prevalidation-*.md` — исход ровно из четырёх,
    не меньше двух строк `Q` с адресом и датой, для «дип» — два файла ответов,
    при исходе «прошло» остальные требования выполнены. Указанный в состоянии
    путь к отчёту обязан существовать на диске.
 3. Отчёты судьи `workspace/judge-report-*.md` — заполнено решение (показывать или
    не показывать), заполнена версия результата, есть результат проверок.
    «Кто проверял» пустым не бывает: парсер не подхватывает соседнюю строку.
    Независимость судьи — признак «другой проход», а не сравнение строк: честное
    «сам автор» — нарушение, «другой агент» / «второй проход» — нет.
 4. `workspace/audit-log.md` — у каждой строки класс A/B/C/D и допустимый статус.
 5. `workspace/artifact.md` — ворота как условие сборки: исход «прошло» требует
    файла отчёта предвалидации с исходом «прошло» (а не только строки пути).
 6. Показ — событие с требованиями: читаются все носители статуса (поле, таблица
    артефакта, таблица состояния, строка «Показ состоялся»); показ, записанный
    только в таблицу, — тоже показ, и он обязан сойтись с полем «Статус»,
    решением судьи, подписью человека и журналом решений.
 7. `workspace/memory/decisions.md` — цитата, канал, дата и автор решения: «Кто
    решил: агент» — код 1, решение принимает человек.

Чего не проверяет: качество содержания, правдивость цитат, ход разговора; путь
к файлу на диске подтверждает существование, а не то, что это нужный файл.

Коды: 0 — нарушения нет или проверять нечего; 1 — артефакт нарушает правило;
2 — workspace есть, но не читается (или самопроверка не смогла выполниться).
"""

import glob
import hashlib
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
ARTIFACT_VOCAB = ("черновик", "показан человеку", "есть обязательство")
OUTCOMES_ORDER = ("не запускалось", "не прошло", "заблокировано", "прошло")
LIMITS = {"first": 5, "later": 3}


def outcome_of(value):
    """Исход ворот: сначала «не прошло», потом «прошло» — иначе «не» перебьёт значение."""
    text = re.sub(r"\s+", " ", (value or "").strip().lower())
    for outcome in OUTCOMES_ORDER:
        if text.startswith(outcome):
            return outcome
    return None


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
    """Значение поля в той же строке, где стоит ключ.

    Перенос строки значением не считается: пустое поле — это пусто, а не соседняя
    строка отчёта. Пояснение между ключом и двоеточием допустимо (формы пишут
    «Решение судьи — вписать одно значение…:**» и «Уровень готовности делиться
    (заполняет человек):»), но за двоеточием ответ всё равно обязателен.
    """
    pattern = (r"(?<![А-Яа-яЁё])" + re.escape(key)
               + r"(?:[ \t]*(?:[—–-][^\n:]{0,80}|\([^\n:)]{0,80}\)))?"
               + r"[ \t]*\**:[ \t]*\**"
               + r"([^\n]*)")
    match = re.search(pattern, content)
    if not match:
        return None
    value = match.group(1).strip().strip("*` ")
    if not value:
        return None
    lowered = value.lower()
    if value.startswith("(") or "____" in value or "вписать" in lowered or "заполняет" in lowered:
        return None
    if " / " in value:
        return None
    return value


def version_of(value):
    """Номер версии из значения: «1» и «1 — пояснение» одинаково дают 1."""
    if value is None:
        return None
    match = re.match(r"\s*(\d+)(?!\d)", value)
    return int(match.group(1)) if match else None


SELF_JUDGE_RE = re.compile(r"\bсам\b|\bсама\b|\bсамо\b|сам автор|сам проверил|свою работу|"
                           r"своей работы|свою же работу|является автором", re.IGNORECASE)
OTHER_PASS_RE = re.compile(r"друг|втор|независим|рецензент|отдельн\w+ проход|чистого листа|"
                           r"коллег|человек", re.IGNORECASE)
SHOW_STATUS = "показан человеку"


def path_exists_any(value):
    """Указанный путь к файлу существует: от корня, от workspace или по имени в папке."""
    candidate = (value or "").strip().strip("`").strip()
    if not candidate or "<" in candidate or "вписать" in candidate.lower():
        return False
    candidates = [os.path.join(ROOT, candidate), os.path.join(WS, candidate),
                  os.path.join(WS, os.path.basename(candidate))]
    return any(os.path.exists(path) for path in candidates)


def table_statuses(content):
    """Статусы артефакта из таблиц «Артефакт | Статус | …» в любом носителе."""
    found = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) >= 2 and cells[1].lower().strip(" .") in ARTIFACT_VOCAB:
            found.append(cells[1].lower().strip(" ."))
    return found


def load_escalation():
    path = os.path.join(ROOT, "rules", "canon.json")
    defaults = {"attempts_without_progress": 2, "repeated_blocker_rounds": 2,
                "regressions_limit": 1, "unknowns_without_source": 3}
    if not os.path.exists(path):
        return defaults
    try:
        canon = json.load(open(path, encoding="utf-8"))
        merged = dict(defaults)
        merged.update(canon.get("escalation", {}))
        return merged
    except Exception:
        return defaults


def main():
    global ROOT, WS
    if __name__ == "__main__" and "--root" in sys.argv:
        index = sys.argv.index("--root")
        if index + 1 >= len(sys.argv):
            print("ИТОГ: 2 — параметр --root без значения: проверять нечего")
            return 2
        ROOT = os.path.abspath(sys.argv[index + 1])
        WS = os.path.join(ROOT, "workspace")
        if not os.path.isdir(WS):
            print("ИТОГ: 2 — корень %s не найден: проверять нечего" % ROOT)
            return 2
    if not os.path.isdir(WS):
        print("workspace/ нет — проверять нечего (режим пользователя)")
        print("\nИТОГ: 0 — артефактов нет")
        return 0

    problems = []
    checked = 0
    state_version = None
    state_decision = None
    state_ready = None
    state_gate = None
    state_signature = None
    state_content = None
    show_event = None
    judge_checker = None
    judge_version = None
    judge_authorizes_artifact = False
    report_outcomes = []

    state_path = os.path.join(WS, "state.md")
    if os.path.exists(state_path):
        checked += 1
        content = read(state_path)
        state_content = content
        for key in ("Текущий шаг", "Режим", "Задано вопросов", "Номер сессии"):
            if field(content, key) is None:
                problems.append("state.md — не заполнено поле «%s» (подсказка не считается ответом)" % key)
        step = field(content, "Текущий шаг") or ""
        if not any(v in step.lower() for v in STEP_VOCAB):
            problems.append("state.md — текущий шаг «%s» не из словаря" % step)
        marker = os.path.exists(os.path.join(WS, "LOCAL-ONLY"))
        mode = re.sub(r"\s+", " ", (field(content, "Режим") or "").strip().lower())
        if "/" in mode:
            problems.append("state.md — режим «%s»: не выбран один из двух" % mode)
            mode = ""
        if mode and mode not in MODE_VOCAB:
            problems.append("state.md — режим «%s» не из словаря" % mode)
        if marker and mode and mode != "только локально":
            problems.append("state.md — файл LOCAL-ONLY есть, а режим «%s»: расхождение" % mode)
        if not marker and mode == "только локально":
            problems.append("state.md — режим «только локально», а файла LOCAL-ONLY нет")
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
        for key in ("Исход ворот", "Решение судьи", "Контур", "Версия результата"):
            if len(re.findall(re.escape(key) + r"[^\n:]*:", content)) > 1:
                problems.append("state.md — поле «%s» встречается больше одного раза" % key)
        gate_value = outcome_of(gate) if gate is not None else None
        state_gate = gate_value
        if gate is not None and gate_value is None:
            problems.append("state.md — исход ворот «%s» не из словаря" % gate)
        if gate_value == "прошло":
            if not glob.glob(os.path.join(WS, "research", "prevalidation-*.md")):
                problems.append("state.md — исход ворот «прошло», а отчёта предвалидации нет")
            declared_report = field(content, "Отчёт предвалидации")
            if declared_report is not None and not path_exists_any(declared_report):
                problems.append("state.md — отчёт предвалидации указан, но файла нет: %s" % declared_report)
        if gate_value in ("не прошло", "заблокировано", "не запускалось") \
                and os.path.exists(os.path.join(WS, "artifact.md")):
            problems.append("state.md — ворота не пройдены, а артефакт собран")
        version_field = field(content, "Версия результата")
        if version_field is not None:
            state_version = version_of(version_field)
            if state_version is None:
                problems.append("state.md — версия результата «%s» не число" % version_field)
        decision_field = field(content, "Решение судьи")
        if decision_field is not None:
            lowered_decision = decision_field.lower()
            if re.search(r"показывать\s+(нельзя|не|нет)", lowered_decision):
                problems.append("state.md — решение «%s» читается как запрет, а не как разрешение" % decision_field)
                state_decision = "не показывать"
            elif "не показывать" in lowered_decision:
                state_decision = "не показывать"
            elif lowered_decision.strip(" .").startswith("показывать"):
                state_decision = "показывать"
        signature = field(content, "Подписал человек")
        if signature is not None:
            lowered_signature = signature.lower()
            weak = lowered_signature.strip(" .—-") in ("", "нет", "да", "ок", "—", "-") \
                or "не ответил" in lowered_signature or "агент" in lowered_signature
            if weak:
                problems.append("state.md — подпись человека «%s» не является цитатой согласия" % signature)
            elif not re.search(r"\d{2}\.\d{2}\.\d{4}", signature) or "|" not in signature:
                problems.append("state.md — в подписи должны быть цитата | канал | дата (дд.мм.гггг)")
            else:
                state_signature = signature
        event = field(content, "Показ состоялся")
        if event is not None:
            show_event = event
        ready = field(content, "Готов к показу")
        if ready is not None:
            head = ready.strip().split()[0].strip(".,:;—-").lower()
            if head not in READY_VOCAB:
                problems.append("state.md — «готов к показу» = «%s» не из да/нет" % ready)
            else:
                state_ready = head
            if head == "да":
                decision = field(content, "Решение судьи")
                normalized = (decision or "").lower()
                if "не показывать" in normalized:
                    problems.append("state.md — «готов к показу», но судья сказал «не показывать»")
                elif not normalized.strip(" .").startswith("показывать"):
                    problems.append("state.md — «готов к показу», но строгого решения судьи «показывать» нет")

        # Внешняя проверка: счётчики триггера против порогов канона
        thresholds = load_escalation()
        for key in ("Раундов без прогресса", "Повторяющийся блокер", "Регрессий от последней правки",
                    "Открытых вопросов без источника", "Запрос составлен", "Отправлен человеком"):
            if field(content, key) is None:
                problems.append("state.md — не заполнен блок «Внешняя проверка»: «%s»" % key)

        def counter(key):
            value = field(content, key)
            if value is None:
                return 0
            match = re.search(r"\d+", value)
            return int(match.group(0)) if match else 0

        rounds = counter("Раундов без прогресса")
        regressions = counter("Регрессий от последней правки")
        unknowns = counter("Открытых вопросов без источника")
        blocker = field(content, "Повторяющийся блокер") or ""
        lowered_blocker = blocker.lower()
        if "нет" in lowered_blocker:
            blocker_rounds = 0
        else:
            digits = re.search(r"\d+", lowered_blocker)
            blocker_rounds = int(digits.group(0)) if digits else 0
        triggered = (rounds >= thresholds["attempts_without_progress"]
                     or regressions >= thresholds["regressions_limit"]
                     or unknowns >= thresholds["unknowns_without_source"]
                     or blocker_rounds >= thresholds["repeated_blocker_rounds"])
        request = field(content, "Запрос составлен")
        sent = (field(content, "Отправлен человеком") or "").lower()
        if triggered:
            if request is None or request.strip().lower() in ("нет", "—", "-", "не составлен"):
                problems.append("state.md — счётчики внешней проверки превышены, а запрос не составлен "
                                "(нужен навык m4-external-check)")
            else:
                candidate = request.strip().strip("`")
                found = (os.path.exists(os.path.join(ROOT, candidate))
                         or os.path.exists(os.path.join(WS, candidate))
                         or os.path.exists(os.path.join(WS, "requests", os.path.basename(candidate))))
                if not found:
                    problems.append("state.md — запрос указан, но файла нет: %s" % request)
                if not sent.startswith("да"):
                    problems.append("state.md — запрос составлен, но человеком не отправлен: правки остановлены")

    profile_path = os.path.join(WS, "profile.md")
    if os.path.exists(profile_path):
        checked += 1
        content = read(profile_path)
        consent = field(content, "Уровень готовности делиться")
        if consent is None:
            problems.append("profile.md — не заполнен уровень готовности делиться данными (вопрос шага 0)")
        else:
            normalized = consent.strip().strip(".:;—-").lower()
            if normalized not in ("файлы", "метаданные", "только ответы", "ответы", "только локально", "локально"):
                problems.append("profile.md — уровень готовности «%s» не из четырёх вариантов (меню не ответ)" % consent)

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
                fact_lines = [line for line in content.splitlines()
                              if re.search(r"Q\d+\.\d+", line) and "http" in line
                              and re.search(r"\d{2}\.\d{2}\.\d{4}", line)]
                packet_match = re.search(r"Пакет\**\s*:\**\s*(\d+)\s*из\s*(\d+)", content)
                if packet_match:
                    packet_number, packet_total = int(packet_match.group(1)), int(packet_match.group(2))
                    if packet_number < 1 or packet_total < 1 or packet_number > packet_total:
                        problems.append("%s — «Пакет: %d из %d»: номер и всего должны быть ≥1 и N ≤ M"
                                        % (name, packet_number, packet_total))
                else:
                    packet_number = None
                if packet_number is not None:
                    wrong = [line for line in fact_lines
                             if re.search(r"Q(\d+)\.[0-9]+", line)
                             and int(re.search(r"Q(\d+)\.[0-9]+", line).group(1)) != packet_number]
                    if wrong:
                        problems.append("%s — строки Q не из пакета %d: %s"
                                        % (name, packet_number, wrong[0].strip()[:40]))
                if len(fact_lines) < 2:
                    problems.append("%s — при исходе «прошло» нужно не меньше двух строк Q с адресом и датой (найдено %d)"
                                    % (name, len(fact_lines)))
                else:
                    ids = [re.search(r"Q\d+\.\d+", line).group(0) for line in fact_lines]
                    if len(set(ids)) < 2:
                        problems.append("%s — два факта с одинаковым номером Q: нужны два разных вопроса" % name)
                    for fact in fact_lines:
                        if not re.search(r"https?://\S+", fact):
                            problems.append("%s — в строке Q нет адреса" % name)
                        if not re.search(r"\d{2}\.\d{2}\.\d{4}", fact):
                            problems.append("%s — в строке Q нет даты" % name)
                        text_only = re.sub(r"Q\d+\.\d+|https?://\S+|\d{2}\.\d{2}\.\d{4}", " ", fact)
                        if len(re.findall(r"[А-Яа-яЁёA-Za-z]", text_only)) < 3:
                            problems.append("%s — строка Q без текста вопроса: один номер не считается фактом" % name)
                if len({re.search(r"Q\d+\.\d+", line).group(0) for line in fact_lines}) < 2:
                    problems.append("%s — два факта должны быть разными вопросами" % name)
                hashes = []
                for response in responses:
                    hashes.append(hashlib.sha256(read(response).encode("utf-8", "replace")).hexdigest())
                if len(set(hashes)) < len(hashes):
                    problems.append("%s — файлы ответов не уникальны: копия ответа не считается вторым каналом" % name)
                for response in responses:
                    body = read(response)
                    if len(body) < 200:
                        problems.append("%s — ответ %s короче 200 знаков: мусор не считается ответом"
                                        % (name, os.path.basename(response)))
                    elif len(set(re.findall(r"Q\d+\.\d+", body))) < 2:
                        problems.append("%s — ответ %s не содержит двух разных вопросов"
                                        % (name, os.path.basename(response)))
                if not responses:
                    problems.append("%s — исход «прошло», но ни одного файла ответа нет: ворота не пройдены" % name)
                else:
                    for response in responses:
                        body = read(response)
                        if len(body) < 100 or not re.search(r"Q\d+\.\d+", body):
                            problems.append("%s — файл ответа %s пустой или без ответов Q: ворота не пройдены"
                                            % (name, os.path.basename(response)))
                if "дип" in content and len(responses) < 2:
                    problems.append("%s — полный запрос, а файлов ответов %d (нужно два)" % (name, len(responses)))
        if report_outcomes and state_gate == "прошло" and any(o != "прошло" for _n, o in report_outcomes):
            problems.append("state.md — исход ворот «прошло», а в отчёте ворот есть «%s»: сборка запрещена"
                            % ", ".join(sorted({o for _n, o in report_outcomes if o != "прошло"})))
        if "Пакет" not in content:
            problems.append("%s — нет поля «Пакет: N из M»" % name)
        if not re.search(r"Пакет\**\s*:\**\s*\d+\s*из\s*\d+", content):
            problems.append("%s — поле пакета должно быть «Пакет: N из M» с числами" % name)
        if outcome is not None and outcome_of(outcome) is not None:
            report_outcomes.append((name, outcome_of(outcome)))
        category_line = re.search(r"Категория запуска:[^\n]*", content)
        if category_line and "/" not in category_line.group(0) and "дип" in category_line.group(0):
            if len(responses) < 2:
                problems.append("%s — категория «дип», а файлов ответов %d (нужно два)" % (name, len(responses)))

    for report in sorted(glob.glob(os.path.join(WS, "judge-report-*.md"))):
        checked += 1
        name = os.path.basename(report)
        content = read(report)
        judge_checker = field(content, "Кто проверял")
        decision_raw = field(content, "Решение судьи")
        normalized = (decision_raw or "").lower().strip(" .")
        if re.search(r"показывать\s+(нельзя|не|нет)", normalized):
            problems.append("%s — решение «%s» не распознано как «показывать» или «не показывать»" % (name, decision_raw))
        if decision_raw is not None and len(re.findall(r"Решение судьи", content)) > 1:
            problems.append("%s — поле «Решение судьи» встречается больше одного раза" % name)
        if judge_checker is None:
            problems.append("%s — не заполнено «Кто проверял»: независимость судьи не доказана" % name)
        if "не показывать" in normalized:
            pass
        elif not normalized.startswith("показывать"):
            problems.append("%s — нет строгого решения судьи «показывать» или «не показывать»" % name)
        version = field(content, "Версия результата")
        judge_version = version_of(version)
        what = (field(content, "Что проверяли") or "").lower()
        if "показывать" in normalized and "не показывать" not in normalized and "артефакт" in what:
            judge_authorizes_artifact = True
        if version is not None and judge_version is None:
            problems.append("%s — версия «%s» не число: сравнение версий невозможно" % (name, version))
        if version is None:
            problems.append("%s — нет привязки к версии результата" % name)
        elif state_version is not None and judge_version != state_version:
            problems.append("%s — версия результата %s не совпадает с состоянием %s"
                            % (name, version.strip(), state_version))
        if "Итог проверок" not in content:
            problems.append("%s — нет строки «Итог проверок»: пустые результаты не отличить от непроверенных" % name)
        elif not re.search(r"Итог проверок[^\n]*\d+", content):
            problems.append("%s — «Итог проверок» без числа проверенных" % name)
        if state_decision is not None:
            report_decision = "не показывать" if "не показывать" in normalized else "показывать"
            if state_decision != report_decision:
                problems.append("%s — решение судьи «%s» против состояния «%s»"
                                % (name, report_decision, state_decision))
        result_rows = []
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped.startswith("|") or "---" in stripped:
                continue
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if any(cell in ("Результат", "Итог", "#") for cell in cells):
                continue
            if len(cells) >= 2 and cells[-1]:
                result_rows.append(stripped)
        summary = re.search(r"Итог проверок[^\n]*?(\d+)\s*из\s*(\d+)", content)
        if summary is None:
            problems.append("%s — нет строки «Итог проверок: N из M» с числами" % name)
        else:
            done, declared = int(summary.group(1)), int(summary.group(2))
            if done < 1:
                problems.append("%s — «Итог проверок: 0 из %d»: ни одной проверки не выполнено" % (name, declared))
            if declared < 9:
                problems.append("%s — «Итог проверок: … из %d»: в форме девять проверок, а объявлено меньше" % (name, declared))
            if done != len(result_rows):
                problems.append("%s — «Итог проверок: %d из %d», а заполненных строк результатов %d: число не совпадает"
                                % (name, done, declared, len(result_rows)))

    audit_path = os.path.join(WS, "audit-log.md")
    open_findings = []
    if os.path.exists(audit_path):
        checked += 1
        for number, line in enumerate(read(audit_path).splitlines(), 1):
            if not line.strip().startswith("|") or "---" in line:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 6 or cells[0].startswith("#"):
                continue
            if cells[0] in ("", "№"):
                if any(cell for cell in cells[1:]):
                    problems.append("audit-log.md:%d — строка без номера: находка не учтена" % number)
                continue
            if cells[3] not in CLASSES:
                problems.append("audit-log.md:%d — класс «%s» не из A/B/C/D" % (number, cells[3]))
            if cells[3] in ("A", "B") and len(cells) > 4 and not cells[4]:
                problems.append("audit-log.md:%d — класс %s без адреса «Где (файл:строка)»" % (number, cells[3]))
            if cells[5] in ("найдено", "предложено"):
                open_findings.append(number)
            if cells[5] not in FINDING:
                problems.append("audit-log.md:%d — статус «%s» не из словаря" % (number, cells[5]))
            if cells[5] == "внедрено" and not cells[6]:
                problems.append("audit-log.md:%d — статус «внедрено» без доказательства внедрения" % number)
            if cells[5] == "отклонено" and (len(cells) < 9 or not cells[7]):
                problems.append("audit-log.md:%d — статус «отклонено» без того, кто решил" % number)
            if cells[5] == "проверено":
                who = cells[8].strip() if len(cells) > 8 else ""
                if not who:
                    problems.append("audit-log.md:%d — статус «проверено» без того, кто проверил" % number)

    decisions_path = os.path.join(WS, "memory", "decisions.md")
    decisions_signed = False
    if os.path.exists(decisions_path):
        checked += 1
        for number, line in enumerate(read(decisions_path).splitlines(), 1):
            if not line.strip().startswith("|") or "---" in line:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 8 or cells[0] in ("", "Дата"):
                continue
            if not any(cells):
                continue
            who, quote, channel, when = cells[6], cells[3], cells[4], cells[5]
            if who and re.search(r"\bагент", who.lower()):
                problems.append("decisions.md:%d — в графе «Кто решил» стоит агент: решение "
                                "принимает человек, агент его не вписывает" % number)
            if who and not quote:
                problems.append("decisions.md:%d — решение записано, а дословной цитаты решения нет" % number)
            if who and not channel:
                problems.append("decisions.md:%d — решение записано, а канала нет" % number)
            if who and not when:
                problems.append("decisions.md:%d — решение записано, а даты нет" % number)
            if who and quote and channel and when:
                decisions_signed = True

    artifacts_dir = os.path.join(WS, "artifacts")
    if os.path.isdir(artifacts_dir):
        for path in sorted(glob.glob(os.path.join(artifacts_dir, "**", "*.md"), recursive=True)):
            checked += 1
            body = read(path)
            if "показан человеку" in body.lower():
                problems.append("artifacts/%s — статус «показан человеку» в отдельном файле; "
                                "единственный носитель статуса и версии — workspace/artifact.md"
                                % os.path.basename(path))

    artifact_path = os.path.join(WS, "artifact.md")
    if os.path.exists(artifact_path) and not os.path.exists(os.path.join(WS, "state.md")):
        problems.append("artifact.md — артефакт есть, а состояния нет: версии и решения не с чем сверять")
    if os.path.exists(artifact_path):
        checked += 1
        content = read(artifact_path)
        if report_outcomes and any(outcome != "прошло" for _name, outcome in report_outcomes):
            bad = sorted({outcome for _name, outcome in report_outcomes if outcome != "прошло"})
            problems.append("artifact.md — артефакт собран при исходе отчёта ворот «%s»: сборка запрещена"
                            % ", ".join(bad))
        if "Показан человеку" in content:
            problems.append("artifact.md — статус с заглавной буквы: не из словаря")
        status = field(content, "Статус")
        status_key = None
        if status is not None:
            status_key = status.strip().lower().strip(" .")
            if status_key not in ARTIFACT_VOCAB:
                problems.append("artifact.md — статус «%s» не из словаря (черновик / показан человеку / есть обязательство)"
                                % status)
        # Показ — событие, и читается он со всех носителей: поле «Статус», таблица
        # артефакта, таблица состояния и строка «Показ состоялся». Показ, записанный
        # только в таблицу, всё равно показ, а не способ его спрятать.
        carriers = []
        if status_key == SHOW_STATUS:
            carriers.append("поле «Статус»")
        if SHOW_STATUS in table_statuses(content):
            carriers.append("таблица артефакта")
        if state_content is not None and SHOW_STATUS in table_statuses(state_content):
            carriers.append("таблица состояния")
        if show_event is not None:
            carriers.append("строка «Показ состоялся» (%s)" % show_event)
        shown = bool(carriers)
        if shown and show_event is None:
            problems.append("artifact.md — показ записан (%s), а строки-события «Показ состоялся» в "
                            "state.md нет: показ — событие, а не ячейка таблицы" % ", ".join(carriers))
        if shown and status_key is not None and status_key != SHOW_STATUS:
            problems.append("artifact.md — поле «Статус» = «%s», а показ записан (%s): носители расходятся"
                            % (status, ", ".join(carriers)))
        if shown:
            if not os.path.exists(state_path):
                problems.append("artifact.md — статус «показан человеку», а состояния нет: сверять не с чем")
            if open_findings:
                problems.append("artifact.md — артефакт показан, но в журнале находок есть открытые (%d): показ запрещён"
                                % len(open_findings))
            if state_ready is None or state_ready != "да":
                problems.append("artifact.md — статус «показан человеку», а «Готов к показу» в состоянии не «да»")
            if state_signature is None:
                problems.append("artifact.md — артефакт показан без подписи человека в состоянии: показ не разрешён")
            if not judge_authorizes_artifact and glob.glob(os.path.join(WS, "judge-report-*.md")):
                problems.append("artifact.md — отчёт судьи не про артефакт: он не разрешает показ артефакта")
            if not decisions_signed:
                problems.append("artifact.md — артефакт показан, а в журнале решений нет подписи человека "
                                "(цитата, канал, дата)")
            judges = glob.glob(os.path.join(WS, "judge-report-*.md"))
            ok = False
            for judge in judges:
                decision = field(read(judge), "Решение судьи")
                if decision and "показывать" in decision and "не показывать" not in decision:
                    ok = True
            if not ok:
                problems.append("artifact.md — статус «показан человеку», но нет отчёта судьи с решением «показывать»")
        artifact_version_raw = field(content, "Версия результата") or field(content, "Версия")
        artifact_version = version_of(artifact_version_raw)
        artifact_author = field(content, "Кто собрал")
        artifact_outcome = field(content, "Исход проверки")
        outcome_key = outcome_of(artifact_outcome or "")
        if artifact_outcome is None:
            problems.append("artifact.md — не заполнен «Исход проверки»: без него артефакт не считается проверенным")
        elif shown and outcome_key in ("не прошло", "заблокировано", "не запускалось"):
            problems.append("artifact.md — артефакт показан при исходе проверки «%s»: показ запрещён" % outcome_key)
        # Ворота — условие сборки: исход «прошло» без файла отчёта предвалидации
        # не исход, а самодельная строка. Проверяется файл, а не только путь.
        if os.path.exists(state_path) and state_gate is None:
            problems.append("artifact.md — артефакт собран, а «Исход ворот» в состоянии не заполнен: "
                            "ворота — условие сборки")
        if outcome_key == "прошло":
            reports = sorted(glob.glob(os.path.join(WS, "research", "prevalidation-*.md")))
            passed = [report for report in reports
                      if outcome_of(field(read(report), "Исход ворот") or "") == "прошло"]
            if not passed:
                problems.append("artifact.md — исход проверки «прошло», а отчёта предвалидации с исходом "
                                "«прошло» в workspace/research нет: ворота не пройдены")
            declared_report = field(content, "Отчёт предвалидации")
            if declared_report is not None and not path_exists_any(declared_report):
                problems.append("artifact.md — отчёт предвалидации указан, но файла нет: %s" % declared_report)
        if artifact_version_raw is not None and artifact_version is None:
            problems.append("artifact.md — версия «%s» не число" % artifact_version_raw)
        if artifact_version is not None and judge_version is not None and artifact_version != judge_version:
            problems.append("artifact.md — версия артефакта %s не совпадает с версией в отчёте судьи %s"
                            % (artifact_version, judge_version))
        if artifact_version is not None and state_version is not None and artifact_version != state_version:
            problems.append("artifact.md — версия артефакта %s не совпадает с версией в состоянии %s"
                            % (artifact_version, state_version))
        if judge_checker is not None:
            checker_text = re.sub(r"\([^)]*\)", "", judge_checker.lower()).strip()
            if SELF_JUDGE_RE.search(checker_text):
                problems.append("artifact.md — отчёт судьи прямо говорит, что проверял сам автор: "
                                "нужен другой проход (человек или другой агент)")
            elif artifact_author is not None and not OTHER_PASS_RE.search(checker_text):
                author_text = re.sub(r"\([^)]*\)", "", artifact_author.lower()).strip()
                if author_text == checker_text or ("агент" in author_text and "агент" in checker_text):
                    problems.append("artifact.md — судья и автор совпадают: отчёт не называет другой проход "
                                    "(человек или другой агент)")

    print("файлов проверено: %d" % checked)
    for line in problems:
        print("НАРУШЕНИЕ: %s" % line)
    if problems:
        print("\nИТОГ: 1 — артефакты нарушают правила (%d)" % len(problems))
        return 1
    if checked == 0:
        print("\nИТОГ: 0 — проверять нечего: в workspace нет ни одного артефакта "
              "(состояние, профиль, отчёты не созданы)")
        return 0
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
             encoding="utf-8").write(
                 "# Ответ\n\nQ1.1: по данным сервиса ставка составляет 12 тысяч рублей в месяц, "
                 "источник — прайс-лист на сайте, проверено 01.10.2026, ссылка сохранена в отчёте.\n"
                 "Q1.2: второй факт — срок действия тарифа до 31.12.2026, источник тот же прайс-лист, "
                 "проверено 01.10.2026, ссылка сохранена в отчёте.\n")
    state = (
        "# Состояние\n\n"
        "- **Текущий шаг:** артефакт\n- **Что дальше (один шаг):** судья\n"
        "- **Режим:** обычный\n- **Задано вопросов:** 4\n"
        "- **Номер сессии:** 1\n"
        "- **Контур:** внешний\n- **Исход ворот:** прошло\n"
        "- **Отчёт предвалидации:** workspace/research/prevalidation-2026-10-20.md\n"
        "- **Версия результата:** 1 — растёт при каждой переделке\n- **Готов к показу:** да\n"
        "- **Решение судьи:** показывать\n"
        "- **Решение человека:** «давай» | telegram | 20.10.2026\n"
        "- **Подписал человек:** «давай» | telegram | 20.10.2026\n"
        "- **Показ состоялся (дата, канал):** 20.10.2026, telegram\n"
        "- **Раундов без прогресса:** 0\n- **Повторяющийся блокер:** нет\n"
        "- **Регрессий от последней правки:** 0\n- **Открытых вопросов без источника:** 0\n"
        "- **Запрос составлен:** нет\n- **Отправлен человеком:** нет\n"
    )
    report = (
        "# Отчёт предвалидации\n\n- **Исход ворот:** прошло\n"
        "- **Пакет:** 1 из 1\n\n"
        "| Q | Вопрос | Ссылок |\n|---|---|---|\n"
        "| Q1.1 | вопрос | https://a.example/1 01.10.2026 |\n"
        "| Q1.2 | вопрос | https://b.example/2 02.10.2026 |\n"
    )
    artifact = (
        "# Артефакт\n\n- **Статус:** показан человеку\n"
        "- **Версия результата:** 1 — единственный источник workspace/state.md\n"
        "- **Кто собрал:** агент\n- **Исход проверки:** прошло\n"
        "- **Отчёт предвалидации:** workspace/research/prevalidation-2026-10-20.md\n"
        "- **Текст сообщения человеку (до 80 слов):** Здравствуйте, собрал сводку.\n"
    )
    judge = (
        "# Отчёт судьи\n\n- **Что проверяли:** артефакт\n- **Кто проверял:** другой агент\n"
        "- **Версия результата:** 1 — из workspace/state.md\n- **Итог проверок:** 1 из 9\n\n"
        "| # | Что проверено | Как | Результат |\n|---|---|---|---|\n"
        "| 1 | числа | чтение | да |\n\n- **Решение судьи:** показывать\n"
    )
    decisions = (
        "# Решения\n\n| Дата | Решение | На каком основании | Цитата решения | Канал | Когда | Кто решил | Что дальше |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| 20.10.2026 | показать | проверено | «давай» | telegram | 20.10.2026 | Иван | встреча |\n"
    )
    for root in (ok_root, bad_root):
        open(os.path.join(root, "workspace", "state.md"), "w", encoding="utf-8").write(state)
        open(os.path.join(root, "workspace", "research", "prevalidation-2026-10-20.md"),
             "w", encoding="utf-8").write(report)
        open(os.path.join(root, "workspace", "artifact.md"), "w", encoding="utf-8").write(artifact)
        open(os.path.join(root, "workspace", "judge-report-2026-10-20.md"),
             "w", encoding="utf-8").write(judge)
        os.makedirs(os.path.join(root, "workspace", "memory"))
        open(os.path.join(root, "workspace", "memory", "decisions.md"),
             "w", encoding="utf-8").write(decisions)
    bad_report = os.path.join(bad_root, "workspace", "research", "prevalidation-2026-10-20.md")
    content = open(bad_report, encoding="utf-8").read().replace(":** прошло", ":** ____", 1)
    open(bad_report, "w", encoding="utf-8").write(content)

    esc_root = os.path.join(base, "esc")
    os.makedirs(os.path.join(esc_root, "workspace"))
    esc_state = (state
                 .replace("Раундов без прогресса:** 0", "Раундов без прогресса:** 2")
                 .replace("Повторяющийся блокер:** нет", "Повторяющийся блокер:** 2 круга"))
    open(os.path.join(esc_root, "workspace", "state.md"), "w", encoding="utf-8").write(esc_state)

    nojudge_root = os.path.join(base, "nojudge")
    shutil.copytree(ok_root, nojudge_root)
    os.remove(os.path.join(nojudge_root, "workspace", "judge-report-2026-10-20.md"))

    # Ворота — условие сборки: «прошло» без файла отчёта предвалидации — код 1.
    noreport_root = os.path.join(base, "noreport")
    shutil.copytree(ok_root, noreport_root)
    os.remove(os.path.join(noreport_root, "workspace", "research", "prevalidation-2026-10-20.md"))

    # Судья не автор: «сам автор» — код 1 (независимость не строковое сравнение),
    # пустое «Кто проверял» — код 1 (парсер не берёт соседнюю строку).
    selfjudge_root = os.path.join(base, "selfjudge")
    shutil.copytree(ok_root, selfjudge_root)
    selfjudge_path = os.path.join(selfjudge_root, "workspace", "judge-report-2026-10-20.md")
    selfjudge_text = open(selfjudge_path, encoding="utf-8").read()
    open(selfjudge_path, "w", encoding="utf-8").write(
        selfjudge_text.replace("Кто проверял:** другой агент", "Кто проверял:** сам автор"))
    emptychecker_root = os.path.join(base, "emptychecker")
    shutil.copytree(ok_root, emptychecker_root)
    emptychecker_path = os.path.join(emptychecker_root, "workspace", "judge-report-2026-10-20.md")
    emptychecker_text = open(emptychecker_path, encoding="utf-8").read()
    open(emptychecker_path, "w", encoding="utf-8").write(
        emptychecker_text.replace("Кто проверял:** другой агент", "Кто проверял:**"))

    # «Кто решил: агент» в журнале — код 1: решение принимает человек.
    agent_root = os.path.join(base, "agentdecisions")
    shutil.copytree(ok_root, agent_root)
    agent_path = os.path.join(agent_root, "workspace", "memory", "decisions.md")
    agent_text = open(agent_path, encoding="utf-8").read()
    open(agent_path, "w", encoding="utf-8").write(agent_text.replace("| Иван |", "| агент |"))

    # Показ, записанный только в таблицу артефакта, — тоже показ и обязан сойтись
    # с полем «Статус» и строкой-событием.
    table_root = os.path.join(base, "table")
    shutil.copytree(ok_root, table_root)
    table_path = os.path.join(table_root, "workspace", "artifact.md")
    table_text = open(table_path, encoding="utf-8").read()
    table_text = table_text.replace("- **Статус:** показан человеку", "- **Статус:** черновик")
    table_text += "\n| Артефакт | Статус | Кому показан | Дата | Обязательство |\n|---|---|---|---|---|\n| | показан человеку | Иван | 20.10.2026 | |\n"
    open(table_path, "w", encoding="utf-8").write(table_text)

    scenarios = (
        ("корректный комплект", ok_root, 0, None),
        ("испорченные ворота", bad_root, 1, None),
        ("триггер внешней проверки", esc_root, 1, "внешней проверки"),
        ("показ без отчёта судьи", nojudge_root, 1, "судьи"),
        ("артефакт без отчёта ворот", noreport_root, 1, "предвалидации"),
        ("судья — сам автор", selfjudge_root, 1, "сам автор"),
        ("пустое «Кто проверял»", emptychecker_root, 1, "Кто проверял"),
        ("решение записано агентом", agent_root, 1, "Кто решил"),
        ("показ только в таблице", table_root, 1, "показ"),
    )
    failed = []
    for title, root, expected, needle in scenarios:
        run = subprocess.run([sys.executable, __file__, "--root", root], capture_output=True)
        text = run.stdout.decode("utf-8", errors="replace")
        ok = run.returncode == expected and (needle is None or needle in text)
        print("%s: код %d (ожидался %d)%s" % (title, run.returncode, expected,
                                              "" if ok else " — ПРОВАЛ"))
        if not ok:
            failed.append((title, run.returncode, text))
    shutil.rmtree(base, ignore_errors=True)
    if failed:
        print("")
        for title, code, text in failed:
            print("ПРОВАЛ: %s, код %s" % (title, code))
            for line in text.splitlines():
                if line.startswith("НАРУШЕНИЕ") or line.startswith("ИТОГ"):
                    print("  %s" % line)
        print("\nИТОГ: 2 — самопроверка не пройдена")
        return 2
    print("\nИТОГ: 0 — самопроверка пройдена: 0 на корректном комплекте и 1 на каждом нарушении")
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        try:
            sys.exit(self_test())
        except Exception as error:
            print("ИТОГ: 2 — самопроверка не смогла выполниться: %s" % error)
            sys.exit(2)
    try:
        sys.exit(main())
    except Exception as error:
        print("ИТОГ: 2 — проверка не смогла прочитать артефакты: %s" % error)
        sys.exit(2)
