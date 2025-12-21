from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

UPLOAD_FOLDER = '1HlGWysxjdBaxcLsJOPes5J7PBob90qbP'
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'client_secret.json'  # 金鑰檔案

# 建立憑證
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# 串連服務
service = build('drive', 'v3', credentials=creds)

print("開始上傳檔案...")
file = {'name': "0056.html", 'parents': [UPLOAD_FOLDER]}
file_id1 = service.files().create(body=file).execute()
file = {'name': "0050.html", 'parents': [UPLOAD_FOLDER]}
file_id2 = service.files().create(body=file).execute()
file = {'name': "0056.js", 'parents': [UPLOAD_FOLDER]}
file_id = service.files().create(body=file).execute()
file = {'name': "000.js", 'parents': [UPLOAD_FOLDER]}
file_id4 = service.files().create(body=file).execute()
file_id = (file_id1, file_id2, file_id, file_id4)
print(file_id)   # 印出上傳檔案後的結果
