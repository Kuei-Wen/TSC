import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import openai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# === 設定 Gemini API ===
# 設定 API Key

# 載入 .env 環境變數（確保你已經在 .env 檔案中設定 OPENAI_API_KEY）
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


llm = OpenAI(temperature=0.9, openai_api_key=OPENAI_API_KEY)

# 2. Create a Prompt Template
# The template will be filled with the variable 'product'
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

# 3. Create a Chain
# The chain links the LLM and the prompt.
chain = LLMChain(llm=llm, prompt=prompt)

# 4. Run the Chain
# We pass the input variable 'product' to the chain.
product_idea = "colorful socks"
response = chain.invoke(product_idea)

print(f"Product Idea: {product_idea}")
print(f"Suggested Company Name: {response['text'].strip()}")

# --- Example with a different input ---
product_idea_2 = "home-baked cookies"
response_2 = chain.invoke(product_idea_2)

print(f"\nProduct Idea: {product_idea_2}")
print(f"Suggested Company Name: {response_2['text'].strip()}")

# 設定 Key
openai.api_key = OPENAI_API_KEY

# 要追蹤的公司
tickers = ["TSLA", "AAPL", "NVDA"]

openai.api_key = OPENAI_API_KEY


# 下載過去 6 個月股價
data = yf.download(tickers, start="2024-01-01", end="2024-08-01")["Close"]

print(data.head())


plt.figure(figsize=(12,6))
for ticker in tickers:
    plt.plot(data.index, data[ticker], label=ticker)

# 標題與標籤使用中文字體
plt.title("多公司股價對比", fontproperties=font_prop, fontsize=16)
plt.xlabel("日期", fontproperties=font_prop)
plt.ylabel("收盤價 (USD)", fontproperties=font_prop)
plt.legend(prop=font_prop)  # 圖例也套用中文字體
plt.show()


# 下載成交量資料
volume_data = yf.download(tickers, start="2024-01-01", end="2024-08-01")["Volume"]

plt.figure(figsize=(12,6))
for ticker in tickers:
    plt.plot(volume_data.index, volume_data[ticker], label=ticker)

# 套用中文字體
plt.title("多公司成交量對比", fontproperties=font_prop, fontsize=16)
plt.xlabel("日期", fontproperties=font_prop)
plt.ylabel("成交量", fontproperties=font_prop)
plt.legend(prop=font_prop)  # 圖例也套用字體
plt.show()

returns = (data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100
print("各公司漲幅 (%)：\n", returns)

# 丟給 AI 總結




prompt = f"""
以下是三家公司在 2024-01 到 2024-08 的漲幅：
{returns.to_dict()}

請用投資顧問的口吻，分析誰表現最好，誰最需要注意風險，並用 200 字左右說明。
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


# 註冊中文字型 (例如：MSung-Light 或 MHei-Medium)
try:
    pdfmetrics.registerFont(UnicodeCIDFont("MSung-Light"))
    chinese_font = "MSung-Light"
except:
    print("MSung-Light not available, trying MHei-Medium")
    try:
        pdfmetrics.registerFont(UnicodeCIDFont("MHei-Medium"))
        chinese_font = "MHei-Medium"
    except:
        print("Neither MSung-Light nor MHei-Medium are available. Please install a CJK CID font compatible with ReportLab.")
        chinese_font = None


def draw_wrapped_text(c, text, x, y, font_name, font_size, max_width, line_height, page_margin=50):
    """在 PDF 中自動換行並處理翻頁"""
    c.setFont(font_name, font_size)
    lines = []
    current_line = ""

    # Split the text into words or characters to handle wrapping
    # For CJK, character by character might be more appropriate
    words = list(text) # Treat each character as a "word" for wrapping

    for word in words:
        # Check if adding the next word/character exceeds the max width
        if c.stringWidth(current_line + word, font_name, font_size) < max_width:
            current_line += word
        else:
            # If it exceeds, add the current line to the list and start a new line with the current word/character
            lines.append(current_line)
            current_line = word

    # Add the last line
    if current_line:
        lines.append(current_line)

    # Draw the lines
    for line in lines:
        if y < page_margin:  # 如果到頁底，自動換頁
            c.showPage()
            c.setFont(font_name, font_size)
            y = letter[1] - page_margin
        c.drawString(x, y, line)
        y -= line_height
    return y


if chinese_font:
    pdf_file = "multi_stock_report.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # 標題
    c.setFont(chinese_font, 18)
    c.drawString(100, height - 50, "多公司投資報告")

    # 插入數據
    c.setFont(chinese_font, 12)
    y = height - 100

    if 'returns' in globals() and 'response' in globals():
        for company, growth in returns.items():
            c.drawString(100, y, f"{company}: {growth:.2f}%")
            y -= 20

        # AI 分析
        y -= 30
        c.drawString(100, y, "AI 分析：")
        y -= 30

        # 用自動換行函式寫 AI 分析
        y = draw_wrapped_text(
            c,
            response.text,
            x=100,
            y=y,
            font_name=chinese_font,
            font_size=12,
            max_width=width - 200,  # Adjusted max_width to leave more margin
            line_height=18
        )

        c.save()
        print(f"報告已生成：{pdf_file}")
    else:
        print("Required data (returns or response) not found. Please run previous cells.")
else:
    print("Could not find a suitable Chinese font to generate the PDF.")