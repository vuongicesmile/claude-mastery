# Module 05 — Skills & Workflows

> Skills = custom instructions Claude loads on demand
> Workflows = multi-agent orchestration scripts

## 📚 Skills System

Skills = markdown files Claude reads as instructions.

```
~/.claude/skills/          ← global skills
.claude/skills/            ← project-specific skills
```

### Anatomy of a Skill

```markdown
---
name: tdd-workflow
description: Test-driven development workflow enforcing write-tests-first
when_to_use: When implementing new features or fixing bugs
---

## TDD Workflow

MANDATORY steps:
1. Write failing test FIRST
2. Run test → must FAIL (Red)
3. Write minimal implementation
4. Run test → must PASS (Green)
5. Refactor while keeping tests green
6. Verify coverage >= 80%

Never skip the Red phase.
Never write implementation before tests.
```

Invoke: `claude /tdd-workflow`

### Skill Examples

#### `/debug` skill
```markdown
---
name: debug
description: Systematic debugging approach for any bug or unexpected behavior
---

## Debugging Protocol

1. **Reproduce** — Create minimal reproduction case
2. **Isolate** — Binary search to find exact location
3. **Hypothesize** — Form theory about root cause
4. **Verify** — Test hypothesis with targeted change
5. **Fix** — Apply minimal fix
6. **Prevent** — Add test to catch regression

Do NOT guess. Do NOT fix multiple things at once.
Always understand WHY before fixing.
```

#### `/architect` skill
```markdown
---
name: architect
description: System design and architecture review
---

When reviewing or designing systems, always consider:

## Functional Requirements
- What must it do?
- What are the user journeys?

## Non-Functional Requirements  
- Scale: how many users/requests?
- Latency: p99 acceptable?
- Availability: 99.9% or 99.99%?
- Consistency: eventual vs strong?

## Design Decisions
For each major decision, document:
- Options considered
- Tradeoffs
- Decision made and why
- What would make you reconsider

## Red Flags to Check
- Single points of failure
- N+1 query patterns
- Unbounded growth
- Missing error handling
- Security boundaries
```

## ⚙️ Workflows

Workflows = JavaScript scripts that orchestrate multiple agents.

```javascript
// .claude/workflows/code-review.js
export const meta = {
  name: 'code-review',
  description: 'Multi-angle code review with auto-fix',
  phases: [
    { title: 'Review', detail: 'Bug, security, performance analysis' },
    { title: 'Fix', detail: 'Apply critical fixes' },
  ]
}

const DIMENSIONS = [
  { key: 'bugs',     prompt: 'Find logic bugs and incorrect behavior' },
  { key: 'security', prompt: 'Find security vulnerabilities (OWASP Top 10)' },
  { key: 'perf',     prompt: 'Find performance issues (N+1, O(n²), memory leaks)' },
]

// Fan out parallel reviews
const results = await pipeline(
  DIMENSIONS,
  d => agent(d.prompt, { label: `review:${d.key}`, phase: 'Review' }),
)

// Collect critical findings
const critical = results.flat().filter(r => r?.severity === 'CRITICAL')
log(`Found ${critical.length} critical issues`)

// Auto-fix critical issues
await parallel(critical.map(issue => () =>
  agent(`Fix this issue: ${issue.description} in ${issue.file}`, { phase: 'Fix' })
))
```

Run: `claude /workflow code-review`

## 🔄 Built-in Workflows

```bash
/workflow code-review           # multi-angle review
/workflow test-coverage         # find gaps, generate tests  
/workflow security-audit        # full security scan
/workflow refactor-module       # safe refactoring
/workflow dependency-update     # check + update deps
```

## 💡 Workflow Patterns

### Parallel Fan-out
```javascript
// Run N agents at once
const results = await parallel([
  () => agent("Find bugs"),
  () => agent("Find security issues"),
  () => agent("Find performance issues"),
])
```

### Pipeline (staged)
```javascript
// Each stage feeds the next
const findings = await pipeline(
  files,
  file => agent(`Analyze ${file}`),
  finding => agent(`Verify: ${finding}`),
  verified => agent(`Fix: ${verified}`),
)
```

### Loop until done
```javascript
// Keep searching until nothing new found
const issues = []
let dry = 0
while (dry < 2) {
  const found = await agent("Find more issues not yet in list")
  const fresh = found.filter(f => !issues.includes(f))
  if (fresh.length === 0) { dry++; continue }
  dry = 0
  issues.push(...fresh)
}
```
