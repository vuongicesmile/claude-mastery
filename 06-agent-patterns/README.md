# Module 06 — Agent Patterns

> Multi-agent = spawn Claude instances để làm việc song song hoặc theo pipeline

## 🤖 When to Use Agents

```
Single Claude session:
  ✅ Most tasks (chat, code, review)
  ✅ Tasks under ~100K tokens
  ✅ Linear workflows

Multi-agent:
  ✅ Tasks needing multiple independent perspectives
  ✅ Large codebases (agent per module)
  ✅ Parallel work (test + docs + review simultaneously)
  ✅ Long-running tasks that would overflow context
  ✅ Tasks needing adversarial verification
```

## 🏗 Agent Types in Claude Code

```
claude        → main orchestrator (you talk to this)
  ↓ spawns
Explore       → fast read-only search
Plan          → architecture/design planning
code-reviewer → code quality review
tdd-guide     → test-driven development
security-reviewer → security analysis
```

## 🔁 Pattern 1: Orchestrator + Workers

```
You → Claude (orchestrator)
         ↓
    Worker A: "Analyze auth module"
    Worker B: "Analyze payment module"  (parallel)
    Worker C: "Analyze user module"
         ↓
    Synthesizer: "Combine findings + prioritize"
```

Example prompt:
```
"Spawn 3 parallel agents:
1. Review auth.py for security issues
2. Review payments.py for security issues
3. Review users.py for security issues
Then synthesize findings into a prioritized report"
```

## 🔍 Pattern 2: Researcher + Implementer

```
Researcher agent:
  → Read codebase
  → Find relevant patterns
  → Return: existing conventions, similar code

Implementer agent:
  → Receives researcher output as context
  → Implements following established patterns
  → No need to re-read everything
```

## ✅ Pattern 3: Adversarial Verification

```
Generator:    "Implement JWT auth"
                    ↓
Attacker 1:   "Try to bypass this auth" → finds issues
Attacker 2:   "Find race conditions"    → finds issues
Attacker 3:   "Find injection points"   → finds issues
                    ↓
Fixer:        "Fix all identified issues"
```

```javascript
// In a workflow
const implementation = await agent("Implement JWT auth")
const attacks = await parallel([
  () => agent(`Attack this auth implementation: ${implementation} — focus on bypass`),
  () => agent(`Attack this auth implementation: ${implementation} — focus on race conditions`),
  () => agent(`Attack this auth implementation: ${implementation} — focus on injection`),
])
const vulnerabilities = attacks.flat().filter(Boolean)
const fixed = await agent(`Fix these vulnerabilities: ${vulnerabilities.join('\n')} in:\n${implementation}`)
```

## 🗺 Pattern 4: Map-Reduce

```
Input: 50 files to analyze

Map phase:
  Agent 1: analyze files 1-10
  Agent 2: analyze files 11-20  (parallel)
  ...
  Agent 5: analyze files 41-50

Reduce phase:
  Agent 6: merge all findings, deduplicate, prioritize
```

## 🔄 Pattern 5: Self-Reflection Loop

```
Draft → Critic → Revise → Critic → Revise → ...
```

```
Turn 1: "Write a design doc for X"
Turn 2: "Now criticize your design. What's weak?"
Turn 3: "Revise based on your criticism"
Turn 4: "What would a skeptical senior engineer object to?"
Turn 5: "Address those objections"
```

## 📊 Agent Communication

Agents communicate through:
1. **Return values** — structured output passed to next agent
2. **Files** — write to disk, next agent reads
3. **Context injection** — paste output into next prompt
4. **Shared tools** — both agents use same MCP server

## ⚡ Agent Spawning Syntax

```
In Claude Code chat:
"Use the Agent tool to spawn a sub-agent that..."
"Run these 3 tasks in parallel using agents:"
"Delegate the security review to a specialized agent"

In Claude's thinking:
Agent({ description: "...", prompt: "..." })
```

## 🎯 Real-World Example: PR Review

```
PR Review Agent System:

1. Diff Reader (1 agent)
   → Reads git diff
   → Returns: changed files + line ranges

2. Parallel Reviewers (3 agents)
   → Agent A: correctness & logic
   → Agent B: security vulnerabilities
   → Agent C: performance & scalability

3. Test Generator (1 agent)
   → Receives: identified bugs
   → Generates: regression tests for each bug

4. Summarizer (1 agent)
   → Receives: all findings
   → Generates: PR review comment with severity ratings
```
