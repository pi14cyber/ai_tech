# Память между сессиями, фиксация контекста, задачи и коммуникации: что переносится

Источники (только чтение, клоны не менялись):

- `internal/research/screenpipe-screenpipe` — `62482a7`, 2026-10-17, Rust + TypeScript (Tauri). Рабочее дерево неполное: 5924 файла в HEAD, на диске меньше 500, поэтому читалось через `git show`; ссылки на этот клон даны формой `HEAD:<путь>:<строки>`, потому что файлов на диске нет и сверять номер строки не с чем.
- `internal/research/thedotmack-claude-mem` — `9e4f313`, 2026-10-19, TypeScript (Bun, SQLite, Chroma).
- `internal/research/MemPalace-mempalace` — `f884dd4`, 2026-10-18, Python (ChromaDB, MCP).
- `internal/research/elie222-inbox-zero` — `f351f0a`, 2026-10-19, TypeScript (Next.js, Prisma).
- `internal/research/taskosaur-taskosaur` — `a5bea52`, 2026-09-05, TypeScript (NestJS + Next.js).
- `internal/research/didhd-personal-ai-task-assistant` — `b45054c`, 2024-08-26, Python (LangGraph + Streamlit).

Ссылки: `путь:строка`. Утверждается только прочитанное в файлах.

---

## 1. screenpipe-screenpipe

**Структура.** Монорепо: `crates/` (захват, хранилище, движок), `apps/screenpipe-app-tauri`, `packages/` (SDK, MCP), `docs/`. Внутри `crates/screenpipe-core/assets/pipes/` — готовые «пайпы»: markdown-файл с промптом и расписанием, который исполняет агент поверх записанной истории. Запись: SQLite `~/.screenpipe/db.sqlite` (`HEAD:crates/screenpipe-core/src/pipes/mod.rs:1751`), медиа — файлами на диске.

**1.1. Захват по событию, а не по таймеру.**
Скриншот снимается на смену приложения, клик, паузу в наборе, скролл; к кадру прикладывается дерево доступности, а OCR только как запасной путь — `HEAD:README.md:235`. Что именно индексируется, перечислено явно: дерево доступности, OCR, транскрипция, спикеры, ввод с клавиатуры, переключения приложений — `HEAD:README.md:124`; поиск — SQLite FTS5, «returns screenshots and audio clips alongside text results» — `HEAD:README.md:249`.
**Взять.** Как формулировку «что именно попадает в запись»: у шаблона `templates/state.md` такого перечня нет, и от этого непонятно, что считается фактом дня. Адрес: `templates/state.md:5-10`.

**1.2. Ресурсы названы числом и с оговоркой.**
«CPU: approximately 5-20%», «RAM: approximately 0.5-3 GB for capture», «Storage: varies… Measure a representative day on your device» — `HEAD:README.md:125-128`; цель продукта: «<20% CPU, <3GB RAM on release builds» — `HEAD:docs/VISION.md:35`. Отдельно сказано, что это плановые оценки, а не бенчмарк каждой машины, — `HEAD:README.md:230`.
**Взять.** Приём «число плюс граница его применимости» для наших карточек замера: в `skills/00b-telemetry-setup/SKILL.md:39-42` метаданные уже описаны, но стоимость сбора не названа ни разу.

**1.3. Живой список обязательств вместо карточек.**
Пайп `commitments` собирает из переписки, встреч и трекеров только явные обещания, поручения, ожидания и сроки — `HEAD:crates/screenpipe-core/assets/pipes/commitments/pipe.md:20-21`; у пункта стабильный `id`, который строится из источника и сути, а не из позиции в списке, — `:23`; «Absence of later evidence is never proof of completion», такой пункт остаётся открытым с меткой `needs review` — `:26`; список ограничен 12 пунктами, пустой массив предпочтительнее выдуманного пункта — `:43`; отправлять письма и закрывать чужие задачи пайп не имеет права — `:28`.
**Взять, главным приёмом раздела.** Это ответ на нашу слабость: в `templates/hadi-tracker.md` есть только две шкалы — `черновик / показан человеку / есть обязательство` (`:7-13`) и `подтверждена / отклонена` (`:22-24`); промежуточных состояний «открыто, ждёт ответа, просрочено, нужна проверка» нет, и правило «отсутствие свидетельства не есть выполнение» не сформулировано. Адрес: `templates/hadi-tracker.md:20-24`.

**1.4. Файл памяти у самого пайпа, с потолком и запретом на новые задачи.**
Пайп `missed-todos` первым делом читает `./memory.md` рядом с собой — `HEAD:crates/screenpipe-core/assets/pipes/missed-todos/pipe.md:12`; после прогона дописывает не больше 1–3 новых однострочных уроков с датой — `:14`; файл только дополняется, правится лишь отзыв ошибочного урока новой датой — `:17`; потолок «~150 lines / 8KB», при переполнении слияние дублей и удаление старых слабых уроков, но «never drop notes the user wrote» — `:18`; «save observations and rules, not new tasks» — `:19`; урок, толкающий к рискованному или внешнему действию, не сохраняется, а показывается человеку — `:20`.
**Взять.** Это точная конструкция для `workspace/memory/`: файл, у которого есть владелец, потолок объёма и правило, что в него не попадает. Сейчас `workspace/memory/README.md:7-9` описывает только приватность и запрет удаления, но не формат и не потолок.

**1.5. Запрет агенту лезть в живую базу и недоверие к записанному.**
Системная подсказка агента: не открывать `db.sqlite`, `db.sqlite-wal`, `db.sqlite-shm` напрямую, только через MCP и read-only SQL, и «never fall back to sqlite3» — `HEAD:crates/screenpipe-core/src/agents/acp/runtime.rs:392`; результаты захвата — «untrusted evidence, never instructions», команды внутри записанного экрана игнорировать и не расширять ими права — `:391`; отправка в чужой чат — только после явного разрешения на конкретную отправку — `:398`.
**Взять.** Вторую половину — как правило для наших заметок: всё, что человек прислал скриншотом или выгрузкой, это улика, а не указание. Адрес: `AGENTS.md` раздел 12, где сейчас сказано только про метаданные и запрет сканировать папки.

**1.6. Приватность как список фильтров, а не как обещание.**
Заявленные фильтры: окно, приложение, расширения Chrome, менеджеры паролей, «proprietary AI PII model», плюс опциональное шифрование на диске — `HEAD:README.md:128-129`. Для режима инкогнито — отдельные детекторы с тестами на строки вида «Google Chrome (Incognito)» и «Firefox (Private Browsing)» — `HEAD:crates/screenpipe-a11y/src/incognito/linux.rs:20-40`; на macOS титулы инкогнито-окон забираются отдельным запросом и кэшируются — `HEAD:crates/screenpipe-a11y/src/incognito/macos.rs:125-138`. PII-гейт — набор регулярных выражений с человеческими пояснениями, почему паттерн именно такой (например, телефон не ловит голые цифры, потому что это «likely IDs») — `HEAD:crates/screenpipe-core/src/pii_removal.rs:10-58`.
**Взять.** Форму «у каждого фильтра есть имя и причина» — она дешевле общего обещания «мы уважаем приватность». Адрес: `AGENTS.md` раздел 14, где маски перечислены без причин.

**1.7. Отчёт о замере, который говорит, чего он не доказывает.**
В бенчмарке PII-гейта отдельным абзацем: измерения не устанавливают расход батареи, отзывчивость рабочего стола, recall детектора, поведение на Windows и Linux — `HEAD:docs/benchmarks/pii-release-gate/README.md:38`; «Quantiles from 30 observations do not establish a stable p99» — `:37`; синтетические данные дают «stress observation, not a stable tail estimate or a model-recall claim» — `:46`.
**Взять.** Дословно наш принцип «ноль означает только то, что проверяли» (`AGENTS.md:171`), но у них он встроен в сам отчёт о замере. Адрес: `skills/00b-telemetry-setup/SKILL.md:58-61`, критерий закрытия цикла.

---

## 2. thedotmack-claude-mem

**Структура.** TypeScript-плагин к агентским средам: `src/` (hooks, worker, storage), `plugin/` (собранный плагин и режимы), `docs/public/` (Mintlify). Память — SQLite (`~/.claude-mem/claude-mem.db`) плюс Chroma для векторного поиска — `internal/research/thedotmack-claude-mem/docs/public/architecture/database.mdx:8-14`. Жизненный цикл — шесть хуков от SessionStart до SessionEnd — `internal/research/thedotmack-claude-mem/README.md:269`.

**2.1. Три слоя выдачи вместо «вывалить всё».**
Сначала индекс (заголовки, даты, типы, цена в токенах), потом детали по запросу, потом исходные файлы — `internal/research/thedotmack-claude-mem/docs/public/progressive-disclosure.mdx:12-14`; SessionStart отдаёт индекс примерно на 800 токенов вместо 25–35 тысяч — `:53-62`, `:280-296`. Отдельное предупреждение: четвёртый слой (сырые тела вызовов, до 64 КБ на строку) нельзя открывать первым и нельзя запрашивать без id из первых трёх слоёв — `:430-439`.
**Взять.** Наш `AGENTS.md:11` требует читать `workspace/state.md` первым, но не говорит, что делать с `workspace/memory/`: сейчас это папка, из которой можно прочитать всё. Нужен индекс памяти с ценой чтения. Адрес: `workspace/memory/README.md`.

**2.2. Решение — отдельный тип записи, а не побочный эффект.**
В схеме есть поле `type` со значением `decision` наравне с `bugfix`, `refactor`, `discovery` — `internal/research/thedotmack-claude-mem/docs/public/architecture/database.mdx:85-91`; в настройках впрыска пример фильтра ровно по решениям: `"CLAUDE_MEM_CONTEXT_OBSERVATION_TYPES": "bugfix,decision,discovery"` — `internal/research/thedotmack-claude-mem/docs/public/configuration.mdx:632`; список концептов включает `why-it-exists` и `trade-off` — `:580-587`.
**Взять.** У нас «Последнее решение» — три строки в `templates/state.md:37-41` (что решили, на каком основании, дата), и в них нет места отвергнутым вариантам: сейчас провал цикла теряется, хотя `workspace/memory/README.md:3` обещает хранить провалы. Нужна запись решения с отвергнутым вариантом и его причиной.

**2.3. Сколько наблюдений подмешивать — числом, с ценой настройки.**
По умолчанию 50 наблюдений из 10 сессий, диапазоны 1–200 и 1–50 — `internal/research/thedotmack-claude-mem/docs/public/configuration.mdx:557-566`; последняя сводка и последнее сообщение по умолчанию НЕ подмешиваются — `:619-620`; полный текст показывается только для 5 последних наблюдений, остальные идут строкой в таблице — `:598-601`; чтение целого файла от 32 КБ блокируется, если по нему уже есть история — `:621`.
**Взять.** Форму «окно памяти имеет число и цену»: у нас лимит есть только на вопросы (`AGENTS.md:126`), лимита на объём памяти нет. Адрес: `templates/state.md`.

**2.4. Приватность на входе, а не на выходе.**
Тег `<private>`: модель видит содержимое в текущей сессии, но в базу оно не попадает — `internal/research/thedotmack-claude-mem/docs/public/usage/private-tags.mdx:22`; вырезается в хуке до записи и «never reaches the database, search indices, or memory agent» — `:158-160`; теги снимаются при сохранении, а не из живого разговора, — `:94`. Авторедакция секретов — опциональный регулярный конвейер, который срабатывает и на то, чего человек не печатал (ключ в ответе curl), — `internal/research/thedotmack-claude-mem/docs/public/usage/auto-redaction.mdx:8`; честные ограничения: поле больше ~1M символов заменяется целиком (`:104`), JSON-стиль `AWS_SECRET_ACCESS_KEY` не ловится (`:105`), Azure и GCP не покрыты (`:106`), и всё это «destructive replacement, not encryption» (`:109`).
**Взять.** Разделение «убрать целиком» и «заменить меткой» плюс список непокрытого. Адрес: `AGENTS.md` раздел 14 и `workspace/LOCAL-ONLY.template:23`, где сейчас одна строка «при сомнении считать секретом» без указания, что маскировка необратима.

**2.5. Чекпоинт и «проверено человеком» — разные вещи.**
Статусы карточки: «In progress» — это последнее сохранённое состояние, а не признак, что агент работает; «Needs you» — работа явно просит человека; «Ready to check» — родительский запрос отчитался о завершении, «a finished subtask does not finish its parent»; «Checked» — человек нажал кнопку, и это «does not certify correctness» — `internal/research/thedotmack-claude-mem/docs/public/usage/my-work.mdx:17-26`; новое содержательное обновление отменяет прежнюю проверку — `:29-31`; «Copy handoff» копирует цель, состояние, следующий шаг и последние обновления, но ничего не отправляет — `:50-52`.
**Взять, третьим приёмом группы.** У нас ступень «показан человеку» ставит только человек, с датой и указанием, кому показал (`templates/hadi-tracker.md:15-16`), но у статуса нет основания: чем именно подтверждено — не сказано, а слово агента «готово» улики не требует. Адрес: `templates/hadi-tracker.md:11-18` и `skills/05-validation-gate`.

**2.6. Телеметрия: включена по умолчанию, но с опубликованным белым списком.**
«It is on by default (opt-out)» — `internal/research/thedotmack-claude-mem/docs/public/telemetry.mdx:10`; локальный лог пишется всегда и в полном виде, а наружу уходит только прошедшее через скруббер — `:22`; таблица «What is NEVER collected»: промпты, пути, код, имена проектов, поисковые запросы, IP, железо, значения переменных окружения — `:264-278`; исключение названо прямо: «error messages and stack traces ARE collected» — `:280`; четыре способа выключить, включая `DO_NOT_TRACK` — `:286-294`; ключи API хранятся только хешем — `internal/research/thedotmack-claude-mem/docs/security.md:5`.
**Взять.** Форму «белый список полей плюс честное исключение». Адрес: `AGENTS.md` раздел 14: у нас режим «только локально» бинарный, промежуточного состояния «наружу уходит вот это и только это» нет.

---

## 3. MemPalace-mempalace

**Структура.** Python-пакет `mempalace/` (miner, searcher, layers, knowledge_graph, backends), `hooks/` (скрипты автосохранения), `mcp_server/`. Долгая память разложена на «крылья, комнаты, ящики»: люди и проекты, дни и сессии, дословный текст — `internal/research/MemPalace-mempalace/CLAUDE.md:13-15`. Индекс — «клозеты», компактные строки-указатели на ящики, — `:16`.

**3.1. Стек пробуждения с бюджетом токенов.**
Четыре слоя: L0 личность ~100 токенов (всегда), L1 «essential story» ~500–800 (всегда), L2 по требованию ~200–500, L3 полный поиск — `internal/research/MemPalace-mempalace/mempalace/layers.py:8-11`; стоимость пробуждения ~600–900 токенов, «leaves 95%+ of context free» — `:13`; чтение только read-only, чтобы не брать чужой замок, — `:47-63`; на весь сбор свежих воспоминаний отведено 300 мс, потому что хук живёт в лимите 500 мс, — `:85-88`.
**Взять, первым приёмом группы.** Это ровно то, чего не хватает нашему чекпоинту: не «сохрани всё», а «в начале сессии прочитай столько-то, остальное по запросу». Адрес: `templates/state.md:5-10` — добавить бюджет чтения в шапку.

**3.2. Потолки производительности как требование, а не пожелание.**
«Hooks under 500ms. Startup injection under 100ms. Memory should feel instant» — `internal/research/MemPalace-mempalace/CLAUDE.md:27`; «Background everything… Zero tokens spent on bookkeeping in the chat window» — `:29`.
**Взять.** Число вместо «быстро». Адрес: `AGENTS.md` раздел 6 («обновлять состояние после каждого шага») — без бюджета это может съесть сессию.

**3.3. Три хука: каждые 15 сообщений, перед сжатием, на выходе.**
Сохранение каждые 15 человеческих сообщений — `internal/research/MemPalace-mempalace/hooks/README.md:28`; SessionEnd уходит в фон, чтобы короткая сессия не потерялась и закрытие не тормозило, — `:29`; PreCompact срабатывает «right before context compaction» и «forces the AI to save EVERYTHING before losing context» — `:30`; захват двухслойный: хук сам вытаскивает сырой вывод инструментов из транскрипта, а модели дополнительно приказывают сохранить — «belt and suspenders» — `:32`. Файл-обёртка прямо называет себя legacy — `internal/research/MemPalace-mempalace/hooks/mempal_precompact_hook.sh:2-4`.
**Взять.** Наш чекпоинт перед исчерпанием контекста существует одной строкой в `internal/draft/24_cloned_tooling.md:57`. Здесь он разложен на три триггера и два независимых слоя записи. Адрес: `AGENTS.md` раздел 6 и `skills/03-prevalidation` (там самые длинные сессии).

**3.4. Задача как конверт с целью и определением готовности.**
`create_task` требует непустые `goal` и `done`, ветку и неизменяемый `base_commit` (не ветку и не тег) — `internal/research/MemPalace-mempalace/mempalace/tasks.py:15-23`, `:60-80`; событие пишется в поток проекта с `correlation_id` — `:89-100`; переносимая строка пробуждения: «Open MemPalace task <id> as <agent>. Claim it, follow its exact definition of done» — `:52-57`.
**Взять.** Форму «одна строка, которой задача передаётся другому исполнителю». Адрес: `templates/hadi-tracker.md` — там есть критерий подтверждения, но нет строки передачи.

**3.5. Санитайзер запроса: тихая деградация поиска.**
Агенты иногда приклеивают к поисковому запросу системный промпт на 2000+ символов, и качество поиска падает с 89,8% до 1,0% R@10 — `internal/research/MemPalace-mempalace/mempalace/query_sanitizer.py:4-7`; лечение ступенчатое, с названным потолком восстановления (~70–80% в худшем случае) и честным словом «Mitigation — not perfect prevention» — `:9-18`.
**Взять.** Как метафору для обезличивания: неудачная замена в тексте не «немного ухудшает», а обнуляет смысл, и это надо мерить. Адрес: `scripts/verify_notes.py` — проверка ссылок уже ловит похожий класс ошибок.

**3.6. Бенчмарк, который сам называет слабое место.**
R@5 96,6% на «сыром» поиске без LLM — `internal/research/MemPalace-mempalace/README.md:245`; «held-out 98,4% is the honest generalisable figure» — `:251-252`; «we do not headline a 100% number because the last 0.6% was reached by inspecting specific wrong answers… teaching to the test» — `:258-260`; отказ от сравнения с соседями, потому что метрики на разных разбиениях несопоставимы, — `:271-275`.
**Взять.** Формулировку отказа от красивого числа. Адрес: `skills/05-validation-gate` — там шкала силы сигнала, но нет правила «не хвалиться максимумом».

**3.7. Локальность как свойство архитектуры.**
«Nothing leaves your machine unless you opt in» — `internal/research/MemPalace-mempalace/README.md:39`; эмбеддинги считаются локально, внешний провайдер только по явной настройке, — `:338`; правило проекта: «External BYOK is always a deliberate user choice, never a default and never a silent fallback» — `internal/research/MemPalace-mempalace/CLAUDE.md:26`; телеметрии нет вовсе — `:28`.
**Взять.** Разделение «локально по умолчанию» и «внешнее по явному выбору» с запретом молчаливого отката. Адрес: `AGENTS.md` раздел 14 — наш `workspace/LOCAL-ONLY` переключается только человеком, но правила «молчаливого отката нет» в тексте не сказано.

---

## 4. elie222-inbox-zero

**Структура.** Монорепо на Turborepo: `apps/web` (Next.js, Prisma), `apps/desktop`, `packages/`, `docs/` (Mintlify). Продукт — две части: фоновый ассистент для Gmail и Outlook и почтовый клиент — `internal/research/elie222-inbox-zero/README.md:35`. Правила фильтрации — «условие + действия», где условие может быть и ИИ-инструкцией, и статическим полем, — `internal/research/elie222-inbox-zero/docs/essentials/email-ai-personal-assistant.mdx:37`, `:43-46`.

**4.1. Необратимое действие требует подтверждения, обратимое — нет.**
Подтверждение спрашивается перед отправкой сообщений и созданием автоматизации, которая умеет писать наружу, — `internal/research/elie222-inbox-zero/docs/essentials/security-and-data.mdx:20`; правило после включения работает само, поэтому совет: сначала тестировать на свежих письмах и смотреть историю — `:22`; при уборке предпочитать метки, папки и архив, потому что «deletion is more difficult to recover» — `:43`; при сбое правила — выключить его, посмотреть запись в истории, применить «Fix», и есть рубильник на весь ящик — `:45`.
**Взять.** Наша шкала «черновик → показан человеку → есть обязательство» (`templates/state.md:18`) — про артефакт, а не про действие. Нужна вторая ось: обратимо или необратимо. Адрес: `AGENTS.md` раздел 11 и `skills/05-validation-gate`.

**4.2. Политика чувствительных данных: разрешить, замазать, заблокировать.**
Настройка ассистента может «allow, redact, or block» найденные учётные данные и номера карт до отправки провайдеру — `internal/research/elie222-inbox-zero/docs/essentials/security-and-data.mdx:26`; тут же оговорка, что это «not a substitute for removing secrets from email» — `:28`. Честный список ограничений ИИ: правило может совпасть с неожиданным письмом, черновик может выдумать допущение, сводка может потерять деталь, ответы зависят от внешних сервисов, — `:32-37`.
**Взять.** Три исхода вместо двух «отправить / не отправлять». Адрес: `AGENTS.md` раздел 14 — сейчас есть только маскировка и запрет, промежуточного «замазать и отправить» нет.

**4.3. Правило проверяется на прошлом, а не на будущем.**
Тест правил прогоняет его по письму или свободному тексту, «Test All» оценивает письмо по всем правилам без применения действий — `internal/research/elie222-inbox-zero/docs/essentials/email-ai-personal-assistant.mdx:106`; по умолчанию на письмо срабатывает одно правило, множественный выбор включается отдельно — `:94`; ассистент учится на исправлениях, а «Fix» объясняет неверное совпадение и обновляет правило — `:98-102`.
**Взять.** Приём «прогон на истории без побочных эффектов» — дешёвая предвалидация правила. Адрес: `skills/03-prevalidation` и `skills/05-validation-gate`; прямого аналога «прогнать на прошлом и не применить» у нас нет.

**4.4. Фильтр с памятью о прошлом и границей охвата.**
Холодные письма отсекаются, но «anyone who has emailed you before always gets through» — `internal/research/elie222-inbox-zero/docs/essentials/cold-email-blocker.mdx:7`; детекция работает только на новых письмах и не переобрабатывает старые — `:33`; отмена ложного срабатывания снимает метку «до 500 бесед» отправителя, но письма остаются там, где лежали, — `:41`; в отписке две разные кнопки: «Unsubscribe» при наличии ссылки и «Block» при её отсутствии — `internal/research/elie222-inbox-zero/docs/essentials/bulk-email-unsubscriber.mdx:28-29`.
**Взять.** Различение «отписаться» и «заблокировать» как модель двух разных решений по одному источнику. Адрес: `skills/01-field-filter` — фильтр поля сейчас не различает «этот человек не мой рынок» и «этот человек попросил не писать».

**4.5. Правило про логи, которое дороже всей остальной приватности.**
PII-поля (`from`, `to`, `subject`) пишутся только на уровне `trace`, исключение — собственный адрес авторизованного пользователя — `internal/research/elie222-inbox-zero/AGENTS.md:34`; в публичном репозитории запрещено помещать непубличные данные и детали закрытых сервисов, о смежной работе говорить обобщённо — `:62`.
**Взять.** Первое — прямое правило для наших отчётов о замере: у нас нет указания, на каком уровне писать имена и темы. Адрес: `AGENTS.md` раздел 14 и `skills/00b-telemetry-setup`.

---

## 5. taskosaur-taskosaur

**Структура.** Монорепо: `backend/` (NestJS, Prisma, BullMQ) и `frontend/` (Next.js), плюс `docker/`, `scripts/`. Ассистент живёт в модуле `backend/src/modules/ai-chat/` и правит приложение через браузерную автоматизацию: «click», «type», «select», «press_enter» — `internal/research/taskosaur-taskosaur/backend/src/modules/ai-chat/ai-chat.service.ts:373-378`. Правила автоматизации — отдельный модуль поверх очереди — `internal/research/taskosaur-taskosaur/backend/src/modules/automation/automation.service.ts:22`.

**5.1. «Сначала спроси, потом действуй» — и запрет спрашивать лишнее.**
При любом создании, изменении или удалении агент сначала проверяет, есть ли у него всё нужное (рабочее пространство, проект, имя задачи), и при нехватке отвечает `ASK:` до любого действия — `internal/research/taskosaur-taskosaur/backend/src/modules/ai-chat/ai-chat.service.ts:393`; «NEVER guess or assume which workspace, project, or entity to use» — `:404`; по необязательным полям (описание, приоритет, срок) не спрашивать — `:405`; один вопрос за раз, начиная с самого важного — `:406`.
**Взять.** Форму «список обязательных полей, без которых действие запрещено», вместо нашего «лишний вопрос лучше правдоподобного вымысла» (`AGENTS.md:27`) без перечня. Адрес: `skills/04-mvp-artifact` — там таких обязательных полей нет.

**5.2. Свой же выдуманный текст как способ обойти требование.**
В правилах создания рабочего пространства: поле описания обязательное, кнопка создания неактивна без него, и «If the user didn't provide a description, invent a simple one» — `internal/research/taskosaur-taskosaur/backend/src/modules/ai-chat/ai-chat.service.ts:426`.
**Отклонить.** Это ровно наша граница: выдуманное поле выглядит как данные человека и переживёт сессию. Адрес запрета: `AGENTS.md` раздел 7 («не выдумывать инструменты, цифры и факты»).

**5.3. Что не записано, то потеряно — и агент повторяет действия.**
История берётся из базы (`chatMessage`, последние 40 сообщений на беседу) — `internal/research/taskosaur-taskosaur/backend/src/modules/ai-chat/ai-chat.service.ts:585-593`; но результаты шагов браузерной автоматизации («Action completed») никогда не сохраняются, и раньше предпочтение истории из базы оставляло агента слепым: он повторял действия до предела итераций — `:607-612`.
**Взять, главным приёмом раздела.** Это доказательство тезиса «чат не память» (`AGENTS.md:62`) на чужом баге: несохранённый шаг не просто забыт, он воспроизводится заново. Адрес: `AGENTS.md` раздел 6 и чекпоинт перед исчерпанием контекста.

**5.4. Беседа как журнал, а не как файл состояния.**
Беседа создаётся строкой в базе с заголовком «New Chat» — `internal/research/taskosaur-taskosaur/backend/src/modules/ai-chat/ai-chat.service.ts:576-582`; сообщения ограничены 40 последними, а контекст страницы подмешивается к запросу полями `Task:` и `Current URL:` — `:623-629`.
**Отклонить** как образец памяти: это лог переписки, из которого нельзя достать решение, причину и отвергнутые варианты. Адрес альтернативы: `workspace/memory/README.md:3`.
**Взять** узко: привязку «где мы находимся» (страница, проект, задача) к каждому сообщению — у нас эту роль играет `workspace/state.md`, но он не привязан к шагу разговора.

**5.5. Секреты — шифрованием, с флагом на каждую настройку.**
Значения настроек шифруются, если у ключа стоит `isEncrypted`, — `internal/research/taskosaur-taskosaur/backend/src/modules/settings/settings.service.ts:71-73`; пароли IMAP и SMTP помечены как зашифрованные в схеме — `internal/research/taskosaur-taskosaur/backend/prisma/schema.prisma:1158`, `:1168`; ключ Trello — «AES-256-GCM encrypted» — `:1347`.
**Взять.** Флаг «это значение секретное» на уровне поля, а не на уровне файла. Адрес: `workspace/LOCAL-ONLY.template:23` — сейчас секретность определяется на глаз перед отправкой.

---

## 6. didhd-personal-ai-task-assistant

**Структура.** Восемнадцать файлов, Python: `src/app.py` (Streamlit), `src/task_manager.py` (узлы planner, task_executor, project_updater, replanner), `src/state.py` (TypedDict состояния), `src/tools.py` (четыре инструмента). Состав графа — `internal/research/didhd-personal-ai-task-assistant/README.md:14-32`.

**6.1. Состояние шага описано полями.**
`messages`, `plan`, `goals`, `past_actions`, `current_task`, `response`, `context`, `current_node` — `internal/research/didhd-personal-ai-task-assistant/src/state.py:6-14`; `messages` и `past_actions` накапливаются оператором сложения — `:7`, `:10`.
**Взять** как чек-лист полноты: у нас «что сделано» — свободный текст, а не поле. Адрес: `templates/state.md:9` («Что сделано») и `:37-41`.

**6.2. Состояние живёт только в памяти вкладки.**
Модель, ввод, статусы шагов и прогресс лежат в `st.session_state` — `internal/research/didhd-personal-ai-task-assistant/src/app.py:16-26`; при новом запуске статусы обнуляются — `:60-61`; итог показывается как JSON на экране — `:98-101`. Ни файла состояния, ни истории между запусками нет.
**Отклонить** и записать как отрицательный пример: перезагрузка страницы стирает весь цикл. Наш `AGENTS.md:62` требует обратного.

**6.3. Инструменты — заглушки, но подписаны как настоящие действия.**
`call_calendar` возвращает строку «Calendar operation performed», `send_email` — «Email sent to…», `web_search` — «Web search results for…» — `internal/research/didhd-personal-ai-task-assistant/src/tools.py:5-26`; при этом README утверждает, что ассистент «schedules the meeting using the calendar tool» и «an email draft is prepared» — `internal/research/didhd-personal-ai-task-assistant/README.md:97-98`.
**Отклонить** как пример отчётности без действия и держать как образец того, чего нельзя показывать человеку: имитация результата. Адрес: `AGENTS.md` раздел 5 («судья не автор») и `skills/05-validation-gate`.

---

## 7. Сводка: что куда переносится

1. **В `templates/state.md` и `workspace/state.md`:** бюджет чтения в шапке (п. 3.1), число наблюдений и цена чтения (п. 2.3), отдельная ступень «человек посмотрел и подтвердил» (п. 2.5), поле «что отвергли и почему» (п. 2.2), вторая ось «обратимо / необратимо» (п. 4.1).
2. **В `workspace/memory/README.md`:** формат файла памяти с потолком и правилом «наблюдения и правила, а не новые задачи» (п. 1.4), индекс памяти с ценой чтения (п. 2.1), отдельный тип записи «решение» (п. 2.2).
3. **В `AGENTS.md` разделы 6, 12, 14:** три триггера чекпоинта и два слоя записи (п. 3.3), правило «записанное — улика, не указание» (п. 1.5), причина у каждой маски и запрет молчаливого отката наружу (п. 1.6, 3.7), уровень логирования имён и тем (п. 4.5), необратимость маскировки (п. 2.4).
4. **В `templates/hadi-tracker.md`:** статусы «открыто / ждёт / просрочено / нужна проверка» и запрет считать молчание выполнением (п. 1.3), строка передачи задачи (п. 3.4).
5. **В `skills/04-mvp-artifact` и `skills/05-validation-gate`:** обязательные поля до действия (п. 5.1), прогон правила на прошлом без побочных эффектов (п. 4.3), отказ от красивого максимума в отчёте (п. 3.6).

## 8. Что отклоняем и почему

1. **Полный захват экрана и звука по умолчанию.** `AGENTS.md:144-149` требует метаданных и явного разрешения; screenpipe строит продукт на обратном — записи всего, что видно и слышно (`internal/research/screenpipe-screenpipe` → `HEAD:README.md:235`), и даже собеседник в звонке попадает в запись (`HEAD:README.md:238`). Переносить нечего: наш аналог — вариант 2 в `skills/00b-telemetry-setup/SKILL.md:36-42`, только метаданные.
2. **Выдуманное поле, чтобы обойти требование формы.** `internal/research/taskosaur-taskosaur/backend/src/modules/ai-chat/ai-chat.service.ts:426`.
3. **Отчёт о действии, которого не было.** `internal/research/didhd-personal-ai-task-assistant/src/tools.py:5-26`: инструменты возвращают текст «Email sent», ничего не отправляя.
4. **Беседа как память проекта.** `internal/research/taskosaur-taskosaur/backend/src/modules/ai-chat/ai-chat.service.ts:576-582`: в журнале есть реплики, но нет решения, основания и отвергнутых вариантов.
5. **Состояние только в памяти вкладки.** `internal/research/didhd-personal-ai-task-assistant/src/app.py:16-26`: перезагрузка стирает цикл.
6. **Телеметрия, включённая по умолчанию.** `internal/research/thedotmack-claude-mem/docs/public/telemetry.mdx:10`. Берём форму (белый список и честное исключение), но не режим: у нас внешний запрос — решение человека (`AGENTS.md:186`).
7. **Автоматизация с правом писать в чужие сервисы.** Даже screenpipe запрещает пайпу отправлять письма и закрывать задачи (`internal/research/screenpipe-screenpipe` → `HEAD:crates/screenpipe-core/assets/pipes/commitments/pipe.md:28`); у нас такого класса действий нет и не появится.
8. **Ресурсные оценки как факт.** `internal/research/screenpipe-screenpipe` → `HEAD:README.md:125-128` годится только вместе с оговоркой из `HEAD:README.md:230`.

## 9. Чего в клонах нет

- **Нашего главного гейта нет ни в одном.** Ни один клон не отвечает на вопрос «а заплатит ли за это живой человек»: у screenpipe монетизация вынесена в README и тарифы (`internal/research/screenpipe-screenpipe` → `HEAD:README.md:306-312`), у остальных её нет вовсе.
- **Провал как запись.** Все шесть хранят успех и текущее состояние; закрытого «почему отказались» с причиной не нашлось нигде, кроме свободного текста. Наш `workspace/memory/README.md:3` обещает хранить провалы — у клонов перенимать нечего.
- **Юридических оговорок про персональные данные почти нет.** В прочитанных README и `docs/` нашлось два места: «SOC 2 is an attestation, not a product certification», «HIPAA suitability depends on your deployment» (`internal/research/screenpipe-screenpipe` → `HEAD:README.md:340`) и «review the Privacy Policy» для хостинга (`internal/research/elie222-inbox-zero/docs/essentials/security-and-data.mdx:49`). Про согласие второго человека на запись разговора, сроки хранения и удаление по запросу — ни строки, так что этот раздел методики клоны не подпирают.
- **Замера стоимости памяти.** Никто не считает, сколько времени и токенов стоит запись одного решения; есть только потолки (п. 2.3 и 3.1).
- **Согласия второго человека.** У screenpipe записывается и собеседник в звонке (`internal/research/screenpipe-screenpipe` → `HEAD:README.md:238`), но механизма «он согласен» нет: только фильтры, пауза и отключение приложений.

## 10. Спорные утверждения списка

1. **«Около 0,5–3 ГБ оперативной памяти» — подтвердилось, но как оценка, а не замер.** `internal/research/screenpipe-screenpipe` → `HEAD:README.md:126` и `HEAD:README.md:402` называют одну и ту же вилку; цель в `HEAD:docs/VISION.md:35` — «<3GB RAM on release builds», и там же оговорка «planning estimates, not fixed limits or a benchmark for every machine» (`HEAD:README.md:230`). Вилка существует, но это заявление владельца продукта о своём продукте без опубликованного замера; цифры CPU 5–20% даны так же. В клоне есть бенчмарк, который меряет пиковую память процесса (`HEAD:docs/benchmarks/pii-release-gate/README.md:38`), но это профиль сборки, а не суточный захват.
2. **«Подмешивает решения в будущие диалоги» — подтвердилось с оговоркой.** Решение — отдельный тип наблюдения в схеме (`internal/research/thedotmack-claude-mem/docs/public/architecture/database.mdx:86`), тип включается в впрыск (`internal/research/thedotmack-claude-mem/docs/public/configuration.mdx:632`), впрыск идёт на SessionStart (`internal/research/thedotmack-claude-mem/README.md:269` и `internal/research/thedotmack-claude-mem/docs/public/architecture/overview.mdx:149`). Оговорка: в новую сессию попадает **индекс** последних наблюдений (по умолчанию 50 из 10 сессий — `internal/research/thedotmack-claude-mem/docs/public/configuration.mdx:557-566`), а полный текст решения — только если агент его дозапросит (`internal/research/thedotmack-claude-mem/docs/public/progressive-disclosure.mdx:264-269`). «Подмешивает решения целиком» файлами не подтверждается.
3. **«Диалоговый интерфейс вместо карточек трекера» — не подтвердилось для taskosaur.** README прямо перечисляет полноценный трекер: «Kanban boards, sprints, task dependencies, time tracking» (`internal/research/taskosaur-taskosaur/README.md:34`), а в бэкенде живут отдельные модули `sprints`, `gantt`, `task-ranks`, `task-statuses` (`internal/research/taskosaur-taskosaur/backend/src/modules`). Разговорный слой надстроен над карточками, а не заменяет их: «combines traditional project management features with Conversational AI Task Execution» (`internal/research/taskosaur-taskosaur/README.md:25`). Заменяет карточки только маленький `didhd-personal-ai-task-assistant`, и там это как раз слабое место: состояние живёт в памяти вкладки (`internal/research/didhd-personal-ai-task-assistant/src/app.py:16-26`), а инструменты — заглушки (`internal/research/didhd-personal-ai-task-assistant/src/tools.py:5-26`).
