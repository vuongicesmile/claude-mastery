# Key Lessons — What Makes vuonglearning's Claude Setup Effective

## Lesson 1: "What NOT to do" > "What to do"

CLAUDE.md có section riêng cho **What NOT to do**:
```
- No print() — use logger
- No requests — use httpx
- No os.environ — use get_settings()
- No cross-service DB access
```

Claude "biết" cách làm Python. Section này override knowledge đó với project constraints.
**Bạn không cần dạy Claude Python — chỉ cần dạy project-specific rules.**

## Lesson 2: Immutable Stack Tables

Table này không để đọc — để Claude **không suggest wrong libraries**.
Một lần viết, tiết kiệm vô số lần sửa suggestion.

## Lesson 3: Hooks = Silent Quality Gates

- **pre-commit**: auto-fix format → check type → fail nếu còn lỗi
- **commit-msg**: reject nếu không phải conventional commit
- **Stop hook**: scan console.log trong code đã sửa

**Automation > Memory**

## Lesson 4: Per-Service CLAUDE.md

Context-specific instructions > Generic instructions

## Lesson 5: 20+ Audit Commands

Thay vì "review my code" → trigger specific audit với checklist cụ thể.
**Structured prompts > Open-ended requests**

## Lesson 6: Skill Priority Table

Claude phải follow process, không được freestyle.
**Defined workflow > Ad-hoc decisions**

## Lesson 7: Modular Rules Files

7 rule files auto-loaded, mỗi file focused.
**Modular rules > Monolithic instructions**

## Quick Start cho Personal Project (30 phút)

1. Tạo CLAUDE.md với stack + "What NOT to do"
2. Tạo .claude/rules/ cho cross-cutting concerns
3. Tạo .claude/commands/ cho domain-specific audits
4. Setup git hooks (pre-commit, commit-msg)
5. Add permission allowlist trong .claude/settings.json

**Time investment**: 30 phút setup → save giờ mỗi tuần.
