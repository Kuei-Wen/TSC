import whisper
import os

"""
取出音訊並跑語音辨識 → 產生 .srt
用 ffmpeg 把 .srt 燒錄到影片
安裝依賴（擇一）

Whisper（推薦）：pip install openai-whisper
ffmpeg：需安裝到系統並加入 PATH（Windows 可用 winget 安裝）
"""

model = whisper.load_model("base")  # 可用 tiny/base/small/medium/large
result = model.transcribe("input.mp4", language="zh")

# 寫出 SRT
def to_srt(segments, path):
    def fmt(ts):
        h = int(ts // 3600)
        m = int(ts % 3600 // 60)
        s = int(ts % 60)
        ms = int((ts - int(ts)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
    with open(path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            f.write(f"{i}\n{fmt(seg['start'])} --> {fmt(seg['end'])}\n{seg['text'].strip()}\n\n")

to_srt(result["segments"], "output.srt")


#用 ffmpeg 燒錄字幕進影片

os.system('ffmpeg -i input.mp4 -vf "subtitles=output.srt:force_style=\'FontName=Arial,FontSize=24\'" -c:a copy output_with_subs.mp4')