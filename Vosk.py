import os
import sys
import wave
import json
import subprocess
from vosk import Model, KaldiRecognizer

# --- 設定 ---
# 指向您下載並解壓縮後的 Vosk 模型資料夾
"""
FFmpeg 是一個命令列工具，不是 Python 套件。您需要從官網下載並安裝它。
下載頁面：https://ffmpeg.org/download.html
重要：安裝後，請確保將 ffmpeg 的執行檔路徑加入到您系統的環境變數 PATH 中，這樣 Python 才能在任何路徑下呼叫它。您可以在終端機/命令提示字元中輸入 ffmpeg -version 來測試是否安裝成功。
2. 安裝 Python 的 vosk 套件

pip install vosk
3. 下載 Vosk 語音模型

Vosk 需要一個預先訓練好的模型來進行辨識。請前往 Vosk 模型頁面下載。
模型下載頁面：https://alphacephei.com/vosk/models
為了獲得較好的中文辨識效果，建議下載較大的模型，例如 vosk-model-cn-0.22 (約 1.9 GB) 或更適合台灣口音的 vosk-model-small-tw-rh-0.4 (45MB)。
下載後解壓縮，會得到一個資料夾（例如 vosk-model-cn-0.22），請將這個資料夾與您的 Python 腳本放在同一個目錄下，或在程式碼中指定它的完整路徑。
步驟 2：完整 Python 程式碼
下方是完整的 Python 程式碼。它會自動執行所有步驟：提取音訊 -> 產生 SRT -> 合併影片。

請將此程式碼儲存為 Vosk.py。
"""
MODEL_PATH = "vosk-model-cn-0.22" 
# 每一個字幕塊包含的最大詞語數量
MAX_WORDS_PER_LINE = 15

def format_time(seconds):
    """將秒數轉換為 SRT 的時間格式 (HH:MM:SS,ms)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_rem = seconds % 60
    milliseconds = int((seconds_rem - int(seconds_rem)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds_rem):02},{milliseconds:03}"

def generate_srt(video_file):
    """從影片檔產生 SRT 字幕檔"""
    
    video_basename = os.path.basename(video_file)
    audio_file = f"temp_{video_basename}.wav"
    srt_file = f"{os.path.splitext(video_basename)[0]}.srt"

    # 1. 提取音訊 (使用 FFmpeg)
    # 將影片轉為 16000Hz 單聲道 WAV 格式，這是 Vosk 推薦的格式
    print(f"步驟 1: 從 '{video_file}' 提取音訊...")
    ffmpeg_command = [
        'ffmpeg',
        '-y',  # 覆蓋已存在的檔案
        '-i', video_file,
        '-ar', '16000',  # 設置音訊採樣率為 16000Hz
        '-ac', '1',      # 設置音訊聲道為單聲道
        '-f', 'wav',
        audio_file
    ]
    subprocess.run(ffmpeg_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"音訊已提取至 '{audio_file}'")

    # 2. 語音辨識並產生 SRT 內容
    print("步驟 2: 使用 Vosk 進行語音辨識...")
    if not os.path.exists(MODEL_PATH):
        print(f"錯誤: Vosk 模型資料夾 '{MODEL_PATH}' 不存在。")
        print("請從 https://alphacephei.com/vosk/models 下載模型並放置在正確路徑。")
        sys.exit(1)
        
    model = Model(MODEL_PATH)
    wf = wave.open(audio_file, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)  # 設定為 True 以獲取每個詞的時間戳

    all_words = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if 'result' in result:
                all_words.extend(result['result'])

    final_result = json.loads(rec.FinalResult())
    if 'result' in final_result:
        all_words.extend(final_result['result'])

    wf.close()
    
    # 3. 將辨識結果寫入 SRT 檔案
    print(f"步驟 3: 正在生成 '{srt_file}'...")
    with open(srt_file, 'w', encoding='utf-8') as f:
        subtitle_index = 1
        
        for i in range(0, len(all_words), MAX_WORDS_PER_LINE):
            chunk = all_words[i : i + MAX_WORDS_PER_LINE]
            
            if not chunk:
                continue

            start_time = chunk[0]['start']
            end_time = chunk[-1]['end']
            text = " ".join(word['word'] for word in chunk)
            
            f.write(f"{subtitle_index}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"{text}\n\n")
            subtitle_index += 1
            
    print(f"'{srt_file}' 已成功生成！")
    return audio_file, srt_file

def main(video_file):
    if not os.path.exists(video_file):
        print(f"錯誤: 影片檔案 '{video_file}' 不存在。")
        return

    audio_file, srt_file = None, None
    try:
        # 產生字幕
        audio_file, srt_file = generate_srt(video_file)
        
        # 4. 合併影片與字幕
        output_video_file = f"{os.path.splitext(video_file)[0]}_subtitled.mp4"
        print(f"步驟 4: 正在將字幕合併至 '{output_video_file}'...")

        # -c copy: 直接複製影音流，不重新編碼，速度極快
        # -c:s mov_text: 設置字幕編碼，相容性好
        merge_command = [
            'ffmpeg',
            '-y',
            '-i', video_file,
            '-i', srt_file,
            '-c', 'copy',
            '-c:s', 'mov_text',
            output_video_file
        ]
        subprocess.run(merge_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("🎉 影片與字幕合併完成！")

    except Exception as e:
        print(f"處理過程中發生錯誤: {e}")
        
    finally:
        # 5. 清理暫存檔案
        print("步驟 5: 清理暫存檔案...")
        if audio_file and os.path.exists(audio_file):
            os.remove(audio_file)
            print(f"已刪除暫存音訊檔: '{audio_file}'")
        # 可以選擇保留 srt 檔案或刪除它
        # if srt_file and os.path.exists(srt_file):
        #     os.remove(srt_file)
        #     print(f"已刪除暫存字幕檔: '{srt_file}'")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python create_subtitles.py <您的影片檔案.mp4>")
        sys.exit(1)
        
    video_path = sys.argv[1]
    main(video_path)