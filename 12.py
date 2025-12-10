import requests
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import google.generativeai as genai

# 設定 Gemini
genai.configure(api_key="AIzaSyBnIn9k5-O-SaYhvHwWniT5RgsKx26KX54")
model = genai.GenerativeModel("gemini-1.5-flash")

NEWS_API_KEY = "3a27c4790d7f4d0b8f76f58a66f1f455"

def fetch_newsapi_news(ticker: str, max_items: int = 10):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": ticker,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
        "pageSize": max_items
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("NewsAPI 抓取失敗:", resp.status_code, resp.text)
        return pd.DataFrame()
    data = resp.json()
    rows = []
    for item in data.get("articles", []):
        rows.append({
            "ticker": ticker,
            "title": item.get("title") or "",
            "publisher": item.get("source", {}).get("name") or "",
            "published_at": item.get("publishedAt") or "",
            "url": item.get("url") or ""
        })
    return pd.DataFrame(rows)

def sentiment_with_gemini(texts: list[str]):
    results = []
    for t in texts:
        prompt = f"""
請判定以下文字的市場情緒傾向，輸出 JSON：
文字: {t}

輸出格式（僅 JSON）：
{{
  "label": "positive|neutral|negative",
  "score": 0.0
}}
"""
        try:
            res = model.generate_content(prompt)
            txt = res.text.strip()
        except Exception:
            txt = '{"label":"neutral","score":0.5}'
        results.append(txt)
        time.sleep(0.2)
    return results

# 主流程
df_news = fetch_newsapi_news("AAPL", max_items=10)

if df_news.empty or df_news["title"].isna().all():
    print("沒有抓到有效新聞標題。")
else:
    titles = [t for t in df_news["title"].tolist() if t]
    raw_scores = sentiment_with_gemini(titles)
    labels, scores = [], []
    for r in raw_scores:
        try:
            obj = json.loads(r)
            labels.append(obj.get("label", "neutral"))
            scores.append(float(obj.get("score", 0.5)))
        except Exception:
            labels.append("neutral")
            scores.append(0.5)

    df_news = df_news.loc[df_news["title"].notna()].reset_index(drop=True)
    df_news["sentiment_label"] = labels
    df_news["sentiment_score"] = scores
    df_news = df_news.sort_values("sentiment_score", ascending=False).reset_index(drop=True)
    print(df_news.head(10))
#https://newsapi.org/v2/everything?q=apple&from=2025-12-07&to=2025-12-07&sortBy=popularity&apiKey=API_KEY    