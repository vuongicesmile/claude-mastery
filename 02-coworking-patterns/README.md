# Module 02 — Coworking Patterns

> Làm việc hiệu quả với Claude = biết cách **frame vấn đề** + **delegate đúng cách** + **verify kết quả**

## 🧠 Mental Model: Claude là Senior Dev

Đừng dùng Claude như Google Search — dùng như **pair programmer senior**:

```
❌ "fix my code"
✅ "This function should return sorted users by score,
    but it's returning them unsorted. Here's the code: [...]
    What's wrong and how to fix it?"

❌ "add authentication"
✅ "I need to add JWT auth to this FastAPI app.
    Current setup: [context]. Requirements: [specs].
    Existing patterns in codebase: [example].
    Generate the auth middleware following the same patterns."
```

## 📋 The CRAFT Framework

| Letter | Meaning | Example |
|--------|---------|---------|
| **C** | Context | "This is a FastAPI app with PostgreSQL..." |
| **R** | Role | "Act as a security-focused backend engineer" |
| **A** | Action | "Review this auth code for vulnerabilities" |
| **F** | Format | "Return findings as bullet points by severity" |
| **T** | Target | "Focus on SQL injection and auth bypass" |

## 🎯 Pattern 1: Context Priming

Bắt đầu session bằng context dump:

```
"Let me give you context before we start:
- Project: E-commerce API in Python/FastAPI
- Database: PostgreSQL with SQLAlchemy
- Auth: JWT tokens, 15min access / 7day refresh
- Patterns: Repository pattern, dependency injection
- Current issue: [describe]"
```

## 🔄 Pattern 2: Incremental Refinement

```
Step 1: "Generate a basic version of X"
Step 2: "Now add error handling"
Step 3: "Add logging following our pattern: [example]"
Step 4: "Write tests for edge cases"
Step 5: "Review for security issues"
```

Đừng yêu cầu tất cả cùng lúc → output quality giảm.

## 🧩 Pattern 3: Role Assignment

```bash
# Security review
"Act as a senior security engineer. Review this auth code
for OWASP Top 10 vulnerabilities. Be skeptical."

# Performance optimization
"Act as a performance engineer. Profile this function
mentally and suggest optimizations. Show Big O analysis."

# Code review
"Act as a strict code reviewer at Google.
Review this PR with high standards."
```

## 📸 Pattern 4: Show Don't Tell

```
❌ "Add error handling like we do elsewhere"
✅ "Add error handling following this pattern we use:
   ```python
   try:
       result = await service.get_user(id)
   except UserNotFoundError:
       raise HTTPException(status_code=404, detail={'error': {'code': 'user.not_found'}})
   except DatabaseError as e:
       logger.error('db.error', extra={'error': str(e)})
       raise HTTPException(status_code=500)
   ```"
```

## ✅ Pattern 5: Verification Loop

```
1. Claude generates code
2. You: "Walk me through what this does step by step"
3. You: "What edge cases does this NOT handle?"
4. You: "What would break this in production?"
5. You: "Write a test that would catch regressions"
```

## 🚫 Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| "Fix all bugs" | Too vague | Specify which bug, what behavior expected |
| Giant code dumps | Claude loses focus | Break into smaller chunks |
| No context | Generic solutions | Always provide stack/pattern context |
| Accept first output | Missing edge cases | Always ask "what could go wrong?" |
| Skip verification | Silent regressions | Run tests, ask Claude to self-review |

## 🏋️ Advanced: Multi-Turn Strategy

```
Turn 1: "Understand the codebase" — explore
Turn 2: "Plan the implementation" — design  
Turn 3: "Implement step by step" — build
Turn 4: "Review and improve" — refine
Turn 5: "Write tests" — verify
Turn 6: "Document the change" — ship
```
