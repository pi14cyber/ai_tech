# Ответы по источнику gtm-cofounder

Источник: `D:\github\ai_tech\gtm-cofounder`, прочитан целиком 18.10.2026. Сводка: `pres/draft/extracts/gtm.md`. Уровень доказательности `[внешнее]`: это сторонний открытый набор (автор Shane O'Connor, QC Growth), он не речь спикера и не валидация его гипотез. Ссылки: путь к файлу плюс номера строк; в цитатах снята markdown-разметка, слова не менялись.

---

## F1. Что из набора можно показать публично и как он устроен

**Ответ.** Показать можно весь набор: лицензия MIT разрешает использовать, форкать и распространять, а каждый навык самодостаточен, это одна папка с одним `SKILL.md` без зависимостей. Устроен набор как пронумерованный маршрут из 20 навыков (00-start-here, 01-strategy-and-roadmap, 19-research-the-market и далее), внутри которого `review-the-work` это не шаг, а гейт вокруг любого результата. Публичная подача уже описана в источнике: установка по ссылке на репозиторий, запуск `00-start-here`, шаблоны `founder-brief.template.md` и `gtm-roadmap.template.md`. При показе обязательна атрибуция: набор прямо просит отдавать credit Frankl и Czakon там, где используется их фреймворк, и не выдавать чужую работу за свою.

**Опора.**
- «MIT, free to use, fork, and distribute.» (`gtm-cofounder/README.md`, строка 179).
- «Each skill is self-contained: one folder, one `SKILL.md`, zero dependencies.» (`gtm-cofounder/README.md`, строка 76).
- «Note that `review-the-work` is not a step in this line at all: it is a gate you run around any deliverable» (`gtm-cofounder/AGENTS.md`, строка 37).
- «Install the skills from https://github.com/AIDevGTM/gtm-cofounder and run 00-start-here with me.» (`gtm-cofounder/README.md`, строка 36).
- «Where a framework is theirs, the credit is theirs. Where it holds up in practice, that's the founders who tested it. Where it misses, that's on me.» (`gtm-cofounder/README.md`, строка 158).
- «Works with Claude Code, Cursor, Codex, Windsurf, Antigravity and any agent that supports the Agent Skills spec.» (`gtm-cofounder/README.md`, строка 23).

---

## H1. Что предложить аудитории

**Ответ.** Источник даёт готовый оффер: поставить набор из открытого репозитория и пройти `00-start-here`, ответив на пять вопросов, после чего зритель получает свой бриф, исследование рынка и дорожную карту с одним следующим ходом. Материальная часть оффера бесплатна и раздаваема: два шаблона плюс текст навыков, лицензия MIT это позволяет. Ограничение, которое нельзя замалчивать в эфире: набор сам объявляет, что закрывает только познаваемые решения, а за нерешаемым отправляет к человеку, то есть он не продаёт и не даёт валидацию. Механики донатов, подписки или платного доступа в источнике нет вообще, её придётся строить отдельно.

**Опора.**
- «Answer a set of questions once (about 15 minutes). Your agent researches your actual market ... builds you a prioritized GTM roadmap, then works it with you one move at a time» (`gtm-cofounder/README.md`, строка 19).
- «`00-start-here` asks you five questions, one at a time, and writes your **founder brief**: the file every other skill reads first, so the advice is about your product, not a textbook's.» (`gtm-cofounder/README.md`, строка 40).
- «Skills are great at the *knowable* calls. But some days you don't need another framework, you need a person who's been in the trenches» (`gtm-cofounder/README.md`, строка 164).
- «**Know the limit.** These skills cover the *knowable* calls. For a specific wedge or launch that needs a human call, say so, and point to a human» (`gtm-cofounder/AGENTS.md`, строка 39).
- Единственный призыв к действию, который есть в наборе, это консультация: «Free skills for everyone; a human in your corner when the road gets steep.» (`gtm-cofounder/README.md`, строка 171).

---

## H3. С чего человеку начать в понедельник

**Ответ.** В каждом навыке есть блок «Your next 30 minutes», и у `00-start-here` он буквально задаёт первый день: ответить только на пять ядровых вопросов, пометить каждый ответ `[validated]` или `[assumption]`, сохранить бриф в своём проекте, затем запустить исследование рынка и только потом дорожную карту. Дорожная карта обязана дать диагноз одной строкой и один ход Now, причём хотя бы один пункт должен прийти из исследования, а не из собственных ответов основателя. Если бриф почти целиком из допущений и разговоров с людьми не было, честный результат понедельника это не план, а совет пойти поговорить с десятью людьми и вернуться.

**Опора.**
- «Answer just the **core five**. Rough and honest beats polished and fake.» (`gtm-cofounder/skills/00-start-here/SKILL.md`, строка 93).
- «Tag each answer `[validated]` or `[assumption]`.» / «Run `research-the-market` so the agent finds what you didn't tell it» / «Run `01-strategy-and-roadmap` to get your diagnosis and first move. Don't answer the optional questions yet.» (`gtm-cofounder/skills/00-start-here/SKILL.md`, строки 94, 96, 97).
- «**The plan must add something they didn't bring.** A roadmap that only rearranges the founder's own answers has failed, however well organized.» (`gtm-cofounder/skills/01-strategy-and-roadmap/SKILL.md`, строка 23).
- «**Be willing to tell them to do almost nothing.** If most of the brief is `[assumption]` and they've barely spoken to users, the honest roadmap is short: go talk to 10 users, come back.» (`gtm-cofounder/skills/01-strategy-and-roadmap/SKILL.md`, строка 26).
- «**Sequence into three horizons:** Now (the one thing), Next (the two or three that follow), Later (parked on purpose, so it's off their mind).» (`gtm-cofounder/skills/01-strategy-and-roadmap/SKILL.md`, строка 27).

---

## B4. Как набор предлагает выбирать сегмент и нишу

**Ответ.** Набор не выбирает нишу по отсутствию данных, он сужает ICP до состояния, когда кто-то явно не подходит, и заполняет пять атрибутов, включая ответ на вопрос, кто скажет нет. Дальше сегмент раскладывается по ролям в продаже (Alpha Dev, Empowered CTO, VP Engineering, SRE) и по Job To Be Done вместо должности, а дерево решений отделяет одиночную покупку от сложной сделки. Когда ICP размыт, исследование идёт в обратную сторону: ищется сегмент, который громче всех жалуется публично, и находка передаётся в `who-is-this-for`. Места обитания при этом ранжируются по соответствию, а не по размеру. Это принципиально другой критерий, чем у спикера: сегмент доказывается публичной болью и наличием покупателя, а не непроверяемостью результата.

**Опора.**
- «"Developers" is not a market. It's a medium. If your ICP doesn't exclude anyone, it isn't one.» (`gtm-cofounder/skills/02-who-is-this-for/SKILL.md`, строка 8).
- «A usable ICP is specific enough that some people are obviously **out**. "Every developer" gives you nothing to say, because a message that speaks to everyone speaks to no one.» (там же, строка 14).
- «Market to the adopter; sell to the buyer. Confuse the two and you get great meetings and no decisions.» (там же, строка 16).
- «Fill every line with something a stranger couldn't guess: ... 5. **Who says no**: the segment you are deliberately *not* for» (там же, строки 52-57).
- «A job title is not actionable; a **job** is.» (там же, строка 33).
- «If the ICP is vague, run the research anyway, but aim it at *which segment shows the most pain in public*, and hand that finding to `who-is-this-for`.» (`gtm-cofounder/skills/19-research-the-market/SKILL.md`, строка 28).
- «**Rank by fit, not size.** A 4,000-member Discord where your ICP talks about the problem weekly beats a 2 million member subreddit where they never do.» (там же, строка 31).
- Обратный случай уже назван ошибкой: «**TAM theater**: "there are 30M developers." True and useless. Nobody sells to 30M anyone.» (`gtm-cofounder/skills/02-who-is-this-for/SKILL.md`, строка 61).

---

## E4. Какой входной пайплайн требует набор: вопросы, бриф, дорожная карта

**Ответ.** Пайплайн жёсткий по порядку: сначала пять ядровых вопросов по одному (и быстрый скан репозитория, если агент работает внутри проекта), затем файл `docs/gtm-cofounder/founder-brief.md`, затем `docs/gtm-cofounder/market-research.md` со ссылкой на каждую находку, затем `docs/gtm-cofounder/gtm-roadmap.md`. Глубокие вопросы не вываливаются сразу, каждый навык запрашивает две-три штуки в момент нужды и объясняет, что ответ открывает. Состояние помечается `[validated]`, `[assumption]` или `[researched]`, и агент не имеет права сам переводить допущение в проверенное. Перед показом любого результата обязателен гейт `review-the-work`, после хода обновляется дорожная карта, иначе план повторится.

**Опора.**
- «**Ask the five core questions one at a time, and nothing else.** One question, wait for the answer, let it shape the next. ... Never paste multiple questions at once.» (`gtm-cofounder/skills/00-start-here/SKILL.md`, строка 20).
- «**Pull the deeper questions just-in-time.** When a later skill needs more (positioning needs the villain, pricing needs the buyer), ask only the two or three relevant ones right then, and say what answering unlocks. Never front-load them.» (там же, строка 22).
- «Save the answers to `docs/gtm-cofounder/founder-brief.md` in the founder's project ... using the template in this repo (`founder-brief.template.md`).» (там же, строка 83).
- «**Every finding has a link and a date.** No link, it doesn't go in.» (`gtm-cofounder/skills/19-research-the-market/SKILL.md`, строка 29).
- «**Diagnosis:** the one bottleneck, in a sentence. ... **What the research added:** the two or three things from `market-research.md` that shaped this plan ... **Now:** the single next move ... **Next:** two or three moves queued behind it. ... **Later:** parked on purpose ... **Log:** what got done and what was learned» (`gtm-cofounder/skills/01-strategy-and-roadmap/SKILL.md`, строки 51-56).
- «If the brief does not exist, run `start-here` and nothing else. If the research does not exist, run `research-the-market` next. If the roadmap does not exist, run `strategy-and-roadmap` after that.» (`gtm-cofounder/AGENTS.md`, строка 13).
- «never flip `[assumption]` to `[validated]` yourself. Only a real user who is not a friend of theirs earns that flag.» (там же, строка 17).
- «Before you present any substantive deliverable ... run `review-the-work` on it.» (там же, строка 19).

---

## G3. Годится ли набор как образец структуры для собственного репозитория

**Ответ.** Да, структурно набор переносим: одна папка на навык, один `SKILL.md` с frontmatter из `name` и `description`, нулевые зависимости, плюс манифест плагина для установки. Стандарт разделов задан в CONTRIBUTING: когда применять, фреймворк, дерево решений, ошибки, пример, чек-лист на 30 минут, причём ценность требует реальных порогов, а не принципов. Для публичного репозитория есть готовые элементы: лицензия MIT, README с несколькими способами установки, `METRICS.md` и workflow еженедельного снапшота метрик, `AGENTS.md` с воротами для агента. Ограничения: обвязка метрик завязана на GitHub traffic API и skills.sh, а содержательная часть требует порогов, цифр и именованных примеров, это дорогая часть, и структура её не заменяет.

**Опора.**
- «New skill → `skills/<kebab-name>/SKILL.md` with the standard frontmatter (`name`, `description`) and the standard sections (when to use · framework · decision tree · mistakes · example · 30-minute checklist).» (`gtm-cofounder/CONTRIBUTING.md`, строка 16).
- «**Real thresholds, not principles.** "Charge more" is a principle. "If your top-decile users would pay 3× and churn <5%, you're underpriced" is a threshold.» (`gtm-cofounder/CONTRIBUTING.md`, строка 7).
- «**The mistake included.** The most useful frameworks name the thing that *looks* reasonable but quietly fails.» (там же, строка 8).
- «Each skill is self-contained: one folder, one `SKILL.md`, zero dependencies.» (`gtm-cofounder/README.md`, строка 76).
- «Every `SKILL.md` gives you **frameworks with actual thresholds** (not principles), **decision trees** ... and a **checklist you can run in the next 30 minutes**.» (`gtm-cofounder/README.md`, строка 142).
- «**Report skills.sh installs as the headline install number** (it is all-time and CLI-specific).» (`gtm-cofounder/METRICS.md`, строка 5) и «`traffic-daily.csv` is a permanent, de-duplicated **daily** record of GitHub clones and views ... appended weekly by `.github/workflows/traffic-snapshot.yml`.» (`gtm-cofounder/traffic/README.md`, строки 3-4).
- «`clones` ≈ installs (the skills CLI, the Claude Code plugin, and manual `git clone` all clone the repo)» (`gtm-cofounder/traffic/README.md`, строка 11).
- Манифесты для установки: `gtm-cofounder/.claude-plugin/plugin.json` (version 1.4.0, license MIT, keywords) и `gtm-cofounder/.claude-plugin/marketplace.json`.
- Планка содержания: «If a developer would roll their eyes, rewrite it.» (`gtm-cofounder/CONTRIBUTING.md`, строка 10).

---

## Что эти ответы не покрывают

- Ни один из шести ответов не даёт `[рынок]`: набор не проверяет гипотезы спикера, он даёт форму процесса.
- Тезис об уходе от конкуренции источник не поддерживает, он про дифференциацию внутри конкуренции (см. раздел о пробелах в `pres/draft/extracts/gtm.md`).
- Вопрос про монетизацию (донаты, подписка, платный доступ) остаётся открытым: в источнике такой механики нет.
