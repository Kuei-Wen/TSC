import translators as ts
import re
import argparse
import os

def translate_srt(input_file, output_file=None, target_language='zh-TW'):
    """
    將 SRT 字幕檔中的文字翻譯成指定語言。

    Args:
        input_file (str): 輸入的 SRT 檔案路徑。
        output_file (str, optional): 輸出的 SRT 檔案路徑。若為 None，則自動生成檔名。
        target_language (str, optional): 目標翻譯語言代碼。預設為 'zh-TW' (繁體中文)。
    """
    if not os.path.exists(input_file):
        print(f"錯誤: 檔案 '{input_file}' 不存在。")
        return

    # 如果未指定輸出檔名，則自動生成
    if output_file is None:
        basename, ext = os.path.splitext(input_file)
        output_file = f"{basename}_{target_language}{ext}"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用正規表達式來匹配字幕塊，這樣更穩健
        # (字幕序號)\n(時間 --> 時間)\n(字幕內容)
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n([\s\S]*?(?=\n\n|\Z))', re.MULTILINE) 
        
        subtitle_blocks = pattern.findall(content)
        
        translated_content = ""
        total_blocks = len(subtitle_blocks)

        print(f"開始翻譯 '{input_file}'，共 {total_blocks} 個字幕塊...")

        for i, (index, timestamp, text) in enumerate(subtitle_blocks):
            # 去除文字中的HTML標籤 (例如 <i>, <b>)
            text_to_translate = re.sub(r'<.*?>', '', text)
            
            if text_to_translate.strip():
                # 執行翻譯
                translated_text = ts.translate_text(text_to_translate, to_language=target_language)
            else:
                translated_text = "" # 如果原文為空，則不需翻譯

            # 將翻譯好的內容組合回 SRT 格式
            translated_content += f"{index}\n{timestamp}\n{translated_text}\n\n"
            
            # 顯示進度
            print(f"進度: {i + 1}/{total_blocks}", end='\r')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"\n🎉 翻譯完成！已儲存至 '{output_file}'")

    except Exception as e:
        print(f"\n翻譯過程中發生錯誤: {e}")
        print("請檢查您的網路連線，或嘗試更新 'translators' 函式庫: pip install -U translators")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="翻譯 SRT 字幕檔的工具。")
    parser.add_argument("input_file", help="要翻譯的來源 SRT 檔案路徑 (例如 'my_video.srt')。")
    parser.add_argument("-o", "--output_file", help="指定翻譯後輸出的檔案路徑 (可選)。")
    parser.add_argument("-lang", "--language", default='zh-TW', help="目標語言代碼，預設為 'zh-TW' (繁體中文)。")

    args = parser.parse_args()

    translate_srt(args.input_file, args.output_file, args.language)
