"""
Project 1: AI-Powered Code Reviewer
Usage: git diff | python main.py
"""
import anthropic
import sys
import json
from functools import lru_cache

SYSTEM_PROMPT = """You are an expert code reviewer. Review code changes and return ONLY valid JSON:
{
  "summary": "brief summary",
  "score": 0-100,
  "findings": [{"severity":"CRITICAL|HIGH|MEDIUM|LOW","category":"security|bug|perf|style","description":"...","suggestion":"..."}],
  "positives": ["good patterns"]
}"""

@lru_cache
def get_client():
    return anthropic.Anthropic()

def review_diff(diff: str) -> dict:
    client = get_client()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": f"Review this diff:\n\n```diff\n{diff}\n```"}],
    )
    try:
        return json.loads(response.content[0].text)
    except:
        return {"summary": response.content[0].text, "findings": [], "score": 50}

def main():
    diff = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not diff.strip():
        print("Usage: git diff | python main.py"); return
    review = review_diff(diff)
    score = review.get("score", 0)
    print(f"\n{'🟢' if score>=80 else '🟡' if score>=60 else '🔴'} Score: {score}/100")
    print(f"📋 {review.get('summary', '')}\n")
    for f in review.get("findings", []):
        print(f"  [{f['severity']}] {f['description']}")
        print(f"  → {f['suggestion']}\n")

if __name__ == "__main__":
    main()
