import requests
import json

class OllamaAPI:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        
    def generate(self, prompt, model="llama3.2", temperature=0.7):
        """
        使用 Generate API 進行單次問答
        
        Args:
            prompt (str): 問題內容
            model (str): 使用的模型名稱
            temperature (float): 創意程度 (0.0-1.0)
            
        Returns:
            dict: API 回應
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # 檢查 HTTP 錯誤
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 呼叫失敗: {e}")
            return None
            
    def chat(self, messages, model="llama3.2", temperature=0.7):
        """
        使用 Chat API 進行對話
        
        Args:
            messages (list): 對話歷史列表
            model (str): 使用的模型名稱
            temperature (float): 創意程度 (0.0-1.0)
            
        Returns:
            dict: API 回應
        """
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 呼叫失敗: {e}")
            return None

def main():
    # 初始化 API 客戶端
    client = OllamaAPI()
    
    print("=== Generate API 測試 ===")
    # 測試 Generate API
    generate_response = client.generate(
        prompt="請用中文解釋什麼是人工智慧，並列出三個應用領域。",
        temperature=0.7
    )
    
    if generate_response:
        print("\n問題: 請用中文解釋什麼是人工智慧，並列出三個應用領域。")
        print(f"回答: {generate_response['response']}\n")
    
    print("\n=== Chat API 測試 ===")
    # 測試 Chat API
    messages = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！很高興見到你。我能幫你什麼忙嗎？"},
        {"role": "user", "content": "請解釋什麼是機器學習，並舉一個實際應用的例子。"}
    ]
    
    chat_response = client.chat(messages=messages)
    
    if chat_response:
        print("\n對話歷史:")
        for msg in messages:
            print(f"{msg['role']}: {msg['content']}")
        print(f"\nAI回答: {chat_response['message']['content']}")

if __name__ == "__main__":
    main()