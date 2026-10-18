# Ландшафт аналогов: что подтверждено

**Дата проверки:** 18.10.2026.
**Уровень:** `[внешнее]` — то есть факты для планирования, а не валидация.

**Как проверялось.** Поиск в этой сессии недоступен (эндпоинт отвечает `HTTP 402 Insufficient Balance`), поэтому использованы два прямых способа: проверка существования репозитория через `git ls-remote` и чтение страниц репозиториев через прямые запросы.

## 1. Существование подтверждено

Все десять адресов существуют:

| Репозиторий | Ветвей | Описание подтверждено |
|---|---|---|
| `getagentseal/founder-playbook` | 1 | да |
| `sreshtalluri/mom-test` | 2 | да |
| `AIDevGTM/gtm-cofounder` | 8 | да, лежит у нас сабмодулем |
| `eltntawy/idea-discovery-playbook` | 1 | нет |
| `ANVEAI/idea-hunt-skill` | 1 | да |
| `nateherkai/AIS-OS` | 1 | да |
| `Product-nomad/idea-incubator` | 1 | нет |
| `sujalmanpara/harness-engine` | 1 | нет |
| `netresearch/agent-harness-skill` | 2 | нет |
| `ata-akhunzhanov/hypolab` | 1 | нет |

## 2. Что подтверждено описаниями

- **`getagentseal/founder-playbook`** — «15 proven business books distilled into AI-native skills. Works with Claude Code, ChatGPT, Gemini, Cursor». То есть 15 книг и четыре агента подтверждаются.
- **`sreshtalluri/mom-test`** — «The Mom Test as installable Claude Code skills: prep, live-coach, and debrief customer conversations into a compounding discovery/evidence base, gate features against it, and practice in a roleplay league». Подтверждаются: база доказательств из разговоров, гейт против новых функций и дополнительно «лига ролевых игр» для тренировки интервью.
- **`ANVEAI/idea-hunt-skill`** — «evidence-first AI business idea discovery & validation. Find a painful, already-paid-for workflow AI can replace — then prove willingness-to-pay before building». Подтверждается: поиск уже оплачиваемого ручного процесса и доказательство готовности платить до сборки.
- **`nateherkai/AIS-OS`** — «AI Operating System starter kit for Claude Code and Codex. **Five skills: /onboard, /audit, /link, /level-up, and /3d-brain.** Includes the Three Ms framework».

## 3. Расхождение с присланным текстом

Присланный текст утверждал, что в `AIS-OS` шесть навыков и среди них `/grill-me` — контекстное интервью строго по одному вопросу. **Описание репозитория говорит о пяти навыках:** `/onboard`, `/audit`, `/link`, `/level-up`, `/3d-brain`. Навыка `/grill-me` в описании нет.

Значение: механика «по одному вопросу за раз» у них, возможно, есть внутри `/onboard`, но как отдельный навык она не подтверждена. Ссылаться на неё в выступлении как на факт нельзя.

## 4. Что осталось непроверенным

- Внутреннее устройство всех репозиториев: деревья решений, файл `integration.md` с конфликтами книг, скоринговые чек-листы, жизненный цикл статусов в YAML, скрипт `verify-harness.sh`.
- Утверждение «gtm-cofounder стал #1 Product of the Day на Product Hunt». В его README виден значок top-post за день, но конкретное первое место не подтверждено.
- Статьи про Harness Engineering, на которые ссылается текст.
- Существование `PersonaTwin` как отдельного проекта: владелец не назван.

## 5. Что это значит для позиционирования

**Гипотеза, требующая проверки, а не факт:** ни один из перечисленных проектов не соединяет три вещи в одну цепочку — личную телеметрию и снятие рутины, фильтр ниши по отсутствию автоматической метрики, и сборку артефакта-предлога ради доступа к живому эксперту.

Проверить это можно только чтением их навыков. Пока формулировка для стрима должна звучать осторожно: «я не нашёл готового решения, которое делает все три шага», а не «такого не существует».

## 6. Что с этим делать дальше

1. Склонировать два-три самых близких репозитория в отдельную папку и прочитать их навыки: `getagentseal/founder-playbook` (конфликты между книгами), `nateherkai/AIS-OS` (интервью владельца), `sreshtalluri/mom-test` (база доказательств и гейт).
2. Выписать конкретные приёмы, которые сильнее наших, и внедрить их в навыки 01–05.
3. После этого уточнить позиционирование: не «у нас такого нет», а «вот что берём у них, вот что добавляем своего».
