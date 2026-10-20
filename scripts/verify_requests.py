#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка структуры запросов: каждый собран по шаблону и самостоятелен.

Зачем: запрос уходит внешней модели без нас. Если в нём нет границ, контракта
или структуры ответа — модель отвечает как хочет, и ответ некуда девать.
Если запрос ссылается на другой запрос — он не самостоятелен.

Что проверяет, в двух слоях (пользователь и проект):

1. Пять обязательных полей шапки: идентификатор, дата, каналы, куда писать ответ, число вопросов.
2. Шесть разделов шаблона в правильном порядке.
3. Идентификатор в шапке совпадает с именем файла.
4. Вопросы пронумерованы подряд от `Q1.1`, их не больше шести.
5. Нет ссылок на другие запросы: запрос обязан быть самостоятельным.
6. У каждого запроса в корне есть заготовка ответа; закрытый запрос в корне — код 1.

Слои: проект — `internal/draft/requests` + `internal/draft/responses`; человек —
`workspace/requests` + `workspace/responses`. Если папок человека нет, слой
пропускается; если нет ни одного слоя — «проверять нечего» с кодом 0.

Чего не проверяет: смысл вопросов, качество ответов (это `verify_research.py`),
содержимое архива по существу. Не проверяет, что человек действительно отправил
запрос: это внешний факт, доступный только человеку.

Коды возврата: 0 — все запросы по шаблону; 1 — есть отступления; 2 — сломана
декларация (нет папок проекта при живом internal/).
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
INTERNAL = os.path.join(ROOT, "internal")
LAYERS = (
    ("проект", os.path.join(INTERNAL, "draft", "requests"), os.path.join(INTERNAL, "draft", "responses")),
    ("человек", os.path.join(ROOT, "workspace", "requests"), os.path.join(ROOT, "workspace", "responses")),
)
FIELDS = ("**Идентификатор:**", "**Дата:**", "**Каналы:**", "**Ответ писать в:**", "**Вопросов:**", "**Состояние:**")
SECTIONS = (
    "## 1. Границы",
    "## 2. Вопросы",
    "## 3. Контракт формата",
    "## 4. Структура ответа",
    "## 5. Белые пятна",
    "## 6. Параллельные каналы",
)
MAX_QUESTIONS = 6
Q_HEAD = re.compile(r"^### (Q1\.(\d+))\.", re.MULTILINE)
ANY_REQ = re.compile(r"\breq_\d[0-9a-z_]*")


def check_request(path, req_dir, resp_dir, problems):
    name = os.path.basename(path)
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    in_root = os.path.dirname(path) == req_dir

    for field in FIELDS:
        if field not in text:
            problems.append("%s: нет поля шапки «%s»" % (name, field))

    if in_root and "**Категория:**" not in text:
        problems.append("%s: нет поля шапки «**Категория:**» — укажи `быстрая` или `дип`" % name)

    for section in SECTIONS:
        if section not in text:
            problems.append("%s: нет раздела «%s»" % (name, section))

    own = name[:-3]
    declared = re.search(r"\*\*Идентификатор:\*\*\s*`([^`]+)`", text)
    if declared:
        short = declared.group(1).split(" ")[0]
        if short != own:
            problems.append("%s: идентификатор в шапке «%s» не совпадает с именем файла" % (name, short))

    if in_root:
        answers = glob.glob(os.path.join(resp_dir, own + ".*")) \
            + glob.glob(os.path.join(resp_dir, "inbox", own + ".*"))
        if not answers:
            problems.append(
                "%s: нет пары — заготовка ответа не создана (AGENTS §4: пара до отправки)" % name
            )
        for answer_path in answers:
            if not answer_path.endswith(".md"):
                continue
            with open(answer_path, "r", encoding="utf-8", errors="replace") as handle:
                answer_text = handle.read()
            status = re.search(r"Статус обработки:?\**\s*([^\n]*)", answer_text)
            status_text = status.group(1).lower() if status else ""
            if status_text.startswith("принят") or status_text.startswith("отклон"):
                problems.append(
                    "%s: закрытый запрос остался в корне — запусти python scripts/archive_requests.py" % name
                )

    q_section = re.search(r"##\s*2\.\s*Вопросы(.*?)##\s*3\.", text, re.S)
    body = q_section.group(1) if q_section else ""
    ids = Q_HEAD.findall(body)
    numbers = [int(n) for _qid, n in ids]
    if not numbers:
        problems.append("%s: ни одного вопроса вида «### Q1.N»" % name)
    else:
        if len(numbers) > MAX_QUESTIONS:
            problems.append("%s: вопросов %d, предел %d — нарежь пакет" % (name, len(numbers), MAX_QUESTIONS))
        expected = list(range(1, len(numbers) + 1))
        if numbers != expected:
            problems.append(
                "%s: нумерация вопросов должна идти подряд от Q1.1, сейчас %s"
                % (name, ", ".join("Q1.%d" % n for n in numbers))
            )

    foreign = set(ANY_REQ.findall(text)) - {own, "request"}
    if foreign:
        problems.append("%s: ссылается на другие запросы (%s) — запрос обязан быть самостоятельным" % (name, ", ".join(sorted(foreign))))


def main():
    problems = []
    checked = []
    for label, req_dir, resp_dir in LAYERS:
        if not os.path.isdir(req_dir):
            if label == "проект" and os.path.isdir(INTERNAL):
                print("ИТОГ: 2 — нет папки запросов проекта: %s" % req_dir)
                return 2
            continue
        paths = [os.path.join(req_dir, f) for f in sorted(os.listdir(req_dir)) if f.endswith(".md") and f != "README.md"]
        arch_dir = os.path.join(req_dir, "archive")
        if os.path.isdir(arch_dir):
            paths += [os.path.join(arch_dir, f) for f in sorted(os.listdir(arch_dir)) if f.endswith(".md") and f != "README.md"]
        for path in paths:
            before = len(problems)
            check_request(path, req_dir, resp_dir, problems)
            if len(problems) > before:
                for index in range(before, len(problems)):
                    problems[index] = "[%s] %s" % (label, problems[index])
        checked.append((label, len(paths)))

    if not checked:
        print("ИТОГ: 0 — проверять нечего: ни у проекта, ни у человека нет папок запросов")
        return 0

    print("проверено запросов: %s" % ", ".join("%s %d" % (label, count) for label, count in checked))
    for line in problems:
        print("СТРУКТУРА: %s" % line)

    if problems:
        print("\nИТОГ: 1 — %d отступлений от шаблона" % len(problems))
        return 1
    print("\nИТОГ: 0 — все запросы собраны по шаблону и самостоятельны")
    return 0


if __name__ == "__main__":
    sys.exit(main())
