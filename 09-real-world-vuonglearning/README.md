# Module 09 — Real World: How vuonglearning Uses Claude Code

> Đây là cách Claude Code được dùng trong production tại VuongLearning.
> Tất cả examples dưới đây là từ codebase thật, không phải demo.

## 📁 Cấu trúc thực tế

```
vuonglearning/
├── CLAUDE.md                    ← Global architecture guide (1200+ lines!)
├── .claude/
│   ├── settings.local.json      ← Permission allowlist cho máy này
│   ├── rules/                   ← Auto-loaded rules (7 files)
│   │   ├── pre-push.md          ← Pre-push checklist
│   │   ├── pr-review.md         ← PR etiquette + SLA
│   │   ├── maintainability.md   ← Code complexity ceilings
│   │   ├── documentation.md     ← Doc requirements by scope
│   │   ├── observability.md     ← Logging + tracing
│   │   ├── performance.md       ← SLO + profiling
│   │   └── dependencies.md      ← Dependency management
│   └── commands/                ← 20+ audit slash commands
│       ├── audit-security.md
│       ├── audit-performance.md
│       └── ... (18 more)
├── services/
│   ├── vuonglearning-api/CLAUDE.md   ← Per-service guide (2062 lines!)
│   ├── ai-service/CLAUDE.md
│   └── .../CLAUDE.md
└── scripts/hooks/               ← Git hooks
    ├── pre-commit
    ├── pre-push
    ├── commit-msg
    └── lib.sh
```

## 💡 Key Insight

**CLAUDE.md = living architecture document** — không phải README thông thường.
Claude đọc file này trước mỗi task để hiểu:
- Stack và conventions
- What NOT to do (rất quan trọng!)
- Security model
- Testing requirements
- Patterns đang dùng trong codebase
