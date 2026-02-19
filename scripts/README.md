# scripts/prioritize_issues.py

Небольшой скрипт для быстрого ранжирования открытых issue по ключевым словам в заголовках.

Использование:

```bash
python3 scripts/prioritize_issues.py --token $GITHUB_TOKEN --top 10
```

Параметры:
- `--token` — GitHub token (если не задан, возьмётся из `GITHUB_TOKEN`)
- `--owner` — владелец репозитория (по умолчанию `miamok`)
- `--repo` — имя репозитория (по умолчанию `skills-integrate-mcp-with-copilot`)
- `--top` — сколько показать сверху (по умолчанию 5)

Скрипт не делает никаких изменений в репозитории — только читает открытые issues через GitHub API и выводит топ по простой эвристике.