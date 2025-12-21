# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import time , logging , os.path
logging.basicConfig(format="%(asctime)s  %(filename)s %(levelname)s,%(message)s",filename=os.path.join(os.getcwd(),'log.log'),level=logging.INFO)
async def send_line_message(token, user_id, message):
    """
    使用 LINE Messaging API 傳送訊息
    :param token: LINE Channel Access Token
    :param user_id: 接收訊息的 User ID
    :param message: 要傳送的訊息內容
    """
    url = "https://api.line.me/v2/bot/message/push"
    headers ={
        "Content-Type": "application/json",
        "Authorization": f'Bearer {token}'
    }
    data = {
        "to": user_id,
        "messages": [
            {
                'type': 'text',
                'text':message
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                logging.info("訊息傳送成功")
            else:
                response_text = await response.text()
                logging.info(f"傳送失敗: {response.status}, {response_text}")

def SendMessage(Message):
    LINE_CHANNEL_ACCESS_TOKEN = "snfnsELXCfUtue+A/h1E02GELqG48el+KD0GhaiTcbYFcgYgk8H4PbSQJk9GN5ZbLhNFI2kluJqdUgqF+TQUKz0i0ta2P3XYoMbo9BF0aReK3mKK4dXm9dBOlwyAbsVvgHsWnqbpOgny2deQv3J4GgdB04t89/1O/w1cDnyilFU= "
    USER_ID = "Uc5b74bad47f1d11b7073788ab9d6e15d"

    # 執行非同步函數
    asyncio.run(send_line_message(LINE_CHANNEL_ACCESS_TOKEN, USER_ID, Message))  
