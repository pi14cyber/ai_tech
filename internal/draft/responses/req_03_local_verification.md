# Проверка ответов req_03a–req_03d: что подтверждено локально, что нет

Дата разбора: 20.10.2026. Проверял по правилу набора: **веб-поиск запрещён, локальный разбор и клонирование репозиториев разрешены.**

## 1. Состояние ответов

| Ответ | Вопросов | Отвечено | URL | Комментарий |
|---|---|---|---|---|
| `req_03a_judge_independence` | 5 | 5 | 0 | источники названы, адресов нет |
| `req_03b_provenance_versions` | 5 | 5 | 1 | один адрес на весь ответ |
| `req_03c_evidence_grading` | 5 | 5 | 0 | источники названы, адресов нет |
| `req_03d_check_design` | 5 | 5 | 0 | источники названы, адресов нет |

Разбор `internal/draft/responses/req_03_sources.md`: **64 уникальных упоминания** (arXiv, NIST, ISO/IEC, RFC, FIPS, SR) — и ни у одного нет URL. `verify_research.py` → код 1: «19 блоков без ссылки и без пометки белого пятна». По правилу «нет ссылки — нет находки» ответы **не приняты как находки**; 19 блоков уходят в очередь.

## 2. Что подтверждено локально (уровень `[база]`, файл:строка)

Клонирование новых репозиториев в этой среде недоступно (см. §3), но в `internal/research/` уже лежат 56 клонов. В них нашлись прямые подтверждения части утверждений:

### Судья не автор
- `internal/research/AIDevGTM-gtm-cofounder/AGENTS.md:19` — «**The judge is not the author.** Before you present any substantive deliverable…» — правило независимой проверки у нашего же образца.

### Происхождение, подпись, допуск
- `internal/research/AgriciDaniel-claude-obsidian/README.md:243` — «High-risk accepted claims require **two independent sources**».
- `internal/research/AgriciDaniel-claude-obsidian/AGENTS.md:70` — `wiki/meta/ledgers/`: source and claim provenance (журнал происхождения утверждений).
- `internal/research/AgriciDaniel-claude-obsidian/README.md:367` — «Approval hashes bind to the reviewing…» (привязка одобрения к просматриваемому объекту).
- `internal/research/AgriciDaniel-claude-obsidian/CHANGELOG.md:249` — «approvals, signed credential URLs, provenance violations, staged Git state».

### Аттестация и уровни происхождения (supply chain)
- `internal/research/LearningCircuit-local-deep-research/README.md:168` — Cosign + keyless OIDC + SLSA provenance.
- `internal/research/LearningCircuit-local-deep-research/SECURITY.md:345` — «SLSA Provenance | Build attestations for supply chain verification», `:361` — verify SBOM attestation.
- `internal/research/n8n-io-n8n/CHANGELOG.md:4599` — «Implements SLSA L3 provenance and VEX attestation».

### Мутационное тестирование и проверка проверок
- В локальных клонах найдены упоминания mutation testing (docs нескольких репозиториев) — точные строки требуют отдельного прохода; как готовая практика локально не подтверждено.

## 3. Почему клонирование не сработало и что это значит

Попытки склонировать `in-toto`, `slsa-framework/slsa`, `w3c/webauthn`:

- HTTPS: `fatal: unable to access … schannel: AcquireCredentialsHandle failed: SEC_E_NO_CREDENTIALS`.
- SSH: `Please make sure you have the correct access rights and the repository exists`.

То есть **в этой среде нет учётных данных для клонирования**, хотя правило владельца клонирование разрешает. Без этого 64 названных источника проверить нельзя: arXiv/ISO/NIST — не репозитории.

## 4. Решение по ответам

1. **Не принимать как находки** до появления URL/DOI у каждого источника.
2. **Локально подтверждённое** (§2) использовать как `[база]` при доработке правил: связка «судья не автор» уже есть у образца; журнал происхождения и привязка одобрения к объекту — подтверждены локальными клонами.
3. **На адреса — отдельный запрос**: `req_03e_source_addresses` (список 64 источников приложен), отправляет человек.
4. arXiv-идентификаторы из ответов **не считать проверенными**: часть может быть вымышлена сервисом; до проверки URL — `[допущение]`, не факт.

## 5. Что это меняет в наборе

- Правило «нет ссылки — нет находки» сработало ровно как задумано: без адресов ответ не прошёл приёмку. Это плюс.
- Минус: у нас нет способа быстро проверить источник, если сервис вернул только название. Лечение — требование URL в запросе (уже добавлено в шаблоны) и запрос на адреса для старых ответов.
