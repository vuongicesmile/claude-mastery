# Exercises — CLI Commands

## Exercise 1: First Commands
Thử các lệnh này trong terminal:
```bash
claude --version
claude "hello, what can you do in 3 bullet points?"
echo "print('hello world')" | claude "explain this Python"
```

## Exercise 2: File Analysis
```bash
# Tạo 1 file Python có bug
cat > /tmp/buggy.py << 'PYEOF'
def divide(a, b):
    return a / b

result = divide(10, 0)
print(result)
PYEOF

# Nhờ Claude fix
claude "find and fix the bug in @/tmp/buggy.py"
```

## Exercise 3: Git Integration
```bash
# Trong một repo git
git log --oneline -5 | claude "write a release notes from these commits"
git diff HEAD~1 | claude "review this change, any issues?"
```

## Exercise 4: Chain Pipeline
```bash
# Generate code và save thẳng
claude "write a Python function to validate email address, just the code" > /tmp/email_validator.py
cat /tmp/email_validator.py
```

## Challenge: Build a Mini Script
Dùng Claude CLI để:
1. Generate một Python script đọc CSV và tính statistics
2. Save vào file
3. Nhờ Claude thêm error handling
4. Nhờ Claude viết unit tests
