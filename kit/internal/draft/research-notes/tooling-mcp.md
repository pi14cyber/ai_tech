# Четыре MCP-репозитория: что из них нужно навыку документов

Читано 20.10.2026, только чтение; клоны и наш репозиторий не менялись. Каждый факт — из файла, ссылка `путь:строка`, пути полные от корня проекта.
Пометка «заявление» — цифра авторов проекта, не независимая проверка. Цифр, которых нет в файлах, здесь нет.

---

## 1. `zilliztech/claude-context` — `6fc318b`, 2026-07-14

**Что внутри.** Монорепо на TypeScript: `packages/core` (индексация и поиск), `packages/mcp` (сервер), `packages/vscode-extension`, `packages/chrome-extension`, `evaluation/`, `docs/` — `internal/research/zilliztech-claude-context/CLAUDE.md:7-13`. Лицензия MIT — `internal/research/zilliztech-claude-context/LICENSE:1`.

**Инструменты, ровно 4** — `internal/research/zilliztech-claude-context/packages/mcp/src/index.ts:121-222`: `index_codebase` (обязателен абсолютный путь, плюс `force`, `splitter` ast|langchain, `customExtensions`, `customIgnorePatterns`), `search_code` (`path`, `query`, `limit`, `extensionFilter`), `clear_index`, `get_indexing_status`. Транспорт — MCP поверх stdio — `internal/research/zilliztech-claude-context/README.md:440-444`.

**Что уходит наружу.** Каждый фрагмент файла уходит в выбранный эмбеддер, по умолчанию OpenAI — `internal/research/zilliztech-claude-context/.env.example:14`, `internal/research/zilliztech-claude-context/packages/mcp/src/config.ts:170`, — и в векторную БД Milvus/Zilliz Cloud. То есть наружу уходят куски документов и тексты запросов. Локальный вариант есть: Ollama плюс локальный Milvus — `internal/research/zilliztech-claude-context/docs/troubleshooting/faq.md:17-31`.

**Требования и ограничения.** Node ≥ 20 — `internal/research/zilliztech-claude-context/README.md:61`; ключ эмбеддера — `internal/research/zilliztech-claude-context/README.md:48-55`; аккаунт Zilliz Cloud или свой Milvus, адрес БД можно не указывать при наличии токена — `internal/research/zilliztech-claude-context/.env.example:64`. У бесплатного аккаунта Zilliz есть предел числа коллекций: код его только распознаёт и отправляет в прайс, конкретного числа в файлах нет — `internal/research/zilliztech-claude-context/packages/core/src/vectordb/types.ts:154`.

**Приёмы, снижающие стоимость шага.**
- Находка возвращается адресом места, а не файлом: `Location: путь:начало-конец` — `internal/research/zilliztech-claude-context/packages/mcp/src/handlers.ts:800-810`; сниппет режется до 5000 символов — `internal/research/zilliztech-claude-context/packages/mcp/src/handlers.ts:803`; результатов не больше 50 и порог сходства 0.3 — `internal/research/zilliztech-claude-context/packages/mcp/src/handlers.ts:762-768`.
- Переиндексация только изменённого, по Merkle-дереву — `internal/research/zilliztech-claude-context/README.md:531`.
- Статус — фазовый процент, а не доля файлов: 0 / ~5 / 10→100 — `internal/research/zilliztech-claude-context/docs/dive-deep/asynchronous-indexing-workflow.md:38-43`. «10%» может значить «только начали».
- Из коробки индексируются `.md`, `.markdown`, `.ipynb` — `internal/research/zilliztech-claude-context/docs/dive-deep/file-inclusion-rules.md:32`; PDF в списке нет.

**Заявленный эффект** (заявление): −39.4% токенов и −36.3% вызовов при том же F1 0.40, 30 задач SWE-bench, 3 прогона — `internal/research/zilliztech-claude-context/evaluation/README.md:25-34`.

**Вердикт: взять приёмы, сервер отклонить.** Нужны три вещи: ответ как адрес, а не документ; переиндексация только изменённого; порог сходства с жёстким лимитом выдачи. Наш навык работает с PDF и личными файлами, а здесь индексируется код и Markdown.

---

## 2. `upstash/context7` — `c7f80ce`, 2026-10-19

**Что внутри.** TypeScript-монорепо: `packages/mcp`, `packages/cli`, `packages/sdk` и обвязки для отдельных клиентов — `internal/research/upstash-context7/pnpm-workspace.yaml:1-2`. Лицензия MIT — `internal/research/upstash-context7/LICENSE:1`.

**Инструменты, ровно 2** — `internal/research/upstash-context7/packages/mcp/src/lib/tool-names.ts:1-4`: `resolve-library-id` (`libraryName`, `query`) и `query-docs` (`libraryId`, `query`, необязательный `language`). Тот же доступ без MCP — команды `ctx7 library` и `ctx7 docs` — `internal/research/upstash-context7/README.md:99-112`. Транспорты два: stdio и удалённый streamable-http `https://mcp.context7.com/mcp` — `internal/research/upstash-context7/server.json`, `internal/research/upstash-context7/packages/mcp/src/lib/constants.ts:11`.

**Что уходит наружу.** `query` и `libraryName` уходят параметрами URL на `context7.com/api/v2/libs/search` и `/v2/context` — `internal/research/upstash-context7/packages/mcp/src/lib/api.ts:150-152`, `internal/research/upstash-context7/packages/mcp/src/lib/api.ts:190-193`; кроме них уходят заголовки: подтверждение IP клиента, его IDE, версия клиента, плагин и транспорт — `internal/research/upstash-context7/packages/mcp/src/lib/encryption.ts:58-84`. Телеметрия на OpenTelemetry, глушится `OTEL_SDK_DISABLED=true` — `internal/research/upstash-context7/packages/mcp/src/lib/telemetry-config.ts:1-3`. Ключ необязателен — `internal/research/upstash-context7/server.json`, `internal/research/upstash-context7/README.md:47`.

**Ограничение и честность деградации.** При 429 текст говорит «повысьте тариф» или «создайте бесплатный ключ» — `internal/research/upstash-context7/packages/mcp/src/lib/api.ts:62-63`; самих лимитов в коде нет. Таймаут одного вызова 60 с, в комментарии p99.9 ≈ 3.2 с — `internal/research/upstash-context7/packages/mcp/src/lib/api.ts:17-21`. Локального зеркала документации в репозитории нет: вызов каждый раз идёт на сервер, свой адрес задаётся через `CONTEXT7_API_URL` — `internal/research/upstash-context7/packages/mcp/src/lib/constants.ts:14`.

**Приёмы, которые переносятся на любой внешний запрос.**
- Потолок попыток: не больше 3 вызовов на один вопрос, дальше работать с лучшим из найденного — `internal/research/upstash-context7/skills/find-docs/SKILL.md:51`, те же слова в описании инструмента — `internal/research/upstash-context7/packages/mcp/src/index.ts:342`.
- Запрет персональных данных в запросе — `internal/research/upstash-context7/skills/find-docs/SKILL.md:65`, `internal/research/upstash-context7/packages/mcp/src/index.ts:349`.
- Запрет молчаливой подмены: если источник не ответил, сказать почему, а не отвечать по памяти модели — `internal/research/upstash-context7/skills/find-docs/SKILL.md:158`.
- Два шага: сначала найти источник, потом спросить у него; оценка источника по трём признакам — число примеров, репутация, benchmark score — `internal/research/upstash-context7/skills/find-docs/SKILL.md:69-77`, `internal/research/upstash-context7/packages/mcp/src/index.ts:314-321`.

**Вердикт: взять четыре приёма, сервер рассмотреть.** Сервер полезен, только если человек спрашивает про чужие библиотеки; к его собственным документам он отношения не имеет.

---

## 3. `oraios/serena` — `dc60fba`, 2026-10-19

**Что внутри.** Python-пакет `serena-agent` с 44 инструментами — по файлам `internal/research/oraios-serena/src/serena/tools`: 13 JetBrains, 10 символьных, 6 памяти, 4 файловых, 4 конфигурационных, 3 рабочих, 2 запроса к проектам, 1 shell, 1 REPL. Лицензия GPL-3.0-or-later — `internal/research/oraios-serena/pyproject.toml:12`. Ставится через uv — `internal/research/oraios-serena/docs/02-usage/010_installation.md:23`.

**Что уходит наружу.** Работает локально через языковые серверы; данные проекта наружу не отправляются, собирается только анонимная статистика запуска (версия, ОС, интерфейс), отключается `SERENA_USAGE_REPORTING=false` — `internal/research/oraios-serena/docs/01-about/070_privacy.md:6-18`. Часть зависимостей ставится на лету — `internal/research/oraios-serena/docs/02-usage/010_installation.md:15`, значит первый запуск требует сети.

**Главное для нас — память, а не код.** Память это обычные markdown-файлы: проектные в `.serena/memories/`, общие в `~/.serena/memories/global/` — `internal/research/oraios-serena/docs/02-usage/045_memories.md:10-15`. Агент заранее получает список имён и читает по ссылкам вида `mem:имя` — `internal/research/oraios-serena/docs/02-usage/045_memories.md:32-36`, `internal/research/oraios-serena/src/serena/resources/memory_maintenance.md:5-16`. Целостность ссылок проверяется машинно: `serena memories check` — `internal/research/oraios-serena/docs/02-usage/045_memories.md:196`. Часть памятей можно объявить только для чтения или скрыть — `internal/research/oraios-serena/docs/02-usage/045_memories.md:100-124`. Порог записи: только устойчивые неочевидные конвенции, «плотные заметки, не проза» — `internal/research/oraios-serena/src/serena/resources/memory_maintenance.md:21-28`.

**Обоснование, которое стоит перенести в методику.** Ссылки лучше поиска: любой поиск даёт и ложные срабатывания, и пропуски, а решение агента по имени детерминировано — `internal/research/oraios-serena/docs/02-usage/045_memories.md:37-41`; память на SQLite, графах или векторах отклонена там же — `internal/research/oraios-serena/docs/02-usage/045_memories.md:58-59`.
Бюджет ответа задан числом: `default_max_tool_answer_chars: 150000` — `internal/research/oraios-serena/src/serena/resources/serena_config.template.yml:197`.

**Вердикт: взять устройство памяти и проверку ссылок, рассмотреть бюджет ответа, инструменты отклонить.** Наш `knowledge/INDEX.md` — та же идея, но без машинной проверки битых ссылок. Сами инструменты нам не нужны: это код, GPL и языковые серверы.

---

## 4. `wong2/awesome-mcp-servers` — `39eb1d7`, 2026-07-13

**Что внутри.** Один README на 537 записей, разделы: Reference — `internal/research/wong2-awesome-mcp-servers/README.md:23`, Official — `internal/research/wong2-awesome-mcp-servers/README.md:35`, Community — `internal/research/wong2-awesome-mcp-servers/README.md:293`, Clients — `internal/research/wong2-awesome-mcp-servers/README.md:556`, Frameworks — `internal/research/wong2-awesome-mcp-servers/README.md:575`. Лицензия MIT — `internal/research/wong2-awesome-mcp-servers/LICENSE:1`. Кода нет.

**Формат записи** — имя, ссылка, одно предложение. Ни цены, ни квоты, ни локальности в записи нет: `internal/research/wong2-awesome-mcp-servers/README.md:210` (PaddleOCR), `internal/research/wong2-awesome-mcp-servers/README.md:361` (Excel), `internal/research/wong2-awesome-mcp-servers/README.md:468` (Pandoc).

**Маркерам верить нельзя.** Определения значков в файле не нашлось; значок ☁️ стоит у 4 записей из 537, 📇 — тоже у 4. Это неполная разметка, а не признак.

**Что относится к навыку документов:** Fetch — `internal/research/wong2-awesome-mcp-servers/README.md:28`, Filesystem — `internal/research/wong2-awesome-mcp-servers/README.md:29`, Memory — `internal/research/wong2-awesome-mcp-servers/README.md:31`, Chroma — `internal/research/wong2-awesome-mcp-servers/README.md:84`, Needle — `internal/research/wong2-awesome-mcp-servers/README.md:195`, PaddleOCR — `internal/research/wong2-awesome-mcp-servers/README.md:210`, consult7 — `internal/research/wong2-awesome-mcp-servers/README.md:342`, Data Exploration для `.csv` — `internal/research/wong2-awesome-mcp-servers/README.md:343`, Excel — `internal/research/wong2-awesome-mcp-servers/README.md:361`, Jina Reader — `internal/research/wong2-awesome-mcp-servers/README.md:406`, Obsidian — `internal/research/wong2-awesome-mcp-servers/README.md:460`, Pandoc — `internal/research/wong2-awesome-mcp-servers/README.md:468`.

**Вердикт: взять формат каталога, как доказательство отклонить.** Одна строка на источник — по ней можно маршрутизировать чтение, но это список ссылок, а не проверенные факты.

---

## Топ-3 вывода группы

1. **Ответ — адрес, а не документ.** Один раз строим оглавление с адресами, дальше показываем только нужные абзацы с номером строки и жёстким лимитом. Подтверждение: `internal/research/zilliztech-claude-context/packages/mcp/src/handlers.ts:800-810`, `internal/research/zilliztech-claude-context/README.md:531`. Снижает стоимость шага: вместо чтения 200 страниц — три ссылки. Вердикт: взять в навык документов.
2. **Протокол — это markdown-память с машинной проверкой ссылок.** Имена известны заранее, чтение идёт по ссылкам, битые ссылки ловит команда, а не глаз. Подтверждение: `internal/research/oraios-serena/docs/02-usage/045_memories.md:32-41`, `internal/research/oraios-serena/src/serena/resources/memory_maintenance.md:21-28`. Наш `scripts/verify.py` уже делает половину; берём обоснование «почему ссылки, а не вектора» и порог «что вообще записывать». Вердикт: взять в раздел протоколов.
3. **Внешний вызов: два шага, лимит попыток, честная деградация.** Сначала находим источник, потом спрашиваем его; не больше трёх попыток; если не вышло — говорим причину, а не подставляем память модели. Подтверждение: `internal/research/upstash-context7/skills/find-docs/SKILL.md:51`, `internal/research/upstash-context7/skills/find-docs/SKILL.md:158`, `internal/research/upstash-context7/packages/mcp/src/lib/api.ts:62-63`. Вердикт: взять в предвалидацию и в блок протоколов.

---

## Вопросы внешнему исследователю

Из кода это не устанавливается — нужны ссылки и даты.

- **Квоты Zilliz Cloud.** Сколько коллекций и векторов даёт бесплатный аккаунт, что происходит после предела (`internal/research/zilliztech-claude-context/packages/core/src/vectordb/types.ts:154` знает только текст ошибки) и сколько стоит следующий уровень.
- **Цена и лимиты эмбеддингов.** Сколько стоит проиндексировать 100 страниц PDF у OpenAI, VoyageAI, Gemini; какой лимит запросов в минуту у каждого (`internal/research/zilliztech-claude-context/.env.example:14,21` — провайдеры и размер батча, цен нет).
- **Лимиты Context7.** Сколько запросов даёт бесплатный ключ, что после 429 (`internal/research/upstash-context7/packages/mcp/src/lib/api.ts:62-63` отправляет в прайс), есть ли SLA и uptime у `mcp.context7.com`.
- **Надёжность заявления −39.4%.** Проверено на коде и 30 задачах SWE-bench (`internal/research/zilliztech-claude-context/evaluation/README.md:13-26`); есть ли независимые замеры и переносится ли эффект на текстовые документы.
- **Инструменты обработки PDF.** PaddleOCR, Pandoc, Needle, consult7 (`internal/research/wong2-awesome-mcp-servers/README.md:210`, `internal/research/wong2-awesome-mcp-servers/README.md:468`, `internal/research/wong2-awesome-mcp-servers/README.md:195`, `internal/research/wong2-awesome-mcp-servers/README.md:342`): платность, локальность, качество OCR на русском, лицензии — в каталоге только одно предложение на запись.
- **Право и данные.** GPL-3.0 у Serena (`internal/research/oraios-serena/pyproject.toml:12`) — можно ли переносить идеи и код; допустима ли отправка фрагментов личных документов в зарубежные API по нашим правилам обезличивания (`AGENTS.md`, раздел 14).
