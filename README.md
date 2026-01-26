# 影片聲音轉文字工具

這是一個 Python 程式，可以從影片檔案中提取聲音，並使用 OpenAI 的 Whisper 模型將其轉換為文字稿。

## 功能

1.  從各種常見的影片格式中提取音訊。
2.  將提取出的音訊儲存為 `.wav` 檔案。
3.  使用 `openai-whisper` 套件將 `.wav` 檔案的內容轉換為文字。
4.  將生成的文字稿儲存為與影片同名的 `.txt` 檔案。
5.  自動清理暫時生成的 `.wav` 檔案。

## 安裝與設定

### 1. 前置需求：FFmpeg

`moviepy` 和 `whisper` 都需要 `FFmpeg` 這個強大的多媒體處理工具。請先確保您的系統上已安裝 `FFmpeg`。

- **Windows**:
  1.  從 [FFmpeg 官網](https://ffmpeg.org/download.html) 下載。
  2.  解壓縮後，將其 `bin` 資料夾的路徑新增到系統的 `PATH` 環境變數中。
- **macOS (使用 Homebrew)**:
  ```bash
  brew install ffmpeg
  ```
- **Linux (使用 apt)**:
  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```

您可以透過在終端機執行 `ffmpeg -version` 來確認是否安裝成功。

### 2. 安裝 Python 套件

複製這個專案後，在終端機中執行以下指令來安裝所有必要的 Python 套件：

```bash
pip install -r requirements.txt
```

## 如何使用

在終端機中使用以下指令來執行程式。您需要提供影片檔案的路徑。

```bash
python video_to_text.py [您的影片檔案路徑]
```

**範例:**

```bash
python video_to_text.py "C:\MyVideos\lecture_01.mp4"
```

程式執行後，會在 `C:\MyVideos\` 資料夾下生成一個名為 `lecture_01.txt` 的文字檔案。

### 選擇不同的 Whisper 模型

您可以透過 `--model` 參數來選擇不同大小的 Whisper 模型。模型越大，準確率越高，但需要的計算資源和時間也越多。

可用的模型包括：`tiny`, `base`, `small`, `medium`, `large`。預設為 `base`。

**範例 (使用 small 模型):**

```bash
python video_to_text.py "my_video.mov" --model small
```

微軟 MVP 的 GitHub Copilot 實戰教學
https://medium.com/@ianchen0119/github-copilot-%E4%BD%BF%E7%94%A8%E6%8A%80%E5%B7%A7-%E6%8C%81%E7%BA%8C%E6%9B%B4%E6%96%B0-cfb2f52ab026


https://www.youtube.com/watch?v=43Swz6stWwc
https://www.youtube.com/watch?v=OBoDchKNKPE




下面直接說明如何滿足並理解這個正規表示式：

總覽：它用來匹配一個 SRT 字幕的「一個區塊（block）」，包含三個捕獲群組：序號、時間戳、以及可能跨多行的字幕內容。原串：
re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n([\s\S]*?(?=\n\n|\Z))', re.MULTILINE)

群組解釋：

群組1 (\d+)：匹配字幕的索引數字（例如 1、23），一或多位數字。
群組2 (\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})：嚴格匹配 SRT 時間格式：
時間格式為 HH:MM:SS,mmm --> HH:MM:SS,mmm，每個部分的位數固定（HH/MM/SS 為兩位數，毫秒為三位數）。
群組3 ([\s\S]*?(?=\n\n|\Z))：非貪婪地匹配任意字元（含換行），直到下一個空行（\n\n）或檔案結尾（\Z）。因此字幕內容可以有多行。
正則技巧說明：

使用 [\s\S] 是為了包含換行（因為 . 不會匹配換行，除非用 DOTALL）。
*? 是非貪婪模式，保證每個區塊只匹配到下一個空行而非吃掉更多區塊。
(?=\n\n|\Z) 為正向先行斷言，檢查結尾但不消耗字元（保留空行/結尾讓下一次匹配從正確位置開始）。
re.MULTILINE 在此僅影響 ^/$，該模式本身並未使用 ^/$，但原碼加了這個 flag。
實際要滿足的 SRT 範例（會被此 regex 匹配）：
1
00:00:10,500 --> 00:00:12,000
Hello world.

（空行）

或（多行字幕）
2
00:00:12,100 --> 00:00:14,200
This is line one.
This is line two.

常見問題與改進建議：

Windows 的換行為 \r\n：原式只用 \n，在含 CRLF 的檔案上可能失敗或導致不一致。建議要支援 CRLF，可改為：
r'(\d+)\r?\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\r?\n([\s\S]*?)(?=\r?\n\r?\n|\Z)'
這會接受 \n 或 \r\n。
如果想用 . 來包含換行，另一選擇是使用 re.DOTALL（但需調整邏輯以避免貪婪匹配）。
若字幕檔有不一致空行數或多個連續空行，上面的 lookahead (?=\r?\n\r?\n|\Z) 仍能在遇到第一個空白行時停止；如果有多個空行也 OK。
總結要點（快速檢查清單）：

第一行要是數字（索引）。
第二行要精確符合 HH:MM:SS,mmm --> HH:MM:SS,mmm 格式。
第三行開始為字幕內容，可以有多行，並由一個空白行或檔尾分隔下一個區塊。
若在 Windows 上遇不到匹配，請檢查並改用 \r?\n 或先把檔案 newline 正規化為 \n。
需要我把程式中的 pattern 直接改為支援 CRLF 的版本並跑個小測試嗎？

