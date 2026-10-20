# Каталоги инструментов: что годится для набора

**Источники:** четыре клона в `internal/research/`, только чтение, клоны не менялись, ничего не устанавливалось, в сеть не ходили.

**Метод и дата:** `git log -1`, обход дерева, поиск текстом по `*.md` / `*.toml` / `*.json`; бинарники и каталоги `vendor/`, `dist/`, `prebuilt/` не читались; разбор 2026-10-20. Все утверждения ниже — `[база]`: проверяются по указанному файлу и строке.

---

## 1. VoltAgent-awesome-design-md

**Коммит:** `3b60532`, 2026-10-14. **Размер:** 2,43 МБ, 173 файла.

**Что внутри.** 84 каталога брендов: в каждом `DESIGN.md` (39–44 КБ, ~548 строк), у 83 из 84 ещё `README.md`-заглушка на 210 байт («moved to getdesign.md», [design-md/linear.app/README.md:3](internal/research/VoltAgent-awesome-design-md/design-md/linear.app/README.md#L3)). Плюс корневой `README.md` и `CONTRIBUTING.md`. Превью `preview.html` и `preview-dark.html`, обещанные в [README.md:217–218](internal/research/VoltAgent-awesome-design-md/README.md#L217-L218) и требуемые в `CONTRIBUTING.md:5`, в клоне отсутствуют: во всех 84 каталогах только `.md`. На них нельзя рассчитывать.

**Структура каталога:** `.github/ISSUE_TEMPLATE/design-md-request.yml`, `design-md/<бренд>/{DESIGN.md,README.md}`, `README.md`, `CONTRIBUTING.md`, `LICENSE`.

**Структура файла.** YAML-шапка: `version`, `name`, `description` (один абзац-портрет на 5–6 строк), `colors` (23 семантических токена: `primary`, `on-primary`, `ink`, `ink-muted`, `canvas`, `surface-1…4`, `hairline`, `semantic-*`), `typography` (роли `display-xl…mono` с `fontSize`/`fontWeight`/`lineHeight`/`letterSpacing`), `rounded`, `spacing` ([DESIGN.md:1–130](internal/research/VoltAgent-awesome-design-md/design-md/linear.app/DESIGN.md#L1-L130)).

**Разделы (канон, 74 файла из 84):** `Overview` → `Colors` (Brand & Accent / Surface / Text / Semantic) → `Typography` (Font Family / Hierarchy / Principles / Note on Font Substitutes) → `Layout` (Spacing System / Grid & Container / Whitespace Philosophy) → `Elevation & Depth` → `Shapes` (Border Radius Scale) → `Components` (Buttons / Cards / Inputs / Navigation / Footer) → `Do's and Don'ts` (Do / Don't) → `Responsive Behavior` (Breakpoints / Touch Targets / Collapsing Strategy) → `Iteration Guide` → `Known Gaps`. Остальные 10 файлов держат более старую нумерованную редакцию Stitch (`1. Visual Theme & Atmosphere` … `9. Agent Prompt Guide`) — формат не унифицирован.

**Вердикт по формату как эталону визуального языка для слайдов: частично годится, целиком — нет.**
- Берём скелет: шапка-токены → портрет одним абзацем → цвета по ролям → шрифтовая лестница → сетка и поля → «Do / Don't» → `Known Gaps`. Это одна страница, читаемая и человеком, и агентом.
- Не берём `Components`, `Responsive Behavior`, `Touch Targets`, состояния кнопок: это язык веб-интерфейса, к слайду 16:9 не переносится.
- Не хватает того, без чего слайд не описан: пропорции кадра, безопасные поля, минимальный кегль под проектор, бюджет элементов на страницу.
- Ценное в конце: `Iteration Guide` (7 правил правки, включая «lavender тратить скупо») и `Known Gaps` — честный список того, что не задокументировано ([DESIGN.md:532–548](internal/research/VoltAgent-awesome-design-md/design-md/linear.app/DESIGN.md#L532-L548)).

## 2. ZSeven-W-openpencil

**Коммит:** `d155cd0`, 2026-10-17. **Размер:** 316 МБ, 4973 файла — самый тяжёлый клон.

**Что внутри.** Полноценный десктопный редактор дизайна на Rust (аналог Figma): `crates/` (ядро, UI, MCP-сервер, мост авторизации), `packages/`, `templates/step0/`, `docs/`, `vendor/`, подмодули, 14 переводов README. В `crates/op-auth-bridge/prebuilt/` лежат готовые бинарные библиотеки на 30 МБ каждая, в `crates/op-host-web/pkg-*/` — wasm на 23 МБ. Ничего из этого не читалось.

**Что полезно.** Библиотека markdown-навыков `crates/op-ai-skills/skills/`:
- `domains/slides.md` (10 КБ) — тиры оформления S1–S4, кегли, контрастные пороги, контракты раскладок;
- `domains/deck-contract.md` (7 КБ) — три закона колоды, таблица «заперто / меняется», тест «призрачной колоды»;
- `domains/cards.md`, `domains/dashboard.md`, `domains/landing-page.md` — соседние домены;
- `phases/generation/anti-slop.md` — требование разнообразия между генерациями;
- `style-guides/*.md` — 63 файла по 9–18 КБ с полем `platform: slides`.

**Формат style guide (главная находка):** шапка `name` / `tags` / `platform: slides`, затем `Style Scope` → `Style Summary` → `Color System` (Grounds / Text Colors / Accent Colors / Rules) → `Typography` (Font Families / Type Scale / Numerals) → `Layout Grammar` → `Signature Motifs` (пронумерованные приёмы с именами) → `Page Inventory` → `Strictly Avoid` → `Anti-Patterns` ([style-guides/sounding-navy.md:1–182](internal/research/ZSeven-W-openpencil/crates/op-ai-skills/skills/style-guides/sounding-navy.md#L1-L182)).

**Формат deck contract:** одна фраза «после этого [аудитория] должна [решить/сделать/поверить], потому что [один тезис]»; закон 1 — переполнение делит страницу, а не уменьшает кегль; закон 2 — бюджет плотности принадлежит типу страницы; закон 3 — таблица `LOCKED across pages` / `MUST change across pages`; тест заголовков подряд ([deck-contract.md:16–55](internal/research/ZSeven-W-openpencil/crates/op-ai-skills/skills/domains/deck-contract.md#L16-L55)).

**Шаблоны** `templates/step0/` — 72 Python-генератора карточек, колод, инфографики и каруселей плюс PNG-превью. Работают только через API приложения, без установки бесполезны.

**Вердикт: рассмотреть → взять приём, инструмент отклонить.** Формат паспорта стиля и три закона колоды переносятся как текст, весят ноль и решают нашу задачу «единый визуальный язык слайдов». Сам редактор не берём: установка Rust-тулчейна и 316 МБ ради слайдов не снижает стоимость шага.

## 3. filipecalegario-awesome-vibe-coding

**Коммит:** `59d5028`, 2026-04-15. **Размер:** 0,12 МБ, 11 файлов.

**Что внутри.** Один README на 20 КБ и четыре перевода (CN/JP/KR/PT), `contributing.md`, `code-of-conduct.md`, `.claude/`, `to-test.md` на 237 байт. Никакого кода — чистый список ссылок.

**Структура:** `About the concept` → `Browser-based Tools` → `IDEs and Code Editors` → `Mobile Apps` → `Plugins and Extensions` → `Local Apps` → `Command Line Tools` → `Task Management for AI Coding` → `Documentation for AI Coding` → `Communities & Job Boards` → `News and Social Media` ([README.md:7–20](internal/research/filipecalegario-awesome-vibe-coding/README.md#L7-L20)).

**Годные рубрики для формулировок запроса:** `Task Management for AI Coding` ([README.md:131–138](internal/research/filipecalegario-awesome-vibe-coding/README.md#L131-L138)) и `Documentation for AI Coding` ([README.md:140–152](internal/research/filipecalegario-awesome-vibe-coding/README.md#L140-L152)). Остальные восемь рубрик — редакторы, хостинг, сообщества — к нашей задаче отношения не имеют.

**Методы и артефакты, только перечень и место:** Amazon Kiro, spec-driven development ([README.md:59](internal/research/filipecalegario-awesome-vibe-coding/README.md#L59)); Claude Task Master (:134); AI-DLC Workflows AWS Labs (:138); AGENTS.md (:143); awesome-ralph (:145); llms.txt (:148); getdesign.md (:152); The Prompt Engineering Playbook (:172).

**Вердикт: отклонить как материал, оставить две рубрики для запроса.** Каталог не отвечает ни на один наш вопрос и не описывает ни одного шага; из него берутся только слова, которыми называются классы методов.

## 4. no-fluff-awesome-vibe-coding

**Коммит:** `96c9ac9`, 2025-09-17 — самый старый из четырёх. **Размер:** 43 МБ, 408 файлов (из них 42 МБ — картинки, 36 МБ из них в `dist/`).

**Что внутри.** Статический сайт на Astro: пять конфигов сборки под разные витрины, `src/`, `dist/`, `public/`. Данные живут в одном файле `data.toml` (28 КБ), из него генерируется README. Полезная часть — именно TOML, а не сайт.

**Структура данных:** таблицы `[[agents]]` 10, `[[apps]]` 2, `[[interfaces]]` 10, `[[tools]]` 15, `[[workflows]]` 4, `[[hosted-agents]]` 5 ([data.toml:1–476](internal/research/no-fluff-awesome-vibe-coding/data.toml#L1-L476)). Поля записи: `name`, `website`, `repo`, `open_source`, `summary` (одна строка), `detail` (абзац), `category`, `hot`. Подрубрики инструментов заданы явно: Memory, Task management, Codebase understanding, Security, Agent feedback, Design, Backups and change management, Other ([data.toml:476–478](internal/research/no-fluff-awesome-vibe-coding/data.toml#L476-L478)).

**Методы, только перечень и место:** Task Master ([data.toml:402](internal/research/no-fluff-awesome-vibe-coding/data.toml#L402)), BMAD-METHOD (:412), Claude Code PM (:422), Spec Kit (:432); в README те же четыре в разделе Workflows ([README.md:308–337](internal/research/no-fluff-awesome-vibe-coding/README.md#L308-L337)).

**Годная формулировка для запроса.** Шаблон заявки на новый workflow — готовый перечень полей: имя, репозиторий, тип workflow (Development practice / Agent orchestration / Prompting / Testing-QA / CI-CD / On-call / Code review), предпосылки и инструменты, шаги списком, короткое описание «какую проблему решает и когда применяется» ([contribute-a-new-workflow.md:1–40](internal/research/no-fluff-awesome-vibe-coding/.github/ISSUE_TEMPLATE/contribute-a-new-workflow.md#L1-L40)). Это ровно тот каркас, по которому внешний исследователь описывает метод единообразно.

**Вердикт: рассмотреть → взять одну форму для запроса.** Сам каталог — витрина инструментов, в набор не идёт; шаблон заявки экономит нам сочинение структуры вопроса.

## Что берём

1. **Паспорт визуального языка одним файлом** — формат `style-guides` из openpencil: шапка `tags/platform`, цвета по ролям, шкала кеглей, поля, «фирменные приёмы», `Strictly Avoid`. Одной фразой: один файл, где записаны цвета, шрифты, поля и запреты, чтобы все слайды выглядели как один. Подтверждён файлом [sounding-navy.md](internal/research/ZSeven-W-openpencil/crates/op-ai-skills/skills/style-guides/sounding-navy.md#L7-L182).
2. **Три закона колоды** из `deck-contract.md`: переполнение делит страницу, а не сжимает кегль; плотность задаёт тип страницы; язык заперт, структура меняется. Одной фразой: текст не влез — режем текст или делим слайд, шрифт не трогаем. [deck-contract.md:20–55](internal/research/ZSeven-W-openpencil/crates/op-ai-skills/skills/domains/deck-contract.md#L20-L55).
3. **Фраза-задание перед первой страницей**: «после этого аудитория должна решить X, потому что Y». Одной фразой: сначала одно предложение о том, что должен сделать зритель, потом слайды. [deck-contract.md:16–18](internal/research/ZSeven-W-openpencil/crates/op-ai-skills/skills/domains/deck-contract.md#L16-L18).
4. **Хвост «Do / Don't» и `Known Gaps`** из DESIGN.md как обязательная часть любого нашего описания: что запрещено и что осталось не задокументировано. Одной фразой: у каждого описания есть список запретов и список дыр. [DESIGN.md:480–548](internal/research/VoltAgent-awesome-design-md/design-md/linear.app/DESIGN.md#L480-L548).

Предел: четыре приёма, все текстовые, ни одного нового инструмента в наборе.

## Что только в запрос исследователю

Формулировки, а не материал. Ни одна строка из каталогов не становится шагом набора.

- **Рубрики для каркаса вопроса:** типы workflow из шаблона no-fluff (Development practice / Agent orchestration / Prompting / Testing-QA / CI-CD / Code review); пары «Task Management for AI Coding» и «Documentation for AI Coding» из filipecalegario.
- **Слова-классы методов:** spec-driven development, context engineering, agent orchestration, PRD → stories, «спецификация как исполняемый артефакт».
- **Имена, которые можно спросить, не пересказывая:** BMAD-METHOD, Spec Kit, Claude Task Master, Claude Code PM, AI-DLC (AWS Labs), Ralph, AGENTS.md, llms.txt, getdesign.md, DESIGN.md. Где лежат — в разделах 1–4 выше.
- **Вопросы, которые из этого следуют:** какие из методов дают обязательство человека, а не артефакт агента; чем spec-driven отличается от обычного ТЗ по трудозатратам; что в этих методах делает один человек без команды.
- **Структура ответа:** поля из шаблона заявки (проблема, когда применять, шаги, предпосылки) плюс обязательные «факты за / факты против / белые пятна» по правилам предвалидации.

## Что отклоняем

- **openpencil как инструмент.** 316 МБ, Rust-тулчейн, готовые бинарники и подмодули; генераторы шаблонов живут только внутри приложения. Не снижает стоимость шага и не объясняется одной фразой не-разработчику.
- **DESIGN.md целиком как стандарт слайдов.** `Components`, `Responsive Behavior`, `Breakpoints`, `Touch Targets` описывают веб-интерфейс; в слайде 16:9 этих сущностей нет.
- **Библиотеку 63 стилей из openpencil.** Взять её в набор — значит завести каталог, от которого мы отказались правилом. Нужен один наш стиль, а не 63 чужих.
- **Каталоги как источник фактов.** Списки ссылок filipecalegario и no-fluff ничего не доказывают про нашу задачу; их описания — маркетинговые `summary` авторов каталога, а не проверенные данные.
- **Превью из VoltAgent-репозитория.** Их нет в клоне, только обещание в README; планировать на них нельзя.
- **Astro-сайт и `dist/` no-fluff.** 36 МБ собранных картинок и пять конфигов витрин к методике отношения не имеют.

**Итог по четырём.** VoltAgent — рассмотреть (скелет описания, без веб-разделов). openpencil — взять приём (паспорт стиля и законы колоды), инструмент отклонить. filipecalegario — отклонить, две рубрики в запрос. no-fluff — рассмотреть, одна форма в запрос.
