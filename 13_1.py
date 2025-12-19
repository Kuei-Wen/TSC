import requests
import pandas as pd
import yfinance as yf
import ta
import openai
import os
from dotenv import load_dotenv

# === 設定 Gemini API ===
# 設定 API Key

# 載入 .env 環境變數（確保你已經在 .env 檔案中設定 OPENAI_API_KEY）
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# === Step 1: 取得即時新聞 (NewsAPI) ===
symbol = "AAPL"  # 股票代碼

url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}"
response = requests.get(url).json()
articles = response.get("articles", [])[:3]  # 取前三則新聞

news_summary = "\n".join([f"- {a['title']} ({a['source']['name']})" for a in articles])

# === Step 2: 技術指標分析 ===
data = yf.download(symbol, period="3mo", interval="1d", auto_adjust=True)

# 確保 Close 是 1D Series
close_prices = data["Close"].squeeze()

# RSI (14日)
rsi_indicator = ta.momentum.RSIIndicator(close=close_prices, window=14)
data["RSI"] = rsi_indicator.rsi()

# 20日移動平均線
data["MA20"] = data["Close"].rolling(20).mean()

# 取最後一天指標並轉 float
latest_close = float(data["Close"].iloc[-1])
latest_rsi = float(data["RSI"].dropna().iloc[-1])
latest_ma = float(data["MA20"].dropna().iloc[-1])

tech_summary = f"""
最新收盤價：{latest_close:.2f}
RSI：{latest_rsi:.2f} ({'過熱' if latest_rsi>70 else '偏低' if latest_rsi<30 else '中性'})
MA20：{latest_ma:.2f} ({'股價在均線之上' if latest_close>latest_ma else '股價在均線之下'})
"""

# === Step 3: AI 綜合解讀 ===
prompt = f"""
以下是關於 {symbol} 的最新市場資訊：

新聞摘要：
{news_summary}

技術分析：
{tech_summary}

請綜合以上資訊，給我一份整體投資解讀（白話、200字內）。
"""

#analysis = model.generate_content(prompt)
res = openai.Completion.create(
    model="gpt-4o-mini",
    prompt=prompt,
    max_tokens=1024
    ,
    temperature=0.5,
)



# 嘗試取回文字
analysis =res["choices"][0]["text"] 


# === 輸出區塊 ===
print("=== 最新新聞摘要 ===")
print(news_summary if news_summary else "（無最新新聞）")

print("\n=== 技術指標分析 ===")
print(tech_summary)

print("\n=== AI 綜合解讀 ===")
print(analysis)