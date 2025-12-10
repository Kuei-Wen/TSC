import os
import pandas as pd
import numpy as np
import yfinance as yf
import google.generativeai as genai
from datetime import datetime, timedelta

# 設定 Gemini API Key（建議用環境變數）
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBnIn9k5-O-SaYhvHwWniT5RgsKx26KX54")
genai.configure(api_key=GEMINI_KEY)

MODEL_NAME = "gemini-1.5-flash"  # 速度快、夠便宜

TICKER = "AAPL"        # 例：AAPL / TSLA / 2330.TW
PERIOD = "6mo"         # 過去 6 個月
SHORT_MA = 20
LONG_MA = 60
RSI_PERIOD = 14

df = yf.download(TICKER, period=PERIOD)
if df.empty:
    raise ValueError(f"抓不到 {TICKER} 的資料，請確認代號是否正確。")

# 只留必需欄
price = df["Close"].dropna().copy()

# SMA
sma_short = price.rolling(window=SHORT_MA).mean()
sma_long  = price.rolling(window=LONG_MA).mean()

# RSI (Wilder smoothing)
delta = price.diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.ewm(alpha=1/RSI_PERIOD, adjust=False).mean()
avg_loss = loss.ewm(alpha=1/RSI_PERIOD, adjust=False).mean()

rs = avg_gain / (avg_loss.replace(0, np.nan))
rsi = 100 - (100 / (1 + rs))
rsi = rsi.fillna(50)  # 初期 NaN 給中性值

print(sma_short.tail())
print(sma_long.tail())
# print(rsi.tail())

#產出當下解讀要用的「事實摘要」
latest_date = price.index[-1].strftime("%Y-%m-%d")
last_close  = float(price.iloc[-1])
s_short     = float(sma_short.iloc[-1])
s_long      = float(sma_long.iloc[-1])
rsi_now     = float(rsi.iloc[-1])

# 近 5 日均線斜率（估算趨勢）
def slope(series, lookback=5):
    tail = series.dropna().iloc[-lookback:]
    if len(tail) < lookback:
        return 0.0
    x = np.arange(len(tail))
    A = np.vstack([x, np.ones(len(x))]).T
    m, _ = np.linalg.lstsq(A, tail.values, rcond=None)[0]
    return float(m)

slope_short = slope(sma_short)
slope_long  = slope(sma_long)

# 交叉判斷（近 2 日穿越）
diff_today = float(sma_short.iloc[-1]) - float(sma_long.iloc[-1])
diff_yest  = float(sma_short.iloc[-2]) - float(sma_long.iloc[-2])
cross = "none"

if not np.isnan(diff_today) and not np.isnan(diff_yest):
    if diff_yest <= 0 and diff_today > 0:
        cross = "golden_cross"
    elif diff_yest >= 0 and diff_today < 0:
        cross = "death_cross"


facts = {
    "ticker": TICKER,
    "as_of": latest_date,
    "last_close": round(last_close, 3),
    f"SMA_{SHORT_MA}": round(s_short, 3),
    f"SMA_{LONG_MA}": round(s_long, 3),
    "slope_short": round(slope_short, 5),
    "slope_long": round(slope_long, 5),
    f"RSI_{RSI_PERIOD}": round(rsi_now, 2),
    "ma_cross": cross
}
facts


def humanize_interpretation(f):
    lines = []
    # MA 相對位置
    if f["last_close"] > f[f"SMA_{SHORT_MA}"] > f[f"SMA_{LONG_MA}"]:
        lines.append("價格位於短、長期均線之上，屬於偏多排列。")
    elif f["last_close"] < f[f"SMA_{SHORT_MA}"] < f[f"SMA_{LONG_MA}"]:
        lines.append("價格位於短、長期均線之下，屬於偏空排列。")
    else:
        lines.append("價格與均線多空交錯，短線方向不明確。")

    # 均線斜率
    if f["slope_short"] > 0 and f["slope_long"] > 0:
        lines.append("短長期均線皆上彎，整體趨勢偏多。")
    elif f["slope_short"] < 0 and f["slope_long"] < 0:
        lines.append("短長期均線皆下彎，整體趨勢偏弱。")
    else:
        lines.append("短長期均線方向不一致，留意盤整或轉折。")

    # 交叉
    if f["ma_cross"] == "golden_cross":
        lines.append("出現黃金交叉（短上穿長），常被視為偏多訊號。")
    elif f["ma_cross"] == "death_cross":
        lines.append("出現死亡交叉（短下穿長），常被視為偏空訊號。")

    # RSI
    r = f[f"RSI_{RSI_PERIOD}"]
    if r >= 70:
        lines.append(f"RSI ≈ {r}（偏熱），強勢中但留意回檔風險。")
    elif r <= 30:
        lines.append(f"RSI ≈ {r}（偏冷），超賣中但不等同立刻反彈。")
    else:
        lines.append(f"RSI ≈ {r}（中性區間），動能溫和。")

    return "；".join(lines)

#print("工程師口吻解讀：", humanize_interpretation(facts))

model = genai.GenerativeModel(MODEL_NAME)

prompt = f"""
你是一位投資教練，請把下面的技術指標數據，翻成一般人也能聽懂的「白話解讀」，
限制：避免靠單一指標下結論，提醒可能的誤判與風險，內容 150~250 字，條列 3~5 點重點，最後1行給出「短線觀察重點」。

數據（請勿臆測未提供的值）：
{facts}

可參考但不要直接複製的示意句型：
- 價格與均線的相對位置暗示動能方向，但短期可能出現假突破。
- RSI 進入極值不代表一定反轉，強勢趨勢可能長時間維持高檔。
- 交叉訊號在盤整容易洗刷，建議搭配成交量或風險控管。

請用繁體中文輸出。
"""

try:
    res = model.generate_content(prompt)
    print(res.text)
except Exception as e:
    print("Gemini 呼叫失敗，改用本地解讀：")
    print(humanize_interpretation(facts))