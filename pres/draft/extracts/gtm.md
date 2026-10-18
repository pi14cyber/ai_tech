# Источник gtm-cofounder: сводка для стрима

## Что это за источник и как он прочитан

Папка `D:\github\ai_tech\gtm-cofounder` прочитана целиком 18.10.2026: 20 файлов `skills/*/SKILL.md` (от `00-start-here` до `19-research-the-market`), `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `METRICS.md`, два шаблона (`founder-brief.template.md`, `gtm-roadmap.template.md`), обвязка (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.github/workflows/traffic-snapshot.yml`, `.github/scripts/*.py`, `metrics/*`, `traffic/*`, `LICENSE`, `.gitignore`). Заметок по этому источнику в репозитории не было, сводка собрана с нуля.

Пометка по правилам репозитория: это `[внешнее]`. Набор лежит внутри репозитория, но он не речь спикера и не его практика, а сторонний открытый продукт Shane O'Connor и QC Growth (README, строки 146-158, 183). Он годится для планирования, но не является валидацией тезисов спикера.

Условные обозначения ссылок: у книг репозитория ссылка это диапазон строк. Здесь вместо диапазонов строк основная ссылка это путь к файлу навыка (как требует задание). Номера строк даны дополнительно в скобках, чтобы цитату можно было проверить точно. Внутри цитат снята markdown-разметка (`**`, курсив), слова не менялись.

Исходный набор это `[внешнее]`, он сам нигде не называет себя валидацией: он прямо разделяет доказательства на три уровня (`[assumption]`, `[researched]`, `[validated]`) и запрещает повышать уровень своими руками.

---

## Ключевые тезисы

1. Набор адресован тому, кто тянет go-to-market в одиночку, а не компании с отделом маркетинга. Цитата: «If you're a technical founder pouring your own money, your nights, and your weekends into a developer tool or an AI product you believe in, with no funding, no team, no commercial co-founder, and some days it is just plain hard, then this is for you.» (`gtm-cofounder/README.md`, строки 9-11).

2. Это не курс и не набор тактик, а вторая половина работы: кому продавать, почему заплатят, как получить первых. Цитата: «Not marketing tactics or SEO skills. This is the strategy half of go-to-market: who it's for, why they'd pay, and how to land your first users.» (`gtm-cofounder/README.md`, строка 21).

3. Входной контур заявлен как разовый и короткий: несколько вопросов один раз, дальше исследование рынка и дорожная карта. Цитата: «Answer a set of questions once (about 15 minutes). Your agent researches your actual market (where your users already are, how products like yours launched), builds you a prioritized GTM roadmap, then works it with you one move at a time: positioning, first users, launch, pricing, in the order that matters for your stage.» (`gtm-cofounder/README.md`, строка 19).

4. Ценность набора в отказе от списка идей: он называет одно следующее действие и одно доказательство, которое нужно добыть. Цитата: «Your next step is not "post more," it is the one piece of evidence you need to go and get. The value is not more ideas. It is knowing what to do next, grounded in your real market rather than a textbook.» (`gtm-cofounder/README.md`, строка 54).

5. Процесс держится на пяти жёстких воротах, а не на советах. Цитата: «The rules further down are craft. These five are **gates**. A skill's advice is only as good as the process around it, so treat these as hard preconditions, not suggestions, and run them in order every session.» (`gtm-cofounder/AGENTS.md`, строка 11). Сами ворота: состояние прежде совета, диагноз прежде тактики, доказательство прежде веры, судья не автор, обновление состояния после (`gtm-cofounder/AGENTS.md`, строки 13-21).

6. Валидацию даёт только живой человек, который не друг; публичная находка годится для плана, но не для статуса «проверено». Цитата: «Only a real user who is not a friend of theirs earns that flag. ... Public evidence you found yourself (a thread, an issue, a launch result, with a link) is tagged `[researched]`: strong enough to plan channels and launches around, never strong enough to count as validated. And never invent it: no link, no finding.» (`gtm-cofounder/AGENTS.md`, строка 17). То же по-другому: «Research is planning-grade evidence, not proof.» (`gtm-cofounder/skills/19-research-the-market/SKILL.md`, строка 16).

7. Допущение нельзя переводить в проверенное ни усилием, ни агентом: «Do not build load-bearing work (positioning, pricing, an ICP) on an assumption without flagging it, and never flip `[assumption]` to `[validated]` yourself.» (`gtm-cofounder/AGENTS.md`, строка 17). И честный ответ про ноль интервью считается ценным: «"Zero users interviewed" is a valid and revealing answer. Note it plainly, no judgment, and flag `talk-to-users` as the highest-priority next step.» (`gtm-cofounder/skills/00-start-here/SKILL.md`, строка 24).

8. Работа с людьми это отдельный навык и отдельный инструмент: технический совет директоров из 30-50 живых людей. Цитата: «Stand up a **Technical Advisory Board**: 30-50 people who *represent your users and buyers*, not grey-haired advisors telling you how to build. You interview them, on repeat, and let their words become your positioning, roadmap, and homepage copy.» (`gtm-cofounder/skills/03-talk-to-users/SKILL.md`, строки 14-15). Разговор это интервью, а не демо: «A TAB call is **not a demo and not a sales call.** It's an interview. You never mention the product.» (там же, строка 16).

9. Оплата внимания считается в цифрах: массовая рассылка не работает, конверсия около 10 процентов. Цитата: «~10% reply → plan ~500 outreaches for ~50 members» (`gtm-cofounder/skills/03-talk-to-users/SKILL.md`, строка 35).

10. Сегмент выбирается через исключение, а не через размер рынка. Цитата: «"Developers" is not a market. It's a medium. If your ICP doesn't exclude anyone, it isn't one.» (`gtm-cofounder/skills/02-who-is-this-for/SKILL.md`, строка 8). И далее: «A usable ICP is specific enough that some people are obviously **out**.» (там же, строка 14).

11. В сделке всегда больше одного человека, и тот, кто внедряет, редко платит. Цитата: «Market to the adopter; sell to the buyer. Confuse the two and you get great meetings and no decisions.» (`gtm-cofounder/skills/02-who-is-this-for/SKILL.md`, строка 16).

12. Выбор ниши у набора идёт от публичной боли и от ролей в продаже, а не от внутренней готовности основателя. Цитата: «If the ICP is vague, run the research anyway, but aim it at *which segment shows the most pain in public*, and hand that finding to `who-is-this-for`.» (`gtm-cofounder/skills/19-research-the-market/SKILL.md`, строка 28). Роли заданы таблицей: Alpha Dev, Empowered CTO, VP Engineering, SRE / Platform Eng (`gtm-cofounder/skills/02-who-is-this-for/SKILL.md`, строки 22-27), причём «The Alpha Dev is **not your long-term customer**. They chase the next shiny thing. You need them anyway: they carry new tech to the people who pay.» (там же, строка 29).

13. Отличие строится по лестнице до уровня проблемы, а не по списку функций. Цитата: «Compete as high up this ladder as you can. Feature wars are a race to the bottom.» (`gtm-cofounder/skills/04-positioning-and-story/SKILL.md`, строка 41). Верхний уровень: «**Reaching Level 4 / category creation:** talk to enough TAB members (see `talk-to-users`) to surface a problem competitors haven't named, then name it so precisely your product is the obvious answer.» (`gtm-cofounder/skills/04-positioning-and-story/SKILL.md`, строка 50).

14. Утверждения проверяются числами и именами, потому что разработчик всё равно проверит. Цитата: «"Saves time" is banned. "8x faster builds, 2 hrs to 15 min, attributed to a named user" is the standard.» (`gtm-cofounder/AGENTS.md`, строка 29). И: «Developers have a finely tuned BS detector and they *will* verify you. Specificity is credibility.» (`gtm-cofounder/skills/06-value-prop-that-converts/SKILL.md`, строка 14).

15. Для инструмента первого запуска есть два порога: выходные своими силами и ценность за минуты. Цитата: «**The weekend test (Frankl).** A motivated developer should get your product doing something real over a weekend, without a call, a demo, or an email to you. If they cannot, that is your single highest-leverage work, above any channel, launch, or homepage tweak.» (`gtm-cofounder/skills/08-time-to-first-value/SKILL.md`, строка 23). Числовой ориентир: «Time-to-value target: **< 1 hour ideal, 1 day max.**» (`gtm-cofounder/skills/15-know-if-its-working/SKILL.md`, строка 36).

16. Привлечение без удержания это ускоренная потеря людей. Цитата: «For a dev tool, the product is the pitch. A developer tries it alone and decides in minutes. Acquisition without activation is just a faster way to lose people.» (`gtm-cofounder/skills/08-time-to-first-value/SKILL.md`, строка 8). Главная ранняя метрика: «The only early metric that matters is **net developer retention**. Without it, you're not running a funnel; you're running a colander.» (`gtm-cofounder/skills/15-know-if-its-working/SKILL.md`, строка 8).

17. Первых пользователей берут руками и по названным местам, а не объёмом публикаций. Цитата: «You don't get your first 50 users by posting more. You get them by going where your users *already* discover tools, and, at the start, by doing things that don't scale.» (`gtm-cofounder/skills/09-first-50-users/SKILL.md`, строка 8).

18. Публичный запуск это честность и польза, а не полировка. Цитата: «The bar is **usefulness + honesty**, not polish. Developers will test your claims and read your code. Show up as a real engineer sharing real work, be present to answer everything, and never, ever fake it. One genuine launch beats ten hype posts.» (`gtm-cofounder/skills/10-launch-it/SKILL.md`, строка 14).

19. Цена это решение о позиционировании, и она выводится из ценности, а не из затрат или страха. Цитата: «Price is not a number you pick at the end. It is a positioning decision: it tells the market who you are, what you replace, and how much you believe you are worth. Get it from evidence, not fear.» (`gtm-cofounder/skills/12-pricing/SKILL.md`, строка 8). И: «price against the value the customer gets, never against your cost or your fear. Your AWS bill is not a pricing strategy.» (там же, строка 20).

20. Первые сделки основатель закрывает сам, пока движение не повторяется. Цитата: «Nobody can sell it before you can. The first ten deals are not a hire, they are how you learn what you are actually selling and to whom. Do them yourself, badly at first, until the motion repeats.» (`gtm-cofounder/skills/13-founder-led-sales/SKILL.md`, строка 8). Порог: «**Do it yourself through roughly your first 10 to 20 paying customers**, or until you can write down what works and repeat it.» (там же, строка 48).

21. Автор работы не судья своей работы: перед показом результата агент обязан стать скептиком. Цитата: «The person who wrote it is the worst judge of whether it is good. Before this reaches the founder, stop being the author and become the skeptic.» (`gtm-cofounder/skills/17-review-the-work/SKILL.md`, строка 8). Механика: «**the author may submit the work, the author may not issue the verdict.**» (там же, строка 16).

22. Публичный сбор фактов сам по себе не доказывает спрос: «Fifty people complaining in public tells you where to go and what to say. It doesn't tell you they'll switch, or pay. That still takes `talk-to-users`.» (`gtm-cofounder/skills/19-research-the-market/SKILL.md`, строка 118).

23. У набора есть явная граница компетенции: он закрывает «познаваемые» решения и отправляет к человеку за остальным. Цитата: «These skills cover the *knowable* calls. For a specific wedge or launch that needs a human call, say so, and point to a human» (`gtm-cofounder/AGENTS.md`, строка 39). В README это же разделение: «Skills are great at the *knowable* calls. But some days you don't need another framework, you need a person who's been in the trenches» (`gtm-cofounder/README.md`, строка 164).

---

## Методы и этапы

**Пайплайн входа (обязательный порядок).** Протокол задан жёстко: сначала состояние, потом совет. Цитата: «Before you give any GTM advice or apply any skill, read `docs/gtm-cofounder/founder-brief.md`, `docs/gtm-cofounder/market-research.md`, and `docs/gtm-cofounder/gtm-roadmap.md`. If the brief does not exist, run `start-here` and nothing else.» (`gtm-cofounder/AGENTS.md`, строка 13). Никаких диагнозов с чистого листа: «Never diagnose, position, or prescribe from a blank slate. Without the brief you are guessing, and generic guessing is the exact thing this pack exists to replace.» (там же).

**Шаг 1. Интервью и бриф.** Пять вопросов, по одному, затем файл `docs/gtm-cofounder/founder-brief.md`. Цитата: «Answer **five core questions** and the agent writes a **`docs/gtm-cofounder/founder-brief.md`** in your project, enough to give you a real diagnosis and a roadmap in minutes.» (`gtm-cofounder/skills/00-start-here/SKILL.md`, строка 14). Формат разговора: «**Ask the five core questions one at a time, and nothing else.** ... Never paste multiple questions at once.» (там же, строка 20). Глубокие вопросы не вываливают сразу: «**Pull the deeper questions just-in-time.** When a later skill needs more (positioning needs the villain, pricing needs the buyer), ask only the two or three relevant ones right then, and say what answering unlocks. Never front-load them.» (там же, строка 22). Сами пять вопросов: что делает, для кого, что используют сейчас, стадия и возвращаются ли, главный актив (`gtm-cofounder/skills/00-start-here/SKILL.md`, строки 49-53; дублируются в `gtm-cofounder/founder-brief.template.md`, строки 17-30).

**Разметка состояния.** Каждый ответ помечается `[validated]` или `[assumption]`, публичные находки `[researched]`: «For every substantive answer, ask: "have you heard a real user say this, or is that your read for now?" Tag it `[validated]` or `[assumption]`.» (`gtm-cofounder/skills/00-start-here/SKILL.md`, строка 23). Бриф живёт и обновляется: «Every time the founder learns something real from a user ..., update the relevant line and flip its tag from `[assumption]` to `[validated]`. A brief that is mostly `[validated]` is a company that knows itself.» (там же, строка 89).

**Скан репозитория до вопросов.** Если агент внутри проекта, он сначала читает README, манифест, последние коммиты, темы открытых issues. Цитата: «The **last ~15 commit subjects** and recent **PR titles**: what they are actually building right now.» (`gtm-cofounder/skills/00-start-here/SKILL.md`, строка 34). Границы честности: «The repo tells you what was built, not who pays. It grounds the product and roughly the user. It says nothing about the buyer, willingness to pay, or the market» (там же, строка 41).

**Шаг 2. Исследование рынка.** Пять находок: места обитания ICP, как запускались похожие продукты, боль словами чужих людей, неучтённые конкуренты, окна возможностей (`gtm-cofounder/skills/19-research-the-market/SKILL.md`, строки 38-67). Требование к ссылкам: «**Every finding has a link and a date.** No link, it doesn't go in.» (там же, строка 29). Именование: «**Name venues, never categories.** "Reddit" is not a finding.» (там же, строка 30). Ранжирование: «**Rank by fit, not size.**» (там же, строка 31). Ограничение объёма: «This is a sprint, not a thesis: roughly 20 to 40 searches, an hour of agent time at most.» (там же, строка 33).

**Шаг 3. Диагноз и дорожная карта.** Три действия: диагностировать один узкое место, приоритезировать по стадии, сохранить план. Цитата: «**Diagnose.** Read the brief and the research honestly. ... Name one bottleneck, not five.» (`gtm-cofounder/skills/01-strategy-and-roadmap/SKILL.md`, строка 16). Требование к содержанию: «**The plan must add something they didn't bring.** A roadmap that only rearranges the founder's own answers has failed, however well organized.» (там же, строка 23). Жёсткая структура файла: «If `docs/gtm-cofounder/gtm-roadmap.md` does not open with a one-line **Diagnosis**, then **What the research added**, then **Now / Next / Later**, it is wrong.» (там же, строка 29). Шаблон: `gtm-cofounder/gtm-roadmap.template.md` (диагноз, что добавило исследование, Now, Next, Later, лог; строки 8-40). Готовность сказать почти ничего не делать: «**Be willing to tell them to do almost nothing.** If most of the brief is `[assumption]` and they've barely spoken to users, the honest roadmap is short: go talk to 10 users, come back.» (там же, строка 26).

**Выбор стартового хода по стадии.** Таблица стадий (где они, узкое место, с чего начать) (`gtm-cofounder/skills/01-strategy-and-roadmap/SKILL.md`, строки 35-43). Значение по умолчанию: «When in doubt, the default first move for an early founder is almost always `talk-to-users`. Real evidence beats a clever plan.» (там же, строка 45).

**Ворота качества перед показом.** `review-the-work` это не шаг, а гейт вокруг любого результата: «It is a gate, not a stage. It has no place in the linear sequence. Run it around any piece of work, every time.» (`gtm-cofounder/skills/17-review-the-work/SKILL.md`, строка 10). Вердикт обязан быть конкретным: «Give a clear verdict: **PASS**, or **REVISE** with the exact checks that failed and the specific fix for each. Never a vague "looks good."» (там же, строка 21). Запрет на самопохвалу: «**Do not rubber-stamp.** If you cannot find a single weakness, you are not reading as the skeptic.» (там же, строка 22).

**Обновление состояния после хода.** Цитата: «When a move is done, update `docs/gtm-cofounder/gtm-roadmap.md`: log what happened and what was learned, promote the next move, reprioritize if reality changed. The roadmap is the source of truth across sessions, not the chat.» (`gtm-cofounder/AGENTS.md`, строка 21).

**Порядок применения всех навыков.** Приблизительный маршрут: `start-here` → `research-the-market` → `strategy-and-roadmap` → `who-is-this-for` → `talk-to-users` → `positioning-and-story` → `beyond-the-wrapper` (только для AI-продуктов) → `value-prop-that-converts` → `the-homepage` → `time-to-first-value` → `first-50-users` / `launch-it` → `growth-loops` → `market-to-devs-sell-to-buyers` → `pricing` → `founder-led-sales` → `founder-led-content` → `know-if-its-working`, с `market-scan` как периодическим обновлением (`gtm-cofounder/AGENTS.md`, строка 37). Порядок вторичен по отношению к дорожной карте: «Let `docs/gtm-cofounder/gtm-roadmap.md` set the actual priority for their stage. Don't optimize a homepage before you know who it's for» (там же).

**Правила тона и языка.** Специфика вместо общих слов, разработчик всегда герой, пустые усилители запрещены: «**Refuse puffery.** "Powerful," "best-in-class," "seamless," "platform," "revolutionary": flag every one and replace with something provable.» (`gtm-cofounder/AGENTS.md`, строка 33). Отдельный запрет на длинное тире: «No em-dashes or en-dashes anywhere: use commas, colons, or periods. Em-dashes are the clearest AI tell» (там же, строка 41).

**Порядок работы с живыми людьми.** Семь вопросов на 30 минут, не больше: `gtm-cofounder/skills/03-talk-to-users/SKILL.md`, строки 50-58; правило «**The 7 questions (never more than 7 in 30 min)**» (строка 50); каденция «30 minutes · one-on-one · monthly · for ~6 months» (строка 26). Результат разговоров раскладывается по четырём корзинам: боли, выгоды, задачи, изменения среды, последнее даёт «злодея» для позиционирования (там же, строки 62-71).

**Лестница способов доказательства.** «your claim  <  a demo  <  a benchmark you ran  <  a named user's attributed result» (`gtm-cofounder/skills/06-value-prop-that-converts/SKILL.md`, строка 52). Демо это слабейшее доказательство: «A demo is the *weakest* proof (ideal conditions). An **attributed testimonial** (name + title + company + number) is the strongest. Anonymous quotes are assumed invented.» (там же, строка 24).

---

## Ошибки и предостережения

- **Путаница внедряющего и платящего.** «One persona, complex sale: nailing the Alpha Dev and forgetting the buyer → adoption with no revenue.» (`gtm-cofounder/skills/02-who-is-this-for/SKILL.md`, строка 64).
- **Размер рынка вместо сегмента.** «**TAM theater**: "there are 30M developers." True and useless. Nobody sells to 30M anyone.» (`gtm-cofounder/skills/02-who-is-this-for/SKILL.md`, строка 61).
- **Погоня за тем, у кого бюджет.** «**Budget-chasing**: writing everything for the CTO/VP because they pay. They don't visit your homepage; the developer does.» (там же, строка 62).
- **Интервью с друзьями и питч внутри интервью.** «**Interviewing friends**: they're nice and useless. You need people who'll say no.» и «**Pitching mid-interview**: the moment you demo, they start being polite instead of honest.» (`gtm-cofounder/skills/03-talk-to-users/SKILL.md`, строки 75-76).
- **Наводящие вопросы и вопросы о решениях.** «**Leading questions**: "wouldn't it be great if…" gets you the answer you fished for.» (`gtm-cofounder/skills/03-talk-to-users/SKILL.md`, строка 77) и «users are experts in their pain, not in your product. Mine the pain.» (там же, строка 79).
- **Массовая рассылка.** «**Batch outreach**: a templated blast to 200 people gets 200 ignores. Personalize or don't send.» (там же, строка 78).
- **Продукт в роли героя.** «**Product as hero**: "ShipFast helps you…" Make the developer the subject of the sentence.» (`gtm-cofounder/skills/04-positioning-and-story/SKILL.md`, строка 64).
- **Отсутствие злодея и слова-пустышки.** «**No villain**: all solution, no antagonist → zero urgency.» (там же, строка 65) и «**"Platform"**: developers hear *months of integration and risk.*» (там же, строка 66).
- **Позиционирование на модели для AI-продукта.** «**Leading with the model or "AI-powered."** It signals commodity and invites the wrapper objection you are trying to avoid.» (`gtm-cofounder/skills/05-beyond-the-wrapper/SKILL.md`, строка 51). И запрет на сокрытие провалов: «**Overclaiming accuracy or hiding failure modes.** Devs find the failure case, and the trust never comes back.» (там же, строка 52).
- **Стек прилагательных.** «**Adjective stacking**: "powerful, seamless, intuitive." Three words, zero information.» (`gtm-cofounder/skills/06-value-prop-that-converts/SKILL.md`, строка 58).
- **Страница для покупателя, который на неё не заходит.** «**Writing for the buyer**: ROI language up top; the developer bounces.» (`gtm-cofounder/skills/07-the-homepage/SKILL.md`, строка 52) и «**"Contact sales" pricing**: kills self-serve trust instantly.» (там же, строка 54).
- **Оптимизация притока при дырявом первом запуске.** «**Optimizing the homepage or the launch while the first run leaks.** Fix activation before acquisition. A great channel into a broken first run just burns the channel.» (`gtm-cofounder/skills/08-time-to-first-value/SKILL.md`, строка 66) и «**Celebrating signups.** Signups are vanity if they never activate.» (там же, строка 67).
- **Публиковать больше и платная реклама до product-market fit.** «**"Post more"**: volume without a channel thesis is noise.» и «**Paid ads pre-PMF**: you'll pay to accelerate a message that doesn't convert yet.» (`gtm-cofounder/skills/09-first-50-users/SKILL.md`, строки 47-48).
- **Запуск на хайпе и отсутствие автора в треде.** «**Hype title**: emojis and superlatives on HN get flagged to death.» и «**Absent founder**: posting then leaving; the unanswered thread dies.» (`gtm-cofounder/skills/10-launch-it/SKILL.md`, строки 67-68).
- **Накрутка.** «**Astroturfing**: instant, permanent reputational damage.» (`gtm-cofounder/skills/10-launch-it/SKILL.md`, строка 70) и «**Never astroturf.** No vote rings, no sock puppets. Communities detect it and the ban is permanent and public.» (там же, строка 29).
- **Ранний запуск.** «**Launching too early**: before the weekend test passes, a launch amplifies your weakest moment.» (там же, строка 71).
- **Цена от затрат и страх брать деньги.** «**Cost-plus pricing.** "It costs me $8 in compute so I will charge $12." Cost is a floor, not a strategy.» и «**Never charging.** "Developers won't pay" is almost always "I have not asked, and I am scared to."» (`gtm-cofounder/skills/12-pricing/SKILL.md`, строки 73-74).
- **Слишком щедрый бесплатный уровень.** «**A free tier that is too generous.** If a real company never needs to upgrade, you built a great free tool and no business.» (там же, строка 76).
- **Скидка из страха.** «**Fear-driven discounting.** Caving at the first "too expensive" trains every buyer to push and signals you do not believe your own value.» (там же, строка 79).
- **Найм продавца до того, как движение повторяется.** «**Hiring a salesperson too early.** You cannot delegate a motion you have not figured out.» (`gtm-cofounder/skills/13-founder-led-sales/SKILL.md`, строка 56).
- **«Я подумаю» как согласие.** «**Treating "think about it" as a yes.** It is an undiagnosed no.» (там же, строка 60) и «A vague yes-later is a no you have not diagnosed.» (там же, строка 44).
- **Путаница бесплатных пользователей с выручкой.** «**Confusing usage with revenue.** Ten thousand free users and zero conversations with a buyer is not traction, it is a popular free tier.» (там же, строка 61).
- **Метрики тщеславия.** «**Vanity metrics**: stars, pageviews, impressions. They feel like progress and predict nothing.» (`gtm-cofounder/skills/15-know-if-its-working/SKILL.md`, строка 63).
- **Петля роста на дырявом удержании.** «**Building a loop on leaky retention.** Amplifying a product people abandon just abandons faster. The gate is the gate.» (`gtm-cofounder/skills/18-growth-loops/SKILL.md`, строка 61). Модель роста обязана служить пользователю: «every loop must do the *user* a service, not just you. ... If the loop degrades the experience, it is not a loop, it is a leak in your trust.» (там же, строка 16).
- **Платные реферальные награды и навязанная виральность.** «**Paid referral incentives for developers.** "Give $20, get $20" reads as bribery to the exact audience that punishes it» (там же, строка 62) и «**Forced virality.** An unremovable badge or watermark gets stripped, resented, and posted about.» (там же, строка 63).
- **Выдача всплеска запуска за петлю.** «**Mistaking a launch spike for a loop.** A launch is one crank of the handle (`launch-it`). The test is whether the users it brought produce users.» (там же, строка 64).
- **Категории вместо названных мест.** «**Categories instead of venues.** "Developer communities and social media" is not research. If a line has no link, it's a guess.» (`gtm-cofounder/skills/19-research-the-market/SKILL.md`, строка 115).
- **Придумывание цифр.** «**Inventing to fill gaps.** A plausible member count or a remembered launch result that you didn't check is worse than "unknown". Founders act on these numbers.» (там же, строка 117).
- **Исследование вместо разговоров.** «**Researching instead of talking.** Research is an hour, not a hiding place. If it's been a week of research and zero conversations, stop and go talk to the people on your list.» (там же, строка 120).
- **Копирование чужого запуска и реакция на чужой ход.** «**Copying a competitor's launch wholesale.** Their launch fit their product, their audience, and their year. Take the pattern, not the playbook.» (`gtm-cofounder/skills/19-research-the-market/SKILL.md`, строка 119) и «**Reacting to a competitor's launch by copying it.** Their move fits their strategy, not yours.» (`gtm-cofounder/skills/16-market-scan/SKILL.md`, строка 46).
- **Скан рынка без изменения плана.** «**Scanning everything, changing nothing.** A scan that doesn't update the brief or the roadmap was just anxiety with extra steps.» (`gtm-cofounder/skills/16-market-scan/SKILL.md`, строка 47).
- **План, который только пересказывает основателя.** «A roadmap that only rearranges the founder's own answers has failed, however well organized.» (`gtm-cofounder/skills/01-strategy-and-roadmap/SKILL.md`, строка 23).
- **Совет, выданный без состояния.** «Never diagnose, position, or prescribe from a blank slate. Without the brief you are guessing, and generic guessing is the exact thing this pack exists to replace.» (`gtm-cofounder/AGENTS.md`, строка 13).
- **Ложь разработчику как запрещённый приём.** «Generic "growth hacking" tactics, engagement-bait, or anything that tricks developers. The first rule of dev GTM is: don't lie to developers. They find out.» (`gtm-cofounder/CONTRIBUTING.md`, строка 22).
- **Ложь о своей зоне охвата.** «**Know the limit.** These skills cover the *knowable* calls. For a specific wedge or launch that needs a human call, say so, and point to a human» (`gtm-cofounder/AGENTS.md`, строка 39).

---

## Цитаты для слайдов

- «the GTM co-founder you don't have (yet)» (`gtm-cofounder/README.md`, строка 15).
- «Not a course. Frameworks with real numbers and concrete next steps, not theory» (`gtm-cofounder/README.md`, строка 15).
- «Your next step is not "post more," it is the one piece of evidence you need to go and get. The value is not more ideas.» (`gtm-cofounder/README.md`, строка 54).
- «State before advice.» (`gtm-cofounder/AGENTS.md`, строка 13).
- «Evidence before belief.» (`gtm-cofounder/AGENTS.md`, строка 17).
- «The judge is not the author.» (`gtm-cofounder/AGENTS.md`, строка 19).
- «Only a real user who is not a friend of theirs earns that flag.» (`gtm-cofounder/AGENTS.md`, строка 17).
- «Research is planning-grade evidence, not proof.» (`gtm-cofounder/skills/19-research-the-market/SKILL.md`, строка 16).
- «"Developers" is not a market. It's a medium. If your ICP doesn't exclude anyone, it isn't one.» (`gtm-cofounder/skills/02-who-is-this-for/SKILL.md`, строка 8).
- «Market to the adopter; sell to the buyer.» (`gtm-cofounder/skills/02-who-is-this-for/SKILL.md`, строка 16).
- «The best marketing to developers comes from talking to developers.» (`gtm-cofounder/skills/03-talk-to-users/SKILL.md`, строка 8).
- «No villain → no urgency → no story → no conversion.» (`gtm-cofounder/skills/04-positioning-and-story/SKILL.md`, строка 21).
- «"Better" is sloppy thinking. Better how, along what dimension, by how much, proven by whom?» (`gtm-cofounder/skills/06-value-prop-that-converts/SKILL.md`, строка 8).
- «Acquisition without activation is just a faster way to lose people.» (`gtm-cofounder/skills/08-time-to-first-value/SKILL.md`, строка 8).
- «Without it, you're not running a funnel; you're running a colander.» (`gtm-cofounder/skills/15-know-if-its-working/SKILL.md`, строка 8).
- «A Show HN is not an announcement. It's "I built this thing, here's how it works and what's still rough."» (`gtm-cofounder/skills/10-launch-it/SKILL.md`, строка 8).
- «Price is not a number you pick at the end. It is a positioning decision» (`gtm-cofounder/skills/12-pricing/SKILL.md`, строка 8).
- «the author may submit the work, the author may not issue the verdict.» (`gtm-cofounder/skills/17-review-the-work/SKILL.md`, строка 16).
- «don't lie to developers. They find out.» (`gtm-cofounder/CONTRIBUTING.md`, строка 22).
- «No em-dashes or en-dashes anywhere: use commas, colons, or periods. Em-dashes are the clearest AI tell» (`gtm-cofounder/AGENTS.md`, строка 41).

---

## Чего в источнике нет

1. **Нет тезиса об уходе от конкуренции.** Наоборот, набор работает внутри конкуренции и строит дифференциацию: «Compete as high up this ladder as you can. Feature wars are a race to the bottom.» (`gtm-cofounder/skills/04-positioning-and-story/SKILL.md`, строка 41). Спикерский мотив выбора поля по непроверяемости результата здесь отсутствует полностью.

2. **Нет понятия микро-монополии и монополии как цели.** Слово monopoly в наборе не встречается ни разу. Ближайшее по смыслу это уровень 4, проблема, которую никто не назвал (`gtm-cofounder/skills/04-positioning-and-story/SKILL.md`, строка 50), но это позиция в категории, а не уход из соревнования.

3. **Нет сравнения стоимости часа человека и часа ИИ.** Набор нигде не считает экономику человек против ИИ и не описывает ИИ как конкурента. ИИ упоминается только как продукт клиента (`beyond-the-wrapper`) и как исполнитель, которого надо проверять: «An agent without web access that writes up "communities" from memory is guessing» (`gtm-cofounder/skills/19-research-the-market/SKILL.md`, строка 23).

4. **Нет ИИ как инструмента валидации.** Это не пробел, а прямая позиция: единственная валидация это разговор с живым человеком, который не друг (`gtm-cofounder/AGENTS.md`, строка 17). Тезис спикера про валидацию (`pres/draft/01_questionnaire.md`, строка 156: «ИИ не инструмент валидации вообще.») источник подтверждает косвенно, но своими словами и в другой системе координат.

5. **Нет фильтра непроверяемости как критерия выбора поля.** У набора сегмент выбирается по публичной боли и по исключению, а не по тому, есть ли по теме данные: «aim it at *which segment shows the most pain in public*» (`gtm-cofounder/skills/19-research-the-market/SKILL.md`, строка 28).

6. **Нет личного профиля основателя.** Ни резюме, ни опыта, ни сильных сторон как входного артефакта. Вход это продукт, ICP, рынок, стадия: «The brief holds their product, ICP, market, and stage» (`gtm-cofounder/AGENTS.md`, строка 7). Пайплайн профиля из `pres/draft/03_pipeline.md` в источнике не описан.

7. **Нет HADI, нет цикла гипотез и нет списка вопросов, в которых основатель не эксперт.** В пайплайне спикера такой список есть (`pres/draft/03_pipeline.md`, строка 44: «составляет список вопросов, в которых вы не эксперт»), в наборе гипотезы как отдельный артефакт не ведутся; ближайшее это `[assumption]` в брифе и маршрутизация в `talk-to-users`.

8. **Нет материала о публичном выступлении, стриме и личном бренде.** Набор про go-to-market продукта, а не про личную монетизацию. Ни донатов, ни подписок, ни QR: единственный призыв к действию в текстах это приглашение написать автору в LinkedIn и обратиться в QC Growth (`gtm-cofounder/README.md`, строки 166-171).

9. **Нет русскоязычной версии и нет адаптации под русский рынок.** Весь контент на английском и адресован англоязычной аудитории разработчиков; названы HN, Reddit, Product Hunt, Discord, VS Code marketplace (`gtm-cofounder/skills/19-research-the-market/SKILL.md`, строки 42-49).

10. **Нет доказательной базы самого набора.** Он ссылается на чужие фреймворки без первичных данных: Adam Frankl и Jakub Czakon (`gtm-cofounder/README.md`, строки 150-151), для петель роста Jonathan Reimer, Brian Balfour и Casey Winters (`gtm-cofounder/skills/18-growth-loops/SKILL.md`, строка 81). Собственная аудитория измеряется двумя числами: 2.9K установок через skills.sh за всё время и 9.9k посетителей сайта за 14 дней (`gtm-cofounder/METRICS.md`, строки 9-10). Это витрина проекта, а не проверка методики.

11. **Нет гарантий результата и нет обещания валидации.** Набор сам ограничивает себя: «These skills cover the *knowable* calls» (`gtm-cofounder/AGENTS.md`, строка 39). Для стрима это значит, что цитировать набор как подтверждение гипотез спикера нельзя.

12. **Нет встроенной механики монетизации навыков.** Лицензия разрешает всё: «MIT, free to use, fork, and distribute.» (`gtm-cofounder/README.md`, строка 179). Ни платных уровней, ни ограничений на коммерческое использование.

---

## Как этот источник соотносится с тезисами стрима

| Тезис стрима | Что даёт источник | Разрыв |
|---|---|---|
| Цель это уход от конкуренции | Дифференциация до уровня проблемы, `[внешнее]` | Источник не про уход, а про выигрыш внутри конкуренции |
| Проверка гипотез через живых людей и нетворкинг | TAB, 30-50 человек, 7 вопросов, валидирует только не-друг | Нетворкинг как способ получить доступ источником не описан, только интервью |
| ИИ ускоряет исполнение, но не валидирует | `[researched]` никогда не станет `[validated]`, ИИ сам под запретом на выдумывание | Прямой формулировки про ИИ нет, вывод переносится по аналогии |
| Конкуренция с ИИ это тоже конкуренция | Нет | Полный пробел, тезис подтверждается только рынком и другими источниками |

Статус всего файла: `[внешнее]`, дата обращения 18.10.2026, источник `https://github.com/AIDevGTM/gtm-cofounder` (из `gtm-cofounder/.claude-plugin/plugin.json`, строка 9). Ссылка на папку в репозитории: `D:\github\ai_tech\gtm-cofounder`.
