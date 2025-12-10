import yfinance as yf
import pandas as pd

# 設定投資組合
stocks = ["AAPL", "MSFT", "GOOG", "TSLA"]
weights = [0.25, 0.25, 0.25, 0.25]  # 均等分散

# 抓取過去 6 個月的股價，保留 Adj Close
data = yf.download(stocks, period="6mo", auto_adjust=False)["Adj Close"]

# 計算投資組合的每日報酬
returns = data.pct_change().dropna()
portfolio_return = (returns * weights).sum(axis=1)

# 假設投資本金 100,000
initial_capital = 100000
portfolio_value = (1 + portfolio_return).cumprod() * initial_capital

# 設定停損：若單一股票跌超過 10% 就觸發停損訊號
stop_loss = {}
for stock in stocks:
    max_price = data[stock].cummax()
    drawdown = (data[stock] - max_price) / max_price
    stop_loss_dates = drawdown[drawdown < -0.10].index
    stop_loss[stock] = stop_loss_dates

# 結果輸出
print("投資組合最終價值：", round(portfolio_value.iloc[-1], 2))
for stock, dates in stop_loss.items():
    if len(dates) > 0:
        print(f"{stock} 觸發停損日期：")
        for d in dates:
            print("  -", d.strftime("%Y-%m-%d"))
    else:
        print(f"{stock} 在觀察期間內沒有觸發停損")