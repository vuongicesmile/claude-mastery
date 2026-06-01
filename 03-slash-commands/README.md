# Module 03 — Slash Commands & Custom Commands

## Built-in Slash Commands

```bash
/help           # show all commands
/clear          # clear conversation
/compact        # compact conversation (save context)
/config         # open settings
/cost           # show token usage
/doctor         # diagnose setup
/exit           # exit Claude Code
/init           # create CLAUDE.md for project
/login          # login to Claude
/logout         # logout
/memory         # view/edit memory
/model          # switch model
/pr-comments    # show PR comments
/review         # code review current diff
/terminal-setup # setup terminal integration
/vim            # toggle vim mode
```

## /init — Project Setup

```bash
# Trong project folder
cd my-project
claude /init
```

Tạo `CLAUDE.md` — file hướng dẫn Claude về project của bạn:

```markdown
# My Project — CLAUDE.md

## Stack
- Python 3.12, FastAPI, PostgreSQL
- React 19, TypeScript, Tailwind

## Conventions
- snake_case for Python, camelCase for JS
- Always add type hints
- Use httpx, never requests

## Testing
- pytest for backend, vitest for frontend
- 80% coverage minimum

## What NOT to do
- No print() — use logger
- No raw SQL — use SQLAlchemy ORM
```

## /review — Code Review

```bash
# Review staged changes
git add .
claude /review

# Review với custom focus
claude /review --focus security
claude /review --effort high
```

## /memory — Persistent Memory

```bash
# View current memory
claude /memory

# Claude tự lưu memory về bạn và project
# Memory persist qua sessions
```

## 🔨 Custom Slash Commands

Tạo file trong `.claude/commands/`:

```bash
mkdir -p .claude/commands
```

### Example: `/test-gen`

```markdown
<!-- .claude/commands/test-gen.md -->
Generate comprehensive unit tests for the selected code.

Requirements:
- Use pytest for Python, vitest for TypeScript
- Test happy path, edge cases, error cases
- Mock external dependencies
- Add docstrings explaining what each test verifies
- Aim for 100% branch coverage of the provided code
```

Dùng:
```bash
claude /test-gen  # Claude generates tests for selected/recent code
```

### Example: `/security-scan`

```markdown
<!-- .claude/commands/security-scan.md -->
Perform a security audit of the provided code.

Check for:
1. OWASP Top 10 vulnerabilities
2. Hardcoded secrets or credentials
3. SQL injection / NoSQL injection
4. XSS vulnerabilities
5. Insecure deserialization
6. Authentication/authorization bypasses

Return findings as: CRITICAL / HIGH / MEDIUM / LOW
For each finding: location, description, fix recommendation
```

### Example: `/commit-msg`

```markdown
<!-- .claude/commands/commit-msg.md -->
Generate a conventional commit message for the current git diff.

Format: type(scope): description
Types: feat, fix, refactor, docs, test, chore, perf, ci

Rules:
- Under 72 characters
- Present tense, imperative mood
- Focus on WHY not WHAT
- Include breaking changes if any

Output ONLY the commit message, nothing else.
```

Dùng:
```bash
git diff --staged | claude /commit-msg
```

### Example: `/explain-like-5`

```markdown
<!-- .claude/commands/explain-like-5.md -->
Explain the selected code as if the reader is:
- Experienced in programming but new to this specific pattern/technology
- Wants to understand WHAT it does, WHY it was written this way, and HOW it works
- Appreciates analogies to simpler, more familiar concepts

Format:
## What it does (1-2 sentences)
## Why this approach (design decision)
## How it works (step by step)
## Gotchas (what could go wrong)
```

## Global vs Project Commands

```
~/.claude/commands/     ← available in ALL projects
.claude/commands/       ← only in THIS project
```
