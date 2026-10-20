# Проверка результата и работа со знаниями: три репозитория

Прочитаны файлы трёх клонов в `internal/research/`. Утверждения ниже — `[база]`: это прочитанные строки, не пересказ. Инструменты не запускались, ничего не устанавливалось, клоны не менялись.

| Репозиторий | Коммит | Дата | Что внутри |
|---|---|---|---|
| [usestrix-strix](internal/research/usestrix-strix) | `a0f8ea2` | 2026-10-18 | агент-пентестер на Python (`strix/`), 9 потребительских навыков в `skills/`, документация в `docs/` |
| [Egonex-AI-Understand-Anything](internal/research/Egonex-AI-Understand-Anything) | `f2d0164` | 2026-10-12 | плагин разбора кода: 10 агентов в `agents/`, навыки `understand*`, граф знаний, `docs/benchmarks` и `docs/incremental` |
| [roboco-io-awesome-vibecoding](internal/research/roboco-io-awesome-vibecoding) | `e0dc931` | 2026-10-18 | курируемый каталог: политика отбора, журнал проверки на 1756 строк, реестр статусов, автоматизация на LLM |

---

## 1. usestrix-strix: как выглядит отчёт о проверке

**1.1. Таблица покрытия с тремя градациями.** Отчёт по OWASP начинается не с находок, а с честной таблицы «категория → Strong / Partial / Not testable from outside», и в каждой строке сказано, чем именно покрытие ограничено. Категория A09 прямо объявлена непроверяемой снаружи: «State this rather than reporting it as passed» — [skills/owasp-top-10-testing/SKILL.md:22-33](internal/research/usestrix-strix/skills/owasp-top-10-testing/SKILL.md#L22-L33). **Взять как приём:** блок «покрытие» в шаблон отчёта проверки (навык `05-validation-gate`, шаблон отчёта в `templates/`) и в отчёт `verify.py`: что проверено, что частично, что не проверялось и почему.

**1.2. «Ноль» означает «в границах проверенного».** Код возврата `0` трактуется как «ничего эксплуатируемого не доказано в том, что анализировали», и рядом требуется второй свидетель — `run.json` со статусом и расходом бюджета: `0` бывает и у прогона, оборванного по бюджету, — [skills/find-security-vulnerabilities-in-code/SKILL.md:54](internal/research/usestrix-strix/skills/find-security-vulnerabilities-in-code/SKILL.md#L54), [skills/penetration-testing-with-strix/SKILL.md:110](internal/research/usestrix-strix/skills/penetration-testing-with-strix/SKILL.md#L110), «an empty result set from a truncated scan is not a clean bill of health» — [skills/application-security-testing/SKILL.md:64](internal/research/usestrix-strix/skills/application-security-testing/SKILL.md#L64). **Взять как правило:** `0` от `verify.py` не значит «всё проверено», а значит «в пределах перечисленных проверок расхождений нет»; формулировка ложится в `AGENTS.md` §13 рядом с кодами 0/1/2.

**1.3. Ложная зелень от вырожденного входа.** Проверка исправления идёт диффом от базовой ветки, и там прямо предупреждают: если взять upstream текущей ветки, база совпадёт с HEAD, дифф будет пустым и результат «чисто» — ложным; при неразрешимой базе скрипт обязан упасть, а не подставить `HEAD~1` — [skills/fix-security-vulnerabilities-with-strix/SKILL.md:44-57](internal/research/usestrix-strix/skills/fix-security-vulnerabilities-with-strix/SKILL.md#L44-L57). **Взять как приём:** проверка обязана падать, когда её вход пуст; это же основание нашего `verify_harness.py --self-test` (пустой каталог → вердикт `2`, не тихий успех).

**1.4. Карточка приёма заканчивается разделом проверки.** Шаблон навыка жёсткий: `Attack Surface → Methodology → Techniques → Bypass Methods → Validation`, где Validation — «How to confirm findings and avoid false positives» — [docs/advanced/skills.mdx:107-135](internal/research/usestrix-strix/docs/advanced/skills.mdx#L107-L135). Плюс третий пункт в требованиях к вкладу — «Validation steps. How to confirm without false positives» (там же, :139-143). **Взять как приём:** в `templates/knowledge-card.md` нет поля «как проверить, что приём сработал»; добавить раздел «Проверка» и требовать его в `knowledge/03_practices`.

---

## 2. Egonex-AI-Understand-Anything: судья, который не читает исходник

**2.1. Слепой судья с машинным списком замечаний.** Отдельный агент-ревьюер обязан сначала написать и выполнить скрипт детерминированных проверок, а потом судить только по его JSON: `issues` (критические) и `warnings`. Решение формальное: `approved: true` тогда и только тогда, когда `issues` пуст, любое число предупреждений допустимо. Перечитывать исходный файл вручную запрещено: «Trust the script's output» — [agents/graph-reviewer.md:186-194](internal/research/Egonex-AI-Understand-Anything/understand-anything-plugin/agents/graph-reviewer.md#L186-L194), :224-230. **Взять как приём:** это готовая форма нашего правила «судья не автор» — отдельный проход читает не работу, а отчёт проверки.

**2.2. Код возврата скрипта отделён от вердикта.** Скрипт возвращает `0`, даже если нашёл проблемы: «the exit code signals that the script itself ran correctly, not that the graph is valid»; `1` — только если скрипт сам упал — [agents/graph-reviewer.md:24-30](internal/research/Egonex-AI-Understand-Anything/understand-anything-plugin/agents/graph-reviewer.md#L24-L30). **Рассмотреть:** у нас `2` смешивает «декларация сломана» и «проверка не смогла прочитать вход»: падение самого проверяльщика тоже даёт `2` — [scripts/verify.py:51-53](scripts/verify.py#L51-L53), отсутствие папки базы знаний — [scripts/verify_knowledge.py:78-81](scripts/verify_knowledge.py#L78-L81). Разделение стоит зафиксировать словами в `AGENTS.md` §13, даже если коды не менять.

**2.3. «Доказательство не равно полноте».** Разбор собственного провала: схема прошла валидацию, но это не доказывает полноту инвентаря; переменная с именем `completeEvidence` проверяла только форму объекта, и её имя завышало установленное; неподдержанный случай остаётся `unknown` и блокирует удаление, а не исчезает — [docs/incremental/source-evidence-audit.md:33-39](internal/research/Egonex-AI-Understand-Anything/docs/incremental/source-evidence-audit.md#L33-L39), :53. **Взять как правило:** имя проверки не должно обещать больше, чем она проверяет; в отчёте `verify.py` перечислять, что он не ловит (у нас это уже признано в §13, но без запрета на громкие имена).

**2.4. Решение отдельно от доказательства и с причиной.** Компаратор потребляет свидетельства и возвращает «decision plus a reason»; производитель свидетельств и потребитель не знают правил друг друга, а неизвестное покрытие блокирует вывод — [docs/incremental/source-evidence-audit.md:55](internal/research/Egonex-AI-Understand-Anything/docs/incremental/source-evidence-audit.md#L55), :53. **Взять как приём:** в карточке знания и в гейте валидации два поля: `решение` и `причина`, причина ссылается на файл и строку, а не пересказывает.

**2.5. Третье состояние отчёта.** Схема отчёта допускает `status: ok | degraded | failed`, и `degraded` означает «прогон дошёл, но с предупреждениями и пропусками» — [docs/benchmarks/large-repo-report-1.0.0.schema.json:36](internal/research/Egonex-AI-Understand-Anything/docs/benchmarks/large-repo-report-1.0.0.schema.json#L36), [docs/benchmarks/large-monorepo.md:155-165](internal/research/Egonex-AI-Understand-Anything/docs/benchmarks/large-monorepo.md#L155-L165). **Рассмотреть:** полезно, но нам хватает 0/1/2 плюс блок покрытия из 1.1; заводить четыре состояния ради трёх проверок — лишний вес.

---

## 3. roboco-io-awesome-vibecoding: как записывается проверка

**3.1. Пять условий приёма и три исхода.** Приём в каталог проходит пять условий (польза, проверяемое доказательство, отличие, прозрачность доступа, живость), и на выходе ровно три исхода: `Accept` / `Needs review` / `Reject`; отказ обязан называть конкретный критерий, а «needs review» — это не «нет»: временная ошибка доступа не доказательство негодности — [docs/curation-policy.md:5-19](internal/research/roboco-io-awesome-vibecoding/docs/curation-policy.md#L5-L19). Отдельно сказано, что звёзды и популярность — контекст, а не доказательство (:13). **Взять как приём:** перенести на приём в `knowledge/03_practices`: три исхода вместо «берём / не берём», отказ с указанием критерия, «рассмотреть» как рабочее состояние.

**3.2. Формат записи проверки, повторяемый дословно.** Каждая единица — якорь, затем четыре обязательные строки: `Decision` + `location` + `reviewed` (дата), `Finding` (что именно установлено), `Evidence` (нумерованные ссылки). Пример: [docs/lifecycle-review-2026-09-18.md:9-16](internal/research/roboco-io-awesome-vibecoding/docs/lifecycle-review-2026-09-18.md#L9-L16). В шапке журнала — метод и прямое перечисление, чего не делали: «No application installation, paid enrollment, or security audit was performed» (:3-7). **Взять как приём:** это почти наш `templates/knowledge-card.md`, только решение и ссылки-доказательства стоят в одной записи с датой; паспорт карточки расширить полями `decision` / `reason` / `evidence_urls`.

**3.3. Дата проверки принадлежит записи, а не файлу.** Правило: обновлять дату только у той строки, которую действительно перепроверили, и «never refreshes an entry's verification date merely because the page was regenerated» — [docs/automation.md:89](internal/research/roboco-io-awesome-vibecoding/docs/automation.md#L89). Там же граница возможностей: «Semantic translation quality still depends on the model; deterministic checks do not prove every factual statement» (:91). **Взять как правило:** у карточки базы знаний `date_verified` меняется только вместе с новой ссылкой-доказательством; массовое обновление дат — нарушение, и проверять это должен `verify_knowledge.py`, а не память исполнителя.

**3.4. Код проверяет форму, человек или модель судит смысл.** Прямая формулировка: код валидирует структуру результата, наблюдавшиеся ссылки, допустимые файлы, уникальность якорей; «The model still judges relevance, substance, and factual support; those semantic judgments are not proven by URL or Boolean checks» — [docs/curation-policy.md:23-29](internal/research/roboco-io-awesome-vibecoding/docs/curation-policy.md#L23-L29). Выдуманные или не открытые в этом прогоне ссылки отклоняются (:25). **Взять как правило:** это точная формулировка границы `verify.py`: он принимает форму, а «судья не автор» проверяет смысл; в шапке декларации писать, какой уровень кем закрыт.

---

## Топ-3 приёма

1. **Блок покрытия в каждом отчёте о проверке.** Таблица «что проверено → полностью / частично / не проверялось и почему», с отдельной строкой под то, что проверить нельзя в принципе. Проверяющий не может отчитаться «чисто», не сказав, где он не смотрел: [skills/owasp-top-10-testing/SKILL.md:22-33](internal/research/usestrix-strix/skills/owasp-top-10-testing/SKILL.md#L22-L33).
2. **Слепой судья поверх машинного списка замечаний.** Скрипт даёт `issues` и `warnings`, судья читает только их, вердикт формальный: критические непусты — отклонено. Автор не участвует, перечитывать работу вручную запрещено: [agents/graph-reviewer.md:186-194](internal/research/Egonex-AI-Understand-Anything/understand-anything-plugin/agents/graph-reviewer.md#L186-L194).
3. **Запись проверки из четырёх строк.** `Решение (и куда)` + `дата проверки` + `что установлено` + `ссылки-доказательства`, дата ставится только тому, что действительно открывали: [docs/lifecycle-review-2026-09-18.md:9-16](internal/research/roboco-io-awesome-vibecoding/docs/lifecycle-review-2026-09-18.md#L9-L16).

## Чего не берём

- **Из strix:** сам пентест, Docker, LLM-ключи, флаги CLI, SARIF, `--max-budget`, облачную панель. Это инструмент нападения на чужой софт; нашему человеку он не нужен ни на одном шаге, а перенос тянет за собой установку и ключи. Ранжирование «по эксплуатируемости» тоже не берём: у нас для этого есть своя шкала силы сигнала 1–19, и она про обязательства человека, а не про дыры в коде.
- **Из Understand-Anything:** tree-sitter, встроенные парсеры на 24 языка, 16 типов узлов и 29 типов рёбер графа, `pairId` с диджестами, дашборд, протокол бенчмарка, синхронизация версий в шести манифестах. Это ровно тот случай, когда набор превращается в каталог: один только список языковых аддонов (`skills/understand/languages/*.md`) — 24 файла, которые наш человек на шаге интервью не откроет никогда. Граф с типизированными связями нам не нужен: у нас связи держит `knowledge/INDEX.md` и поле `used_in_skills`.
- **Из roboco:** автоматизация на Pi + Exa + Kimi, GitHub Actions, SQLite-кэш, трёхъязычный README, лимиты разделов 10/8/8/6/8/12, регулярный еженедельный обход. Это обслуживание витрины на 156 записей; у нас в базе четыре карточки канона и план пополнения на полтора десятка строк, и автоматизация дороже самой работы. Сам жанр «awesome-list» не берём: он по определению каталог, а критерий у нас обратный — снижать стоимость шага, а не пополнять список.

---

## Проверка самой заметки

`python scripts/verify.py` на этой заметке вернул `0`. Но ни одна из восьми проверок её не читает: заметка не объявлена ни в одной декларации источников, поэтому `0` здесь значит «в проекте нет расхождений», а не «заметка верна». Ровно об этом пункты 1.2 и 2.3: код возврата говорит о границах проверки, а не о качестве текста. Смысл и полноту выжимки проверял отдельным проходом по прочитанным файлам, а не тот, кто её писал.
