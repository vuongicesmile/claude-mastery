# Pattern: Custom Slash Commands — Audit System

## ilmuchat có 20+ audit commands

Tất cả trong `.claude/commands/`. Invoke bằng `/audit-security`, `/audit-performance`, etc.

## audit-security.md (thực tế)

```markdown
Perform a comprehensive security audit of the ilmuchat codebase.

Focus areas:
1. Authentication & Authorization
   - JWT token validation (type checking, expiry)
   - MFA gate enforcement on all auth flows
   - BOLA/IDOR — verify ownership before mutations
   - Anti-enumeration delays on sensitive endpoints

2. Input Validation
   - SQL injection via ORM (parameterized queries)
   - Path traversal in file operations
   - XSS in HTML responses
   - Request body size limits

3. Secrets & Credentials
   - No hardcoded secrets (API keys, passwords, tokens)
   - Environment variables properly sourced via get_settings()
   - No secrets in logs (JWT, passwords, MFA codes)

4. Inter-Service Security
   - INTERNAL_API_KEY on all internal endpoints
   - CORS restricted to explicit allowlist
   - No cross-service DB access

Return findings as:
## CRITICAL (fix before merge)
## HIGH (fix before merge)
## MEDIUM (consider fixing)
## LOW (optional)

For each: location, description, attack vector, remediation
```

## audit-performance.md

```markdown
Analyze ilmuchat for performance issues.

Check:
1. Database Queries
   - N+1 query patterns (missing selectinload/joinedload)
   - Missing indexes on filtered/sorted columns
   - Unbounded queries without pagination/limits
   - Synchronous I/O in async handlers

2. Cache Usage
   - Redis cache hits vs misses (auth user cache 60s TTL)
   - Missing caches on expensive operations
   - Cache invalidation correctness

3. SSE Streaming Path (latency-sensitive)
   - Unnecessary buffering in relay path
   - Processing in hot path that could be async
   - Memory accumulation in long streams

4. Frontend Bundle
   - Bundle size regressions (>200KB new dependency)
   - Unnecessary re-renders
   - Missing lazy loading for heavy components

Report as: [SEVERITY] [COMPONENT] description + estimated impact
```

## audit-api-contracts.md

```markdown
Verify all API contracts in ilmuchat are correct and consistent.

Check:
1. OpenAPI Spec vs Implementation
   - Run: make specs && make specs-check
   - Every new endpoint documented

2. TypeScript Types vs Pydantic Schemas  
   - Run: make types-check
   - Generated types match current schemas

3. SSE Event Shapes
   - Verify all SSE events match CLAUDE.md specification
   - Check payload structure for: content, status, sources, images,
     safety, reasoning, usage, error, done, stream_resumed, stream_resume_fallback

4. Inter-Service Contracts
   - ilmuchat-api → ai-service: POST /chat/completions fields
   - ai-service → ai-safety-service: POST /v1/evaluate fields
   - Internal endpoints match Internal API Key auth

Return: list of mismatches with file locations
```

## Tạo Custom Commands cho Personal Project

Ví dụ cho Python FastAPI project:

```markdown
<!-- .claude/commands/check-endpoints.md -->
Review all FastAPI endpoints in this project for:

1. Missing auth (should every endpoint require authentication?)
2. Missing rate limiting on public endpoints
3. Missing input validation (Pydantic schemas for all bodies)
4. Missing error handling (HTTPException for all error cases)
5. Missing tests (at least 1 test per endpoint)
6. Logging (entry + exit for each request handler)

List endpoints that need attention with specific issues.
```

```markdown
<!-- .claude/commands/db-review.md -->
Review all database operations in this project:

1. N+1 queries (missing eager loading)
2. Missing transactions for multi-step writes
3. Missing indexes (columns in WHERE/ORDER BY clauses)
4. Unbounded queries (missing LIMIT)
5. Sync operations in async handlers

Show the query, the issue, and the fix.
```

## Insight: Commands vs Skills

| | Slash Commands (.claude/commands/) | Skills (~/.claude/skills/) |
|---|---|---|
| **Scope** | Project-specific | Global (all projects) |
| **Purpose** | Domain-specific audits | Generic workflows |
| **Example** | /audit-ilmuchat-security | /tdd, /debug, /code-review |
| **Format** | Instructions only | Can include metadata, workflow |
| **Best for** | "check THIS codebase for X" | "do X using this process" |
