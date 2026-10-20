import os
import requests

API_KEY = "sk-b48ff19209ff4a919f75fc7a82b1e822"

def search_web(query: str, count: int = 3) -> list[dict]:
    """调用 DeepSeek Search API，返回搜索结果列表"""
    resp = requests.post(
        "https://api.deepseek.com/v1/tools/search",
        headers={"Authorization": f"Bearer {API_KEY}"},      # ← 身份：谁是调用者
        json={"query": query, "count": count, "need_content": False},  # ← 参数：搜什么
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])

def fetch_page(url: str) -> dict:
    resp = requests.post(
        "https://api.deepseek.com/v1/tools/fetch",
        headers = {"Authorization": f"Bearer {API_KEY}"},
        json={"url": url},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    results = search_web("DeepSeek 最新模型 2026", count=3)
    for r in results:
        print(f"[{r.get('rerank_score', '?')}] {r.get('title')} -> {r.get('url')}")

    if results:
        page = fetch_page(results[0]["url"])
        print("\n--- 正文前 500 字 ---")
        print(page.get("content", "")[:500])