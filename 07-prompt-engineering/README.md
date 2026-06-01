# Module 07 — Prompt Engineering for Developers

## 🧠 Core Principles

### 1. Specificity > Brevity
```
❌ "Refactor this code"
✅ "Refactor this function to:
    - Reduce cyclomatic complexity from ~8 to <4
    - Extract the validation logic into a separate function
    - Keep the same public interface (don't change function signature)
    - Do NOT change the error handling behavior"
```

### 2. Constraints are Features
```
❌ "Write authentication middleware"
✅ "Write authentication middleware that:
    MUST: verify JWT, inject user into request
    MUST NOT: hit database on every request (use Redis cache)
    MUST NOT: change the existing middleware interface
    SHOULD: log auth failures with user_id and ip
    SHOULD NOT: log successful auths (too noisy)"
```

### 3. Show the Shape of the Answer
```
"Return your findings in this exact format:
## Summary (2 sentences)
## Critical Issues (bullet list)
## Recommendations (numbered, prioritized)
## Estimated effort (S/M/L per item)"
```

## 🎭 Persona Prompts

```
# For deep security review
"You are a paranoid security researcher who has found
critical vulnerabilities in major companies. You assume
all code is vulnerable until proven otherwise. Review this
auth system with maximum skepticism."

# For performance optimization
"You are a performance engineer at a company processing
1 billion requests/day. Even 1ms matters. Profile this
code mentally and suggest every possible optimization,
no matter how small."

# For code review
"You are a senior engineer who values simplicity above all.
Your motto is 'the best code is no code'. Review this PR
and suggest everything that could be simplified, removed,
or replaced with existing libraries."
```

## 🔗 Chain of Thought Prompting

```
"Think through this step by step:
1. First, identify what the current code does
2. Then, identify what the bug report says should happen
3. Find the gap between actual and expected behavior
4. Identify the root cause
5. Propose the minimal fix
6. Consider what else might break

Show your reasoning at each step."
```

## 🎯 Few-Shot Prompting

```
"Generate a commit message for the following diff.
Here are examples of our commit style:

EXAMPLE 1:
Diff: [adds user avatar upload]
Message: feat(profile): add avatar upload with S3 storage

EXAMPLE 2:
Diff: [fixes null check in auth]
Message: fix(auth): prevent crash when user.email is null

EXAMPLE 3:
Diff: [refactors query builder]
Message: refactor(db): extract query builder to reduce duplication

Now generate for this diff:
[your diff here]"
```

## 🏗 Structured Output

```
"Analyze this codebase and return ONLY valid JSON:
{
  'health_score': 0-100,
  'critical_issues': [
    {'file': '...', 'line': 0, 'issue': '...', 'fix': '...'}
  ],
  'tech_debt': ['...'],
  'positive_patterns': ['...']
}"
```

## 🔄 Iterative Refinement Prompts

```
Round 1: "Generate a basic solution"
Round 2: "What are the weaknesses of this solution?"
Round 3: "Fix the weaknesses you identified"
Round 4: "What would make this production-ready?"
Round 5: "Make it production-ready"
Round 6: "Final review — any remaining issues?"
```

## 📐 Prompt Templates Library

### The STAR Bug Report
```
Situation: [codebase context, what the code is supposed to do]
Task: [what behavior is expected]
Action: [what actually happens / error message]
Result: [impact, what's broken]

Code: [minimal reproduction]
Tried: [what you've already attempted]
```

### The PREP Feature Request
```
Problem: [what user pain point this solves]
Result: [what success looks like]
Evidence: [why this matters, data if any]
Proposal: [your suggested approach]

Constraints: [time, backwards compat, performance]
Questions: [decisions that need to be made]
```

### The DEBUG Protocol
```
Bug: [one-line description]
Reproduction: [exact steps]
Expected: [what should happen]
Actual: [what happens instead]
Environment: [OS, versions, config]
Error: [full error + stack trace]
Context: [relevant code, recent changes]
Hypothesis: [your current theory]
Ruled out: [what you've eliminated]
```
