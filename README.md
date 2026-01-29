
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



ffmpeg 
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


Opencode 
https://learnopencode.com/





