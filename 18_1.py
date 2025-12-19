# -*- coding: utf-8 -*-
#此部份需在Colab中才能執行,若要顯示需轉成其它的方法
import openai
import yfinance as yf
import pandas as pd
import ta
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os
from dotenv import load_dotenv

# === 設定 Gemini API ===
# 設定 API Key

# 載入 .env 環境變數（確保你已經在 .env 檔案中設定 OPENAI_API_KEY）
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 設定 Key
openai.api_key = OPENAI_API_KEY
my_font = font_manager.FontProperties(fname="NotoSansTC-VariableFont_wght")

# === 抓取台積電股價 ===
ticker = "2330.TW"
tsmc = yf.Ticker(ticker)
data = tsmc.history(period="6mo")

# === 計算均線 ===
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA60'] = data['Close'].rolling(window=60).mean()

# === 畫 K 線圖，回傳 fig 和 axes ===
fig, axes = mpf.plot(
    data,
    type='candle',
    mav=(20, 60),
    volume=True,
    style="yahoo",
    returnfig=True
)

# === 手動加標題（確保用中文字體） ===
axes[0].set_title(f"{ticker} 股價走勢", fontproperties=my_font)

plt.show()



# 取近期數據摘要
recent_data = data.tail(30)[['Close', 'MA20', 'MA60']]

# 組成提示詞
prompt = f"""
以下是台積電最近 30 天的股價數據 (收盤價、20 日均線、60 日均線)：
{recent_data.to_string()}

請用投資新手聽得懂的方式，解讀股價趨勢：
1. 最近股價是否突破均線？
2. 是否有支撐/壓力跡象？
3. 簡單給一個小結論。
"""


res = openai.Completion.create(
    model="gpt-4o-mini",
    prompt=prompt,
    max_tokens=128,
    temperature=0.5,
)

# 嘗試取回文字
analysis =res["choices"][0]["text"] 



print(analysis)