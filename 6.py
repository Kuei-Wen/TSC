import yfinance as yf
import pandas as pd

# 下載台積電ADR的歷史股價
stock = yf.download("TSM", start="2023-01-01", end="2025-01-01")

# 計算移動平均線 (MA)
stock["MA20"] = stock["Close"].rolling(window=20).mean()  # 20日均線
stock["MA60"] = stock["Close"].rolling(window=60).mean()  # 60日均線

# 計算 RSI
def compute_RSI(data, window=14):
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

stock["RSI14"] = compute_RSI(stock, 14)

# 顯示最近幾筆數據
print(stock[["Close", "MA20", "MA60", "RSI14"]].tail(10))
