import ollama
import requests
import json
import os


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




url = 'http://192.168.31.137:11434/api/chat'
payload = {
    "model": "llama3.2",
    "temperature": 0.6,
    "stream": False,
    "messages": [
        {"role": "system", "content": "You are an AI assistant!"},
        {"role": "user", "content": prompt}
    ]
}

#如果切換成 CPU 這邊會跑很久，大概要 1 分鐘，建議還是用 GPU
response = requests.post(url, json=payload)
message_str = response.content.decode('utf-8')
message_dict = json.loads(message_str)
print(message_dict['message']['content'])
print(response.text) # output is often markdown

