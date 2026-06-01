# Module 01 — CLI Commands & Keyboard Shortcuts

## 🖥 Khởi động Claude Code

```bash
# Cơ bản
claude                          # start interactive session
claude "explain this code"      # one-shot query
claude -p "your prompt"         # pipe mode

# Model selection
claude --model claude-opus-4-7      # Opus — deepest reasoning
claude --model claude-sonnet-4-6    # Sonnet — best coding (default)
claude --model claude-haiku-4-5     # Haiku — fast, lightweight

# File input
claude < input.txt              # pipe file content
cat error.log | claude "fix this"
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel current response |
| `Ctrl+L` | Clear screen |
| `Ctrl+R` | Search history |
| `↑ / ↓` | Navigate history |
| `Tab` | Autocomplete |
| `Shift+Enter` | New line (multi-line input) |
| `Alt+T` | Toggle extended thinking |
| `Ctrl+O` | Toggle verbose/thinking output |

## 🔧 Session Flags

```bash
claude --no-auto-updates        # tắt auto update
claude --verbose                # hiện chi tiết tool calls
claude --debug                  # debug mode
claude --dangerously-skip-permissions  # ⚠️ skip confirmations
```

## 📁 Working with Files

```bash
# Claude đọc files trong context
claude "review @src/app.py"    # @ syntax để reference file

# Nhiều files
claude "compare @old.py and @new.py"

# Cả folder
claude "what does @src/ do"
```

## 🔗 Chaining Commands

```bash
# Pipeline với Unix tools
git diff | claude "summarize these changes"
cat requirements.txt | claude "any security issues?"
ls -la | claude "what's taking the most space?"

# Save output
claude "generate unit tests for @auth.py" > tests/test_auth.py
```

## 💡 Pro Tips

```bash
# Non-interactive mode (CI/CD)
claude -p "fix lint errors" --no-interactive

# Specify working directory
claude --dir /path/to/project "add type hints"

# Continue last session
claude --continue

# With custom system prompt
claude --system "You are a security expert"
```
