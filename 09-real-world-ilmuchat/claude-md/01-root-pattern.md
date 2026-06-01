# Pattern: Root CLAUDE.md

## Tại sao ilmuchat có CLAUDE.md 1200+ dòng?

Vì Claude **đọc lại từ đầu mỗi session**. File này trả lời trước tất cả câu hỏi Claude có thể hỏi.

## Structure thực tế

```markdown
# ILMUchat — AI Coding Agent Instructions

## What This Is
[mô tả project 2-3 dòng]

## YTL AI Labs Skills & Agents
[bảng skill nào dùng cho task nào]

## Layout
[bảng service → path → port → stack]

## Architecture
[diagram ASCII của service dependencies]

## Coding Conventions
[Python: ruff, mypy strict, httpx only, never requests]
[Frontend: pnpm, shadcn/ui, Zustand + TanStack Query]

## Security
[inter-service auth, CORS, never commit secrets]

## API Type Synchronization
[make types-generate khi thay đổi Pydantic schema]

## What NOT to do
[list cụ thể những gì KHÔNG làm — quan trọng nhất!]

## Change Workflow
[mandatory steps cho mọi code change]
```

## "What NOT to do" Section — Cực kỳ quan trọng

```markdown
## What NOT to do
- No `print()` — use logger
- No `requests` or `urllib` — use httpx
- No `os.environ` directly — use `get_settings()`
- No real secrets in `.env.example`
- No committing `.env`, `__pycache__`, `node_modules`, `.next/`
- No cross-service imports — services communicate via HTTP only
- No cross-service database access — each service owns its database
- No `usage_daily.chat_messages` in analytics — source from `ai_usage_records`
```

**Tại sao effective?** Claude sẽ không suggest print() hay requests nữa, dù đó là gợi ý tự nhiên nhất.

## Per-Service CLAUDE.md

Mỗi service có CLAUDE.md riêng với:
1. **Immutable Stack** — table liệt kê library + rules (Never use X, Always use Y)
2. **Domain Module Structure** — template cho folder mới
3. **Naming Conventions** — cụ thể từng loại file
4. **Security Model** — chi tiết auth flow
5. **Known Incomplete Features** — tránh implement lại cái đang làm dở

### Ví dụ Immutable Stack Table:

```markdown
| Component | Library | Rules |
|-----------|---------|-------|
| HTTP | httpx async | Never requests, never aiohttp |
| ORM | SQLAlchemy 2.0 async | asyncpg driver, never sync |
| Config | pydantic-settings | Single Settings class |
| Lint | ruff | Never black, flake8, isort separately |
| Package | uv | Never pip directly, never poetry |
```

Claude sẽ không bao giờ suggest `pip install` hay `import requests` nữa.

## Template: CLAUDE.md cho Project Cá nhân

```markdown
# [Project Name] — CLAUDE.md

## Project Overview
[1-2 sentences: what it does, who uses it]

## Tech Stack (Immutable)
| Layer | Technology | Rules |
|-------|-----------|-------|
| Runtime | Python 3.12 | |
| Framework | FastAPI | No Flask |
| HTTP Client | httpx async | Never requests |
| DB | PostgreSQL + SQLAlchemy async | No raw SQL |
| Cache | Redis | Slot 0 for app cache |
| Tests | pytest | 80% coverage minimum |

## Commands
```bash
make dev     # start development
make test    # run tests
make lint    # lint + format
```

## Naming Conventions
- Files: snake_case.py
- Classes: PascalCase
- Functions: verb_noun (create_user, get_by_id)
- Constants: UPPER_SNAKE_CASE

## What NOT to do
- No print() → use logger
- No os.environ → use get_settings()
- No requests → use httpx
- [Add your own project-specific rules]

## Architecture
[ASCII or describe service dependencies]

## Testing
- Unit: test business logic in isolation
- Integration: test HTTP endpoints
- Coverage: 80% minimum, enforced by CI
```
