# AIS-OS: приёмы

**Источник:** `D:\github\ai_tech\pres\research\nateherkai-AIS-OS` (MIT, © 2026 Nate Herk), только чтение.
**Метод:** прочитаны README, корневые `AGENTS.md` / `aios-intake.md` / `connections.md` / `decisions/log.md` / `EXPANSIONS.md`, все `SKILL.md` и справочники пяти навыков, `rubric.md`, `history.md`, `compatibility.md`, `references/3ms-framework.md`. Не читались: `.git`, `docs/media`, `assets` 3d-brain, `serve.mjs`, бандлы.
**О копиях навыков:** навыки лежат дважды — `.claude/skills/` (авторский источник, README:121) и `.agents/skills/` (копия для Codex). Проверено хешами: файлы побайтово совпадают, кроме `level-up/SKILL.md:36`, где различается только имя папки в тексте. Ниже ссылки на `.claude/`, то есть на источник.
**Чего в репозитории нет физически:** папки `context/` и `archives/` пусты (только `.gitkeep`); `brainstorms/` и `audits/` не созданы и заранее стоят в [.gitignore:8–9](internal/research/nateherkai-AIS-OS/.gitignore#L8-L9); `apps/3d-brain/` создаётся только при запуске навыка ([README.md:109](internal/research/nateherkai-AIS-OS/README.md#L109)). То есть все файлы состояния описаны, но в поставке их нет — они появляются на первом запуске.

---

## 1. Навык onboard: вопросы и порядок

**Сколько.** Ровно 7, потолок жёсткий: заголовок «The interview (7 questions, hard cap)» ([onboard/SKILL.md:33](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L33)), правило «The 7-question cap is non-negotiable. Don't add Q8 in conversation» ([onboard/SKILL.md:96](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L96)), и то же в шапке опросника «Hard cap: 7 questions. Each answerable in under 60 seconds» ([aios-intake.md:5](internal/research/nateherkai-AIS-OS/aios-intake.md#L5)).

**Порядок и логика.** Не «анкета», а лестница от личности к боли, каждый вопрос привязан к будущему файлу или домену:

| № | Вопрос | Зачем в системе |
|---|---|---|
| Q1 | кто вы, что продаёте, кому | `about-me.md`, `about-business.md`, блок «Knowledge base» в мануале |
| Q2 | вставьте 1–2 своих текста | `references/voice.md` |
| Q3 | 2–3 приоритета на 90 дней | `context/priorities.md` |
| Q4 | куда приходит выручка и где учитывается | домен 1, строки `connections.md` |
| Q5 | где говорите с клиентами, командой, миром | домены 2 и 4 |
| Q6 | где записи встреч, заметки, документы | домены 6 и 7 |
| Q7 | какая задача съедает неделю и где ведёте работу | `top_pain` для `/level-up` + домен 5 |

Источник: [onboard/SKILL.md:37–60](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L37-L60). Ключевое: **каждый вопрос заранее знает, в какое поле он ляжет**, и Q7 заранее объявлен входом для другого навыка (:60).

**По одному.** «Ask one at a time. Write each answer into `aios-intake.md` as you go (so the user can resume if interrupted)» ([onboard/SKILL.md:35](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L35)).

**Готовых вариантов ответа нет.** Все семь вопросов открытые, вариантов не предлагают. У нас есть, у них нет. Вместо вариантов у них три других приёма:
- **Q2 вместо вопроса — запрет.** Сэмплы голоса нельзя печатать в чате, только вставлять сырыми, с готовым текстом отказа: «Stop — paste it raw… This is the one rule I can't bend» ([onboard/SKILL.md:41–45](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L41-L45)), обоснование — «chat-shaped samples are worse than no samples (voice contamination)» ([aios-intake.md:21](internal/research/nateherkai-AIS-OS/aios-intake.md#L21)).
- **Q3 с дожимом.** «Push back if they say "grow my business" — make them name a number, a deadline, or a deliverable» ([onboard/SKILL.md:48](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L48)).
- **Домен выводится, а не спрашивается:** «Domain 3 (Calendar) is auto-inferred from Q5: Gmail → Google Cal; Outlook → Outlook Cal. Confirm in Step 3» ([onboard/SKILL.md:62](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L62)). Вывели → показали в собранном файле → человек поправит, если что.

**Как решает, что опрос закончен — по файлу, а не по чату.** Читается `aios-intake.md` и сравнивается с плейсхолдером `[Your answer here]`, дальше три ветки ([onboard/SKILL.md:27–31](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L27-L31)):
- всё заполнено → интервью не проводится вообще, сразу сборка;
- часть заполнена → **один вопрос с выбором**: «I see Q1, Q3, Q4 are answered. Want to fill the rest now, or scaffold from what's there?» Their call (:30);
- ничего не заполнено → интервью.

Это самый переносимый механизм в навыке: состояние входа определяет режим, а не память агента о разговоре.

**Закрытие.** Сборка файлов одним пакетом без промежуточных подтверждений («After Step 2 ends, write Step 3 files in a single batch. No multi-turn confirmation», [onboard/SKILL.md:98](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L98)); финальный экран ровно три строки и явно «Not a menu» ([onboard/SKILL.md:77–85](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L77-L85), :100).

**Идемпотентность.** Повторный запуск не спрашивает отвеченное, оригиналы уносит в `archives/intake-{YYYY-MM-DD-HHMM}/` ([onboard/SKILL.md:66](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L66), :99). У нас есть, у них похоже (обновление состояния после шага): у них добавлена страховка «бэкап перед перезаписью».

**Границы дня 1.** «No `.env` writes. Don't ask for API keys on Day 1» ([onboard/SKILL.md:103](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L103)); «No extra skills generated» ([onboard/SKILL.md:101](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L101)).

**Самопроверка внутри навыка.** В конце файла — три теста приёмки: cold-test (ответ на закрывающий промпт обязан цитировать Q1+Q3+Q7, «Generic = fail»), идемпотентность, отказ на печатный сэмпл ([onboard/SKILL.md:105–109](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L105-L109)). У нас таких блоков в навыках нет.

---

## 2. Файлы состояния

| Файл | Что внутри | Где описано |
|---|---|---|
| `aios-intake.md` | единственный источник правды: 7 вопросов и ответы, плейсхолдер `[Your answer here]`; правится вручную и перечитывается повторным запуском | [aios-intake.md:1–5](internal/research/nateherkai-AIS-OS/aios-intake.md#L1-L5) |
| `context/about-me.md` | личность, роль + `top_pain` | [onboard/SKILL.md:68](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L68) |
| `context/about-business.md` | оффер, ICP, модель выручки | :69 |
| `context/priorities.md` | нумерованный список приоритетов на 90 дней, одна строка на приоритет | :70 |
| `references/voice.md` | сэмплы дословно + короткая шапка «Match this register when drafting; don't fake voice on external content without showing me first» | :71 |
| `connections.md` | реестр из 7 строк: `Domain / Tool / Mechanism / Auth / Last checked`; значения механизма перечислены явно: `mcp`, `script`, `export`, `key+ref`, `not yet connected` | [connections.md:5–15](internal/research/nateherkai-AIS-OS/connections.md#L5-L15) |
| `AGENTS.md` / `CLAUDE.md` | мануалы с плейсхолдерами `{{...}}`, заполняются на онбординге; обязаны обновляться парой | [AGENTS.md:1–5](internal/research/nateherkai-AIS-OS/AGENTS.md#L1-L5), [onboard/SKILL.md:73](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L73) |
| `decisions/log.md` | append-only, формат записи: `Decision / Why / Alternatives considered / Owner` | [decisions/log.md:5–17](internal/research/nateherkai-AIS-OS/decisions/log.md#L5-L17) |
| `brainstorms/{YYYY-MM-DD}-{topic-slug}.md` | файл-захват интервью `/grill-me`, создаётся **до** первого вопроса | [grill-me/SKILL.md:20–25](internal/research/nateherkai-AIS-OS/.claude/skills/grill-me/SKILL.md#L20-L25) |
| `audits/audit-YYYY-MM-DD-HHMMSS-<suffix>.md` | отчёт аудита с YAML-шапкой: `run_id`, `project_root`, `rubric_version`, `previous_reports`, `scores`, `scores_comparable` | [history.md:47](internal/research/nateherkai-AIS-OS/.claude/skills/audit/history.md#L47), [templates/report.md:1–21](internal/research/nateherkai-AIS-OS/.claude/skills/audit/templates/report.md#L1-L21) |
| `archives/` | «Old stuff. Don't delete. Move here» | [README.md:151](internal/research/nateherkai-AIS-OS/README.md#L151), [EXPANSIONS.md:17](internal/research/nateherkai-AIS-OS/EXPANSIONS.md#L17) |

**Три приёма, которых у нас нет в таком виде:**

1. **Реестр соединений со столбцом свежести.** `connections.md` — не список ссылок, а таблица с `Mechanism` и `Last checked`, которую читает аудит ([connections.md:3](internal/research/nateherkai-AIS-OS/connections.md#L3)).
2. **Явная граница приватности через `.gitignore`.** `audits/` и `brainstorms/` не коммитятся, потому что содержат контекст человека ([.gitignore:8–9](internal/research/nateherkai-AIS-OS/.gitignore#L8-L9), [README.md:89](internal/research/nateherkai-AIS-OS/README.md#L89), :93). У нас это правило записано словами в `AGENTS.md:104`, у них — механизмом.
3. **Файл-захват как обязательный артефакт интервью**, а не побочный результат: «The file, not your context, is the source of truth» ([grill-me/SKILL.md:12](internal/research/nateherkai-AIS-OS/.claude/skills/grill-me/SKILL.md#L12)).

---

## 3. Правило «сначала прочитать»

Отдельной канонической формулировки «не спрашивай то, что можно прочитать» в корневом мануале нет. Правило разложено на четыре места, и все они — про навыки, не про корень:

1. **Самая сильная формулировка — в `/grill-me`:** «If a question can be answered by **exploring the codebase or reading a file/doc**, do that instead of asking. If the user hands you a doc (e.g. a Google Doc), read it and only surface what's net-new» ([grill-me/SKILL.md:42](internal/research/nateherkai-AIS-OS/.claude/skills/grill-me/SKILL.md#L42)). Ключевое добавление к нашей формулировке — **«only surface what's net-new»**: прочитанное не пересказывается, а показывается только прирост.
2. «Reuse facts already supplied; ask about gaps, changes, decisions, and tradeoffs» ([grill-me/SKILL.md:16](internal/research/nateherkai-AIS-OS/.claude/skills/grill-me/SKILL.md#L16)).
3. «Populate only answers explicitly supported by existing sources, with references; leave unknowns for the interview» ([onboard/SKILL.md:23](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L23)) — читать можно и нужно, но записывать только то, что источник действительно подтверждает, со ссылкой.
4. «Ask only for information unavailable in the existing sources» ([level-up/SKILL.md:29](internal/research/nateherkai-AIS-OS/.claude/skills/level-up/SKILL.md#L29)).

**У нас есть, у них похоже, но у нас жёстче:** наш гейт 1 запрещает спрашивать и требует оформить вывод на подтверждение ([AGENTS.md:68–69](AGENTS.md#L68-L69)), а у них это мягкое «сделай сам вместо вопроса» без запрета и без формы подтверждения. **Плюс у них есть механизм, которого у нас нет:** вывод, сделанный из файлов, нельзя сохранить как ответ человека — «do not lead the user with invented facts or save your inference as their answer» ([grill-me/SKILL.md:39](internal/research/nateherkai-AIS-OS/.claude/skills/grill-me/SKILL.md#L39)).

---

## 4. Навык audit

**Что считается доказательством.** Пять классов на каждую находку: **verified, documented but unverified, missing, stale, conflicting** — и к каждой обязателен «a file/line, source URL, or dated run reference» ([audit/SKILL.md:21](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L21)). Явные запреты-заменители доказательства:
- «A folder, installed skill, API key, or confident claim is not proof of a working system» ([audit/SKILL.md:8](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L8));
- «File modification times and last-checked labels alone do not prove a successful refresh or execution» ([audit/SKILL.md:21](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L21));
- «A configured MCP or `.env` key does not establish authentication» ([audit/SKILL.md:51](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L51));
- «A skill named `daily-*`, a template, or recently edited files does not establish cadence» ([audit/SKILL.md:55](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L55));
- «Unfilled template placeholders do not count» ([audit/SKILL.md:19](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L19));
- «Never award full points because there was no time to check» ([audit/SKILL.md:22](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L22)).

**Как проверяют факты — пять проб на маршрут.** Фиксированный набор из пяти вопросов к системе («что за бизнес и что важно сейчас», «где авторитетный текущий приоритет и как это проверить», «где последний артефакт и следующий шаг проекта», «где прошлое решение и его источник», «где внешний первоисточник и как он достаётся»), и на каждую пробу обязательный протокол: вопрос → какой маршрут попробовали → какой источник → результат в одном из трёх состояний: **direct / only by fallback search / not found** ([audit/SKILL.md:30–38](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L30-L38)). Ключевая мысль: «A broad search can recover an answer, but it does not prove the declared route works» (:38).

**Счёт.** Рубрика v2: 4 «C» по 25, пять критериев в каждом по 5 баллов, **только 0 / 1 / 3 / 5, без интерполяции** ([rubric.md:5](internal/research/nateherkai-AIS-OS/.claude/skills/audit/rubric.md#L5)). Дальше **гейты и потолки**: если пробы не вытащили цель или авторитетный приоритет — Context режется до 10; ручной режим без автоматического триггера — Cadence не выше 10; любая C ниже 10 → итог не выше 49, ниже 15 → 69, ниже 20 → 84 ([rubric.md:63–72](internal/research/nateherkai-AIS-OS/.claude/skills/audit/rubric.md#L63-L72)), плюс таблица стадий «Unproven → Maintained» ([rubric.md:74–80](internal/research/nateherkai-AIS-OS/.claude/skills/audit/rubric.md#L74-L80)). Смысл потолков прямой: «These gates intentionally prevent a large skill library from compensating for absent connections or cadence» ([rubric.md:82](internal/research/nateherkai-AIS-OS/.claude/skills/audit/rubric.md#L82)).

**История находок.** У каждой находки стабильный ID `AIOS-<run-id>-01`, который переносится между прогонами; шесть статусов с определением, что считается доказательством для каждого: `New / Still open / Resolved / Reopened / Not rechecked / No longer applicable` ([history.md:13–26](internal/research/nateherkai-AIS-OS/.claude/skills/audit/history.md#L13-L26)). Особенно жёстко: «A proposed edit, changed timestamp, installed copy, or self-reported success alone does not establish resolution» (:23); «An item omitted from the three recommended actions is not closed» (:17); «A previously resolved finding not checked today is `Not rechecked` … not a reopened defect» (:28); «No prior comparable report means a new baseline, not an invented improvement» ([audit/SKILL.md:76](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L76)).

**Честность отчёта.** Сохранённый отчёт перечитывается и сверяется: «Read back the saved report… Never say saved without confirming it» ([audit/SKILL.md:78](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L78), [history.md:50](internal/research/nateherkai-AIS-OS/.claude/skills/audit/history.md#L50)). Не удалось записать — «say **report not saved**, return the report in chat» ([history.md:52](internal/research/nateherkai-AIS-OS/.claude/skills/audit/history.md#L52)). Прерванный прогон сохраняется как `report_status: partial` с `null` вместо баллов (:51). Аудит только читает систему, единственная запись — новый отчёт ([audit/SKILL.md:96](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L96)).

**Калибровка как защита от самообмана.** Отдельный список проверок: свежий клон обязан остаться «Unproven», «presence cannot earn full Capabilities or Cadence», 25+25+25+10 = 85 сырых, но 69 итог ([rubric.md:84–91](internal/research/nateherkai-AIS-OS/.claude/skills/audit/rubric.md#L84-L91), [history.md:56–65](internal/research/nateherkai-AIS-OS/.claude/skills/audit/history.md#L56-L65)).

---

## 5. Three Ms framework

Файл: [references/3ms-framework.md](internal/research/nateherkai-AIS-OS/references/3ms-framework.md), 236 строк, три слоя.

**Layer 1 — Mindset (как думать)**, :22–60: Default Shift («to what extent can AI be leveraged here?», :32), Function Breakdown («You don't automate your whole job. You automate one tiny piece», :42), Curiosity Rule (не принимать вывод без «почему», иначе «dark code» — «you've built a liability, not an asset», :52), Expect the Dip (просадка ~20% на 1–2 недели, :58).

**Layer 2 — Method (как решать)**, :64–137 — это и есть рабочая машина:
1. **Find the Constraint** — два вопроса: «If 500 new clients showed up tomorrow, what would break first?» и «What would give you 500 more clients tomorrow?» (:72–74).
2. **EAD: Eliminate → Automate → Delegate**, строго в этом порядке. Eliminate: «If nobody would notice it disappeared, kill it. Don't automate waste» (:82). Automate: **60/30/10** — ~60% полная автоматизация, ~30% с ревью человеком, ~10% руками (:84–89), с прямым выводом «Full automation is rarely the goal» (:89). Delegate: если не тянет 60/30/10 — отдать человеку (:91). Итог: «nothing stays as-is» (:93).
3. **Map the Process** — пять элементов: Trigger, Data Sources, Data Transformations, Decision Points, Destination (:97–103), с правилом-стопом: «if you can't explain it to a person, you can't explain it to an AI» (:105).
4. **Autonomy Spectrum L0–L4** (Manual / Suggested / Drafted / Supervised / Autonomous), «default to the LOWEST level that works» (:109–119), «Workflows beat agents. If a decision doesn't HAVE to be made by AI, don't let AI make it» (:121).
5. **Tie It to a KPI** — три корзины (больше клиентов / дороже клиент / меньше затрат) плюс конкретная метрика; «Because it's cool» — не бизнес-кейс (:127–137).

**Layer 3 — Machine (как строить и держать)**, :141–205: Lego Principle (мельчайшие блоки, сначала шаги без ИИ, :147–153), Assembly Line (не строить универсала, :155–159), Validation Chain («Do NOT build the whole pipeline and test end-to-end», :161–165), Iteration Mindset (:167–171), **Bike Method** — четыре фазы: Training wheels (руками, смотрим) → Guided (черновик, не отправка) → Watched (мониторим) → Hands-off (:175–186), **Intern Rule** (своя личность, read-only по умолчанию, не притворяется вами, полный аудит-трейл, минимальные права, :188–199), **Kill Switch** (если дороже в поддержке, чем экономит — сносить, :201–205).

Сверху три принципа: Boring is beautiful; детерминированные шаги конечны, ИИ-шаги вечны; fail fast, learn faster (:209–215).

**Как применяется.** Не как текст, а как сценарий навыка `/level-up`: Phase 1 — пять вопросов Mindset ([level-up/SKILL.md:53–59](internal/research/nateherkai-AIS-OS/.claude/skills/level-up/SKILL.md#L53-L59)), Phase 2 — пять шагов Method с остановками (:70–105), Phase 3 — выбор способа сборки (:111–118). Рамка = чеклист, а не глава книги.

**Правовая оговорка, важная для переноса.** «The Three Ms of AI™» и «The Four Cs of an AI OS™» — товарные знаки автора; код под MIT, рамки — нет ([README.md:170–174](internal/research/nateherkai-AIS-OS/README.md#L170-L174), [AGENTS.md:11](internal/research/nateherkai-AIS-OS/AGENTS.md#L11)). Переносить можно механику (EAD, 60/30/10, L0–L4, Bike Method), но не названия и не текст под своим именем.

---

## 6. Корневой AGENTS.md

Файл: [AGENTS.md](internal/research/nateherkai-AIS-OS/AGENTS.md), 53 строки, и он **не правило-файл, а файл-настройка**. Содержимое:
- плейсхолдеры `{{Your Name}}`, `{{stated priority}}` (:1, :3) и блоки, которые заполняет онбординг (:36, :44);
- требование парности: «`AGENTS.md` and `CLAUDE.md` share the same standing guidance. Update both together» (:5);
- список навыков и карта папок (:13–32);
- голос: «Casual but professional. Short sentences. No em dashes… Don't fake my voice on external content… without showing me a draft first» (:40);
- шесть поведенческих правил (:48–53), из них три содержательных: логировать решения через `decisions/log.md` (:51), «When you spot a manual task I'm doing 3+ times, surface it next time `/level-up` runs» (:52), Default Shift как обязательный вопрос к новой задаче (:53).

**Гейтов и стоп-условий в корневом мануале нет.** Ни одного «нельзя», ни одного условия выхода, ни одного лимита вопросов. Всё принуждение живёт в двух других местах:
1. **В тексте навыков** — жёсткие потолки и правила (7 вопросов, чекпоинт после каждого ответа, «stop» при отсутствии метрики).
2. **В структуре оценки** — потолки рубрики: любая «C» ниже 10 режет итог до 49, и это блокирует «набрать баллы навыками» ([rubric.md:63–72](internal/research/nateherkai-AIS-OS/.claude/skills/audit/rubric.md#L63-L72)).

**У нас тут сильнее:** наш корневой [AGENTS.md](AGENTS.md) содержит четыре гейта (:64–80), формулу вопроса (:82–84), запрещённые слова (:84), четыре стоп-условия (:108–115) и маршрутизацию файлов (:86–89). У них корень описывает, *кто ты для человека*, а не *что тебе запрещено*. Их подход даёт переносимость (один и тот же мануал для двух рантаймов), наш — исполняемость.

**Единственный жёсткий элемент у них в корне** — требование синхронизации двух мануалов (:5), продублированное в навыках ([onboard/SKILL.md:21](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L21), [link/SKILL.md:15–16](internal/research/nateherkai-AIS-OS/.claude/skills/link/SKILL.md#L15-L16)) и проверяемое аудитом ([compatibility.md:15–19](internal/research/nateherkai-AIS-OS/.claude/skills/audit/compatibility.md#L15-L19)).

---

## 7. Есть ли grill-me

**Есть.** Лежит в двух местах: [.claude/skills/grill-me/SKILL.md](internal/research/nateherkai-AIS-OS/.claude/skills/grill-me/SKILL.md) (авторский источник) и `.agents/skills/grill-me/SKILL.md` (побайтовая копия для Codex, проверено хешем). Упомянут в [README.md:5](internal/research/nateherkai-AIS-OS/README.md#L5), :81, :93, :119; в [AGENTS.md:17](internal/research/nateherkai-AIS-OS/AGENTS.md#L17); в [EXPANSIONS.md:19](internal/research/nateherkai-AIS-OS/EXPANSIONS.md#L19); в [.gitignore:9](internal/research/nateherkai-AIS-OS/.gitignore#L9) (папка `brainstorms/` под него). Ранее осторожная формулировка README («`/grill-me`, if available») в [audit/SKILL.md:77](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L77) — наследие версии, где навыка ещё не было; в поставке он есть.

**Что он делает и чем отличается от нашего онбординга.** Это не первый опрос, а повторяемое интервью по любой теме, и его главный предмет — не ответы, а **надёжность записи**:

- **Файл создаётся до первого вопроса**: `brainstorms/{YYYY-MM-DD}-{topic-slug}.md`, с заголовком, датой, целью и пустым разделом «Open flags» ([grill-me/SKILL.md:20–25](internal/research/nateherkai-AIS-OS/.claude/skills/grill-me/SKILL.md#L20-L25)). Существующий файл не перезаписывается никогда: коллизия в один день → суффикс, «create exclusively» (:22).
- **Чекпоинт после каждого ответа, до следующего вопроса** (:27–33): дописать запись → при противоречии пометить старую как superseded и связать с исправляющей → **перечитать записанное** → только потом спрашивать дальше. «Never batch multiple answers into one write» (:35). Отдельно: «If saving fails, explain the failure and keep the answer visible in chat; do not claim it was saved or continue collecting answers without a working checkpoint» (:32).
- **Один вопрос за раз**, и для решений — предложенный ответ с пометкой «это предложение», а для фактов о человеке — нейтрально, без подсказки (:39).
- **Три сорта утверждений разделены в файле:** подтверждённое человеком, предположение, вопрос без ответа (:40, структура :48–67).
- **Флаг вместо ступора:** не может ответить → записать «вопрос → кто может ответить» и идти дальше, «Don't stall» (:43).
- **Условие выхода:** человек сказал «хватит» / пауза / ветки закрыты; «Respect an explicit stop immediately; do not add a new question», и в конце предложить бэкстоп полноты «anything we haven't touched?» (:44).
- **Финал:** прочитать захват на противоречия, **не выбирать бизнес-факт за человека** (:70); подтверждённое перенести в канонический файл контекста со ссылкой на дату, предположения оставить помеченными (:71); дать резюме с путём к файлу, списком флагов и точкой возобновления (:74).

Чего в нём нет: вариантов ответа, лимита вопросов, детектора усталости, формулы вопроса. Он может длиться сколько угодно (:44) — это осознанно, потому что выход по «хватит», а не по счётчику.

---

## 8. Что взять в наш репозиторий

По убыванию ценности. Всё — механизмы, не текст.

1. **Чекпоинт после каждого ответа с перечитыванием.** В наш `00-onboarding-interview` добавить правило: после каждого ответа дописать `workspace/profile.md`, перечитать записанное, только потом задавать следующий вопрос; при сбое записи — сказать прямо и не продолжать опрос. Источник: [grill-me/SKILL.md:27–35](internal/research/nateherkai-AIS-OS/.claude/skills/grill-me/SKILL.md#L27-L35). У нас сейчас только «после шага обновить файлы» ([AGENTS.md:50](AGENTS.md#L50)) — этого мало, шаг длиннее одного ответа.
2. **Ветка «часть профиля заполнена» с одним вопросом-выбором.** Перед интервью читать целевой файл; если часть блоков заполнена — «вижу, занятие и узкое место есть. Дозаполнить остальное или собирать из этого?». Источник: [onboard/SKILL.md:27–31](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L27-L31). Сейчас наш навык умеет только «профиль устарел → новый опрос».
3. **Запрет на «вывод как ответ человека».** Наш гейт 1 разрешает вывести и подтвердить, но не запрещает потом записать догадку как его слова. Их формулировка: «do not lead the user with invented facts or save your inference as their answer» ([grill-me/SKILL.md:39](internal/research/nateherkai-AIS-OS/.claude/skills/grill-me/SKILL.md#L39)). Дописать в шаг 0 нашего навыка.
4. **Реестр соединений со свежестью.** Завести `workspace/connections.md` по образцу [connections.md:5–15](internal/research/nateherkai-AIS-OS/connections.md#L5-L15): домен / инструмент / механизм / доступ / `проверено когда`. У нас `templates/research-queue.md` фиксирует задания, но нигде не видно, что старо, а что живое.
5. **Навык аудита как отдельный навык.** У нас его нет вообще. Не копировать рубрику целиком (25+25+25+25 не про наш кит), а взять три вещи: пять проб «вопрос → маршрут → результат direct/fallback/not found» ([audit/SKILL.md:30–38](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L30-L38)); классы находок verified/unverified/missing/stale/conflicting (:21); журнал находок со стабильными ID и статусами ([history.md:13–26](internal/research/nateherkai-AIS-OS/.claude/skills/audit/history.md#L13-L26)). Плюс правило «отчёт перечитать перед словом сохранено» (:78, [history.md:50](internal/research/nateherkai-AIS-OS/.claude/skills/audit/history.md#L50)).
6. **Флаг-замок в frontmatter артефакта.** Каждый собранный навык получает `bike-method-phase: 1`, и «They can't silently skip manual validation. Phase advances only by explicit edit» ([level-up/SKILL.md:129–135](internal/research/nateherkai-AIS-OS/.claude/skills/level-up/SKILL.md#L129-L135)). Дешёво, переносится в любой наш шаблон, защищает от перехода к автоматизации без ручного прогона.
7. **Стоп-гейт «Eliminate первым».** Перед сборкой артефакта спрашивать «что будет, если просто перестать это делать?»; если ничего не сломается — закрыть как победу, в `workspace/`, а не строить ([level-up/SKILL.md:75](internal/research/nateherkai-AIS-OS/.claude/skills/level-up/SKILL.md#L75), [3ms-framework.md:82](internal/research/nateherkai-AIS-OS/references/3ms-framework.md#L82)). У нашего пайплайна нет шага «а надо ли вообще».
8. **Два стоп-гейта на артефакт:** не можешь объяснить пять элементов процесса человеку — стоп ([level-up/SKILL.md:86](internal/research/nateherkai-AIS-OS/.claude/skills/level-up/SKILL.md#L86)); не можешь назвать корзину и метрику — стоп (:105). Второй прямо ложится к нашему HADI-критерию.
9. **Блок самопроверки в конце навыка** (cold-test / идемпотентность / отказ): [onboard/SKILL.md:105–109](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L105-L109), [level-up/SKILL.md:162–168](internal/research/nateherkai-AIS-OS/.claude/skills/level-up/SKILL.md#L162-L168). У наших трёх навыков таких тестов нет.
10. **Список антипаттернов роста**: не создавать `notes/`, `misc/`, `tmp/`, `inbox/`; не плодить пустые папки; не держать параллельные `decisions.md` и `decisions/log.md` ([EXPANSIONS.md:53–62](internal/research/nateherkai-AIS-OS/EXPANSIONS.md#L53-L62)).

---

## 9. Что у нас уже лучше

1. **Гейты и стоп-условия у нас алгоритмические и в корне.** У них корневой мануал — настройка личности ([AGENTS.md:46–53](internal/research/nateherkai-AIS-OS/AGENTS.md#L46-L53)), гейтов нет ни одного. Наши четыре гейта с первым сработавшим ([AGENTS.md:64–80](AGENTS.md#L64-L80)) и четыре стоп-условия с детектором усталости ([AGENTS.md:108–115](AGENTS.md#L108-L115)) — переносимая механика, которой у них нет. Их выход из интервью — «пока человек не скажет хватит» ([grill-me/SKILL.md:44](internal/research/nateherkai-AIS-OS/.claude/skills/grill-me/SKILL.md#L44)) или жёсткий счётчик 7 без правил на усталость.
2. **Формула вопроса и запрещённые слова.** У нас: якорь в прошлом + действие + 3–4 варианта, до 120 знаков, список запрещённых слов ([AGENTS.md:82–84](AGENTS.md#L82-L84), [SKILL.md:88–99](skills/00-onboarding-interview/SKILL.md#L88-L99)). У них вопросов длины нет, формулировок-шаблонов нет, вариантов ответа нет вообще — Q1 «Who are you, what do you sell, who do you sell it to?» ([onboard/SKILL.md:37](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L37)) человек отвечает как хочет.
3. **Нулевой цикл вместо «нет данных — ставим допущение».** У нас отсутствие данных превращается в первый работающий артефакт через замер ([12_zero_cycle.md](internal/draft/12_zero_cycle.md), [SKILL.md:52–63](skills/00-onboarding-interview/SKILL.md#L52-L63)). У них при незаполненном интейке выбор бинарный: дозаполнить или собирать из того, что есть ([onboard/SKILL.md:30](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L30)); телеметрии и ветки замера нет ни в одном файле.
4. **Маршрутизация вопросов по адресату.** У нас гейт 2 отправляет вопросы про внешний мир в `workspace/research-queue.md` внешнему исследователю ([AGENTS.md:71–73](AGENTS.md#L71-L73), :88). У них роли внешнего исследователя нет; максимум — флаг «кто может ответить» ([grill-me/SKILL.md:43](internal/research/nateherkai-AIS-OS/.claude/skills/grill-me/SKILL.md#L43)) и подсказка «ask a human» внутри навыка. Поиск по репозиторию: слова research/researcher встречаются только как «researched-once-saved-forever» про API-гайды.
5. **Три зоны с разными правами и запрет писать в `templates/`.** У нас зоны и права прописаны таблицей ([AGENTS.md:91–106](AGENTS.md#L91-L106)). У них «не перезаписывать» обеспечено только текстом в навыке («Read-only on `references/3ms-framework.md`», [onboard/SKILL.md:102](internal/research/nateherkai-AIS-OS/.claude/skills/onboard/SKILL.md#L102)) и `.gitignore`; правила «куда агенту писать нельзя» в мануале нет.
6. **Уровень `[рынок]` как единственная валидация.** У них шкала доказательности в аудите измеряет *работоспособность системы*, а не истинность гипотезы, и это прямо оговорено: «This is not an overall usefulness grade» ([audit/SKILL.md:74](internal/research/nateherkai-AIS-OS/.claude/skills/audit/SKILL.md#L74), :8). Наша трёхуровневая шкала с обязательным рынком как единственной валидацией ([AGENTS.md:27–35](AGENTS.md#L27-L35)) отвечает на другой вопрос — «верна ли гипотеза», и в этом смысле сильнее.

---

## Приложение: где записаны два спорных правила

**«Контекст нельзя пропустить».** Ровно одна формулировка на весь репозиторий: «Dependency graph: Context is non-skippable. Connections + Capabilities can build in parallel. Cadence is last — don't automate workflows that don't work manually» ([README.md:70](internal/research/nateherkai-AIS-OS/README.md#L70)). Это строчка в README, в навыках она не продублирована. Механизм принуждения один и косвенный: потолки рубрики — если пробы не вытащили цель и приоритет, Context режется до 10, а любая «C» ниже 10 режет итог до 49 ([rubric.md:65](internal/research/nateherkai-AIS-OS/.claude/skills/audit/rubric.md#L65), :69). То есть «нельзя пропустить» обеспечивается не запретом, а тем, что за пропуск не дадут баллов.

**«Не автоматизируйте воркфлоу, которые не работают вручную».** Тот же [README.md:70](internal/research/nateherkai-AIS-OS/README.md#L70), и там же — единственное место с этой формулировкой. Дальше правило разложено на три исполняемых куска: Bike Method Phase 1 «Run manually first» с замком в frontmatter ([level-up/SKILL.md:129–135](internal/research/nateherkai-AIS-OS/.claude/skills/level-up/SKILL.md#L129-L135), [3ms-framework.md:179](internal/research/nateherkai-AIS-OS/references/3ms-framework.md#L179)); Validation Chain «Do NOT build the whole pipeline and test end-to-end» ([3ms-framework.md:163](internal/research/nateherkai-AIS-OS/references/3ms-framework.md#L163)); и при выборе способа сборки дефолт — самый неавтоматизированный вариант, «User has to explicitly choose more autonomy» ([level-up/SKILL.md:118](internal/research/nateherkai-AIS-OS/.claude/skills/level-up/SKILL.md#L118)).
