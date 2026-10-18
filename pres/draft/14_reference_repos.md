# Репозитории-образцы: что склонировано и зачем

Дата клонирования: **18.10.2026**. Клоны лежат в `pres/research/` и **не попадают в публичную историю** (папка в `.gitignore`). Здесь сохраняются адреса и точные коммиты, чтобы разбор был воспроизводим.

Клонирование поверхностное (`--depth 1`), потому что нужен только текущий срез, а не история.

## Список

| Репозиторий | Коммит | Дата коммита | Размер | Зачем разбираем |
|---|---|---|---|---|
| [getagentseal/founder-playbook](https://github.com/getagentseal/founder-playbook) | `e811e63` | 2026-10-06 | 10 МБ | 15 книг в навыках: как описываются конфликты между книгами и раздел «книга устарела» |
| [sreshtalluri/mom-test](https://github.com/sreshtalluri/mom-test) | `40d9ee4` | 2026-10-17 | 0,9 МБ | накопительная база доказательств из интервью и гейт против новых функций |
| [AIDevGTM/gtm-cofounder](https://github.com/AIDevGTM/gtm-cofounder) | `8488d7c` | 2026-10-16 | 0,3 МБ | референс формы; лежит ещё и сабмодулем |
| [eltntawy/idea-discovery-playbook](https://github.com/eltntawy/idea-discovery-playbook) | `ccf08f3` | 2026-05-25 | 0,1 МБ | валидация идеи до написания кода |
| [ANVEAI/idea-hunt-skill](https://github.com/ANVEAI/idea-hunt-skill) | `257a580` | 2026-07-14 | 0,1 МБ | доказательство готовности платить до сборки |
| [nateherkai/AIS-OS](https://github.com/nateherkai/AIS-OS) | `ce9cb93` | 2026-09-06 | 66 МБ | опрос владельца и личная среда: как ведётся первое интервью |
| [Product-nomad/idea-incubator](https://github.com/Product-nomad/idea-incubator) | `521e00d` | 2026-04-28 | 0,1 МБ | жизненный цикл статусов идеи |
| [sujalmanpara/harness-engine](https://github.com/sujalmanpara/harness-engine) | `115d41c` | 2026-05-27 | 2,3 МБ | инженерия харнесса: как сбой превращается в жёсткое правило |
| [netresearch/agent-harness-skill](https://github.com/netresearch/agent-harness-skill) | `6550d49` | 2026-10-13 | 0,4 МБ | скрипты проверки и храповик правил |
| [ata-akhunzhanov/hypolab](https://github.com/ata-akhunzhanov/hypolab) | `35ef9f8` | 2026-04-12 | 1,0 МБ | цикл от гипотезы до ресёрча внутри терминала |

## Как обновить клоны

```
cd pres/research
git -C getagentseal-founder-playbook pull
```

Или заново, если папку удалили:

```
git -c http.sslBackend=openssl clone --depth 1 https://github.com/<владелец>/<репозиторий>.git <папка>
```

Флаг `http.sslBackend=openssl` нужен из-за сломанного schannel в этой среде.

## Что с ними делаем

1. Разбор практик идёт в `pres/draft/research-notes/`: по каждому репозиторию отдельный файл с цитатами и номерами строк.
2. В наш набор переносится только то, что подтверждено файлом, и с указанием источника.
3. Чужой код в публичную часть репозитория не попадает: мы берём приёмы, а не файлы.

## Границы

- Уровень всего, что приходит из этих репозиториев: `[внешнее]`. Это не валидация наших гипотез.
- Лицензии у репозиториев разные; при переносе формулировок нужно проверять условия и указывать источник.
