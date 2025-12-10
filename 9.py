from google import genai
import os
google_api_key="AIzaSyBnIn9k5-O-SaYhvHwWniT5RgsKx26KX54"
os.environ["GOOGLE_API_KEY"] = google_api_key
client = genai.Client()

prompt = """
請幫我撰寫一份「分散投資」的分析，要求：
1. 列出至少三個優點
2. 以條列式呈現
3. 適合投資新手閱讀
"""

prompt2 = """
你是一位專業的金融分析師，請撰寫一份「台灣科技股的投資風險分析」。
要求：
1. 先介紹市場背景（半導體、AI、電子零組件的角色）
2. 條列主要風險（如產業競爭、國際局勢、匯率風險）
3. 提供兩個投資建議
4. 內容需專業但一般大學生能看懂
"""

prompt3 = """
請用 JSON 格式輸出「分散投資」的優點，格式如下：
{
  "topic": "",
  "advantages": [
    {"id": 1, "content": ""},
    {"id": 2, "content": ""}
  ]
}
"""




response = client.models.generate_content(
  model='gemini-2.5-flash',
  contents=prompt3,
)
print(response.text) # output is often markdown

