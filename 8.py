from  openai import OpenAI
import os
from dotenv import load_dotenv

# 載入 .env 環境變數（確保你已經在 .env 檔案中設定 OPENAI_API_KEY）
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# 建立 OpenAI 客戶端
client = OpenAI(api_key=OPENAI_API_KEY)

# 定義 Prompt
client = OpenAI(api_key=OPENAI_API_KEY)
# 定義 Prompt
prompt = "顯示 1 到 10 的數字"

# 調用 OpenAI API 進行對話補全
response = client.responses.create(
    model="gpt-5",
    input =prompt
)
# 解析並輸出 AI 產生的回應
print(response.output_text)