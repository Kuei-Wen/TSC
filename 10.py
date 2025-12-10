# 匯入必要套件
import google.generativeai as genai
import yfinance as yf

# 設定 API Key
genai.configure(api_key="AIzaSyBnIn9k5-O-SaYhvHwWniT5RgsKx26KX54")
# 抓取股票基本資料
ticker = yf.Ticker("AAPL")  # 以蘋果公司為例
info = ticker.info

company_info = f"""
公司名稱: {info.get('longName')}
產業: {info.get('industry')}
總部位置: {info.get('city')}, {info.get('country')}
市值: {info.get('marketCap')}
營收: {info.get('totalRevenue')}
員工數: {info.get('fullTimeEmployees')}
"""
print(company_info)


# 準備 Prompt
prompt = f"""
請根據以下資訊，幫我整理出一份投資人友善的公司簡介：
{company_info}
請包含：
1. 公司定位與主要業務
2. 產業背景與競爭力
3. 近期財務狀況摘要
4. 投資人應注意的風險
語氣：清晰、專業，避免過度誇張。
"""

model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content(prompt)
print(response.text)