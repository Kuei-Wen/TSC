import moviepy.editor as mp
import whisper
import os
import argparse

def extract_audio(video_path):
    """
    從影片檔案中提取音訊並存成 .wav。

    :param video_path: 影片檔案的路徑
    :return: 音訊檔案的路徑
    """
    try:
        print(f"開始從 {video_path} 提取音訊...")
        video_clip = mp.VideoFileClip(video_path)
        audio_path = os.path.splitext(video_path)[0] + ".wav"
        video_clip.audio.write_audiofile(audio_path)
        print(f"音訊成功儲存至 {audio_path}")
        return audio_path
    except Exception as e:
        print(f"提取音訊時發生錯誤: {e}")
        return None

def transcribe_audio(audio_path, model_size="base"):
    """
    使用 Whisper 模型將音訊檔案轉換為文字。

    :param audio_path: 音訊檔案的路徑
    :param model_size: 要使用的 Whisper 模型大小 (e.g., "tiny", "base", "small", "medium", "large")
    :return: 轉換後的文字，或在錯誤時返回 None
    """
    if not os.path.exists(audio_path):
        print(f"錯誤: 找不到音訊檔案 {audio_path}")
        return None

    try:
        print(f"正在載入 Whisper 模型 ({model_size})...")
        model = whisper.load_model(model_size)
        print("模型載入完成，開始進行語音轉文字...")
        result = model.transcribe(audio_path)
        transcription = result["text"]
        print("語音轉文字完成。")
        return transcription
    except Exception as e:
        print(f"語音轉文字時發生錯誤: {e}")
        return None

def save_text(transcription, video_path):
    """
    將文字儲存到 .txt 檔案中。

    :param transcription: 要儲存的文字
    :param video_path: 原始影片檔案的路徑，用於命名 .txt 檔案
    """
    text_path = os.path.splitext(video_path)[0] + ".txt"
    try:
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(transcription)
        print(f"轉換後的文字已儲存至 {text_path}")
    except Exception as e:
        print(f"儲存文字檔案時發生錯誤: {e}")

def main():
    """
    主函式，用於處理命令列參數並執行整個流程。
    """
    parser = argparse.ArgumentParser(description="將影片檔案的聲音轉換為文字。")
    parser.add_argument("video_path", help="輸入的影片檔案路徑。")
    parser.add_argument("--model", default="base", help="要使用的 Whisper 模型大小 (預設: base)。")
    args = parser.parse_args()

    if not os.path.exists(args.video_path):
        print(f"錯誤: 找不到影片檔案 {args.video_path}")
        return

    # 1. 提取音訊
    audio_path = extract_audio(args.video_path)
    if not audio_path:
        return

    # 2. 轉換音訊為文字
    transcription = transcribe_audio(audio_path, args.model)

    # 3. 儲存文字
    if transcription:
        save_text(transcription, args.video_path)

    # 4. (可選) 刪除暫時的 .wav 檔案
    try:
        os.remove(audio_path)
        print(f"已刪除暫時的音訊檔案: {audio_path}")
    except OSError as e:
        print(f"刪除暫時檔案 {audio_path} 時發生錯誤: {e}")

if __name__ == "__main__":
    main()
