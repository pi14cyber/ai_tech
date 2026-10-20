# Документы: пять конвертеров PDF/DOCX/PPTX/сканов и что из них переносится

Читано 20.10.2026, только чтение; клоны и наш репозиторий не менялись.

Источники:

- `internal/research/opendatalab-MinerU` — `b7f3dd0`, 2026-10-11, Python. Парсер документов с локальной библиотекой и CLI для агентов: PDF, сканы, Office, HTML, EPUB, OFD → Markdown, JSON и ещё семь форматов.
- `internal/research/docling-project-docling` — `d01c9c0`, 2026-10-19, Python. SDK и CLI, сводящие PDF, Office, HTML, аудио в единый `DoclingDocument` с экспортом в Markdown и JSON.
- `internal/research/datalab-to-marker` — `1749c21`, 2026-10-19, Python. Конвейер PDF → Markdown/JSON на surya VLM: два режима, замеры на стороннем бенчмарке.
- `internal/research/microsoft-markitdown` — `4cc9fa1`, 2026-10-03, Python. Тонкая утилита «файл → Markdown» из текстового слоя плюс MCP-обёртка на один инструмент.
- `internal/research/gavinHuang-pdf2md-mcp` — `7dc134d`, 2025-07-04, Python. Минимальный MCP-сервер: одна функция, 205 строк, PDF → Markdown.

Ссылки: `путь:строка`. Утверждается только прочитанное в файлах. Цифры бенчмарков взяты из README авторов и помечены как заявление.

---

## 1. opendatalab-MinerU

**Структура.** Четыре консольных входа — `mineru`, `mineru-kit`, `mineru-router`, `mineru-webui` — `internal/research/opendatalab-MinerU/docs/next/code-map.md:12-19`. Слои: `cli/`, `doclib/` (постоянный сервис FastAPI + SQLite/FTS5), `parser/`, `backend/`, `model/`, `render/`, `kit/` — `internal/research/opendatalab-MinerU/docs/next/code-map.md:25-34`. Правила для агентов лежат в `CLAUDE.md`, а `AGENTS.md` — одна строка-указатель на него: `internal/research/opendatalab-MinerU/AGENTS.md:1`. Готовый навык инструмента — 890 строк поведения агента с документами: `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:1-4`.

**1.1. Цитата — адрес страницы и блока, а не документ.**
Локатор имеет вид `doc:{short_id}/tier:{tier}/page:{page_no}/block:{block_no}/char:{offset}` — `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:540-548`; страницы и блоки с единицы, смещения символов с нуля — `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:560-561`; пример цитаты в ответе: «The warranty period is 24 months (doc:ab12cd3/tier:standard/page:7/block:3)» — `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:872-880`.

**Взять.** Навык `08-documents` уже создан (`skills/08-documents/SKILL.md:1-4`, место в карте: `internal/draft/21_skill_map.md:53`) — дописать в Часть B, пункт 4 (`skills/08-documents/SKILL.md:36`): цитата несёт документ, страницу и блок. У нас ссылка — файл и строка (`AGENTS.md`, раздел 3), а для PDF страницы нет; вместе с адресом — запрет цитировать конвертацию без номера страницы.

**1.2. Чтение окном с указателем продолжения.**
По умолчанию читается первое окно страниц, обычно 1–10, дальше — по `--limit` и указателю, а не заново с первой страницы — `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:504-509`. Продолжение приходит готовой командой `<!-- Next: mineru read doc:… -->`, угадывать следующую страницу запрещено — `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:511-534`. Отдельным правилом: не грузить документ целиком, если хватает продолжения — `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:887`.

**Взять.** Дописать в Часть B навыка `08-documents` (`skills/08-documents/SKILL.md:31-37`): бюджет чтения — 10 страниц за проход, следующий проход по указателю, «прочитать весь PDF» — отдельное решение человека. В блок 2 (слайд Б2-9 «Четыре роли инструментов», `internal/draft/16_slide_plan.md:169`) — одна фраза: инструмент, который умеет не грузить целиком.

**1.3. Тир — явный выбор, а не молчаливая деградация.**
Четыре тира с ценой и назначением: `flash` — превью и индексация, `basic` — OCR и модели, `standard`/`advanced` — сложная вёрстка — `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:276-286`. При недоступном качестве библиотека возвращает `quality_tier_unavailable`, а не выбирает тайком `flash` и не отправляет файл в облако — `internal/research/opendatalab-MinerU/docs/en/usage/tiers.md:22-25`; `flash` включается только по прямой просьбе — `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:287-298`.

**Взять.** Дописать в Часть B навыка `08-documents` (`skills/08-documents/SKILL.md:31-37`): в отчёте о конвертации отдельная строка «каким режимом читано». Это машинная форма нашего `[допущение]`: качество чтения — не догадка, а названный режим (`AGENTS.md`, раздел 2).

**1.4. Локально по умолчанию, наружу — только по разрешению.**
Файл уходит на внешний парсинг лишь при явном `--remote`; локальный сбой не даёт права молча переключиться на внешний — `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:244-250`. Для чувствительных документов — оставаться локально до явного согласия — `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:258`.

**Взять.** `AGENTS.md`, раздел 14 и Часть C навыка `08-documents` (`skills/08-documents/SKILL.md:39-44`): флаг «только локально» у нас есть, а правила «локальный сбой не равен разрешению на отправку» нет. Ровно этой фразы не хватает, чтобы флаг не обходили «ради результата».

**1.5. Телеметрия: спросить, показать точный пакет, перечислить запрещённое.**
При первом запуске сервис обязан спросить и не предвыбирать ответ; отключение удаляет неотправленные данные; `preview` показывает тот же JSON, что уйдёт — `internal/research/opendatalab-MinerU/docs/next/telemetry.md:34-56`. Запрещено собирать содержимое, имя и путь файла, запросы, промпты, хост, пользователя, модель GPU; разрешено только из белого списка, без прокидывания `kwargs` — `internal/research/opendatalab-MinerU/docs/next/telemetry.md:58-80`.

**Взять.** `AGENTS.md`, раздел 14 и шаг 0 аудита источников (`skills/00-onboarding-interview/SKILL.md:32-49`): вместо «обезличить на глаз» — показать человеку точный список полей и список того, что не уходит никогда.

**1.6. Два режима вывода: читабельный и полный, склейка страниц — отдельное решение.**
`RenderMode.DEFAULT` скрывает колонтитулы, номера страниц и посторонние блоки, склеивает продолжения текста, списков и **только** таблиц между страницами, разделителей между страницами не ставит — `internal/research/opendatalab-MinerU/docs/next/middle-json/rendering.md:484-491`. `FULL` показывает все блоки, склеивает только внутри страницы и сохраняет границу страниц — `internal/research/opendatalab-MinerU/docs/next/middle-json/rendering.md:493-500`; неудачная склейка таблицы оставляет две таблицы — `internal/research/opendatalab-MinerU/docs/next/middle-json/rendering.md:502-505`.

**Взять.** Дописать в Часть B навыка `08-documents` (`skills/08-documents/SKILL.md:31-37`): по умолчанию «читабельный» режим, но номер страницы остаётся в разметке, а «полный» доступен одной командой. Правило «неудачная склейка = две таблицы» берём дословно: испорченная одна таблица хуже двух честных.

**1.7. Один синтаксис страниц во всех входах.**
Выбор страниц общий для CLI, библиотеки, API, веб-интерфейса и Python: с единицы, включительно, `r1` — последняя страница, `all` — все; полновесный `～` и отрицательные номера не поддерживаются — `internal/research/opendatalab-MinerU/README.md:595-597`.

**Взять.** Дописать в Часть B навыка `08-documents` (`skills/08-documents/SKILL.md:31-37`): один способ задать страницы на весь навык. У соседей база разная — у marker диапазон нумеруется с нуля (`internal/research/datalab-to-marker/README.md:132`), у docling с единицы (`internal/research/docling-project-docling/docling/.agents/skills/docling/references/cli.md:136`), поэтому база указывается в самой ссылке и в самой команде.

**1.8. Кэш: перечитать по требованию, но не удалять и не перезаписывать чужое.**
Результаты кэшируются по документу и тиру. `--force` перечитывает только текущий запрос и не стирает прежний результат; `invalidate` запрещает будущим запросам брать готовое, но новый разбор сам не запускает; удалять файлы человека при управлении кэшем запрещено — `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:713-735`.

**Взять.** Часть A, пункт 4 навыка `08-documents` (`skills/08-documents/SKILL.md:28`: «изменения — новой версией, а не молчаливой правкой») и `templates/hadi-tracker.md` — то же разделение «переделать сейчас» и «закрыть старый результат» (см. `internal/draft/research-notes/tooling-agents.md:88-90`, приём 4.3). Второй прогон конвертации пишется новым файлом, старый не перезаписывается.

**1.9. Постоянный сервис, кэш и стек моделей — не наш масштаб.**
`doclib/` — резидентный сервис на FastAPI + SQLite с воркерами парсинга, UDS-сокетом и монитором устройства, и вызов идёт через него — `internal/research/opendatalab-MinerU/docs/next/code-map.md:26-27`. Модели: 0,8–3 ГБ загрузки и 8–16 ГБ памяти на `standard` — `internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:328-334`; 4.x в альфе, публичный API не стабилен, около десяти коммитов в день — `internal/research/opendatalab-MinerU/docs/next/pitfalls.md:26-31`.

**Отклонить.** Навык `08-documents`: не ставим человеку резидентный сервис и 2 ГБ моделей ради «прочитать пару договоров»; альфа-API не годится как зависимость публичного набора.

---

## 2. docling-project-docling

**Структура.** Пакет `docling/`, метапакет `packages/docling/`, урезанный `packages/docling-slim/`, документация MkDocs в `docs/` — `internal/research/docling-project-docling/AGENTS.md:20-28`. Рядом с кодом живёт навык для агентов, который отгружается внутрь колеса: `internal/research/docling-project-docling/AGENTS.md:38-44`. Внутри навыка — справочники по задачам (CLI, SDK, извлечение полей, RAG, удалённый сервис, тонкая установка), точка входа: `internal/research/docling-project-docling/docling/.agents/skills/docling/SKILL.md:49-58`.

**2.1. Навык отгружается вместе с инструментом и синхронизируется с ним.**
Правило авторов: навык лежит в пакете, попадает в wheel/sdist и обновляется вместе с CLI, SDK и опциями — `internal/research/docling-project-docling/AGENTS.md:38-44`.

**Взять.** Блок 2 (Б2-9, `internal/draft/16_slide_plan.md:169`) и навык `08-documents`: инструмент без навыка — половина работы. У нас обратная задача, и это подтверждает, что «как поставить и какой командой читать» обязано жить в навыке, а не в голове человека.

**2.2. Чек-лист приёмки конвертации из четырёх пунктов.**
После конвертации, где важна точность: число страниц совпадает с источником; Markdown не почти пустой; ожидаемые таблицы на месте; нет блоков `�` и бесконечно повторяющихся строк — `internal/research/docling-project-docling/docling/.agents/skills/docling/references/cli.md:181-188`. Те же признаки выведены в таблицу ситуаций: пустой вывод — включить OCR или VLM, `�` — сменить движок — `internal/research/docling-project-docling/docling/.agents/skills/docling/references/cli.md:131-144`.

**Взять.** Навык `08-documents`, Часть D (`skills/08-documents/SKILL.md:46-56`): три статуса «настроено / собрано / проверено» уже есть, а четырёх проверок из этого чек-листа в них нет. Плюс строка в `skills/05-validation-gate`: пустой или мусорный результат — провал конвертации, а не пустой документ.

**2.3. Три конвейера, у каждого названа цена.**
`standard` — цифровые PDF, работает на CPU; `vlm` — сложная вёрстка, рукописный текст и формулы, нужен GPU, медленнее; `native` — только текст и картинки, без моделей, но без порядка чтения, заголовков и таблиц — `internal/research/docling-project-docling/docling/.agents/skills/docling/references/cli.md:41-47`. Выбор по типу документа сведён в таблицу, включая «очень большой документ (500+ страниц)» и «нужна только часть» — `internal/research/docling-project-docling/docling/.agents/skills/docling/references/cli.md:79-87`, `internal/research/docling-project-docling/docling/.agents/skills/docling/references/cli.md:135-136`.

**Взять.** Блок 2 (Б2-9): «режим — это цена точности, а не удобство»; в навык `08-documents`, Часть B (`skills/08-documents/SKILL.md:31-37`) — строка выбора режима по типу документа. Формулировка `native` («быстро, но без структуры») готова для слайда: у скорости названо, что именно теряется.

**2.4. Оценка качества как свойство результата, а не мнение автора.**
`ConversionResult.confidence` даёт четыре оценки (вёрстка, OCR, цифровой текст, таблицы), класс `poor / fair / good / excellent` и два сводных: средний и пятый процентиль, чтобы видеть худшие места — `internal/research/docling-project-docling/docs/concepts/confidence_scores.md:9-13`. Назначение — отбирать документы на ручную проверку и ставить порог пакетной конвертации — `internal/research/docling-project-docling/docs/concepts/confidence_scores.md:15-20`; честная оговорка: оценка таблиц ещё не реализована — `internal/research/docling-project-docling/docs/concepts/confidence_scores.md:39-49`.

**Взять.** Навык `08-documents`, Часть D (`skills/08-documents/SKILL.md:46-56`) и `skills/05-validation-gate`: у нас вердикт пишется прозой, и «не проверено» неотличимо от «проверено». Берём форму «оценка + класс + худшее место», без самих чисел.

**2.5. Уровень заголовка не угадывается.**
Модель вёрстки говорит «это заголовок», но не говорит, какой глубины: все приходят уровнем 1, и структура отчёта схлопывается в плоский список `#` — `internal/research/docling-project-docling/docs/usage/heading_levels.md:1-5`. Восстановление уровней — отдельная стадия по трём сигналам с приоритетом: закладки PDF → нумерация в тексте → визуальный стиль; она **выключена по умолчанию**, потому что неверный уровень хуже отсутствующего — `internal/research/docling-project-docling/docs/usage/heading_levels.md:7-11`, `internal/research/docling-project-docling/docs/usage/heading_levels.md:53-61`. На сканах шрифтовых сигналов нет: OCR не отдаёт метаданные шрифта — `internal/research/docling-project-docling/docs/usage/heading_levels.md:141`.

**Взять.** Дописать в Часть B навыка `08-documents` (`skills/08-documents/SKILL.md:31-37`): иерархия берётся только из закладок и нумерации, иначе документ остаётся плоским, и это пишется в отчёте. Для стрима — сильная фраза «неверный уровень хуже отсутствующего».

**2.6. Колонтитул уводится в отдельный слой, а не выбрасывается.**
Заголовки и подвалы DOCX добавляются в слой `furniture`, а не в тело; дубликаты «linked to previous» пропускаются, чтобы не размножать текст — `internal/research/docling-project-docling/docling/backend/msword_backend.py:4629-4639`.

**Взять.** Дописать в Часть B, пункт 3 навыка `08-documents` (`skills/08-documents/SKILL.md:35`): конвертер помечает служебный текст, а решение «убрать» принимает читатель. Удаление по умолчанию (как у marker, п. 3.3) допустимо, но тогда обязан быть флаг возврата.

**2.7. Внешняя сеть закрыта, пока её не включили флагом.**
Docling блокирует исходящий HTTP, если не задан `--enable-remote-services`; удалённый VLM требует явной настройки в SDK — `internal/research/docling-project-docling/docling/.agents/skills/docling/references/cli.md:146-156`.

**Взять.** `AGENTS.md`, раздел 14 и Часть C навыка `08-documents` (`skills/08-documents/SKILL.md:39-44`): наш режим «только локально» включается файлом; у них закрыто по умолчанию. Правильная сторона по умолчанию — закрытая.

**2.8. Родной разбор для современных форматов, отдельная зависимость для старых.**
Поддержано около двух десятков входов, включая устаревшие бинарные Office (через LibreOffice), EPUB, почту, изображения, а также аудио и видео через ASR — `internal/research/docling-project-docling/docs/usage/supported_formats.md:9-32`. Удалённое преобразование целиком идёт через отдельный сервис с ключом и переключением режима — `internal/research/docling-project-docling/docs/usage/mcp.md:31-41`.

**Отклонить.** Навык `08-documents`: транскрипция и облачный сервис — другой продукт и другой контур данных. Берём только один вывод: у нас, как и здесь, конвертация DOCX/PPTX идёт родным разбором, а `.doc`/`.rtf` — через офисный пакет (`skills/office-docx`, решение о LibreOffice).

**2.9. Старые форматы не читаются без офисного пакета.**
Устаревшие `.doc`, `.xls`, `.ppt` и RTF поддерживаются только через LibreOffice — `internal/research/docling-project-docling/docs/usage/supported_formats.md:13-14`; современные `.docx`, `.xlsx`, `.pptx` разбираются родным путём — `internal/research/docling-project-docling/docs/usage/supported_formats.md:12`.

**Взять.** Дописать в Часть B, пункт 1 навыка `08-documents` (`skills/08-documents/SKILL.md:33`): назвать зависимость заранее и одной строкой («старый `.doc` читается через связанный LibreOffice»), а не выяснять это на документе человека.

---

## 3. datalab-to-marker

**Структура.** Конвейер из шести заменяемых частей: провайдеры (PDF как источник), builders (блоки и текст), processors (таблицы, колонтитулы, уравнения), renderers (Markdown, JSON, HTML, chunks), schema (типы блоков), converters (весь конвейер) — `internal/research/datalab-to-marker/README.md:398-407`. Замеры и скрипты сравнения с конкурентами лежат в `benchmarks/` и воспроизводимы — `internal/research/datalab-to-marker/README.md:536-544`.

**3.1. Режим назван вместе с картой потерь.**
`balanced` — surya VLM для вёрстки, OCR формул и перечитывание страницы целиком, если встроенный текст плох; `fast` — лёгкий детектор вёрстки и текстовый слой, VLM только точечно; `--disable_ocr` выключает VLM полностью — `internal/research/datalab-to-marker/README.md:102-106`. Потери посчитаны по категориям: математика arXiv — 83,9 у `balanced`, 23,4 у `fast`, 0,0 без OCR; таблицы — 73,4 / 69,0 / 46,1 — `internal/research/datalab-to-marker/README.md:497-508`. Вывод прямо: для формул нужен `balanced`, быстрый режим читает уравнения из текстового слоя — `internal/research/datalab-to-marker/README.md:510-514`.

**Взять.** Блок 2 (Б2-9): «у режима есть цена, и она измерена». Дописать в Часть B навыка `08-documents` (`skills/08-documents/SKILL.md:31-37`) правило выбора: формулы и сканы → качественный режим, чистый цифровой текст → быстрый, и выбор пишется в отчёт.

**3.2. Каждая страница помнит, откуда в ней текст.**
Метаданные содержат `page_stats` с полем `text_extraction_method` — `internal/research/datalab-to-marker/README.md:357-380`. Поле есть у каждого блока и принимает значения `pdftext`, `surya`, `gemini` — `internal/research/datalab-to-marker/marker/schema/blocks/base.py:89`; собирается в отчёт рендерера — `internal/research/datalab-to-marker/marker/renderers/__init__.py:103-123`.

**Взять.** Дописать в Часть B, пункт 4 навыка `08-documents` (`skills/08-documents/SKILL.md:36`): на уровне страницы хранится метка «текстовый слой / OCR / модель». Это прямое продолжение нашей разметки `[validated: data]` и `[assumption]` (`AGENTS.md`, раздел 12) на документ: цитата со страницы, прочитанной OCR, — `[допущение]`, а не факт.

**3.3. Удаление колонтитулов с четырьмя оговорками и флагом возврата.**
Колонтитулом блок считается, только если он целиком в полосе 8 % сверху или 13 % снизу, является крайним текстовым блоком на странице, по высоте не больше 3,5 % страницы и не длиннее 150 знаков; каждая оговорка защищает реальный случай (титул, узкая колонка) — `internal/research/datalab-to-marker/marker/processors/marginalia.py:13-46`. Удаление отменяется флагами `keep_pageheader_in_output` и `keep_pagefooter_in_output` — `internal/research/datalab-to-marker/marker/processors/marginalia.py:41-46`, `internal/research/datalab-to-marker/marker/processors/marginalia.py:95-106`; в CLI они же — `internal/research/datalab-to-marker/README.md:142`.

**Взять.** Дописать в Часть B, пункт 3 навыка `08-documents` (`skills/08-documents/SKILL.md:35`): выбрасывать текст можно только по названным условиям и с возможностью вернуть. У нас есть «не выдумывать», но нет «что разрешено потерять при конвертации».

**3.4. Гибрид с языковой моделью: по умолчанию в облако.**
`--use_llm` добавляет склейку таблиц между страницами, инлайн-математику и разбор форм; по умолчанию сервис — `gemini-3.5-flash`, список включает Claude, OpenAI, OpenRouter и локальный Ollama — `internal/research/datalab-to-marker/README.md:51-53`. Ollama подключается отдельным классом сервиса с адресом и моделью — `internal/research/datalab-to-marker/README.md:382-392`.

**Отклонить как режим по умолчанию.** `AGENTS.md`, раздел 14: путь «сомневаешься — отправь страницу в облако» несовместим с локальным режимом. Разрешён только локальный Ollama и только с согласия человека.

**3.5. Предел метода назван до того, как его найдёт читатель.**
Раздел ограничений: очень сложная вёрстка с вложенными таблицами и формами может не получиться, формы могут отрисоваться плохо, оба случая лечатся `--use_llm` и `--force_ocr` — `internal/research/datalab-to-marker/README.md:560-567`. Рядом таблица «что делать, если» на девять ситуаций — `internal/research/datalab-to-marker/README.md:440-447`.

**Взять.** Дописать в Часть D навыка `08-documents` (`skills/08-documents/SKILL.md:46-56`): предел называется заранее, а не после вопроса «почему тут каша». Созвучно `AGENTS.md`, раздел 5.

**3.6. Структурный выход нужен там, где нужен адрес факта.**
В Markdown картинки идут ссылками, таблицы — разметкой, формулы — в `$$`, код — в тройных кавычках — `internal/research/datalab-to-marker/README.md:283-301`. В JSON блоки лежат деревом с координатами полигона и полем `section_hierarchy`, где `1` — это `h1` — `internal/research/datalab-to-marker/README.md:303-322`; отдельный формат `chunks` отдаёт плоский список верхнеуровневых блоков с готовым HTML — `internal/research/datalab-to-marker/README.md:353-355`.

**Взять.** Дописать в Часть B навыка `08-documents` (`skills/08-documents/SKILL.md:31-37`): два выхода на два случая — Markdown, когда документ читают глазами, и структурный JSON, когда надо вынуть факт с адресом. Это же ложится в «Куда писать» (`skills/08-documents/SKILL.md:58-64`), где уже разделены `workspace/artifacts/` и `workspace/data/`.

**3.7. Лицензия весов и парк воркеров.**
Код — Apache 2.0, веса — OpenRAIL-M: бесплатно для исследований, личного использования и компаний до 5 млн выручки, дальше платно — `internal/research/datalab-to-marker/README.md:63-65`. Пакетная обработка идёт многопроцессным пулом с общим инференс-сервером и шардированием по машинам — `internal/research/datalab-to-marker/README.md:153-170`.

**Отклонить.** Пакетная обработка не наш сценарий (у человека единицы документов), а лицензия весов делает инструмент непригодным как рекомендация без оговорки.

---

## 4. microsoft-markitdown

**Структура.** Четыре пакета: ядро `markitdown`, обёртка `markitdown-mcp`, плагин `markitdown-ocr`, образец плагина — `internal/research/microsoft-markitdown/README.md:325-333`. Конвертеров около двадцати, по одному на формат: PDF, DOCX, PPTX, XLSX, аудио, ZIP, EPUB, YouTube — `internal/research/microsoft-markitdown/README.md:11-24`.

**4.1. Граница применения написана в первом абзаце.**
«Лёгкая утилита… для текстового анализа; может не быть лучшим выбором для высокоточного преобразования для человека» — `internal/research/microsoft-markitdown/README.md:9`.

**Взять как форму отказа.** Дописать в «Чего не делать» навыка `08-documents` (`skills/08-documents/SKILL.md:74-81`): у нас нет фразы «этот инструмент не для правки документа и не для точных таблиц». Готовая формулировка экономит человеку час на разочарование.

**4.2. Ядро из шести зависимостей, форматы — опциями.**
Обязательных зависимостей шесть: `beautifulsoup4`, `requests`, `markdownify`, `magika`, `charset-normalizer`, `defusedxml` — `internal/research/microsoft-markitdown/packages/markitdown/pyproject.toml:27-34`. PDF, DOCX, XLSX, аудио и Azure-конвертеры подключаются extras, а `[all]` тянет pandas, lxml, pdfminer, pdfplumber, olefile и Azure SDK — `internal/research/microsoft-markitdown/packages/markitdown/pyproject.toml:36-64`.

**Взять.** Дописать в Часть B навыка `08-documents` (`skills/08-documents/SKILL.md:31-37`): «текст читается лёгким путём, сложная вёрстка — отдельной установкой». Что потянет за собой `[all]` — pandas, lxml, pdfminer, pdfplumber, Azure SDK, — это цена, которую называем заранее, а не ставим человеку молча.

**4.3. Самая узкая функция вместо универсальной.**
`convert()` намеренно всеяден: локальные файлы, URL и потоки. Если нужен только локальный файл — `convert_local()`, нужен контроль над загрузкой — сам `requests.get()` и `convert_response()`, максимум контроля — `convert_stream()` — `internal/research/microsoft-markitdown/README.md:394-400`. Там же предупреждение, что утилита работает с правами процесса и может открыть любую доступную ему ссылку.

**Взять.** `AGENTS.md`, раздел 12 (презумпция приватности) и Часть C навыка `08-documents` (`skills/08-documents/SKILL.md:39-44`): читаем локальный файл локальной функцией, URL не передаём в конвертер. Дешёвая техническая форма нашего «не сканировать лишнего».

**4.4. Тип файла определяется содержимым, а не расширением.**
Тип угадывается библиотекой `magika` по байтам потока — `internal/research/microsoft-markitdown/packages/markitdown/src/markitdown/_markitdown.py:762-765`; если угаданное расходится с подсказкой по имени файла, в список кандидатов попадают оба варианта — `internal/research/microsoft-markitdown/packages/markitdown/src/markitdown/_markitdown.py:818`.

**Взять.** Дописать в Часть B навыка `08-documents` (`skills/08-documents/SKILL.md:31-37`): расширение — не доказательство типа; при сомнении читать тем конвертером, который соответствует содержимому, и это не скрывать от человека.

**4.5. MCP-сервер конвертации: один инструмент и отсутствие прав.**
Инструмент один — `convert_to_markdown(uri)`, где `uri` это `http:`, `https:`, `file:` или `data:` — `internal/research/microsoft-markitdown/packages/markitdown-mcp/README.md:11-13`. Сервер не поддерживает аутентификацию, работает с правами пользователя и умеет прочитать любой файл, который тому доступен, поэтому по умолчанию слушает только localhost — `internal/research/microsoft-markitdown/packages/markitdown-mcp/README.md:132-134`.

**Отклонить сервер; взять фразу.** Блок 2, слайд Б2-10 «Протокол: зачем MCP» (`internal/draft/16_slide_plan.md:170`): протокол не выдаёт прав — их выдаёт процесс, под которым он запущен. Точная иллюстрация нашей границы «доступ даёт человек» (`AGENTS.md`, раздел 12).

**4.6. PDF здесь — текстовый слой плюс эвристика по координатам слов.**
Таблицы собираются из позиций слов, и в коде прямо оговорено, что это для счётов и форм, а не для многоколоночной вёрстки научных статей — `internal/research/microsoft-markitdown/packages/markitdown/src/markitdown/converters/_pdf_converter.py:398-405`. При отсутствии форм-вёрстки весь документ читается `pdfminer` без структуры — `internal/research/microsoft-markitdown/packages/markitdown/src/markitdown/converters/_pdf_converter.py:520-589`. OCR нет, формулы не разбираются, номеров страниц в выводе нет.

**Отклонить как инструмент точности.** Дописать в Часть B, пункт 2 навыка `08-documents` (`skills/08-documents/SKILL.md:34`): это нижняя граница ожиданий — «прочитать текст», а не «получить документ». Хорошо как дешёвый первый проход, плохо как единственный.

**4.7. Половина конвертеров тянет содержимое из сети.**
Кроме файлов поддерживаются RSS, Wikipedia, YouTube и поисковая выдача Bing — `internal/research/microsoft-markitdown/packages/markitdown/src/markitdown/converters/__init__.py:7-11`; для YouTube-транскрипта отдельная зависимость — `internal/research/microsoft-markitdown/packages/markitdown/pyproject.toml:61`.

**Отклонить.** Навык `08-documents`: наш предмет — документ человека на его диске. Сетевые источники — это уже внешний запрос, и он живёт в навыке предвалидации (`skills/03-prevalidation/SKILL.md:91-93`), а не в конвертере.

---

## 5. gavinHuang-pdf2md-mcp

**Структура.** Один файл `pdf2md_mcp/server.py` на 205 строк, один инструмент, документация в `docs/API.md`, тесты на 196 строк, примеры в `examples/` — `internal/research/gavinHuang-pdf2md-mcp/init.md:14-35`. Зависимости: `fastmcp`, `httpx`, `aiofiles`, `pymupdf4llm` — `internal/research/gavinHuang-pdf2md-mcp/pyproject.toml:25-32`.

**5.1. Тонкая обёртка: один глагол, два поля, пять полей ответа.**
Инструмент `convert_pdf_to_markdown(file_path, output_dir)` — `internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:117-121`. Ответ: путь к файлу, сводка, число страниц, страница старта, источник — `internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:183-189`.

**Взять как форму.** Блок 2 (Б2-10): сервер конвертации — обёртка на 200 строк, качество даёт библиотека, а не сервер. Полезно против ожидания «поставлю MCP — станет точно».

**5.2. Запись рядом с исходником.**
По умолчанию результат кладётся в ту же папку, что и входной файл — `internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:45-56`; для URL — в текущую рабочую папку — `internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:141-142`.

**Отклонить.** `AGENTS.md`, раздел 12 и навык `04-mvp-artifact` (`skills/04-mvp-artifact/SKILL.md:56-59`) плюс «Куда писать» в навыке документов (`skills/08-documents/SKILL.md:58-64`): пишем только в `workspace/`. Инструмент, который сыпет файлы в папку человека, нарушает нашу границу и засоряет рабочий каталог.

**5.3. Ошибка, записанная как результат.**
При сбое извлечения сервер формирует «успешный» markdown с текстом ошибки, заголовком страницы и подписью «Extraction failed, using fallback» — `internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:108-112`. Наружу при этом уходит обычный ответ без поля ошибки — `internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:183-189`.

**Отклонить решительно; взять зеркально.** `skills/05-validation-gate` и Часть D навыка документов (`skills/08-documents/SKILL.md:46-56`): конвертация, записавшая ошибку в файл, обязана считаться провалом. Наш аналог — правило приёмки из п. 2.2: почти пустой результат это провал, а не пустой документ.

**5.4. Приём, которого здесь нет: продолжение после обрыва.**
Докачка ищет в своём же файле маркеры `## Page N` и `<!-- Page N -->` и берёт наибольший номер — `internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:58-77`; извлечение запрашивает Markdown без указания постраничной разбивки — `internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:88-96`; маркер страницы пишется только в текст ошибки — `internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:111`. Разбор — в «Спорных утверждениях», п. 4.

**Отклонить как образец.** Дописать в Часть B навыка `08-documents` (`skills/08-documents/SKILL.md:31-37`): докачка опирается на собственный учёт обработанных страниц (как локаторы в п. 1.1), а не на догадку по тексту файла.

---

## Чего в клонах нет

1. **Русского языка по существу.** Списки языков есть: 37 языков распознавания, включая русский, в changelog MinerU (`internal/research/opendatalab-MinerU/docs/en/reference/changelog.md:314`); кириллица с русским среди 34 языков в OCR docling (`internal/research/docling-project-docling/docs/concepts/OCR_native.md:91-95`); у marker — только «multilingual» со ссылкой на чужой README (`internal/research/datalab-to-marker/README.md:151`). Ни одного замера качества на русских сканах и русских таблицах в клонах нет.
2. **Человеко-часов.** Скорость измерена в страницах в секунду на конкретном железе (`internal/research/datalab-to-marker/README.md:522-530`), память — в гигабайтах (`internal/research/opendatalab-MinerU/docs/en/usage/tiers.md:54`). Сколько человек потом проверяет результат глазами, не считает никто — а это и есть наша единица счёта (правило часа).
3. **Цен.** Ни одной цифры стоимости облачных путей: у marker только «$5 бесплатных кредитов» (`internal/research/datalab-to-marker/README.md:39`), у MinerU — команда запроса остатка квоты без прайса (`internal/research/opendatalab-MinerU/skills/mineru/SKILL.md:767-774`). Это вопрос внешнему исследователю, из кода он не решается.
4. **Что делать с результатом дальше.** Техническая приёмка есть (п. 2.2), но ни один клон не говорит, кому и зачем показывать конвертацию. У нас это шаг артефакта (`skills/04-mvp-artifact/SKILL.md:46-55`), и в клонах ему соответствия нет.
5. **Проверки, что формула не потерялась.** Формулы отдаются как LaTeX (`internal/research/opendatalab-MinerU/docs/next/middle-json/current-medium.md:80`) или в `$$` (`internal/research/datalab-to-marker/README.md:291`), но ни один не сверяет число формул до и после конвертации. Для нашей приёмки это очевидный пункт, которого в чужих чек-листах нет.

## Спорные утверждения списка

Проверялись заявления владельца из `internal/draft/25_owner_repo_list.md:5-9`.

**1. «MinerU склеивает разорванные между страницами таблицы» — подтвердилось с оговоркой.**
Склейка есть, но она часть режима отображения: `DEFAULT` склеивает только таблицы между страницами — `internal/research/opendatalab-MinerU/docs/next/middle-json/rendering.md:490`; `FULL` не склеивает таблицы вообще — `internal/research/opendatalab-MinerU/docs/next/middle-json/rendering.md:499`; неудачная склейка оставляет две таблицы — `internal/research/opendatalab-MinerU/docs/next/middle-json/rendering.md:505`. Отдельная LLM-склейка ячеек на границе страниц выключена по умолчанию и требует внешнего OpenAI-совместимого сервиса — `internal/research/opendatalab-MinerU/docs/en/usage/quick_usage.md:97-113`. Значит «склеивает» верно для качественного режима, а не как свойство формата.

**2. «MinerU восстанавливает математические формулы в формате LaTeX» — подтвердилось частично.**
Формула хранится как LaTeX без внешних разделителей — `internal/research/opendatalab-MinerU/docs/next/middle-json/current-medium.md:80`; тип `equation` описан как «межстрочный LaTeX» — `internal/research/opendatalab-MinerU/docs/next/middle-json/current-medium.md:115`. В Markdown при непустом содержимом выводится LaTeX, при пустом — подставляется изображение — `internal/research/opendatalab-MinerU/docs/next/middle-json/rendering.md:516`. У быстрого режима межстрочные формулы очищаются и остаются только картинкой с рамкой — `internal/research/opendatalab-MinerU/docs/en/reference/output_files.md:99-106`. То есть LaTeX есть не всегда и не во всех тирах.

**3. «markitdown — легковесная утилита» — подтвердилось частично.**
Ядро действительно шесть зависимостей — `internal/research/microsoft-markitdown/packages/markitdown/pyproject.toml:27-34`. Но покрытие форматов из README (`internal/research/microsoft-markitdown/README.md:11-24`) требует extras, а `[all]` включает pandas, lxml, pdfminer, pdfplumber, olefile и Azure SDK — `internal/research/microsoft-markitdown/packages/markitdown/pyproject.toml:36-64`. Легковесность ядра не равна лёгкости установки полного набора.

**4. «pdf2md-mcp… с поддержкой докачки при обрыве сессии» — не подтвердилось.**
Заявление стоит в README (`internal/research/gavinHuang-pdf2md-mcp/README.md:9`), но механизм держится на регулярном выражении по маркерам `## Page N` в собственном выводе (`internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:58-77`), а извлечение заказывает Markdown без постраничного режима (`internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:88-96`) — маркеры никто не создаёт, кроме ветки ошибки (`internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:111`). Тесты докачку не проверяют: они вызывают метод `extract_pdf_content_with_sampling` и поле `sampling_used`, которых в коде нет — `internal/research/gavinHuang-pdf2md-mcp/tests/test_server.py:76-83`, `internal/research/gavinHuang-pdf2md-mcp/tests/test_server.py:144-154`; в сервере метод называется иначе и работает без контекста — `internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:78-80`. Дополнительно `init.md` помечает галочками «использовать MCP sampling» и «не использовать библиотеку» — `internal/research/gavinHuang-pdf2md-mcp/init.md:6`, — а код говорит обратное: «instead of MCP sampling» — `internal/research/gavinHuang-pdf2md-mcp/pdf2md_mcp/server.py:80`.

**5. «docling… с сохранением иерархии заголовков и таблиц» — не подтвердилось по умолчанию.**
Иерархия заголовков восстанавливается отдельной стадией, выключенной по умолчанию; без неё все заголовки приходят уровнем 1 — `internal/research/docling-project-docling/docs/usage/heading_levels.md:1-11`. Оценка качества таблиц ещё не реализована — `internal/research/docling-project-docling/docs/concepts/confidence_scores.md:42`. Заявление верно для настройки, а не из коробки.
