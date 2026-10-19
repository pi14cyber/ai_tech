# Персональная эффективность, выжимки и локальный ресёрч: что переносится

Источники (только чтение, клоны не менялись; в сеть не ходил, ничего не устанавливал):

- `internal/research/danielmiessler-fabric` — `a7ef0a1`, 2026-10-19, Go + Markdown-шаблоны, 27,7 МБ.
- `internal/research/LearningCircuit-local-deep-research` — `683a967`, 2026-10-19, Python + FastAPI, 67,9 МБ.
- `internal/research/assafelovic-gpt-researcher` — `3582a68`, 2026-10-10, Python + JavaScript, 25,8 МБ.
- `internal/research/AgriciDaniel-claude-obsidian` — `b0d8867`, 2026-10-17, Python + Markdown-навыки, 3,0 МБ.
- `internal/research/khoj-ai-khoj` — `ae229ca`, 2026-08-02, Python + TypeScript, 81,3 МБ.
- `internal/research/raold-second-brain` — `7bf52b2`, 2026-05-10, Python + Svelte, 4,9 МБ.

Коммиты и даты сверены с `internal/research/_clones.tsv:36-41`.

Ссылки: `путь:строка`. Утверждается только прочитанное в файлах.

Навыка «документы» в наборе нет: его роль играют карточка знания (`templates/knowledge-card.md`) и шаблон ответа исследователя (`templates/research-response.md`), поэтому адреса «Взять» ведут туда, в предвалидацию и в память проекта.

---

## 1. danielmiessler-fabric

**Структура.** Go-CLI: `cmd/` — вход, 11 пакетов в `internal/` (`cli`, `core`, `plugins`, `tools`), `web/` — интерфейс на Svelte. Содержание лежит отдельно от кода: 265 каталогов `internal/research/danielmiessler-fabric/data/patterns/<имя>/system.md` и 9 стратегий в `internal/research/danielmiessler-fabric/data/strategies/`; `docs/` — гайды и три примера workflow.

**1.1. Шаблон — документ с закрытым скелетом.**
`internal/research/danielmiessler-fabric/data/patterns/create_pattern/system.md:7-17` называет обязательные разделы шаблона: IDENTITY and PURPOSE, STEPS, OUTPUT INSTRUCTIONS, EXAMPLE; файл заканчивается секцией `INPUT:` (`:37`). Скелет повторяется, но не строго: раздел IDENTITY есть в 251 шаблоне из 265, OUTPUT INSTRUCTIONS — в 209. Шаблон собирается из текста человека, а не из кода.
**Взять.** В `templates/knowledge-card.md:29-37` правила карточки фиксируют паспорт и три раздела, но не запрещают дописывать свои. Добавить правило: разделы 1–3 не переименовываются и не дополняются, новый раздел — новая версия шаблона.

**1.2. Длина единицы выжимки задана в словах.**
`internal/research/danielmiessler-fabric/data/patterns/extract_wisdom/system.md:31-45`: каждый пункт ровно 16 слов, IDEAS не меньше 25, INSIGHTS не меньше 10; ONE-SENTENCE TAKEAWAY — 15 слов (`:23`). Это не стиль: длину видно машиной, воду — тоже.
**Взять.** Пункт раздела 1 карточки сейчас без лимита (`templates/knowledge-card.md:17-21`). Одна строка, до 25 слов, цитата отдельным полем — тогда выжимку проверяет скрипт, а не глаз.

**1.3. Проверка утверждения: обе стороны и запрет выдумывать ссылки.**
`internal/research/danielmiessler-fabric/data/patterns/analyze_claims/system.md:22-27` на каждое утверждение требует доказательства за и опровержение с ссылками и прямо запрещает выдумывать: ссылки должны быть внешне проверяемыми, «DO NOT make any of those up».
**Взять.** Наш контракт «факты за / факты против» есть (`templates/research-response.md:16-18`), но он не запрещает ссылку из головы. Добавить в `templates/research-response.md:126-131` строку: адрес проверяем, а не просто присутствует.
**Отклонить.** Балл A–F за утверждение и OVERALL SCORE (`internal/research/danielmiessler-fabric/data/patterns/analyze_claims/system.md:31-44`): это ИИ оценивает истинность. У нас валидацию даёт только рынок (`AGENTS.md:38`), а сила сигнала считается по цене, а не по мнению модели.

**1.4. Цепочка шагов вместо одного шаблона.**
`internal/research/danielmiessler-fabric/docs/Using-Workflows.md:3` — workflow гоняет шаблоны подряд, выход шага идёт на вход следующего; `internal/research/danielmiessler-fabric/docs/examples/fact-checked-brief.yaml:8-17` — сначала разбор утверждений сильной моделью, потом сводка дешёвой. До запуска файл проверяется целиком: нет шагов, нет `pattern`, два одинаковых шаблона подряд — ошибка (`internal/research/danielmiessler-fabric/docs/Using-Workflows.md:77-84`).
**Взять.** Полный запрос как два шага: пакет 1 — факты, пакет 2 — только белые пятна первого, без повтора вопросов. Проверку «нет пустых и нет двух одинаковых вопросов» добавить в `scripts/verify_research.py`; сухой прогон (`internal/research/danielmiessler-fabric/docs/Using-Workflows.md:67`) печатает, что уйдёт, но не отправляет, — это и есть шаг «показать запрос человеку».

**1.5. Транскрипт как вход и адрес вместо строки.**
`internal/research/danielmiessler-fabric/README.md:720` — `-y/--youtube` берёт транскрипт и комментарии, `:733` — `--spotify` метаданные подкаста. Для видео нет строки, есть время.
**Взять.** `templates/knowledge-card.md:15` требует «номер строки в книге»; для ролика и подкаста адрес — таймкод, иначе выжимку не проверить.
**Отклонить.** PDF через отдельный бинарь `to_pdf` и LaTeX (`internal/research/danielmiessler-fabric/README.md:1024-1050`): второй тулчейн, к методике не относится, Markdown достаточно.

---

## 2. LearningCircuit-local-deep-research

**Структура.** Python-пакет `internal/research/LearningCircuit-local-deep-research/src/local_deep_research/` — 33 подпакета (`advanced_search_system`, `citation_handlers`, `journal_quality`, `web_search_engines`, `exporters`), веб на FastAPI (`internal/research/LearningCircuit-local-deep-research/pyproject.toml:120-130`, где Flask назван выбывшим — `:179`), 2378 файлов в `tests/`, Docker. Академические движки — arXiv, PubMed, Semantic Scholar, OpenAlex, NASA ADS — регистрируются в `internal/research/LearningCircuit-local-deep-research/src/local_deep_research/web_search_engines/engine_registry.py:30-31,64-65,147-148`.

**2.1. Ресёрч как цикл: вопросы → параллельный поиск → фильтр → синтез с цитатами.**
`internal/research/LearningCircuit-local-deep-research/src/local_deep_research/advanced_search_system/strategies/source_based_strategy.py:34-64`: 5 итераций, со второй вопросы строятся из накопленного; вопросы итерации ищутся параллельно; после всех итераций работает кросс-движковый фильтр; номера цитат смещаются, чтобы продолжаться между разделами; единый список источников — источник правды для библиографии.
**Взять.** В `skills/03-prevalidation/SKILL.md:27` полный запрос — один заход. Добавить раунд 2 по белым пятнам (до трёх вопросов) и правило «раунд без новых ссылок — стоп». Это дешевле, чем сразу пятнадцать вопросов.

**2.2. Нет источников — отказ, а не ответ.**
`internal/research/LearningCircuit-local-deep-research/src/local_deep_research/citation_handlers/base_citation_handler.py:416-438`: если список источников пуст, обработчик не вызывает модель и возвращает явный текст: без ссылок ответ опирался бы на память модели и мог содержать выдуманные цитаты.
**Взять.** Машинное правило для `scripts/verify_research.py`: блок `Q` с нулём ссылок не может иметь статус «отвечено». Сейчас это только проза (`templates/research-response.md:129`).

**2.3. Библиография собирается программой, модель только нумерует.**
`internal/research/LearningCircuit-local-deep-research/src/local_deep_research/citation_handlers/standard_citation_handler.py:70-81`: модель просят ставить `[1]`, `[2]` в тексте, прямо запрещают писать список источников («links are added automatically») и запрещают выдумывать источники. Список собирается из метаданных документов (`:51-55`), а в отчёт попадают ссылки, у которых есть номер в тексте; при неразборчивом разборе номеров режим по умолчанию отдаёт весь список, чтобы не терять библиографию (`internal/research/LearningCircuit-local-deep-research/src/local_deep_research/utilities/search_utilities.py:484-510,1185-1197`; вызов — `internal/research/LearningCircuit-local-deep-research/src/local_deep_research/report_generator.py:1686-1700`).
**Взять.** Таблицу покрытия (`templates/research-response.md:106-124`) заполняет скрипт: считает ссылки в блоках `Q` сам и сравнивает с заявленным числом. Число источников считать по каноническому URL, а не по строкам (`internal/research/LearningCircuit-local-deep-research/src/local_deep_research/utilities/search_utilities.py:1257-1270`).

**2.4. Порог отсечения: убирать только доказанный мусор.**
`internal/research/LearningCircuit-local-deep-research/docs/journal-quality.md:25-32`: порог по умолчанию 2 отсекает только хищнические журналы, а источники без библиометрии намеренно не удаляются — там сказано, что система не стирает молча то, о чём у неё нет данных. Оценки не сплошные — выдаются `{1,4,5,6,7,8,10}` (`:7`), а у метода названо смещение h-index по дисциплинам (`internal/research/LearningCircuit-local-deep-research/src/local_deep_research/journal_quality/scoring.py:78-81`).
**Взять.** Правило разбора ответа: источник отбрасывается по положительному признаку (фейк, ошибка, реклама), а не по «не нашёл данных»; незнакомый идёт в `[внешнее]` с пометкой. Адрес — `skills/03-prevalidation/SKILL.md:95-100`.
**Отклонить.** Сам числовой рейтинг журналов: наши темы — ставки, инструменты, практики, квартили и h-index для них пусты.

**2.5. Справочник компилируется и открывается только на чтение.**
`internal/research/LearningCircuit-local-deep-research/src/local_deep_research/journal_quality/db.py:1-21`: пять gzip-снапшотов (OpenAlex, DOAJ, Stop Predatory Journals, JabRef, Institutions) собираются в один SQLite; рантайм открывает его `mode=ro` и `immutable=1`, файл получает `chmod 0o444`, кросс-модульное открытие без `mode=ro` запрещено pre-commit-хуком. Единственный писатель — `build_db()`.
**Взять.** Для `knowledge/INDEX.md`: индекс должен генерироваться из паспортов карточек одной командой, как уже сделано для состояния (`templates/request-full.md:10`), а руками правится только карточка. Тогда расхождение «файл есть, строки в индексе нет» невозможно по построению, а не ловится после (`knowledge/INDEX.md:41-46`).
**Отклонить.** SQLCipher с паролем на пользователя (`internal/research/LearningCircuit-local-deep-research/src/local_deep_research/database/encrypted_db.py:894-904`): у нас нет БД и нет чужих персональных данных в репозитории, приватность решается файлом `workspace/LOCAL-ONLY` (`AGENTS.md:183`).

**2.6. Заявленный в коде бенчмарк — не доказательство.**
`internal/research/LearningCircuit-local-deep-research/src/local_deep_research/advanced_search_system/strategies/focused_iteration_strategy.py:1-20` заявляет 96,51% на SimpleQA и требует «сохранить стратегию»; конфигурация — 8 итераций по 5 вопросов (`:66-67`). Цифра живёт в docstring, методики замера рядом нет.
**Отклонить** как довод: тот же класс, что «улучшили на 40%» в README. Для стрима годится только то, что перепроверяется командой.

---

## 3. assafelovic-gpt-researcher

**Структура.** Python-пакет `internal/research/assafelovic-gpt-researcher/gpt_researcher/` — 12 подпакетов (`actions`, `skills`, `retrievers`, `scraper`, `context`, `mcp`), FastAPI в `backend/` (`internal/research/assafelovic-gpt-researcher/backend/server/app.py:14,97`), статический `frontend/` на HTML, CSS и JS, отдельно `multi_agents/` и `evals/`; документация — Docusaurus в `docs/`.

**3.1. Параллельность по подзапросам, а не по числу источников.**
Подзапросы идут одновременно (`internal/research/assafelovic-gpt-researcher/gpt_researcher/skills/researcher.py:289-295`), но потолки жёсткие: 5 результатов на запрос, 3 итерации, 3 подтемы, 15 воркеров скрапера (`internal/research/assafelovic-gpt-researcher/gpt_researcher/config/variables/default.py:22,26,29,31`); глубокий ресёрч — ширина 3, глубина 2, параллельность 4 (`:40-42`), на спуске ширина делится вдвое (`internal/research/assafelovic-gpt-researcher/gpt_researcher/skills/deep_research.py:540-543`).
**Взять.** Наш предел «шесть вопросов в пакете» — та же инженерия, и её стоит назвать в `templates/request-full.md:3` потолком, а не вкусом. Плюс правило «раунд без успешных результатов останавливает спуск» (`internal/research/assafelovic-gpt-researcher/gpt_researcher/skills/deep_research.py:507-511`).
**Отклонить.** «Более 20 источников» как обещание: разбор в разделе спорных утверждений.

**3.2. Список литературы — из посещённых адресов и отсортированный.**
`internal/research/assafelovic-gpt-researcher/gpt_researcher/actions/markdown_processing.py:101-124`: `## References` дописывается программой из множества посещённых URL; в комментарии сказано, что порядок зависел от итерации множества и отчёт был невоспроизводим, поэтому добавлена сортировка.
**Взять.** Детерминизм как требование к нашим файлам: ссылки в блоке — в порядке появления, итоговый список отсортирован, повторный прогон даёт тот же файл, и diff показывает смысл, а не перестановку.

**3.3. Глубина — параметр, а не пожелание.**
`internal/research/assafelovic-gpt-researcher/gpt_researcher/skills/deep_research.py:240-255`: прогресс хранит текущую глубину и ширину, значения приходят из конфига, а не из промпта.
**Взять.** В шапку запроса — числа (раундов, вопросов, слов), чтобы «короткий» и «полный» различались цифрами. Сейчас числа есть только в `skills/03-prevalidation/SKILL.md:18-25`, в шаблоне — «до 2500 слов» (`templates/request-full.md:3`).

---

## 4. AgriciDaniel-claude-obsidian

**Структура.** 15 навыков в `internal/research/AgriciDaniel-claude-obsidian/skills/` (`wiki`, `save`, `wiki-ingest`, `wiki-query`, `wiki-lint`, `autoresearch`, `wiki-mode`, `wiki-retrieve`), переносимое ядро на stdlib в `claude_obsidian/`, 16 скриптов в `scripts/` (`bm25-index.py`, `retrieve.py`, `rerank.py`), шаблон хранилища в `templates/vault/`.

**4.1. Контракт ресёрча до первого запроса.**
`internal/research/AgriciDaniel-claude-obsidian/skills/autoresearch/SKILL.md:31-49`: до старта согласуются тема и исключения, разрешение на выход в сеть, домены и классы источников, бюджеты (раунды, поиски, загрузки, время, страницы) и стоп-условие; по умолчанию 3 раунда, 5 источников за раунд, 15 страниц (`:45-46`); после каждого раунда — отчёт о расходе бюджета (`internal/research/AgriciDaniel-claude-obsidian/skills/autoresearch/references/program.md:23-25`).
**Взять.** В шапку `templates/request-full.md:5-10` добавить три поля: раундов, источников на вопрос, стоп-условие. Сейчас там только «до 2500 слов» и «минимум два канала».

**4.2. Контр-позиция входит в список вопросов.**
`internal/research/AgriciDaniel-claude-obsidian/skills/autoresearch/SKILL.md:55-56` требует разложить тему на вопросы, «включая правдоподобную контр-позицию»; `:62-63` — искать пробелы и противоречия, а не новые примеры ведущей точки зрения; `internal/research/AgriciDaniel-claude-obsidian/skills/autoresearch/references/program.md:12` — то же про контр-доказательства.
**Взять.** Один из шести вопросов пакета обязан быть «кто пробовал и отказался / при каких условиях практика не работает». Сейчас симметрия держится на «фактах против» внутри каждого вопроса, отдельного вопроса-опровержения нет (`templates/request-full.md:20-28`).

**4.3. Три отдельных реестра и словарь состояний.**
`internal/research/AgriciDaniel-claude-obsidian/skills/wiki/references/provenance.md:14-23`: манифест загрузки, реестр источников и реестр утверждений — разные файлы, «не перегружать один реестр тремя работами». Источник: `authority` из набора official / primary / secondary / community / synthetic / unknown, `review_state` (unreviewed, active, superseded, rejected), `independence_key` для зависимых источников (`:25-38`). Утверждение: accepted / provisional / contested / unsupported / deprecated; принятое высокорисковое — два независимых источника (`:40-49`).
**Взять.** Паспорт карточки (`templates/knowledge-card.md:2-9`) дополнить `authority` и `independence_key`, а белым пятнам дать состояние `unsupported`. Тогда «два и более независимых канала» (`AGENTS.md:48`) перестаёт быть лозунгом: два канала с одним пресс-релизом — один источник.
**Отклонить.** SHA-256 каждой загрузки и `refresh_due` (`internal/research/AgriciDaniel-claude-obsidian/skills/wiki/references/provenance.md:27-32`): у нас карточка, а не архив байтов, хватает `date_verified` и `freshness_ttl` (`templates/knowledge-card.md:4-8`).

**4.4. Проверка отдельно от починки.**
`internal/research/AgriciDaniel-claude-obsidian/skills/wiki-lint/SKILL.md:8-9` — линт наблюдает и не создаёт отчётов и правок; `:41-52` — детерминированный разбор и прямой запрет заявлять семантические проверки, которых не было; `:66-77` — починка отдельной операцией: перечитать цели, записать хеши, собрать один пакет, показать пути, применить, прогнать линт заново и сравнить.
**Взять.** Два правила в `AGENTS.md` §13 (`:157-177`): проверка ничего не чинит сама, и после починки нужен повторный прогон со сравнением находок. Требование называть покрытие у нас уже есть (`:171`), запрета на авто-починку — нет.

**4.5. Аварийный поиск без модели.**
`internal/research/AgriciDaniel-claude-obsidian/scripts/bm25-index.py:1-6` — чистый stdlib, Okapi BM25 с k1=1.5 и b=0.75, один JSON-индекс, полная пересборка (`:41`); `internal/research/AgriciDaniel-claude-obsidian/scripts/retrieve.py:13-22` — если реранкер не может посчитать эмбеддинги, остаётся порядок BM25, а не пустая выдача.
**Взять.** Режим «модель недоступна» должен давать ответ по индексу и тексту, а не «попробуйте позже». У нас `knowledge/INDEX.md` уже маршрутизатор (`knowledge/INDEX.md:3`), но правила «читать индекс и карточки без ИИ» не записано.
**Отклонить.** Свою реализацию BM25: база на десятки карточек, grep по `knowledge/` дешевле и объяснимее.

**4.6. Память проекта с бюджетом.**
`internal/research/AgriciDaniel-claude-obsidian/templates/vault/wiki/hot.md:12-27` — четыре раздела: последнее обновление, ключевые недавние факты, недавние изменения, активные нити; `internal/research/AgriciDaniel-claude-obsidian/skills/save/SKILL.md:75` ограничивает hot-файл 500 словами; `internal/research/AgriciDaniel-claude-obsidian/skills/wiki/SKILL.md:78` запрещает писать туда транскрипт.
**Взять.** `templates/state.md` (45 строк) не имеет лимита и раздела «активные нити»: добавить потолок около 500 слов и правило «транскрипт в состояние не попадает». Иначе `state.md` превращается в чат.

**4.7. «Локально» — это список исключений.**
`internal/research/AgriciDaniel-claude-obsidian/PRIVACY.md:3-7`: ядро в сеть не ходит, но агент, веб-инструмент или внешний адаптер могут отправить контент провайдеру; `:30-42` перечисляет, что считается выходом, и отдельно — что удалённый Ollama отклоняется без явного согласия (`:39`).
**Взять.** В `workspace/LOCAL-ONLY.template:5-9` перечислены категории запрета, но не сказано, что «локальная модель» — только на этом же хосте. Добавить строку «модель на другом хосте = внешний запрос» и к `workspace/LOCAL-ONLY.template`, и к `AGENTS.md:183`.

---

## 5. khoj-ai-khoj

**Структура.** Django-приложение `internal/research/khoj-ai-khoj/src/khoj/` — 8 подпакетов (`app`, `database`, `processor`, `routers`, `search_type`, `search_filter`, `interface`, `utils`), Postgres + pgvector, Docusaurus-документация в `documentation/`. Источники данных: PDF, Markdown, org-mode, Word, Notion (`internal/research/khoj-ai-khoj/README.md:47`).

**5.1. Двухступенчатый поиск с порогом уверенности.**
`internal/research/khoj-ai-khoj/documentation/docs/features/search.md:20-24`: би-энкодер строит векторы, кросс-энкодер переранжирует; `:46-48` — порог уверенности от 0 до 1 отсекает далёкие документы и его надо подбирать под модель. В коде: `internal/research/khoj-ai-khoj/src/khoj/search_type/text_search.py:125` — `top_k = 10`, `:251-257` — сначала сортировка по би-энкодеру, потом по кросс-энкодеру, `:141-164` — в результат кладутся файл, URI и заголовок раздела.
**Взять.** Адрес внутри источника. `templates/knowledge-card.md:15` требует строку, но карточка не хранит раздел; для больших документов адрес — «раздел + строка», иначе проверка цитаты упирается в файл.
**Отклонить.** Векторный поиск и реранкер: десятки карточек дешевле искать по индексу-маршрутизатору.

**5.2. Фильтры запроса как отдельный синтаксис.**
`internal/research/khoj-ai-khoj/documentation/docs/miscellaneous/query-filters.md:9-24`: слово (`+"термин"`), дата (`dt>=`), файл (`file:`), и всё это приклеивается к естественному вопросу.
**Взять.** В `templates/research-queue.md:9-16` у задания нет ни периода, ни типа источника. Добавить поля «период», «тип источника», «что исключить»: без них белое пятно не отличить от «искали не там».

**5.3. Интеграция снимается, а список источников — нет.**
`internal/research/khoj-ai-khoj/documentation/docs/data-sources/github_integration.md:4`: интеграция не поддерживается, рассматривается снятие. При этом код репозиториев на месте (`internal/research/khoj-ai-khoj/src/khoj/processor/content/github/github_to_entries.py:1`), а список источников в `internal/research/khoj-ai-khoj/README.md:47` GitHub уже не упоминает: документ и код расходятся в оценке того, что поддерживается.
**Взять.** В записи о находке — поле состояния источника (жив / снят / устарел). `templates/research-queue.md:22-28` его не имеет, поэтому «найдено в Khoj» через полгода не значит ничего.

---

## 6. raold-second-brain

**Структура.** FastAPI `app/` (`routes`, `services`, `storage`, `models`; приложение собирается в `internal/research/raold-second-brain/app/factory.py:10,158`), SvelteKit `frontend/`, Postgres + pgvector в Docker, GPU-сервисы CLIP и LLaVA в `services/gpu/`. Заявка — «100% локальная система управления знаниями» (`internal/research/raold-second-brain/README.md:6`).

**6.1. Ярлык «локально» проверяется списком вызовов.**
`internal/research/raold-second-brain/README.md:15` и `:19` обещают полную локальность и «ни байта в облако»; `:35-40` в ключевых функциях — Google Drive с OAuth. В коде реальные исходящие HTTPS-вызовы к `accounts.google.com` и `www.googleapis.com`: `internal/research/raold-second-brain/app/services/google_drive_enhanced.py:95,112,134,161`. Эмбеддинги при этом действительно локальные — обёртки OpenAI заменены локальным клиентом (`internal/research/raold-second-brain/app/utils/local_embedding_client.py:238-247`), хотя CSP всё ещё разрешает `api.openai.com` (`internal/research/raold-second-brain/app/core/security_audit.py:306`).
**Взять.** Форму проверки: «локально» подтверждается списком доменов в коде, а не словом в README. Для нас — `AGENTS.md:183` и `workspace/LOCAL-ONLY.template:5-9`: требовать перечень доменов, а не только категории запрета.
**Отклонить.** Ярлык и «Complete Privacy» (`internal/research/raold-second-brain/README.md:48-53`) как утверждение: рядом с OAuth он не выдерживает проверки.

**6.2. Слияние дублей памяти: сухой прогон по умолчанию и сохранение источников.**
`internal/research/raold-second-brain/app/services/memory_service_postgres.py:390-423`: для слияния нужно не меньше двух записей, тип `merge`, в метаданные пишутся `source_ids`; `:446-466`: автоконсолидация по умолчанию `dry_run=True` и только по явному вызову сливает пары с похожестью от 0.95.
**Взять.** Процедуру в `workspace/memory/README.md:5-9`: сейчас там сказано «ничего не удаляется без разрешения», но нет правила слияния. Добавить: сначала список пар, в слитой заметке — список исходных файлов, по умолчанию без записи.

**6.3. Граф знаний и гибридный поиск — продукт, а не метод.**
`internal/research/raold-second-brain/README.md:29-46` перечисляет мультимодальный поиск, граф связей, консолидацию и дедупликацию как фичи; схемы, БД и API занимают весь `app/`.
**Отклонить.** Перенос инфраструктуры: сервера у нас нет, роль графа выполняют маршрутизатор `knowledge/INDEX.md:18-23` и поле `used_in_skills` в паспорте (`templates/knowledge-card.md:7`).

---

## 7. Топ-3 приёма группы

1. **Отказ без источников.** `internal/research/LearningCircuit-local-deep-research/src/local_deep_research/citation_handlers/base_citation_handler.py:416-438`: пустой список источников — явный отказ, а не ответ по памяти модели. Для не-разработчика звучит так: «если ссылок нет, система не отвечает».
2. **Контракт ресёрча с бюджетом и контр-позицией.** `internal/research/AgriciDaniel-claude-obsidian/skills/autoresearch/SKILL.md:31-49` и `:55-56`: тема, домены, число раундов и источников, стоп-условие и обязательный вопрос против ведущей версии — до первого запроса.
3. **Словарь состояний утверждения.** `internal/research/AgriciDaniel-claude-obsidian/skills/wiki/references/provenance.md:40-49`: accepted / provisional / contested / unsupported / deprecated и правило «высокорисковому — два независимых источника». Это машинная форма нашего «двух каналов».

---

## 8. Чего в клонах нет

- **Уровня `[рынок]`.** Ни один не фиксирует обязательство живого человека: у local-deep-research вердикт — качество отчёта, у fabric — тир контента (`internal/research/danielmiessler-fabric/data/patterns/label_and_rate/system.md:51-55`), у khoj и second-brain — релевантность выдачи. Наша шкала 1–19 (`AGENTS.md:40`) измеряет цену сигнала, аналога ей нет.
- **Шага «узкое место → поле».** Все шесть получают тему на входе: контракт ресёрча начинается с темы и исключений (`internal/research/AgriciDaniel-claude-obsidian/skills/autoresearch/SKILL.md:31-43`), а не с вопроса «где у человека теряется время».
- **HADI и условий смерти.** У них стоп-условия по бюджету (`internal/research/AgriciDaniel-claude-obsidian/skills/autoresearch/references/program.md:68-78`), но нет «условия смерти гипотезы» и записи провала как результата.
- **Артефакта-предлога и разговора.** Выход у всех — документ: страница или досье (`internal/research/AgriciDaniel-claude-obsidian/skills/autoresearch/SKILL.md:83-95`), отчёт с библиографией (`internal/research/LearningCircuit-local-deep-research/src/local_deep_research/report_generator.py:1730-1733`). Дальше человек не идёт.
- **Проверки полноты по идентификаторам `Q`.** У них проверяется наличие источников и расход бюджета, а не «каждый вопрос отвечен»: контракта из `templates/research-response.md:12` там нет.
- **Обезличивания.** fabric и gpt-researcher отправляют текст как есть; только claude-obsidian требует согласия на выход и запрещает частные пути (`internal/research/AgriciDaniel-claude-obsidian/skills/wiki-ingest/SKILL.md:40-44`).
- **«Нет ссылки — нет факта» на уровне пункта.** `internal/research/danielmiessler-fabric/data/patterns/extract_wisdom/system.md:9-25` вообще не просит ссылок, а у local-deep-research проверяется наличие номера, не совпадение с источником.
- **Белого пятна, доказанного поиском.** Состояние `unsupported` есть (`internal/research/AgriciDaniel-claude-obsidian/skills/wiki/references/provenance.md:47`), но требования перечислять каналы и формулировки поиска, как в `skills/03-prevalidation/SKILL.md:102-106`, нет ни у кого.

---

## 9. Спорные утверждения списка

Проверялись формулировки из `internal/draft/25_owner_repo_list.md`.

**9.1. «Оценивает рейтинг цитируемых журналов»** (`internal/draft/25_owner_repo_list.md:72`) — **подтвердилось с оговоркой.** Оценка есть: 1–10 из квартиля SJR, h-index, DOAJ и списка хищнических изданий (`internal/research/LearningCircuit-local-deep-research/src/local_deep_research/journal_quality/scoring.py:51-88,110-128`), фильтр — `internal/research/LearningCircuit-local-deep-research/src/local_deep_research/advanced_search_system/filters/journal_reputation_filter.py:1-27`. Но это не рейтинг цитируемости: квартиль выводится из процентилей `cited_by_count` (`internal/research/LearningCircuit-local-deep-research/docs/journal-quality.md:44`), h-index имеет смещение по дисциплинам (`internal/research/LearningCircuit-local-deep-research/src/local_deep_research/journal_quality/scoring.py:78-81`), шкала не сплошная (`internal/research/LearningCircuit-local-deep-research/docs/journal-quality.md:7`), а порог по умолчанию отсекает только хищническое (`:25-32`).

**9.2. «Параллельно опрашивая более 20 веб-источников»** (`internal/draft/25_owner_repo_list.md:73`) — **не подтвердилось.** «Over 20 sources» — фраза из `internal/research/assafelovic-gpt-researcher/README.md:80`; в конфиге по умолчанию 5 результатов на запрос, 3 итерации, 3 подтемы, 15 воркеров скрапера (`internal/research/assafelovic-gpt-researcher/gpt_researcher/config/variables/default.py:22,26,29,31`), глубокая ветка — 3 на 2 при параллельности 4 (`:40-42`). Параллельно работают подзапросы (`internal/research/assafelovic-gpt-researcher/gpt_researcher/skills/researcher.py:289-295`), но потолок одновременных загрузок — 15, и цифры 20 в коде нет.

**9.3. «Детерминированный поиск BM25»** (`internal/draft/25_owner_repo_list.md:77`) — **подтвердилось.** `internal/research/AgriciDaniel-claude-obsidian/scripts/bm25-index.py:1-6` — своя реализация Okapi BM25 на stdlib, k1=1.5, b=0.75, один JSON-индекс; сортировка по score (`:772`), модели в пути нет. Оговорка: при равных score порядок задаёт порядок вхождений в индексе, то есть детерминизм здесь — про воспроизводимость на одном индексе, а не про канонический tie-break.

**9.4. «Без отправки байтов во внешние облачные сервисы»** (`internal/draft/25_owner_repo_list.md:79`) — **не подтвердилось как абсолютное.** Google Drive — ключевая функция (`internal/research/raold-second-brain/README.md:35-40`), и код делает исходящие вызовы OAuth и Drive API (`internal/research/raold-second-brain/app/services/google_drive_enhanced.py:95,112,134,161`). Локальность эмбеддингов при этом подтверждается (`internal/research/raold-second-brain/app/utils/local_embedding_client.py:238-247`).

**9.5. «После закрытия облачной версии в апреле 2026 года»** (`internal/draft/25_owner_repo_list.md:78`) — **не нашёл.** Документация клона продолжает продвигать облако (`internal/research/khoj-ai-khoj/README.md:54`, `internal/research/khoj-ai-khoj/documentation/docs/get-started/overview.md:31`), автоматизации ссылаются на облачный адрес и требуют Resend для писем (`internal/research/khoj-ai-khoj/documentation/docs/features/automations.md:3,8-9`). Признаков закрытия в файлах нет; утверждение остаётся `[внешнее]` без источника.
