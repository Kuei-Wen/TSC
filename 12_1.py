import os, time, feedparser, pandas as pd, google.generativeai as genai
from urllib.parse import quote_plus

# 設定 API Key
genai.configure(api_key="AIzaSyBnIn9k5-O-SaYhvHwWniT5RgsKx26KX54")
model = genai.GenerativeModel("gemini-2.5-flash")

def fetch_google_news(query: str, lang="zh-Hant", region="TW", max_items: int = 20):
    """
    從 Google News RSS 抓取新聞。lang/region 可改成 en/US 等。
    """
    q = quote_plus(query)
    url = f"https://news.google.com/rss/search?q={q}&hl={lang}&gl={region}&ceid={region}:{lang}"
    feed = feedparser.parse(url)
    rows = []
    for entry in feed.entries[:max_items]:
        rows.append({
            "query": query,
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "published": entry.get("published", ""),
            "link": entry.get("link", "")
        })
    return pd.DataFrame(rows)

def sentiment_batch_gemini_bulk(headlines: list[str], summaries: list[str] | None = None):
    """
    一次把多則新聞送進 Gemini，回傳 JSON 陣列結果
    """
    import json, re

    # 建立提示詞
    prompt = "請閱讀以下多則新聞（標題+摘要），逐一評估市場情緒，最後輸出 JSON 陣列：\n\n"
    for i, h in enumerate(headlines):
        s = (summaries[i] if summaries else "") or ""
        prompt += f"新聞{i+1}:\n標題: {h}\n摘要: {s}\n\n"

    prompt += """
定義：
- label: positive / neutral / negative
- score: 0~1，越大越正面，約0.5為中性
- rationale: 1~2 句理由（中文，避免誇大）

請輸出 JSON 陣列，例如：
[
 {"label":"positive","score":0.8,"rationale":"理由"},
 {"label":"neutral","score":0.5,"rationale":"理由"},
 {"label":"negative","score":0.3,"rationale":"理由"}
]
    """

    res = model.generate_content(prompt)

    # 嘗試取回文字
    output_text = res.text.strip() if hasattr(res, "text") else res.candidates[0].content.parts[0].text.strip()

    # 只取 JSON 陣列部分
    match = re.search(r"\[.*\]", output_text, re.S)
    if not match:
        raise ValueError(f"模型輸出不含 JSON 陣列:\n{output_text}")

    return json.loads(match.group())

# === 使用範例 ===
df_g = fetch_google_news("台積電", lang="zh-Hant", region="TW", max_items=15)

if not df_g.empty:
    results = sentiment_batch_gemini_bulk(df_g["title"].tolist(), df_g["summary"].tolist())

    # 把結果展開合併回 DataFrame
    df_res = pd.DataFrame(results)
    df_g = pd.concat([df_g, df_res], axis=1)

    # 依分數排序
    df_g = df_g.sort_values("score", ascending=False).reset_index(drop=True)

df_g.head(10)