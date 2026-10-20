# harness-engine, agent-harness-skill: приёмы

Прочитаны все файлы двух репозиториев в `internal/research/`. Все утверждения ниже — `[база]`: это прочитанные строки, не пересказ.

Сокращения путей:

- `HE/` = [internal/research/sujalmanpara-harness-engine](internal/research/sujalmanpara-harness-engine)
- `AH/` = [internal/research/netresearch-agent-harness-skill](internal/research/netresearch-agent-harness-skill)

**Честная оговорка по термину.** Слова «ratchet» и «храповик» нет ни в одном файле обоих репозиториев (поиск по всем файлам, 0 совпадений; в AH есть только `provenance: regression`). Механизм существует под другими именами, и ниже разобрано, под какими именно.

---

## 1. Храповик: формулировка и применение

### 1.1. В HE: лозунг без механизма

Храповик заявлен как принцип и процитирован дважды:

- [HE/README.md:222](internal/research/sujalmanpara-harness-engine/README.md#L222): строка про Хэшимито — «Agent = Model + Harness.» **Every mistake → permanent fix in harness.**
- [HE/docs/phase2-architecture.md:184](internal/research/sujalmanpara-harness-engine/docs/phase2-architecture.md#L184): принцип 7 из списка — «**Every failure improves the harness** (Hashimoto) — harness grows from mistakes».

Применения нет: в репозитории один скрипт, `eval/run_eval.py`, и он офлайн-раннер евала, не гейт. Сам храповик лежит в роадмапе незакрытым пунктом — [HE/README.md:253](internal/research/sujalmanpara-harness-engine/README.md#L253): `v0.5 — Self-improving harness (learns from failures)`. То есть в HE это направление мысли, а не работающая петля.

### 1.2. В AH: храповик как замена прозы проверкой

Формулировка дана один раз и очень жёстко, в [AH/skills/agent-harness/references/enforcement-mechanisms.md:86-89](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L86-L89):

> 1. **A rule that must hold gets a mechanism from the table below, not a sentence in a skill.** If it can be checked by a script, it belongs in a hook and in CI. Prose is how an agent is *offered* a way to do the job; it is not how the job is *required* to come out.

Практическая форма — [enforcement-mechanisms.md:105](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L105):

> when CI catches a mechanical issue that a hook could have caught, the absence of the hook is the bug. Strengthen the harness rather than asking the operator to be more careful.

То есть в AH сбой переопределяется: он не «ошибка исполнителя», а «отсутствующая проверка». Дальше — §4.

### 1.3. Почему AH вообще не верит правилам в тексте

Это измеренная часть, а не декларация: [enforcement-mechanisms.md:8-39](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L8-L39). Четыре рычага прогонялись на `claude-haiku-4-5-20251001` против контрольной ветки:

| рычаг | что меняет | замер |
|---|---|---|
| файл-справка, который прикладывает скилл | нужный текст доступен | 3 из 3 загрузок скилла, файл не открыл никто |
| шаг в рабочем процессе скилла | скилл велит агенту | предложение было в контексте во всех прогонах, изменений нет |
| чекпойнт в собственном валидаторе скилла | скилл проверяет работу | проверку не запускали ни разу |
| `description`, слова в хвосте триггеров | загрузится ли скилл | 1 из 6 против 1 из 6, Fisher p 1.000 |

И отдельно ([enforcement-mechanisms.md:80-82](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L80-L82)): «**And being reached is not being obeyed.**» — скилл загружался 6 из 6, механический результат остался 0 из 6. Тот же замер в [AH/skills/agent-harness/SKILL.md:62](internal/research/netresearch-agent-harness-skill/skills/agent-harness/SKILL.md#L62) со ссылкой на issue #61: собственный валидатор скилла запускался 1 раз из 6 в самом очевидном случае.

**Вывод, который переносится к нам напрямую:** «правило написано в AGENTS.md» — это ноль. Именно этим объясняется, почему правило от 18.10.2026 могло не сработать.

### 1.4. Храповик для уже существующих правил: лестница

Для правил, которые уже написаны, но нарушаются, в AH есть явная лестница повышения жёсткости — [enforcement-mechanisms.md:626](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L626):

> **Escalate advisory to deny when the nudge is ignored.** Ship a rule as `systemMessage` first and let it run for a few sessions. If the transcript shows the nudge firing correctly and the behaviour continuing anyway, that is the evidence for promoting it to `deny` — the rule is not unclear, it is unenforced.

Три ступени: `systemMessage` (видно, не блокирует) → `deny` → `updatedInput` (переписать вызов). Верхняя ступень ограничена правилом обратного доказательства ([enforcement-mechanisms.md:698-701](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L698-L701)): повышать до перезаписи только там, где в транскрипте видно, что **тот же** `deny` срабатывал повторно на форме, у которой ровно один правильный вид.

---

## 2. Скрипты проверки

Скриптов два, оба в AH. В HE скриптов проверки нет.

### 2.1. `verify-harness.sh`

Файл: [AH/skills/agent-harness/scripts/verify-harness.sh](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh), 797 строк. Шапка — [строки 1-5](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L1-L5): `set -euo pipefail`, зависимости только coreutils + git, `jq` опционален. Запускается из корня проверяемого репозитория.

Три уровня, каждый — своя функция: `run_level1` ([203-208](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L203-L208)), `run_level2` ([427-432](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L427-L432)), `run_level3` ([565-570](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L565-L570)).

| Уровень | Что физически проверяется | Строки |
|---|---|---|
| 1 | `AGENTS.md` существует | [161-167](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L161-L167) |
| 1 | `wc -l` по `AGENTS.md` < 150 | [169-181](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L169-L181) |
| 1 | в `AGENTS.md` есть заголовок `## Commands` | [183-193](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L183-L193) |
| 1 | каталог `docs/` существует | [195-201](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L195-L201) |
| 2 | каждая markdown-ссылка из `AGENTS.md` разрешается в существующий путь | [215-241](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L215-L241) |
| 2 | команда `make X` из `AGENTS.md` есть целью в `Makefile`; `composer X` — скриптом в `composer.json` (со списком встроенных команд, [277](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L277)); `npm run X` — скриптом в `package.json` | [244-321](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L244-L321) |
| 2 | `docs/ARCHITECTURE.md` существует | [323-329](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L323-L329) |
| 2 | CI-workflow с harness-job есть | [364-425](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L364-L425) |
| 3 | git-хуки автоактивируются (`.envrc` + hooksPath, `.husky/`, `composer.json` post-install) | [438-467](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L438-L467) |
| 3 | декларация `.harness/checkpoints.yml` и CI-джоб, который её запускает — **в обе стороны** | [336-362](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L336-L362) |
| 3 | PR/MR-шаблон есть (включая org-level через `gh api`) | [469-522](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L469-L522) |
| 3 | дрейф: в последнем коммите менялись build/CI-файлы, а `AGENTS.md` — нет | [524-563](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L524-L563) |

Что делает при провале:

- Копит счётчики: `fail()` ([127-141](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L127-L141)) печатает `✗`, добавляет GitHub-аннотацию `::error file=AGENTS.md::<msg> -- required for Level N` ([135](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L135)) и gitlab-строку; `warn()` ([143-156](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L143-L156)) — то же с `::warning`.
- Код возврата различает «сломан харнесс» и «есть советы»: `0` — всё прошло, `1` — есть ошибки, `2` — только предупреждения ([788-794](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L788-L794)).
- Форматов три: text / github / gitlab, автоопределение по `GITHUB_ACTIONS`/`GITLAB_CI` ([60-71](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L60-L71)).
- Портативность — как принцип в [AH/skills/agent-harness/references/adr/001-verify-first-design.md:26](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/adr/001-verify-first-design.md#L26): скрипт копируется в чужой репозиторий и работает без установленного скилла.

Чего он **не** делает, и это важно для нас: он проверяет непротиворечивость документации и CI, а не работу агента. Где агент пишет файлы, он не смотрит.

### 2.2. `run-shipped-checkpoints.sh`

Файл: [AH/skills/agent-harness/scripts/run-shipped-checkpoints.sh](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/run-shipped-checkpoints.sh). Читает `.harness/checkpoints.yml`, подтягивает каждый скилл по закреплённому ref и запускает его чекпойнты против репозитория. Валяется по `severity`: провал `error` — код 1, всё остальное — 0 ([вывод](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/run-shipped-checkpoints.sh#L173-L192)); `blocked` не гейтит никогда, потому что это сломанный чекпойнт, а не сломанный проект ([27-29](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/run-shipped-checkpoints.sh#L27-L29)). Неразрешимая декларация — код `2`, а не тихий пропуск ([86-97](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/run-shipped-checkpoints.sh#L86-L97), [128-163](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/run-shipped-checkpoints.sh#L128-L163)).

### 2.3. Тест, который проверяет сам проверяльщик

[AH/tests/verify-harness-runs.sh:4-14](internal/research/netresearch-agent-harness-skill/tests/verify-harness-runs.sh#L4-L14) объясняет, зачем он есть: скрипт падал на `set -euo pipefail` из-за незащищённого `git remote get-url origin | sed` в проверке PR-шаблона; без remote пайплайн возвращал ненулевой код, `set -e` убивал скрипт до отрисовки, на выходе было **ноль байт и код 2** — что читается как сломанный харнесс, а не как отсутствующий remote. Поэтому свойство под тестом сформулировано так ([14](internal/research/netresearch-agent-harness-skill/tests/verify-harness-runs.sh#L14)): «the property under test is not a message, it is that the verifier speaks at all». Дальше два фикстурных репозитория, разница ровно одна — есть ли `origin` ([57-65](internal/research/netresearch-agent-harness-skill/tests/verify-harness-runs.sh#L57-L65)), и оба обязаны прийти к одному вердикту, иначе «фикс изменил поведение, а не остановил падение».

---

## 3. Как оформляются жёсткие правила

### 3.1. Разделение: текст правила и машинная форма

Одна и та же норма живёт в двух местах, и это осознанная конструкция.

**Текст** — `AGENTS.md`. По [enforcement-mechanisms.md:461-493](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L461-L493) это механизм №8, сила — **Soft**: «No mechanical enforcement. An agent can ignore instructions. This is why CI and hooks exist as harder layers» ([493](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L493)). Шаблон формы — [AH/skills/agent-harness/templates/AGENTS.md.tmpl:30-36](internal/research/netresearch-agent-harness-skill/skills/agent-harness/templates/AGENTS.md.tmpl#L30-L36): пять пунктов, каждый называет предмет и куда идти за деталью (`**Commits:** Use Conventional Commits`, `**Plans:** Multi-file changes require an exec-plan in docs/exec-plans/active/`). Правила не пересказывают содержание, а адресуют.

**Машинная форма** — `checkpoints.yaml`, где у правила есть `id`, `severity` и исполняемое тело. Пример с `severity: error` — [AH/skills/agent-harness/checkpoints.yaml:51-55](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L51-L55) (AH-10, все ссылки в `AGENTS.md` разрешаются). Шкала: `error` гейтит, `warning` сообщает, `info` не значит ничего.

Схема ID — [AH/skills/agent-harness/references/adr/005-checkpoint-maturity-model.md:74-77](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/adr/005-checkpoint-maturity-model.md#L74-L77): `AH-0x` уровень 1, `AH-1x` уровень 2, `AH-2x` уровень 3, с запасом внутри диапазона, чтобы не перенумеровывать.

### 3.2. Требования к формулировке проверяемой части

Из комментариев в самом `checkpoints.yaml` выводится набор правил качества, каждый — след конкретной поломки:

- **`desc` — однострочный скаляр.** [155-159](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L155-L159): `desc: >-` доехал до раннера литеральной строкой `>-`, и каждая строка отчёта по этому чекпойнту читалась как `[AH-32] >-` вместо правила.
- **Тело — только из белого списка команд.** [190-197](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L190-L197): `pattern: >-` был отвергнут раннером (`'>-' not in allowed command whitelist`), то есть чекпойнт не запускался вообще. Многострочное тело — `type: script`, а `||` переносится в конец левого операнда, потому что строка literal-блока, начинающаяся с `||`, — синтаксическая ошибка bash.
- **Никаких `$(...)`.** [109-113](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L109-L113): раннер их отвергает, поэтому AH-22 собирает вывод через `cat ... | grep`, а не через подстановку.
- **`| head -1` выброшен.** [107-108](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L107-L108): `head` на пустом входе возвращает 0, значит он может только замаскировать статус, который `grep -q` и так несёт.
- **Ограничение записывается рядом с правилом, а не умалчивается.** [109-113](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L109-L113) содержит `KNOWN LIMIT:` с точным описанием случая, который проверка не покрывает. Обоснование — [enforcement-mechanisms.md:189-193](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L189-L193): «**A documented gap beats a wrong guard**», и записывать надо в самом чекере, рядом с правилом, которое он ограничивает.

### 3.3. Слои и их сила

[AH/skills/agent-harness/references/adr/002-enforcement-layers.md:9-10](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/adr/002-enforcement-layers.md#L9-L10) фиксирует решение: три слоя по силе — жёсткий (сервер: CI + branch protection), автоматический (локально: хуки, `.envrc`, post-install), мягкий (конвенция: `AGENTS.md`, PR-шаблон, Makefile). Вывод, который стоит унести: «No single mechanism is sufficient alone» ([10](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/adr/002-enforcement-layers.md#L10)).

Полная таблица силы — [enforcement-mechanisms.md:197-210](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L197-L210), 12 механизмов от `Hard` до `Soft`.

### 3.4. Правило, которое нельзя обойти агенту

Механизм №11 — [enforcement-mechanisms.md:579-701](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L579-L701). Это `PreToolUse`-хук Claude Code, который читает payload инструмента со stdin и отвечает вердиктом на stdout, **до** выполнения инструмента.

Сила заявлена отдельно ([587](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L587)): «Automatic and unbypassable *by the agent* — unlike every other mechanism here, there is no `--no-verify` equivalent the agent can reach for». И область применения ([589](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L589)): «the right instrument for a rule the agent keeps violating across every repo».

Требования к самому запрету: причина отказа пишется для того, кто её прочтёт, и в ней **называется, что запрет не блокирует** ([628](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L628)): «A gate that blocks a legitimate variant with no stated escape sends the agent hunting for a workaround. State the allowed forms explicitly».

### 3.5. Калибровка проверки перед выпуском

Отдельный раздел, который стоит прочитать целиком: [enforcement-mechanisms.md:146-193](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L146-L193). Тезисы:

- «**A false reject silently disables a real check**» ([153](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L153)): один проход ужесточения белого списка отклонил четыре законные проверки, включая ту, что искала ровно ту атаку, ради которой список делали, — и все четыре с тех пор рапортовали `fail` на каждом прогоне.
- Перед выпуском назвать **оба** направления ошибки: что даёт инцидент, ради которого делается проверка, и что даёт самый громкий законный вход ([161-166](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L161-L166)). Порог запрещающего гейта — там, где молчит негативный корпус, а не на краю позитивного ([167-168](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L167-L168)).
- Общий предикат у двух инструментов не должен читать окружающее состояние ([179-187](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L179-L187)): «a check that answers differently in two places is not one rule, it is two».

---

## 4. Превращение сбоя в правило

Отдельного документа «как превратить сбой в правило» нет ни в одном репозитории. Есть пять мест, из которых складывается шаг за шагом, и одно из них — ссылка наружу.

**Шаг 1. Сбой попадает в разбор, а не в фразу.** AH прямо отказывается владеть обучением: [AH/skills/agent-harness/references/harness-engineering-overview.md:50](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/harness-engineering-overview.md#L50) — «**The harness does not store learning itself.** It provides the rails… Learning is performed by `retro-skill` and materialized through specialist skills». Уточнение области — [SKILL.md:76](internal/research/netresearch-agent-harness-skill/skills/agent-harness/SKILL.md#L76): «Does not own learning».

**Шаг 2. Выбирается адрес правила, по старшинству.** Семь адресов, «authority-first»: `canonical-source`, `personal-rule`, `project-rule`, `skill-update`, `new-skill`, `checkpoint`, `harness-artefact` — [AH/skills/agent-harness/references/skill-integration-map.md:251](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/skill-integration-map.md#L251). Разделение по области:

- `project-rule` дописывается в `AGENTS.md`, который считается единственным хранилищем проектных правил; `CLAUDE.md` в проекте и дерево `docs/feedback/` не создаются ([259](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/skill-integration-map.md#L259)).
- `personal-rule` в репозиторий не попадает вообще — уходит в `~/.claude/CLAUDE.md` ([260](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/skill-integration-map.md#L260)).

**Шаг 3. Если правило механическое — оно становится чекпойнтом с происхождением.** Это самое переносимое. В [AH/skills/agent-harness/checkpoints.yaml:217-226](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L217-L226) у AH-37 два поля, которых нет у остальных:

```yaml
    provenance: regression
    source: https://github.com/netresearch/agent-harness-skill/issues/61
```

`provenance: regression` означает «этот чекпойнт появился из регрессии», `source` — ссылка на инцидент. Правило перестаёт быть мнением: у него есть дата и адрес причины.

**Шаг 4. Чекпойнт выносится из-под власти агента.** [enforcement-mechanisms.md:736-758](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L736-L758), механизм №12. Формулировка ([738](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L738)): «A check whose execution depends on an agent deciding to run it is not a control, however good the check is». Исполнение переезжает в CI: репозиторий объявляет в `.harness/checkpoints.yml`, чьи чекпойнты к нему применяются, закрепляя ref, и джоб их запускает. Три свойства, которые надо сохранить при переносе ([754-758](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L754-L758)): каждый ref закреплён (иначе гейт меняет смысл без коммита в гейтуемом репозитории); сломанная декларация орёт кодом 2, а не пропускается; декларация и джоб подразумевают друг друга в обе стороны.

**Шаг 5. Если правило про поведение агента, а не про файл — лестница §1.4**, с доказательством из транскрипта, а не из ощущения.

**Шаг 6. Перед выпуском — калибровка §3.5.**

**Честная граница:** шаг 2 описан в спеке, которой в этом репозитории нет. [AH/docs/specs/retro-skill.md:1-18](internal/research/netresearch-agent-harness-skill/docs/specs/retro-skill.md#L1-L18) сообщает, что спека переехала в `netresearch/retro-skill`, а местная копия удалена, потому что второй экземпляр снова разъедется. Так что полный шаг за шагом по превращению сессии в правило здесь не прочитать — только контракт интеграции, [skill-integration-map.md:249-268](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/skill-integration-map.md#L249-L268).

---

## 5. Примеры «до и после»

Форма одна и та же во всех сильных примерах: **не переписанное правило, а код проверки плюс комментарий, который называет сбой, вызвавший правку.** Комментарий — часть артефакта, а не история в голове.

### 5.1. HE: провал, который харнесс поймал

[HE/eval/results/EVAL_RESULTS.md:22-25](internal/research/sujalmanpara-harness-engine/eval/results/EVAL_RESULTS.md#L22-L25):

- Контроль: создал `myproject/{src,tests,docs}` как **один литеральный каталог** с таким именем — фигурные скобки не развернулись. Структуру не проверял.
- С харнессом: создал три отдельных каталога и проверил, что они есть.
- Вердикт ([25](internal/research/sujalmanpara-harness-engine/eval/results/EVAL_RESULTS.md#L25)): «Control agent wrote-and-forget».

Это ближайший аналог нашего сбоя: файлы легли не туда, и никто не посмотрел на диск. Приёмка задана списком путей в [HE/eval/tasks.json:42](internal/research/sujalmanpara-harness-engine/eval/tasks.json#L42) — `files_exist` перечисляет пять конкретных путей, включая три каталога. Слабость: список живёт в евале и применяется офлайн, гейтом он не стал.

### 5.2. AH: чекпойнт, который проходил на чём угодно

[AH/skills/agent-harness/checkpoints.yaml:25-35](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L25-L35), AH-03. Было: поле `value:` вместо `pattern:` — раннер его не читает. Дальше цепочка, записанная в комментарии: «The regex reached grep empty, and an empty pattern matches every line, so this checkpoint passed on any AGENTS.md — including one with no Commands section». Стало: `pattern: "(?i)## commands"`. То есть до правки проверка была зелёной всегда — ровно тот класс отказа, который AH называет худшим.

### 5.3. AH: проверка, которая не запускалась

[checkpoints.yaml:190-197](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L190-L197), AH-36. Было: `pattern: >-`, раннер отверг тело (`'>-' not in allowed command whitelist`), чекпойнт «never ran». Стало: `type: script` с literal-блоком и `||` в конце левого операнда. Плюс отдельно выброшен `| head -1`, который «only masks the status `grep -q` already carries».

### 5.4. AH: проверка, которая считала чужие файлы

[checkpoints.yaml:166-176](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L166-L176), AH-33 — самый близкий к нашей теме «посчитать файлы» пример. Было: `find` без отсечения деревьев зависимостей, и «of 150 `*Test.php` hits in one TYPO3 extension, 112 were under .Build/vendor/. A project with no tests of its own passed on its dependencies' test suites». Стало: явный `-prune` по `.Build`, `vendor`, `node_modules`, и обе группы в скобках, потому что без скобок `-prune -o` цепляется к первому `-name`, а `-print` — к последнему.

Мораль, которую стоит перенести: **счёт совпадений без указания, что именно считалось, — не проверка.** Тот же урок в [enforcement-mechanisms.md:170-177](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L170-L177): число «0 verdict changes across 274 patterns» пришлось публиковать с поправкой, потому что 274 — это строки после разрезания многострочных YAML-блоков, а реальный корпус был 230 однострочных шаблонов. Требование: «Write down the extraction command next to the number».

### 5.5. AH: три мелкие регрессии того же типа

- [checkpoints.yaml:63-68](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L63-L68) AH-12: в списке путей не было Forgejo/Gitea, поэтому репозиторий с рабочим workflow рапортовал, что его нет.
- [145-151](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L145-L151) AH-31: не был перечислен `phpstan.dist.neon`, поэтому проект с уровнем 9 в `.dist`-файле рапортовал как ниже 8.
- [73-81](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L73-L81) AH-20: не было org-level фолбэка, поэтому репозиторий на общем шаблоне организации рапортовал как репозиторий без шаблона.

### 5.6. AH: «до и после» внутри самого скрипта

[AH/skills/agent-harness/scripts/verify-harness.sh:504-511](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L504-L511) — комментарий стоит ровно над строкой, которую объясняет:

```
# `|| true` is load-bearing under `set -euo pipefail`: with no origin
# remote, git exits non-zero, pipefail makes the whole pipeline
# non-zero, and set -e kills the script here — before anything is
# rendered...
```

Ценность приёма: следующий читатель, желающий «почистить лишний `|| true`», наткнётся на инцидент, а не удалит защиту.

### 5.7. AH: регрессионный фикстур вместо описания

[AH/tests/verify-harness-runs.sh:43-65](internal/research/netresearch-agent-harness-skill/tests/verify-harness-runs.sh#L43-L65). Правило «проверяльщик обязан говорить» превращено в два репозитория, отличающихся одним флагом, и в проверку `[ -n "$out" ]`. Плюс третья проверка на то, что вердикт у обоих одинаков, — чтобы фикс не изменил поведение. Это шаблон, который стоит скопировать буквально: **инцидент → фикстура, отличающаяся одной деталью → проверка свойства, а не сообщения.**

---

## 6. Что взять в наш репозиторий

По убыванию отдачи. Первые три относятся прямо к инциденту 18.10.2026.

**1. Поле происхождения у нашего правила.** У нас правило записи файлов лежит текстом в [METHODOLOGY.md](METHODOLOGY.md), раздел 13.1 (файл `internal/draft/07_assistant_method.md` после переноса методики стал заглушкой на 20 строк). Взять форму `provenance: regression` + `source:` ([checkpoints.yaml:225-226](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L225-L226)) и приписать к пунктам 1-5 дату `2026-10-18` и что именно было затёрто. Дёшево, и снимает главную слабость: сейчас связь между сбоем и правилом есть только в разделе 13.1.

**2. Машинная форма правила — сверка ожидаемого списка с диском в обе стороны.** Копировать логику [verify-harness.sh:336-362](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L336-L362): декларация без исполнителя и исполнитель без декларации — оба `error`. Перенос буквальный: перед выдачей задания ведущий пишет список ожидаемых путей; после работы скрипт сравнивает список с фактическим деревом и даёт три исхода:

- путь ожидается, на диске нет → `error`, код 1;
- файл на диске есть, но его нет ни в одном списке → `error`, код 1 (именно это случилось 18.10.2026: файлы легли под именами другого источника, то есть одновременно пропажа и лишний файл);
- список не читается или битый → код `2`, никогда `0` ([run-shipped-checkpoints.sh:86-97](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/run-shipped-checkpoints.sh#L86-L97)). Третий исход — главный: сломанная декларация не должна выглядеть как зелёный прогон.

**3. Запрет на запись до записи, а не после.** Механизм №11 ([enforcement-mechanisms.md:579-628](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L579-L628)) — единственное во всём прочитанном, что физически не даёт сбою повториться: хук на `PreToolUse` для инструмента записи, `permissionDecision: deny` при пути вне выданного списка, и в причине отказа перечислены разрешённые пути ([628](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L628)). Агент не может обойти это флагом, в отличие от любого git-хука ([587](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L587)).
Важное ограничение, которое надо соблюсти: перезапись вызова (`updatedInput`) здесь **не** применяется. По таблице применимости ([676-683](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L676-L683)) переписывать можно только там, где правильный вид выводится из входных данных; неверный целевой путь из них не выводится, значит — `deny`, а не автоисправление.

**4. Коды возврата 0/1/2 как контракт.** [verify-harness.sh:788-794](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L788-L794): `0` чисто, `1` ошибки, `2` только предупреждения. Разделение позволяет вешать `1` на merge, а `2` — на отчёт. У нас сейчас проверок с кодами возврата нет вообще.

**5. Тест на самого проверяльщика.** [tests/verify-harness-runs.sh:4-14, 43-65](internal/research/netresearch-agent-harness-skill/tests/verify-harness-runs.sh#L4-L14): проверять не сообщение, а факт, что проверка вообще произнесла вердикт. Наш аналог: скрипт сверки путей обязан прогнаться на фикстуре с пустым каталогом и сказать «ноль ожидаемых, ноль найденных», а не молча упасть.

**6. Калибровка перед включением гейта.** [enforcement-mechanisms.md:146-193](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L146-L193). До включения запрета на запись прогнать два вопроса: что даёт сценарий 18.10.2026 и что даёт самая шумная законная запись (например, агент пишет промежуточный файл в `workspace/`). Порог — там, где молчит законный корпус. Иначе получим то, что описано в [153](internal/research/netresearch-agent-harness-skill/skills/agent-harness/references/enforcement-mechanisms.md#L153): ложный отказ тихо отключает настоящую проверку.

**7. Ограничение — рядом с правилом.** [checkpoints.yaml:109-113](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L109-L113), `KNOWN LIMIT:`. Нам есть что туда записать сразу: сверка по списку путей не поймает случай, когда путь правильный, а содержимое затёрто.

**8. Дрейф-проверка по последнему коммиту.** [verify-harness.sh:524-563](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L524-L563): в последнем коммите менялись build/CI-файлы, а `AGENTS.md` — нет, значит предупреждение. Перенос: менялись файлы в `internal/draft/`, а карта `internal/draft/00_narrative_map.md` — нет, значит предупреждение о дрейфе.

**9. Индекс вместо энциклопедии, с числом.** `AGENTS.md` < 150 строк, проверяется `wc -l` ([169-181](internal/research/netresearch-agent-harness-skill/skills/agent-harness/scripts/verify-harness.sh#L169-L181)). Наш `AGENTS.md` в эту рамку не влезает, но сам приём — «у правила есть бюджет объёма, и он проверяется» — переносим на любой наш файл правил.

---

## 7. Что у нас уже лучше

- **Разбор инцидента с датой и последствием.** [METHODOLOGY.md](METHODOLOGY.md), раздел 13.1 называет дату, участников, что именно затёрто и почему нашлось только при сверке. У AH инцидент сведён к номеру issue ([checkpoints.yaml:226](internal/research/netresearch-agent-harness-skill/skills/agent-harness/checkpoints.yaml#L226)), у HE инцидентов нет вовсе.
- **Правило записи файлов** — у нас есть, пять пунктов, расписывать не буду (METHODOLOGY.md, раздел 13.1).
- **Проверка количества файлов** — у нас есть, как ручная сверка ведущим (AGENTS.md, раздел 13); у AH эквивалента нет, у HE он только в офлайн-евале.
- **Приёмка по артефактам на диске** — у нас названа прямо (AGENTS.md, раздел 13). У HE ближайшее — один пункт сенсора «verify paths are valid, no destructive overwrites» ([HE/docs/phase2-architecture.md:77](internal/research/sujalmanpara-harness-engine/docs/phase2-architecture.md#L77)) без контракта имён; у AH такого нет.
- **Разделение ролей «пишущий / ведущий»** есть у нас; в обоих репозиториях проверяет тот же, кто делает, либо CI после факта.
- **Запрет записи в `templates/`** у нас жёсткий ([AGENTS.md](AGENTS.md) §10); у AH аналог — «never overwrite existing files without confirmation» ([SKILL.md:54](internal/research/netresearch-agent-harness-skill/skills/agent-harness/SKILL.md#L54)), то есть проза, которую их же документ объявляет неработающей.
- **Чего у нас нет:** машинной формы правила. Всё перечисленное выше — текст и дисциплина, ни один пункт не проверяется скриптом с кодом возврата. Это и есть разрыв, который закрывают пункты 2 и 3 из §6.
