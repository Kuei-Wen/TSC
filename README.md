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







基於 playwright 的萬用AI爬蟲 Crawl4AI


Playwright + Test Design + AI Agent：自動化測試實戰 系列
https://ithelp.ithome.com.tw/m/users/20169442/ironman/8719


https://playwright.dev/docs/writing-tests

Playwright 玩家攻略：從新手村到魔王關系
https://ithelp.ithome.com.tw/articles/10376953

Google翻譯API
https://ithelp.ithome.com.tw/m/articles/10218704


基本上我們有好幾種方式可以將 *.srt 字幕檔嵌入到字幕中，以下是幾個範例：

將字幕「內嵌」到影片中，並透過影片播放器控制字幕的開關

使用 -c:s mov_text 參數，可以指定將字幕檔的編碼格式為 mov_text，這是 MP4 文件常用的字幕格式。

ffmpeg -i 'video.mp4' -i 'video.zh.srt' -c copy -c:s mov_text 'video.zh.mp4'

這裡兩個 -i 參數都是指定輸入檔路徑，一個為來源影片，一個為來源字幕檔 ，建議用 *.srt 格式。

將字幕「燒錄」到影片中，影片播放器無法控制字幕的開關

使用 -vf "subtitles=subtitle.srt" 可以套用影像過濾器 -vf 來燒錄字幕，直接把指定的字幕檔燒錄到影片上 (關不掉的那種)。

ffmpeg -i 'video.mp4' -vf "subtitles=video.zh_TW.srt" -c:a copy 'output.mp4'

這裡的 subtitle.srt 是指明要使用的字幕檔。而 -c:a copy 則是直接複製 audio 資料流，不做任何編碼。

將字幕「燒錄」到影片中，但可以自訂字幕的顯示樣式

由於 FFmpeg 可以指定的樣式非常多，你幾乎可以調整出任何你想要的字幕樣式，包含文字大小、文字顏色、背景顏色、邊框顏色、邊框寬度、陰影等等，幾乎都可以自訂，功能十分強大。

基本上 FFmpeg 在燒錄字幕時，使用的是 libass 開源套件，所以其實你很難在 FFmpeg Filters Documentation 官方文件找到任何資訊，頂多只能知道有個 force_style 選項可以設定而已。這也是我覺得 FFmpeg 很難上手的其中一個原因，他真的太複雜了。

我最後從 ASS File Format Specification 找到了所有樣式參數的清單，總共有 Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding 共 23 個。這是我找出最權威的資訊來源了！

其實我第一時間不到 10 秒鐘就從 ChatGPT 問到了這 23 種 force_style 可用的選項，但我實在無法判斷他是不是在胡說八道，所以花了十幾分鐘才找到我要的權威資料！😅

以下這組參數是我調整無數次之後覺得最美觀的字幕樣式，但你其實還可以做出許多特殊的調整！

ffmpeg -i video.mp4 -vf "subtitles=video.zh_TW.srt:force_style='PrimaryColour=0xCCCCCC,BackColour=0x000000,OutlineColour=0x000000,BorderStyle=1,Outline=1,Shadow=0,MarginV=10,Fontsize=14'" -c:a copy output.mp4

如果你的影片擁有比較雜亂的畫面，那麼你可以改用以下參數，讓整個字幕套上一個不透明的方框(BorderStyle=3)：

ffmpeg -i video.mp4 -vf "subtitles=video.zh_TW.srt:force_style='PrimaryColour=0xCCCCCC,BackColour=0x000000,OutlineColour=0x000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=10,Fontsize=14'" -c:a copy output.mp4

如果字太小，也可以調整 Fontsize 參數調大字體。

關於常用 force_style 樣式選項的筆記
PrimaryColour：字體顏色

範例: PrimaryColour=0xCCCCCC (淡灰色)

格式: BBGGRR (Blue, Green, Red)

BackColour：這是「字幕邊框」或「陰影」的顏色，但不一定是所謂的「背景色」

範例: BackColour=0x000000 (黑色)

格式: BBGGRR (Blue, Green, Red)

BorderStyle：字幕的外框樣式

BorderStyle 只有兩個選項 1 (文字邊框+陰影) 與 3 (不透明的盒子)

當 BorderStyle=1 時，字幕不會壓上一個大的方框當背景色，而是在「文字」的邊緣劃上一個框，像是替文字描邊線的感覺。這種樣式比較適合影片背景較為乾淨的情況下使用。

當 BorderStyle=3 時，字幕就會壓上一個大大的方框當背景色，文字是放進這個不透明的盒子中，讓字幕可以更清晰的呈現，不受影片背景物件所影響。

Outline：字幕的外框寬度，預設值為 1

Outline 可以設定的值為 0, 1, 2, 3 與 4 這五種。

當 BorderStyle=1 時，這個邊框就是文字的「描邊線」的寬度

當 BorderStyle=3 時，這個邊框就是「盒子」的邊框寬度

OutlineColour：字幕的外框顏色

範例: OutlineColour=0x000000 (黑色)

格式: BBGGRR (Blue, Green, Red)

Shadow：字幕的陰影寬度

當 BorderStyle=1 時，這個 Shadow 就是文字的「描邊線」加上「陰影」的寬度，可以設定的值為 0, 1, 2, 3 與 4 這五種。

字幕的描邊線一定會加上，但看起來像陰影，你如果不要這個描邊線，那就一定要將 Outline 設定為 0

MarginV：字幕的垂直邊距

這個是從螢幕底部往上移動的距離，數字越大，字幕擺放的位置就越高。

Fontsize：字幕的文字大小，預設值為 16

有些時候字幕過長，超出螢幕時，你可以將 Fontsize 將字幕的文字大小調小，這樣就可以讓字幕完全顯示在螢幕上。


如何用FFmpeg合併影片和字幕？
https://magiclen.org/ffmpeg-subtitle/


範例程式
import subprocess
import os
import sys
def validate_file(file_path, file_type="file"):
    """验证文件是否存在"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_type.capitalize()} 文件不存在: {file_path}")
    print(f"{file_type.capitalize()} 已验证: {file_path}")
    return True
def merge_video_with_subtitles(video_path, srt_path, output_path):
    """使用 FFmpeg 将视频与 SRT 字幕合并"""
    # 1. 验证输入文件
    validate_file(video_path, "video")
    validate_file(srt_path, "subtitle")
    # 2. FFmpeg 指令
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', video_path,     # 输入视频
        '-i', srt_path,       # 输入字幕
        '-c:v', 'copy',       # 视频无损copy
        '-c:a', 'copy',       # 音频无损copy
        '-c:s', 'mov_text',   # 字幕转换为 mp4 可识别格式
        '-metadata:s:s:0', 'language=chi',  # 字幕语言设置为中文
        output_path
    ]
    # 强制字幕按 UTF-8 解码（避免乱码）
    ffmpeg_cmd.insert(3, '-sub_charenc')
    ffmpeg_cmd.insert(4, 'UTF-8')
    try:
        # 3. 调用 FFmpeg 进行处理
        result = subprocess.run(
            ffmpeg_cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"成功生成视频: {output_path}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 处理失败: {e.stderr}")
        raise
    except Exception as e:
        print(f"运行 FFmpeg 时发生异常: {e}")
        raise
def main():
    # 输入文件路径（可自行修改）
    video_path = r"SS.online_Gesture Drawing Practice _ 20 and 40 sec. poses_1080p.mp4"
    srt_path = r"SS.online_Gesture Drawing Practice _ 20 and 40 sec. poses_1080p.srt"
    output_path = "output.mp4"
    # 合并视频 + 字幕
    merge_video_with_subtitles(video_path, srt_path, output_path)
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"程序错误: {e}")
        sys.exit(1)
        




