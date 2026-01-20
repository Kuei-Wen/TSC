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