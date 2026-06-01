# Coworking Cheat Sheet

## Prompt Templates

### Bug Fix
```
Bug: [describe unexpected behavior]
Expected: [what should happen]
Actual: [what happens]
Code: [relevant snippet]
Already tried: [what you've attempted]
```

### Code Review Request
```
Review this [language] code for:
1. Correctness (logic bugs)
2. Security (OWASP Top 10)
3. Performance (Big O, N+1)
4. Maintainability (naming, structure)

Context: [what it does, how it's called]
Code: [snippet]
```

### Feature Implementation
```
Feature: [what to build]
Stack: [tech stack]
Constraints: [performance, security, backwards compat]
Existing pattern: [show example from codebase]
Tests needed: [yes/no, what kind]
```

### Debugging Session
```
I'm debugging [issue].
Environment: [OS, versions, config]
Error: [full error message + stack trace]
Reproduction: [steps to reproduce]
What I've tried: [attempted solutions]
Hypothesis: [my current theory]
```

### Architecture Decision
```
Decision: [what to decide]
Options I'm considering:
  A) [option with tradeoffs]
  B) [option with tradeoffs]
  
Context: [scale, team size, timeline]
Constraints: [budget, existing tech, skills]
Recommendation: [your leaning and why]
```
