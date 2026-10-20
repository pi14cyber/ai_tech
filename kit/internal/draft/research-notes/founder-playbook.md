# founder-playbook: приёмы

**Источник:** `internal/research/getagentseal-founder-playbook` (getagentseal/founder-playbook, коммит `e811e63`, 2026-10-06).
**Дата разбора:** 18.10.2026.
**Уровень:** `[внешнее]` целиком. Разбор не является валидацией наших гипотез.
**Метод:** только чтение файлов; каждый пункт с путём и номерами строк. Ссылки внутри отчёта даны от корня чужого репозитория (`skills/...`, `README.md`, `experiments/...`).

---

## 1. Структура навыков

**Единица поставки.** 16 навыков, у 15 из них пять файлов по схеме прогрессивного раскрытия: `SKILL.md` (вход), `frameworks.md` (глубина), `cases.md` (кейсы книги), `examples.md` (шаблоны), `integration.md` (связи и конфликты) — объявлено в `README.md:96-103`, там же обещана длина `SKILL.md` «~250-500 lines» (`README.md:98`). Фактически разброс 153-463 строки: `skills/mom-test/SKILL.md` 207 строк, `skills/crossing-the-chasm/SKILL.md` 463, `skills/diagnose/SKILL.md` 204.

**Отклонения от собственной схемы** (проверено перечнем файлов):
- `skills/diagnose/` — только `SKILL.md`, вспомогательных файлов нет вообще;
- `skills/influence/` — вместо frameworks/cases/examples лежат `principles.md`, `pre-suasion.md`, `replication-notes.md` плюс `integration.md`;
- `skills/100m-leads/` — добавлены два вне схемы: `lead-getters.md`, `paid-ads.md`.

**Frontmatter.** Только два поля, `name` и `description`, без версии, лицензии и даты: `skills/mom-test/SKILL.md:1-4`, `skills/diagnose/SKILL.md:1-4`. Кавычки вокруг значений непоследовательны: `skills/100m-leads/SKILL.md:2-3` в кавычках, `skills/mom-test/SKILL.md:2-3` без.

**Description работает роутером, а не аннотацией.** Внутри три слоя: назначение, список триггеров живой речью и обязательный отрицательный хвост «NOT for … use X». Примеры: `skills/traction/SKILL.md:3` («NOT for product development (use Lean Startup), not for positioning/messaging (use Obviously Awesome)…»), `skills/lean-startup/SKILL.md:3`, `skills/crossing-the-chasm/SKILL.md:3`, `skills/four-steps/SKILL.md:3`, `skills/storybrand/SKILL.md:3`, `skills/made-to-stick/SKILL.md:3`.

**Обязательная вставка-дисклеймер на шестой строке у всех 16 файлов.** Формулировка одна и та же, с вариацией только у мета-навыка: «This skill is independent analysis and commentary, not a reproduction of the original text… surfaces where frameworks are outdated or incomplete» — `skills/mom-test/SKILL.md:6`, полный список тот же во всех `SKILL.md`; у диагноста своя редакция `skills/diagnose/SKILL.md:6`.

**Порядок разделов не зафиксирован, но набор повторяется.** Из сквозного просмотра заголовков `##`:
- входной фильтр «Should You Use This Skill?» / «When to Use» — `skills/crossing-the-chasm/SKILL.md:13`, `skills/four-steps/SKILL.md:13`, `skills/traction/SKILL.md:13`, `skills/lean-startup/SKILL.md:13`, `skills/obviously-awesome/SKILL.md:13`, `skills/blue-ocean-strategy/SKILL.md:13`; у пяти навыков его нет вовсе (`skills/mom-test/`, `skills/made-to-stick/`, `skills/storybrand/`, `skills/money-models/`, `skills/100m-offers/`);
- дерево решений — `skills/mom-test/SKILL.md:19`, `skills/crossing-the-chasm/SKILL.md:279`, `skills/monetizing-innovation/SKILL.md:117`, `skills/money-models/SKILL.md:112`;
- «Critical Numbers & Rules of Thumb» — `skills/monetizing-innovation/SKILL.md:159`, `skills/crossing-the-chasm/SKILL.md:320`, `skills/four-steps/SKILL.md:412`, `skills/traction/SKILL.md:362`, `skills/spin-selling/SKILL.md:357`;
- ошибки — «Common Mistakes» `skills/100m-offers/SKILL.md:190`, «Common Failure Patterns» `skills/crossing-the-chasm/SKILL.md:338`, «Warning Signs» `skills/100m-leads/SKILL.md:161`;
- признаки успеха — «Success Signals» `skills/100m-offers/SKILL.md:200`, `skills/money-models/SKILL.md:210`;
- границы — «When This Doesn't Apply» `skills/100m-leads/SKILL.md:203`, «When NOT to Use This Skill» `skills/blue-ocean-strategy/SKILL.md:179`;
- закрывающие — «The Big Idea» `skills/spin-selling/SKILL.md:398`, «Supporting Files» `skills/mom-test/SKILL.md:195`.

**Секция «Supporting Files»** — перечень соседних файлов с одной строкой «что внутри»: `skills/mom-test/SKILL.md:197-200`, `skills/made-to-stick/SKILL.md:245-248`. Внутренние ссылки идут с якорями, вплоть до конкретного шага: `skills/100m-offers/SKILL.md:132` → `[frameworks.md](frameworks.md#step-5-trim--stack-value-cost-matrix)`, `skills/crossing-the-chasm/SKILL.md:384`.

---

## 2. Конфликты между книгами

**Файл.** `integration.md` есть у 15 навыков из 16 (нет у `skills/diagnose/`). Заголовок по шаблону «# <Название> - Integration with Other Skills» — `skills/mom-test/integration.md:1`, `skills/blue-ocean-strategy/integration.md:1`.

**Состав не унифицирован, шесть разных имён для одного и того же раздела:**

| Имя раздела | Где |
|---|---|
| Conflicts and Tensions | `skills/mom-test/integration.md:54`, `skills/100m-offers/integration.md:108` |
| Honest Conflicts | `skills/obviously-awesome/integration.md:17`, `skills/blue-ocean-strategy/integration.md:51` |
| Honest Conflicts (Cross-Skill Resolution) | `skills/crossing-the-chasm/integration.md:232` |
| Conflict Resolution (Honest Version) | `skills/spin-selling/integration.md:169` |
| When Skills Appear to Contradict | `skills/monetizing-innovation/integration.md` |
| Honest Conflicts (Real Ones) | `skills/influence/integration.md:16` |

**Микрошаблон одного конфликта жёсткий и переносимый:** `### Conflict N: [утверждение A] vs [утверждение B]` → `**Сторона:**` / `**Reality:**` → `**Resolution:**`. Шесть конфликтов подряд в `skills/100m-offers/integration.md:110-146`; четыре в `skills/mom-test/integration.md:56-87`; в формате без нумерации — `skills/obviously-awesome/integration.md:19-47`. Утверждения сторон подаются от лица авторов: «**Mom Test rule:** …», «**Reality:** …» (`skills/mom-test/integration.md:58-62`), «**Hormozi:** …», «**Reality:** …» (`skills/100m-offers/integration.md:112-113`).

**Пять типов разрешения, все реально присутствуют:**
1. Разные уровни абстракции (стратегия против тактики): `skills/blue-ocean-strategy/integration.md:55`, `skills/obviously-awesome/integration.md:33`.
2. Разные этапы (до/после продукта): `skills/mom-test/integration.md:78`, `skills/100m-offers/integration.md:96`.
3. Одно слово, два смысла: «niche» у Dunford против «niche trap» у BOS — `skills/obviously-awesome/integration.md:21-23`, `skills/blue-ocean-strategy/integration.md:71-73`.
4. Явный решающий тест: «**Test:** Is the segment growing? Does it have shared unmet needs? Could you dominate it?» — `skills/obviously-awesome/integration.md:25`, повтор в `skills/blue-ocean-strategy/integration.md:75`.
5. Признание правоты одного с оговоркой: «Porter is right that … BOS is right that … The simultaneity is real - but only when it flows from reconstructing the value curve» — `skills/blue-ocean-strategy/integration.md:9`.
Отдельно фиксируется «конфликта нет»: `skills/obviously-awesome/integration.md:43`, `:47`, `skills/crossing-the-chasm/integration.md:278`.

**Как цитируются источники.** Атрибуция только по автору и названию книги или навыка; номеров страниц, глав и URL в `integration.md` нет ни одного (проверено поиском по `http`, `p.`, `Ch.`). Единственное указание провенанса цифры на весь корпус: «(Source: the 74% figure is from the Fuji Xerox study, Rackham.)» — `skills/spin-selling/integration.md:136`. Взамен — явная девальвация чисел: «Treat all numerical claims (the 30% premium, the 2x revenue heuristic, the 80-90%/100% threshold) as Moore's heuristics from worked examples, not measured rules» — `skills/crossing-the-chasm/integration.md:307`.

**Карта зависимостей по слоям** — сильный приём, у нас такого нет. `skills/100m-offers/integration.md:165-177`: Discovery → Strategy → Tactical → Influence, и правило выхода наверх: «100m-offers operates at the tactical layer. It assumes higher layers have been resolved. If you're in this skill but the layers above are unclear, go up the stack first» (`:177`). Тот же приём в `skills/money-models/integration.md:142`, `skills/100m-leads/integration.md:197`.

**Мастер-последовательность по фазам** с перечислением навыков внутри каждой: SEARCH / LAUNCH / SCALE — `skills/traction/integration.md:233-257`; своя версия у `skills/lean-startup/integration.md:232`, `skills/four-steps/integration.md:210`, `skills/monetizing-innovation/integration.md:136`.

**Цепочка одного автора** как отдельный блок: «mom-test → 100m-offers → money-models → 100m-leads» со подписями под стрелками (discovery → packaging → monetization → traffic) — `skills/mom-test/integration.md:5-9`, `skills/100m-offers/integration.md:5-9`, развёрнутая версия `skills/money-models/integration.md:3`.

**Запрет стекирования** как прямое правило роутера: «Every diagnosis should output: one primary skill, one secondary skill (optional), and one concrete next action the founder can do this week… If two skills genuinely both apply, sequence them… Never in parallel» — `skills/diagnose/SKILL.md:144-152`.

---

## 3. Раздел «книга устарела»

Раздел есть у всех 15 книжных навыков, но единого шаблона и единого имени нет. Ниже фактические варианты.

**Вариант A. «Modern Relevance (год → 2026)»** с тремя-четырьмя подблоками: где ещё применимо / где ломается / что автор понял неверно.
- `skills/crossing-the-chasm/SKILL.md:354-384`: «When Crossing the Chasm STILL Applies» (`:358`), «Where the Framework BREAKS in 2026» (`:366`), «What Moore Got Wrong (Now Visible)» (`:375`). Пункты лома конкретны, с продуктами: PLG (Slack, Figma, Cursor), open source, network effects, маркетплейсы, AI-модели, чистый консьюмер (`:368-373`).
- `skills/four-steps/SKILL.md:467-494`: «When Four Steps STILL Applies» (`:471`), «Where the Framework Shows Its Age» (`:479`), «What Blank Got Permanently Right» (`:487`) — третий блок важен: он не только ругает, но и отделяет непреходящее.
- `skills/lean-startup/SKILL.md:333`, `skills/traction/SKILL.md:394` — те же блоки.

**Вариант B. «Honest Scope of the Book (Detailed)»** — паспорт источника из шести фиксированных полей: год издания, примеры, эмпирическая база, где сильна, где слаба, коммерческий интерес автора, что брать вперёд: `skills/crossing-the-chasm/integration.md:295-334`. Ядро — `:305-307` («Anecdotes and case studies from Moore's consulting practice. **No statistical validation**») и `:323-328` («Moore founded The Chasm Group consulting firm. The book is partly marketing for that practice»). Короткая версия в `SKILL.md`: `skills/crossing-the-chasm/SKILL.md:454`, `skills/four-steps/SKILL.md:558`, `skills/lean-startup/SKILL.md:367`, `skills/traction/SKILL.md:429`.

**Вариант C. «Scope and Limitations»** из трёх подблоков — что framework делает верно / что устарело / честная оценка: `skills/made-to-stick/SKILL.md:224-241` (`:226` «What This Framework Gets Right», `:233` «What's Dated or Limited», `:240` «The Honest Assessment»); `skills/storybrand/SKILL.md:257-274` (`:266`, `:274`). Внутри — конкретика: «**No digital-native guidance.** Written in 2007, before social media, short-form video, or AI» (`skills/made-to-stick/SKILL.md:234`).

**Вариант D. «Where … Is Showing Age (2026)» + что осталось годным + что считать сомнительным** — три отдельных списка: `skills/blue-ocean-strategy/integration.md:77-84`, `:86-96` (таблица Tool | Status), `:98-103`. Внутри — приём, которого нет больше нигде: обвинение в нефальсифицируемости, «any failure gets reclassified as "not real blue ocean" or "didn't apply correctly"» (`:84`).

**Вариант E. «What's Outdated Since 1988»** — пять пунктов, каждый из которых описывает изменившееся условие рынка, а не «книга старая»: `skills/spin-selling/integration.md:26-58` (покупатель проходит 57-70% пути до контакта, `:32`; inside sales вместо 40-минутных личных визитов, `:38-39`; аутрич автоматизирован, `:43-45`; покупатель пост-доверчивый, `:49-51`; асимметрия информации исчезла, `:55-57`).

**Вариант F. «Critical Caveats (Read First)» — таблица Issue | Status по каждому спорному исследованию**, поставленная в начало файла, до содержания: `skills/influence/SKILL.md:20-38`. Девять строк, у каждой — вердикт: «Factually false», «Largely failed to replicate», «Contested by Sinclair (2014)» (`:28`, `:29`, `:32`). Там же прямо сказано, чем заменять: «this skill DOES NOT use Genovese as evidence. We rely only on the lab studies (Latane & Darley) which DO replicate» (`:28`), и «Treat as "these are the levers" - not "this is the precise math"» (`:45`).

**Вариант G. «When This Doesn't Apply» — таблица Context | Why** с указанием, к какому навыку уйти: `skills/money-models/SKILL.md:220-229` (шесть строк), `skills/mom-test/SKILL.md:179-185`, `skills/100m-offers/SKILL.md:220`, `skills/monetizing-innovation/SKILL.md:229`.

**Самый сильный приём раздела — реестр поправок с приоритетами.** `skills/influence/replication-notes.md` целиком (146 строк):
- приоритеты P0/P1/P2 у каждой записи: `:5`, `:17`, `:35`, `:48`, `:62`, `:88`, `:96`, `:104`, `:108`, `:112`, `:116`, `:120`;
- предписанная формулировка при цитировании: «When citing Bickman, use **42% / 92%** for the parking-meter task» (`:13`), «always note this is the 1966 figure and that modern replications are much lower» (`:46`), «Citing "65%" without context misrepresents the research. The correct framing: "65% in a specific condition; range 0-92% across 24 conditions"» (`:73`);
- разбор, какое из двух похожих условий даёт цифру: таблица трёх условий Freedman & Fraser с выводом «The 76% figure is ONLY for the small-sign condition» (`:50-58`);
- отдельный список того, что реплицируется, — «What's Robust», семь пунктов (`:134-146`), с итогом «The framework's PRINCIPLES are robust. SPECIFIC EFFECT SIZES from individual cited studies are unreliable» (`:146`);
- отдельный пункт про WEIRD-смещение выборок (`:124-132`).

**Оценка каждой цифры прямо в тексте навыка**: «Treat these as directional illustrations of compounding, not a measured law» — `skills/money-models/SKILL.md:72`; «correlational, post-hoc» — `skills/blue-ocean-strategy/frameworks.md:190-191`; пометка о том, что цифра из клиентского опроса вендора, «not independently verified - same provenance caveat as the 72% figure» — `skills/monetizing-innovation/integration.md:64`.

**Метка устаревания внутри кейсов, а не только в отдельном разделе**: «Iconic Cases - Decline Notes Inline» — `skills/blue-ocean-strategy/SKILL.md:189`.

---

## 4. Чек-листы и пороги

**Сквозной формат — таблица «Number | Rule»** под заголовком «Critical Numbers & Rules of Thumb»: `skills/monetizing-innovation/SKILL.md:159-176` (16 строк), `skills/crossing-the-chasm/SKILL.md:320-334`, `skills/four-steps/SKILL.md:412-427`, `skills/traction/SKILL.md:362-384`, `skills/spin-selling/SKILL.md:357-368`. Особый случай — «Critical Numbers (With Caveats)» в `skills/influence/SKILL.md:148-159`, где к каждой цифре приписана её ущербность: «**65%** | Milgram compliance | From 1 of 24 conditions; range 0-92%» (`:153`), «**42%** | Bickman … (NOT 19% - that figure is unverified.)» (`:159`).

**Конкретные шкалы и пороги, которые можно переносить как есть:**

| Что измеряется | Шкала | Порог и действие | Ссылка |
|---|---|---|---|
| Ранний евангелист, 5 характеристик | 1-5 по каждой, сумма до 25 | ≥20 сильный; 15-19 разбираться; <15 пропускать | `skills/four-steps/frameworks.md:167-179` |
| Разметка шкалы словами (что значит 1 и что значит 5) | 5 строк-полюсов | «Vaguely aware» → «Can articulate precisely + quantify cost» | `skills/four-steps/frameworks.md:169-175` |
| Плацдарм (beachhead), 9 факторов | 1-5; 4 шоу-стоппера + 5 «приятных» | любой шоу-стоппер ≤2 → ELIMINATE; среди выживших максимум суммы «приятных» | `skills/crossing-the-chasm/examples.md:39-66` |
| Итог отбора плацдарма | — | «Pick ONE. You cannot cross the chasm in two places» | `skills/crossing-the-chasm/examples.md:66` |
| Сообщение по SUCCESs | 6 принципов × 4 пункта, каждый до 5 | 25-30 сильно; 18-24 чинить 1-2 худших; <18 переделывать с Simple | `skills/made-to-stick/examples.md:3-57` (`:52-56`) |
| Приоритет правки | — | «Identify the 1-2 weakest areas and fix those first» | `skills/made-to-stick/examples.md:5`, `skills/made-to-stick/SKILL.md:60` |
| Каналы привлечения, 19 штук | 4 измерения (CPA, объём, качество, время) × 1-5, сумма /20 | делится на A/B/C, в A максимум 3 | `skills/traction/examples.md:112-158` (`:140-145` расшифровка осей, `:146-149` лимит трёх) |
| Проверка собственного предубеждения перед ранжированием | 4 вопроса-чекбокса | «Did I skip or phone in any channels above?» | `skills/traction/examples.md:103-107`, `skills/traction/frameworks.md:9` |
| Компоненты оффера | ценность 1-10 × стоимость 1-10 | в ядро — высокая ценность/низкая стоимость; цель 6-10 компонентов; отсечка ниже 8/10 по ценности | `skills/100m-offers/SKILL.md:130`, `:213`, `skills/100m-offers/frameworks.md:59-80`, `skills/100m-offers/examples.md:224` |
| Распределение по тарифам Good/Better/Best | проценты выбора | ≤25% Good, ~70% Better+Best, ≥10% Best — здорово; >50% Good — утечка; Best <10% — слабый премиум | `skills/monetizing-innovation/SKILL.md:84-86`, `skills/monetizing-innovation/frameworks.md:110-112` |
| Деньги: отмены и возвраты | проценты | >10% отмен Pay-Later; >5% ранних отмен по fee-офферу; возвраты выше ~5% → проблема в продукте, а не в оффере | `skills/money-models/SKILL.md:152`, `:193`, `:207`, `skills/money-models/frameworks.md:84`, `:228` |
| Структура звонка по SPIN | доля времени | подготовка ≤20% времени звонка; <10% крупных звонков должны кончаться Order или No-sale | `skills/spin-selling/SKILL.md:364`, `:366` |
| Число Implication-вопросов | 0/1/2/3+ | 22% / 61% / ~40% / <20% успеха — оптимум один | `skills/spin-selling/cases.md:181-184` |
| Время на привлечение | доля | 50% времени против 0% | `skills/traction/SKILL.md:366`, `:384` |
| Доля рынка по Ланчестеру | четыре полосы | ≥74% монополия (не атаковать); ≥41% лидер; 26-41% нестабильный; <26% фрагментированный — с минимальным бюджетом входа для каждой полосы | `skills/four-steps/frameworks.md:193-206`, `skills/four-steps/SKILL.md:268-271` |
| Коммерческая состоятельность идеи | 4 ворот | «All four must score "High" … Mixed scores = back to the drawing board» | `skills/blue-ocean-strategy/frameworks.md:143` |
| Дисциплина цены | счётное правило | 3 неценовых действия до любого снижения цены | `skills/monetizing-innovation/SKILL.md:173` |
| Качество интервью | доля | 25% вопросов должны быть «Why?» | `skills/monetizing-innovation/SKILL.md:176` |
| Предел восприятия | счётное правило | 9 выгод / 4 продукта до психологической перегрузки | `skills/monetizing-innovation/SKILL.md:168` |
| Доля первых лидов | проценты | конверсия лид → квалифицированный >15% хорошо, <5% плохо; квалифицированный → сделка >20% хорошо, <10% плохо | `skills/four-steps/examples.md:305-307` |

**Чек-листы по фазам процесса** — не общий список, а разбитый на «до / во время / после» с чекбоксами: `skills/mom-test/SKILL.md:130-149`. Аналогично по четырём фазам Бланка: `skills/four-steps/SKILL.md:498-535`; по диагностике чазмы: `skills/crossing-the-chasm/SKILL.md:388-409`.

**Анти-чеклист** как отдельный жанр — не «что делать», а «по каким признакам понять, что ты проваливаешься»: `skills/mom-test/SKILL.md:151-159` («You weren't scared of any question you asked»), таблица Pattern | Description | Cure `skills/crossing-the-chasm/SKILL.md:338-351`.

**Классификатор мусора с готовым ответом на каждый тип** — таблица «Bad Data | Example | Response»: «Compliments → "Thanks - but how are you dealing with this stuff at the moment?"», «Fluff → "When's the last time that happened? Walk me through it."», «Ideas/Features → "Why do you want that? What would it let you do? How are you coping without it?"» — `skills/mom-test/SKILL.md:59-65`. Рядом — парный список «хорошие концовки разговора» против «вежливых отказов»: «What are the next steps?», «Can I buy the prototype?» против «That's so cool, I love it!», «Let me know when it launches» — `skills/mom-test/SKILL.md:77-86`. Это готовый способ различать сигналы, которые чего-то стоят, от сигналов, которые не стоят ничего.
→ **у нас есть, у них похоже:** наш запрет на комплименты, мнения и намерения (ступени 1-7, `skills/05-validation-gate/SKILL.md:55`) — то же разделение, но у нас оно идёт ступенями 1-19 с вердиктом, у них дано тремя категориями и текстом без счёта.

---

## 5. Шаблоны для человека

**Место.** Все воркшиты лежат в `examples.md` соответствующего навыка; в `SKILL.md` от них только ссылки. Всего порядка 50 шаблонов и калькуляторов. Инвентарь по навыкам:

| Навык | Шаблоны (строка заголовка в `examples.md`) |
|---|---|
| `skills/made-to-stick` | SUCCESs-аудит `:3`, Message Clinic `:61`, Commander's Intent `:154`, переформулировка статистики `:194`, Three Whys `:228`, Story Spotting `:262` |
| `skills/storybrand` | BrandScript `:3`, One-Liner `:139`, каркас сайта `:175`, drip-кампания `:251`, сбор отзывов `:318` |
| `skills/traction` | брейншторм Bullseye `:3`, матрица ранжирования каналов `:112`, тест канала `:162`, калькулятор CPA/LTV `:243`, калькулятор виральности `:278`, пайплайн партнёрств `:315` |
| `skills/four-steps` | шкала боли евангелиста `:3`, worksheet типа рынка `:41`, карта продаж `:105`, позиционирование по типу рынка `:187-239`, матрица типа запуска `:240` |
| `skills/lean-startup` | выбор MVP `:46`, настройка инновационного учёта `:126`, встреча «пивот или упорство» `:192`, когортный анализ `:340`, Five Whys `:384`, scorecard обученной валидацией `:443` |
| `skills/crossing-the-chasm` | позиционирование в два предложения `:7`, «день из жизни» `:70`, карта целого продукта `:123` |
| `skills/money-models` | worksheet денежной модели `:7`, лестница рассрочек `:125`, калькулятор цены подписки `:143` |
| `skills/100m-offers` | одностраничная презентация оффера `:3`, пустой worksheet сборки оффера `:235` |
| `skills/monetizing-innovation` | шаблоны теста BECAUSE `:49`, MOCA-матрица `:75` |
| `skills/100m-leads` | письма `:3`, тёплый аутрич `:79`, контент `:119`, сценарии платной рекламы `:164`, лид-магниты `:217` |
| `skills/obviously-awesome` | история продажи `:51`, аудит позиционирования `:98` |
| `skills/spin-selling` | открытие звонка `:153`, предложение о следующем шаге `:183`, поведенческий самоаудит `:213` |
| `skills/mom-test` | письма `:60`, самоаудит качества разговора `:143` |

**Форма подачи — три приёма:**
1. Кодовый блок с подчёркиваниями и полями-вопросами в верхней части, чтобы человек сразу понял контекст: `MESSAGE: ___`, `AUDIENCE: ___`, `GOAL (what should they do after hearing this?): ___` — `skills/made-to-stick/examples.md:8-12`.
2. Чекбоксы `[ ]` внутри каждой оценки — не абстрактный балл, а список того, за что он ставится: `skills/made-to-stick/examples.md:17-20`.
3. Пустая колонка `Score (1-5)` в таблице факторов, рядом с самим вопросом-критерием: `skills/crossing-the-chasm/examples.md:45-60`; в «дне из жизни» — таблица-шапка из семи полей (отрасль, география, отдел, должность, технический покупатель, экономический покупатель) `:74-83`.
4. Скалярный вывод и несколько готовых ссылок-примеров под шаблоном: итог `/30` и три полосы вердикта `skills/made-to-stick/examples.md:52-56`.

**Заполненный пример идёт сразу за пустым шаблоном** — отдельный блок «Worked Example»: `skills/made-to-stick/examples.md:100`, счёт по 9 факторам `skills/crossing-the-chasm/examples.md:210`.

**След применения шаблонов под примером** — сноска-аудит: `*Templates used: Earlyvangelist Pain Hierarchy, Sales Roadmap - Buying Process Map*` — `skills/four-steps/examples.md:388`, `:405`, `:420`, `:445`, `:470`.

**Важно и прямо: разделения «что заполняет человек, что агент» в шаблонах нет.** Ни в одном файле нет указаний вида «это поле заполняет основатель», нет ролей, нет запрета агенту заполнять. Все шаблоны адресованы человеку во втором лице («Score any message against the six principles» — `skills/made-to-stick/examples.md:5`; «Your job to fix them» — `skills/mom-test/SKILL.md:165`), но заполняются они в равной мере и моделью: `README.md:82-86` прямо предлагает вставить `SKILL.md` и нужный `examples.md` в чат с любым LLM. Механика шаблона без ролей — это переносимо только вместе с нашим гейтом 4.

**Ограничений на заполнение у шаблонов нет**: ни лимита времени, ни условия «остановись, если человек устал», ни требования полноты перед переходом дальше. Ни одного стоп-правила внутри `examples.md` нет.

---

## 6. Гейты и условия выхода

**Входной гейт навыка — «Should You Use This Skill?»**: дерево решений, где первым делом отсекается неподходящий контекст, а не описывается польза. `skills/crossing-the-chasm/SKILL.md:13-35`: четыре вопроса подряд, у каждого ветка отказа с адресом, куда идти вместо (`:19-22`), проверка предварительного условия «Do you have at least 10 paying customers or repeatable early-adopter revenue?» → «NO → You're still in Customer Discovery/Validation. Use **four-steps** and **mom-test** first. Come back when you have real traction» (`:24-26`), и поправка на ресурс: нет шести месяцев запаса → «Apply tactical bits (positioning, beachhead) without multi-year choreography» (`:32-34`).

**Отрицательный роутинг в метаданных** — тот же гейт, но машинно-читаемый: `NOT for PLG/freemium SaaS (Slack, Notion, Cursor), pure consumer apps, two-sided marketplaces, or AI-native products` — `skills/crossing-the-chasm/SKILL.md:3`.

**Раздел «когда этот навык не нужен»** есть почти у каждого и обычно с адресом замены:
- `skills/blue-ocean-strategy/SKILL.md:179` «When NOT to Use This Skill»;
- `skills/obviously-awesome/SKILL.md:229` «When NOT to Use This Skill»;
- `skills/obviously-awesome/integration.md:49-74` «When OA Is Less Critical» с таблицей компаний-контрпримеров;
- `skills/influence/SKILL.md:206` «When NOT to Use This Skill (Ethically)» — единственный этический гейт в корпусе;
- `skills/spin-selling/SKILL.md:415` «When SPIN Fails (Don't Use Here)», полная анти-триггерная таблица в `skills/spin-selling/integration.md:1-24`;
- `skills/100m-offers/integration.md:155-163` «When 100m-offers is the Wrong Tool» — семь строк «проблема → другой навык»; то же в `skills/100m-leads/integration.md`, `skills/money-models/integration.md`.

**Самоограничение мета-навыка** — самый сильный гейт корпуса, `skills/diagnose/SKILL.md:156-167` «When No Framework Fits»: четыре признака, что пора прекратить применять фреймворки (три и более фреймворка без улучшения; ситуация без прецедента; фреймворк используется, чтобы избежать неприятного разговора; фреймворки противоречат друг другу) и метаправило «If you scored a 9/10 on a rubric but your gut says something is off, trust the gut and investigate» (`:167`). Там же прямо: «A diagnostic that always gives an answer is more dangerous than one that sometimes says "I don't know"» (`:204`).

**Гейты-вентили внутри процессов, с явным «pass/fail» и предписанным откатом:**
- переход Discovery → Validation: четыре проверки (продукт, процесс продаж, канал, финансовая модель), «All four pass → proceed to Customer Creation. Any fail → **pivot back to Customer Discovery** (the canonical pivot)» — `skills/four-steps/frameworks.md:151-159`;
- форма паспорта валидации с чекбоксами: «Have founders personally sold? □ Yes □ No; Is the sales process repeatable? □ Yes □ No» и вывод «**If any answer is No → do NOT proceed to Customer Creation. Iterate or pivot back to Customer Discovery.**» — `skills/four-steps/examples.md:141-148`;
- полный pass/fail-раздел: три обязательных условия «All three conditions must be met» (`:154-174`) и отдельный список fail-сигналов (`:176-183`) — `skills/four-steps/examples.md:152-183`;
- вентиль преждевременного масштабирования: «**If ≥3 boxes checked: you are likely in premature scaling. Stop. Go back to Customer Validation.**» — `skills/four-steps/examples.md:366`;
- вентиль цены: «If any answer is NO, stop and fix it before launch» — `skills/monetizing-innovation/examples.md:278`;
- вентиль последовательности запуска: четыре шага, из них два с прямым «Stop» — «NO → Stop. Rethink.» и «NO → Re-engineer offer» — `skills/blue-ocean-strategy/SKILL.md:155-164`;
- вентиль по голосам критериев: «All four must score "High" for commercial viability. Mixed scores = back to the drawing board» — `skills/blue-ocean-strategy/frameworks.md:143`.

**Условие выхода из метода** (не из навыка, а из практики): `skills/mom-test/integration.md:89-99` «When to Stop Using Mom Test» — пять признаков, что интервью пора прекращать (несколько человек описывают проблему одними словами; ответы предсказуемы; люди платят; сегмент называем; есть евангелист, толкающий продукт), и предписание переключаться на продажи. Рядом анти-паттерн с предписанным действием: «Stop interviewing. Look at your notes… Re-interview only that segment» — `skills/mom-test/integration.md:101-105`.

**Порог допуска к позднему навыку продублирован в таблице роутера**: «crossing-the-chasm (only if 10+ paying customers)» — `skills/diagnose/SKILL.md:182`.

**Что у них отсутствует как класс:** нет лимита на число вопросов к человеку, нет детектора усталости, нет условия выхода по времени сессии, нет требования полноты артефакта перед переходом дальше. Единственная защита от бесконечного диалога — «One-Skill Rule» (`skills/diagnose/SKILL.md:146-152`) и правило «не стекировать фреймворки». Гейты у них есть у навыка, но не у вопроса.
→ **у нас есть, у них похоже:** стоп-условия и блокировка валидации — наши четыре жёстче; их «When to Stop Using Mom Test» это выход из метода, а не из сессии.

---

## 7. Что взять в наш репозиторий (список конкретных изменений)

1. **Завести `integration.md` рядом с каждым нашим навыком** (`skills/00-onboarding-interview/`, `00b-telemetry-setup/`, `03-prevalidation/` и будущими 01, 02, 04, 05) и писать конфликты по жёсткому микрошаблону: `### Конфликт N: [утверждение A] vs [утверждение B]` → `**Сторона A:**` / `**Reality:**` / `**Resolution:**` → при необходимости `**Тест:**`. Образец: `skills/100m-offers/integration.md:110-146`, `skills/mom-test/integration.md:56-87`, тест-развилка `skills/obviously-awesome/integration.md:25`.

2. **Разрешать конфликт только одним из пяти способов**, а не общими словами: разные уровни, разные этапы, разные смыслы одного слова, решающий тест, признание правоты с оговоркой. Источники типов: `skills/blue-ocean-strategy/integration.md:55`, `:9`, `skills/mom-test/integration.md:78`, `skills/obviously-awesome/integration.md:21-25`.

3. **Ввести карту слоёв для наших навыков** с правилом выхода наверх: Discovery → Strategy → Tactical → Influence, «если верхний слой не решён, идти наверх, а не вниз». Образец: `skills/100m-offers/integration.md:165-177`. У нас аналог — `internal/draft/03_pipeline.md`; карту положить туда же или в `METHODOLOGY.md`.

4. **Добавить в каждый навык раздел «где приём ломается в 2026»** из трёх подблоков: где ещё работает / где ломается (с названиями продуктов и технологий) / что автор понял неверно. Образцы: `skills/crossing-the-chasm/SKILL.md:358-382`, `skills/four-steps/SKILL.md:471-494`, `skills/blue-ocean-strategy/integration.md:77-84`.

5. **Открыть `internal/draft/extracts/corrections.md` — реестр поправок с приоритетами P0/P1/P2** и предписанной формулировкой: «при цитировании цифры X писать Y». Образец: `skills/influence/replication-notes.md:5-15`, `:46`, `:73`, плюс обязательный список «что реплицируется» `:134-146`. Это дополняет наши три уровня доказательности: уровни говорят, чем подкреплять вывод, реестр говорит, как именно произносить цифру.

6. **Свести наши пороги в таблицу `Number | Rule`** внутри каждого навыка, с обязательной колонкой оговорки о происхождении числа. Образцы: `skills/monetizing-innovation/SKILL.md:159-176`, `skills/influence/SKILL.md:148-159` (образец оговорок), `skills/spin-selling/SKILL.md:357-368`.

7. **Задавать шкалы словами, а не только числами** — расписывать, что означает минимум и максимум балла. Образец: `skills/four-steps/frameworks.md:169-175`. У нас числовых шкал нет вообще, это чистое добавление.

8. **Оформлять пороги полосами с предписанным действием** (не «порог 2», а «≤2 → вычеркнуть; 3 → разбираться; 4-5 → брать»). Образцы: `skills/crossing-the-chasm/examples.md:43-66`, `skills/monetizing-innovation/SKILL.md:84-86`, `skills/four-steps/frameworks.md:193-206`.

9. **Добавить отрицательные триггеры в `description` наших навыков**: «НЕ для … — используй X». Образцы: `skills/traction/SKILL.md:3`, `skills/lean-startup/SKILL.md:3`, `skills/crossing-the-chasm/SKILL.md:3`. Сейчас наши описания только положительные (`skills/00-onboarding-interview/SKILL.md:3`, `skills/03-prevalidation/SKILL.md:3`).

10. **Ввести блок «Test» как обязательный вывод чек-листа** — одну проверяемую фразу, отделяющую один случай от другого. Образцы: `skills/obviously-awesome/integration.md:25`, `skills/100m-leads/lead-getters.md:107` («If you vanished tomorrow, could a stranger get your results following only your checklist?»), `skills/money-models/SKILL.md:231-239`.

11. **Завести в `internal/` регрессионный набор реальных задач с таблицей прогона**: колонки «задача / категория / какие навыки / кто победил / был ли перегиб», плюс раздел «что подкрутили по итогам». Образец: `experiments/real-founder-problems.md:8-33`, `:228-234`. Полезен именно столбец «Overfit?» — у них он поймал два перегиба (`:15`, `:21`).

12. **Ставить под разобранным примером сноску «какие шаблоны применены»** — `*Шаблоны: …*`. Образец: `skills/four-steps/examples.md:388`, `:470`. Даёт след, по которому видно, что пример не выдуман.

13. **Разделить воркшиты по заполняющему** — прямо то, чего у них нет. Формат их шаблонов (поля, чекбоксы, шкала словом, полосы вердикта) брать, но каждое поле помечать: `[агент: из базы]`, `[человек: гейт 4]`, `[внешний исследователь: гейт 2]`. Их шаблоны безусловны (`skills/made-to-stick/examples.md:8-12`), наши метки сделают их честными.

14. **Ввести правило «один навык, один следующий шаг»** для нашего интервью и разбора: одна основная практика, необязательно одна дополнительная, одно конкретное действие; не параллелить. Образец: `skills/diagnose/SKILL.md:144-152`. Смыкается с нашим правилом «один следующий шаг» (`skills/00-onboarding-interview/SKILL.md:141`).

15. **Добавить раздел «когда метод не нужен» с адресом замены** в наши навыки, включая запрет на применение навыка в неподходящем контексте с указанием, куда идти. Образец: `skills/spin-selling/SKILL.md:415`, `skills/100m-offers/integration.md:155-163`.

16. **Перенести в `templates/interview.md` таблицу «мусор → готовый ответ»** из трёх строк: на комплимент, на общее слово, на просьбу о функции — с дословной репликой интервьюера в каждом случае. Образец: `skills/mom-test/SKILL.md:59-65`. Это ровно то, чего не хватает нашему счёту: ступень сигнала мы определяем, а что сказать собеседнику в момент, когда сигнал слабый, у нас не написано.

17. **Добавить в тот же шаблон парный список «чем заканчивается разговор, который чего-то стоил»** — конкретные фразы-обязательства против фраз-отказов. Образец: `skills/mom-test/SKILL.md:77-86`. Прямо ложится на границу 15/16 в нашей шкале: фразы из правой колонки не должны поднимать ступень.

18. **Зафиксировать формат вывода гейта списком полей** так, как это сделано у них в шаблоне «Message Clinic»: у нас двенадцать строк вывода (`skills/05-validation-gate/SKILL.md:38-51`), у них каждый шаблон начинается с контекстных полей «что и кому сообщаем» — `skills/made-to-stick/examples.md:68-70`. Приём небольшой, но полезный: перед разбором фиксировать предмет разбора одной строкой.

---

## 8. Что у нас уже лучше

**Гейты вопроса против гейтов навыка.** У них гейт стоит на входе в навык (`skills/crossing-the-chasm/SKILL.md:13-35`), у нас — на каждом вопросе, четыре фильтра, и первый сработавший решает судьбу вопроса: `skills/00-onboarding-interview/SKILL.md:72-86`, `AGENTS.md` раздел 9. Их гейт отвечает «нужен ли этот фреймворк», наш — «имею ли я право это спрашивать». Второе строже.

**Стоп-условия вместо условий выхода из метода.** У них есть «когда перестать брать интервью» (`skills/mom-test/integration.md:89-99`) и правило не стекировать (`skills/diagnose/SKILL.md:146-152`). Лимита вопросов, детектора усталости и принудительной остановки по полноте артефакта нет ни в одном из 16 навыков. У нас это четыре жёстких условия выхода: `skills/00-onboarding-interview/SKILL.md:125-134`, `AGENTS.md` раздел 11.

**Формула вопроса, запрещённые слова, лимит 120 знаков, один вопрос за сообщение** — `skills/00-onboarding-interview/SKILL.md:88-99`. У них вопросов как объектов управления нет вовсе: есть списки хороших и плохих вопросов (`skills/mom-test/SKILL.md:37-57`), но нет правил сборки вопроса и нет запрещённых слов.

**Три уровня доказательности с колонкой «запрет»** (`AGENTS.md` раздел 3). У них есть провенанс отдельных цифр (`skills/influence/SKILL.md:148-159`) и оговорки о хрупкости исследований (`skills/influence/replication-notes.md`), но нет разделения «чем позволено подкреплять вывод»: у них любая цифра из книги идёт в один список с любой цифрой из практики. Наш запрет «считать `[база]` валидацией» сильнее.

**Шкала силы сигнала 1-19 с вердиктом и счётом** — второе измерение, которого у них нет как системы (`AGENTS.md` раздел 3, `skills/05-validation-gate/SKILL.md:26-34`). У них ближайшее по смыслу — «Commitment Currencies»: время, репутация, деньги (`skills/mom-test/SKILL.md:69-76`) — три категории без ступеней, без порога и без вычислимой формулы; наш вердикт считается (`N = max(1, 3 − подтверждающих)`, `skills/05-validation-gate/SKILL.md:32`) и цитирует дословно (`:56`). Их вклад, которого у нас нет, — готовая реплика интервьюера на каждый тип слабого сигнала (`skills/mom-test/SKILL.md:59-65`), см. пункт 16 раздела 7.
→ **у нас есть, у них похоже:** сам принцип «вес сигнала определяется тем, чего он стоил человеку» — у них он выражен словами, у нас шкалой и гейтом.

**Слепой файл-запрос внешнему исследователю** — гипотеза и предпочтительный ответ в запрос не попадают, каждый вопрос требует обе стороны, ответ обязан содержать факты за, факты против и белые пятна (`AGENTS.md` раздел 4, `skills/03-prevalidation/SKILL.md:22-24`, `:55`). У них ничего подобного нет: конфликты разбирают авторы навыков, заранее зная, чью сторону они сводят, и в `integration.md` нет ни одного вопроса, адресованного внешнему источнику. При этом их собственный замер угодливости есть — `experiments/real-founder-problems.md:4` сравнивает ответ «сырой модели» и ответ со навыками, но только между собой, а не со слепым поиском.

**Статусы артефакта и лестница опоры** `[validated: data]` / `[validated]` / `[assumption]` (`AGENTS.md` раздел 12, `skills/00b-telemetry-setup/SKILL.md:54`, `:60-61`). У них ни один шаблон не помечен статусом: заполненный воркшит выглядит одинаково достоверно и когда человек смотрел в свой трекер, и когда он вспоминал на глаз. Это их главная дыра, и она ровно наша сильная сторона.

**Приоритет данных над памятью и нулевой шаг «аудит источников»** (`skills/00-onboarding-interview/SKILL.md:31-50`, `AGENTS.md` раздел 12). У них весь корпус построен на том, что человек расскажет о себе сам; вопроса «откуда мне взять факты, чтобы меньше спрашивать» нет ни в одном навыке.

**Цикл замера с критерием закрытия и обработкой срыва** — `skills/00b-telemetry-setup/SKILL.md:58-70`. У них нет ни одного навыка, который бы вел сбор данных о человеке.

**Презумпция приватности как правило, а не как оговорка** — `skills/00-onboarding-interview/SKILL.md:48`, `skills/00b-telemetry-setup/SKILL.md:79-84`. У них этот слой отсутствует полностью.

**Правило «нет ссылки, нет находки» с датой и обязательной строкой «Чего найти не удалось»** — `skills/03-prevalidation/SKILL.md:22-24`, `:55`. У них ссылок на страницы нет ни в одном `integration.md` (единственная атрибуция цифры — `skills/spin-selling/integration.md:136`), то есть проверить конфликт по первоисточнику нельзя.

**Отдельный навык на шаг маршрута** — `skills/`, четыре навыка (`00-onboarding-interview`, `00b-telemetry-setup`, `03-prevalidation`, `05-validation-gate`) против 16 монолитных книжных навыков у них. Их `SKILL.md` до 463 строк грузится целиком (`skills/crossing-the-chasm/SKILL.md`), то есть «прогрессивное раскрытие» из `README.md:105` работает только между файлами, внутри файла его нет.

**Формальные дефекты их корпуса, которые мы не копируем:**
- обещанная в `README.md:96-103` схема из пяти файлов не соблюдается: у `skills/diagnose/` один файл, у `skills/influence/` другой набор, у `skills/100m-leads/` два лишних (`lead-getters.md`, `paid-ads.md`);
- обещанная длина `SKILL.md` «~250-500 lines» (`README.md:98`) фактически 153-463;
- один и тот же раздел назван шестью разными именами (см. раздел 2 отчёта);
- `skills/diagnose/` — единственный навык без файла конфликтов: `integration.md` у него нет, хотя именно он маршрутизирует по всем 15 книгам и именно у него конфликтов больше всего. Схема «пять файлов на навык» из `README.md:96-103` на него не распространяется, и оговорки об этом в README нет.

---

## Приложение. Проверка целостности

`python scripts/verify_harness.py` на 18.10.2026 → код 0, покрытие по всем четырём источникам сходится (`blank` 1-15407, `blankdorf` 1-19713, `momtest` 1-5113, `thiel` 1-5487). Настоящий отчёт лежит вне проверяемой папки `internal/draft/extracts/notes` и под правило имени «источник-от-до.md» не подпадает: он разбирает внешний репозиторий, а не том из `internal/docs/biblio`.
