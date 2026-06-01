# Pattern: Git Hooks — Automation Layer

## ilmuchat dùng 3 hooks

```
scripts/hooks/
├── pre-commit    ← auto-fix + check trước commit
├── pre-push      ← lint + typecheck trước push
├── commit-msg    ← validate conventional commit format
└── lib.sh        ← shared utilities
```

Cài đặt: `make hooks-install` → sets `core.hooksPath = scripts/hooks`

## pre-commit — Tự động fix + check

```bash
#!/bin/bash
# Phase 0: File hygiene + secrets scan
gitleaks detect --source . --staged

# Phase 1: Auto-fix staged files
# Python
if has_python_changes; then
    uv run ruff format src/       # format
    uv run ruff check --fix src/  # lint fix
    git add -u                    # re-stage fixed files
fi

# Node
if has_node_changes; then
    pnpm eslint --fix src/
    pnpm prettier --write src/
    git add -u
fi

# Phase 2: CI-equivalent checks (fail fast)
run_python_checks   # ruff format --check, ruff check, mypy
run_node_checks     # pnpm lint, pnpm typecheck
```

**Result:** Commit chỉ pass khi code đã format + type-safe.
Claude không cần nhớ phải chạy format — hook làm tự động.

## commit-msg — Enforce Conventional Commits

```bash
#!/bin/bash
MSG=$(cat "$1")
PATTERN="^(feat|fix|refactor|docs|test|chore|perf|ci)(\(.+\))?: .{1,72}$"

if ! echo "$MSG" | grep -qE "$PATTERN"; then
    echo "ERROR: Commit message không đúng format!"
    echo "Expected: type(scope): description"
    echo "Types: feat, fix, refactor, docs, test, chore, perf, ci"
    echo "Scopes: web, api, ai-service, ai-safety, ops, shared"
    exit 1
fi
```

**Result:** Mọi commit trong ilmuchat đều có format:
```
feat(api): add JWT refresh token rotation
fix(web): prevent crash when user.email is null
refactor(ai-service): extract tool dispatch to separate module
```

## lib.sh — Detect Changed Services

```bash
# Chỉ check service bị thay đổi — không check tất cả
detect_changed_services() {
    local changed_files=$(git diff --cached --name-only)
    
    echo "$changed_files" | grep -q "^services/ilmuchat-api/"  && echo "ilmuchat-api"
    echo "$changed_files" | grep -q "^services/ai-service/"    && echo "ai-service"  
    echo "$changed_files" | grep -q "^services/ai-safety/"     && echo "ai-safety"
    echo "$changed_files" | grep -q "^clients/web/"            && echo "web"
    echo "$changed_files" | grep -q "^clients/ops/"            && echo "ops"
}

# Chỉ chạy checks cho service thay đổi
for service in $(detect_changed_services); do
    case "$service" in
        "ilmuchat-api") cd services/ilmuchat-api && make format-check typecheck ;;
        "web")          cd clients/web && pnpm lint typecheck ;;
    esac
done
```

**Tại sao clever?** 5 services, nhưng chỉ check service bạn đang thay đổi.
Tiết kiệm 80% thời gian pre-commit.

## Template: Pre-commit cho Personal Project

```bash
#!/bin/bash
# scripts/hooks/pre-commit

set -e

echo "🔍 Running pre-commit checks..."

# Check Python files changed
if git diff --cached --name-only | grep -q "\.py$"; then
    echo "  Fixing Python..."
    uv run ruff format . --quiet
    uv run ruff check . --fix --quiet
    git add -u
    
    echo "  Checking Python..."
    uv run ruff format . --check --quiet || { echo "❌ Format check failed"; exit 1; }
    uv run mypy src/ --quiet || { echo "❌ Type check failed"; exit 1; }
fi

# Check TypeScript files changed
if git diff --cached --name-only | grep -qE "\.(ts|tsx)$"; then
    echo "  Fixing TypeScript..."
    pnpm prettier --write src/ --quiet
    git add -u
    
    echo "  Checking TypeScript..."
    pnpm lint --quiet || { echo "❌ Lint failed"; exit 1; }
    pnpm typecheck || { echo "❌ Type check failed"; exit 1; }
fi

echo "✅ Pre-commit passed!"
```

Setup:
```bash
git config core.hooksPath scripts/hooks
chmod +x scripts/hooks/pre-commit
```
