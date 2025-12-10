import yfinance as yf

# 下載台積電美股 ADR 資料
tsm = yf.Ticker("TSM")

# 抓取基本面資訊
info = tsm.info

# EPS
eps = info.get("trailingEps", "N/A")

# PE
pe = info.get("trailingPE", "N/A")

# 股息殖利率
dividend_yield = info.get("dividendYield", 0)
if dividend_yield:
    dividend_yield = round(dividend_yield * 100, 2)

print("📊 台積電 (TSM) 基本面指標")
print(f"EPS：{eps}")
print(f"PE (本益比)：{pe}")
print(f"殖利率：{dividend_yield}%")