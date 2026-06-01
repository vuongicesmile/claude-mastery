# Pattern: Skills System — VuongLearning Plugin

## Cách vuonglearning dùng Skills

CLAUDE.md có bảng "Skill Priority" — bắt Claude dùng skill thay vì tự làm:

```markdown
## VuongLearning Skills & Agents

### Skill & Command Priority
When a vuonglearning skill or command exists for the task, **always prefer it**:

| Task | Use This | Not This |
|------|----------|----------|
| Planning | `/vuonglearning:plan` | ad-hoc planning |
| TDD | `/vuonglearning:tdd` | writing tests without workflow |
| Code review | `/vuonglearning:code-review` | manual review |
| Build errors | `/vuonglearning:build-fix` | guessing at fixes |
| E2E tests | `/vuonglearning:e2e` | writing Playwright from scratch |
| Security scan | `/vuonglearning:security-scan` | manual checklist |

### Agent Delegation
For sub-agent work, prefer `vuonglearning:*` agents:
- `vuonglearning:code-reviewer` over generic `code-reviewer`
- `vuonglearning:tdd-guide` over generic `tdd-guide`
- `vuonglearning:architect` over generic `architect`
```

**Result:** Claude không tự "freestyle" — luôn follow đúng process của team.

## Anatomy của một Production Skill

Skill `/vuonglearning:tdd` thực tế:

```markdown
---
name: tdd-workflow
description: Test-driven development — enforces write-tests-first methodology
when_to_use: When implementing new features, fixing bugs, or refactoring
---

## TDD Workflow — MANDATORY

### Phase 1: RED
1. Understand the requirement completely before writing ANY code
2. Write the test first — describe expected behavior
3. Run the test — it MUST FAIL (if it passes, test is wrong)
4. Commit the failing test: `test: add failing test for [feature]`

### Phase 2: GREEN
5. Write MINIMAL implementation to make test pass
6. No over-engineering — just enough to pass
7. Run tests — they MUST PASS
8. Commit: `feat: implement [feature] (tests passing)`

### Phase 3: REFACTOR
9. Improve code quality while keeping tests green
10. Extract functions, improve naming, remove duplication
11. Run tests after each change
12. Commit: `refactor: improve [feature] implementation`

### Coverage Gate
- Check: `make test-cov` or `pnpm test:cov`
- Must be >= 80% on changed paths
- Never decrease existing coverage

NEVER skip RED phase.
NEVER write implementation before tests.
NEVER commit code without passing tests.
```

## Skill cho Personal Projects

Tạo `~/.claude/skills/my-python-project.md`:

```markdown
---
name: my-python-project
description: Standards for my FastAPI projects
when_to_use: When working on any Python FastAPI project
---

## My Python Standards

### Always
- Type hints on all function signatures
- Docstring on public functions (one line is fine)
- httpx for HTTP calls, never requests
- pydantic-settings for config
- pytest + pytest-asyncio for tests
- ruff for formatting/linting

### Never
- print() → use structlog or logging
- os.environ.get() → use Settings class
- Hardcoded secrets or API keys
- Sync SQLAlchemy in async handlers

### Test Pattern
```python
# One test per behavior, not per function
async def test_create_user_returns_201_with_valid_data():
    response = await client.post("/users", json=valid_user)
    assert response.status_code == 201
    assert response.json()["email"] == valid_user["email"]

async def test_create_user_returns_422_with_invalid_email():
    response = await client.post("/users", json={"email": "not-email"})
    assert response.status_code == 422
```

### Error Pattern
```python
try:
    result = await service.do_thing(id)
except ThingNotFoundError:
    raise HTTPException(404, detail={"error": {"code": "thing.not_found"}})
except DatabaseError as e:
    logger.error("db.error", extra={"error": str(e)})
    raise HTTPException(500)
```
```

## Rules Files — Auto-loaded Standards

vuonglearning có 7 rule files trong `.claude/rules/` — tự động load vào mọi session:

```
pre-push.md         → nhắc chạy lint + test trước push
pr-review.md        → format PR + review checklist
maintainability.md  → soft ceilings cho file/function size
documentation.md    → khi nào cần viết doc
observability.md    → structured logging standards
performance.md      → SLO và profiling guidance
dependencies.md     → cách thêm dependency mới
```

### Tạo Rules cho Personal Project

`.claude/rules/my-standards.md`:

```markdown
# My Coding Standards

## Test Coverage
- Minimum 80% coverage, enforced by CI
- Every bug fix needs a regression test
- Run: `pytest --cov=src --cov-fail-under=80`

## Commit Format
- Use conventional commits: type(scope): description
- Types: feat, fix, refactor, docs, test, chore
- Run `make check` before committing

## Code Review Checklist
- [ ] No hardcoded values (use constants or config)
- [ ] No TODO without a ticket number
- [ ] Tests pass locally
- [ ] No debug code (print, breakpoint, etc.)

## Documentation
- Public functions: one-line docstring minimum
- New endpoints: update API docs
- Architecture changes: update CLAUDE.md
```

**Tại sao rules > CLAUDE.md?** Rules files focus vào specific domains,
dễ update từng file riêng mà không phải sửa CLAUDE.md monolith.
