#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка структуры запросов: каждый собран по шаблону и самостоятелен.

Зачем: запрос уходит внешней модели без нас. Если в нём нет границ, контракта
или структуры ответа — модель отвечает как хочет, и ответ некуда девать.
Если запрос ссылается на другой запрос — он не самостоятелен.

Что проверяет каждый файл в `internal/draft/requests/` (кроме README):

1. Пять обязательных полей шапки: идентификатор, дата, каналы, куда писать ответ, число вопросов.
2. Шесть разделов шаблона в правильном порядке.
3. Идентификатор в шапке совпадает с именем файла.
4. Вопросы пронумерованы подряд от `Q1.1`, их не больше шести.
5. Нет ссылок на другие запросы: запрос обязан быть самостоятельным.

Коды возврата: 0 — все запросы по шаблону; 1 — есть отступления; 2 — нечего проверять.
"""

import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ_DIR = os.path.join(ROOT, "internal", "draft", "requests")
ARCH_DIR = os.path.join(REQ_DIR, "archive")
RESP_DIR = os.path.join(ROOT, "internal", "draft", "responses")
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


def main():
    if not os.path.isdir(os.path.join(ROOT, "internal")):
        print("РЕЖИМ ПОЛЬЗОВАТЕЛЯ: папки internal/ нет — структура запросов проекта не проверяется")
        print("\nИТОГ: 0 — проверять нечего")
        return 0

    if not os.path.isdir(REQ_DIR):
        print("ИТОГ: 2 — нет папки запросов: %s" % REQ_DIR)
        return 2

    paths = [os.path.join(REQ_DIR, f) for f in sorted(os.listdir(REQ_DIR)) if f.endswith(".md") and f != "README.md"]
    if os.path.isdir(ARCH_DIR):
        paths += [os.path.join(ARCH_DIR, f) for f in sorted(os.listdir(ARCH_DIR)) if f.endswith(".md") and f != "README.md"]
    if not paths:
        print("ИТОГ: 2 — в папке запросов нет ни одного файла")
        return 2

    problems = []
    for path in paths:
        name = os.path.basename(path)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()

        for field in FIELDS:
            if field not in text:
                problems.append("%s: нет поля шапки «%s»" % (name, field))

        if os.path.dirname(path) == REQ_DIR and "**Категория:**" not in text:
            problems.append(
                "%s: нет поля шапки «**Категория:**» — укажи `быстрая` или `дип`" % name
            )

        for section in SECTIONS:
            if section not in text:
                problems.append("%s: нет раздела «%s»" % (name, section))

        own = name[:-3]
        declared = re.search(r"\*\*Идентификатор:\*\*\s*`([^`]+)`", text)
        if declared:
            short = declared.group(1).split(" ")[0]
            if short != own:
                problems.append("%s: идентификатор в шапке «%s» не совпадает с именем файла" % (name, short))

        if os.path.dirname(path) == REQ_DIR:
            import glob as _glob
            answers = _glob.glob(os.path.join(RESP_DIR, own + ".*")) \
                + _glob.glob(os.path.join(RESP_DIR, "inbox", own + ".*"))
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

    print("проверено запросов: %d" % len(paths))
    for line in problems:
        print("СТРУКТУРА: %s" % line)

    if problems:
        print("\nИТОГ: 1 — %d отступлений от шаблона" % len(problems))
        return 1
    print("\nИТОГ: 0 — все запросы собраны по шаблону и самостоятельны")
    return 0


if __name__ == "__main__":
    sys.exit(main())
