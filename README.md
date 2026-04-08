
微軟 MVP 的 GitHub Copilot 實戰教學
https://medium.com/@ianchen0119/github-copilot-%E4%BD%BF%E7%94%A8%E6%8A%80%E5%B7%A7-%E6%8C%81%E7%BA%8C%E6%9B%B4%E6%96%B0-cfb2f52ab026



Git 
git fetch --all

git pull --force
git fetch --force
想清理一些不再存在于远程仓库中的分支
git fetch --all --prune


https://www.youtube.com/watch?v=43Swz6stWwc
https://www.youtube.com/watch?v=OBoDchKNKPE



基於 playwright 的萬用AI爬蟲 Crawl4AI

Playwright + Test Design + AI Agent：自動化測試實戰 系列(有BDD和AI的整合)
https://ithelp.ithome.com.tw/m/users/20169442/ironman/8719


https://playwright.dev/docs/writing-tests

Playwright 玩家攻略：從新手村到魔王關系
https://ithelp.ithome.com.tw/articles/10376953

https://medium.com/@sreekanth.parikipandla/automating-wpf-applications-with-flaui-and-reqnroll-in-c-bf6c637f32f2
使用 FlaUI 和 ReqnRoll 在 C# 中自動化 WPF 應用程式
FlaUI
https://github.com/FlaUI/FlaUI
https://www.youtube.com/playlist?list=PLacgMXFs7kl_fuSSe6lp6YRaeAp6vqra9

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




如何用FFmpeg合併影片和字幕？
https://magiclen.org/ffmpeg-subtitle/


Opencode 
OpenCode 
https://github.com/vbgate/learn-opencode
https://learnopencode.com/
https://learnopencode.com/1-start/04g-ollama.html
https://opencode.ai/docs/zh-tw/network/

TypeScript 新手指南
https://willh.gitbook.io/typescript-tutorial

ECMAScript 6.0
https://wangdoc.com/es6/intro

使用 AutoGen 打造多 AI 工作流 — Two-Agent Chat 與 Group Chat
https://myapollo.com.tw/blog/autogen-two-agent-chat-group-chat/#google_vignette


Prompt 学习笔记
https://book.trumandu.top/ai/prompt%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0


Microsoft Speech SDK 
https://github.com/Azure-Samples/cognitive-services-speech-sdk?tab=readme-ov-file
https://learn.microsoft.com/en-us/azure/ai-services/speech-service/quickstarts/setup-platform?tabs=linux%2Cdebian%2Cdotnetcli%2Cjre%2Cmaven%2Cnodejs%2Cmac%2Cpypi&pivots=programming-language-python


WPF
https://youtu.be/lbyID3KXLOU?si=gdMd1V_RD4YU1Zrb


DIY Google Assisant With Raspberry Pi
https://www.youtube.com/shorts/6h46gpdTIno#:~:text=DIY%20Google%20Nest%20Mini%20With%20Raspberry%20Pi,Google%20Assistant%20SDK%20Python%20%7C%20Coders%20Cafe.


實作 WPF 複合控制項
https://learn.microsoft.com/zh-tw/dotnet/desktop/wpf/advanced/walkthrough-hosting-a-wpf-composite-control-in-windows-forms



Google Antigravity：無經驗小白也能做出桌面版應用程式和App
https://vocus.cc/article/6934212afd897800016e3857

使用Antigravity 和Spec-kit 進行規格導向的ADK 代理開發
https://codelabs.developers.google.com/sdd-adk-antigravity?hl=zh_tw#0

[ Google IDE 工具] 藉由 Google Antigravity IDE 工具，來體驗 AI 直接實作個人網站
https://medium.com/@simon3458/google-antigravity-ide-intro-2025-1-e8e6a4675a36

定要學會使用 GitHub spec kit — SDD 規格驅動開發
https://milkmidi.medium.com/ai-%E6%99%82%E4%BB%A3-%E4%B8%80%E5%AE%9A%E8%A6%81%E5%AD%B8%E6%9C%83%E4%BD%BF%E7%94%A8-github-spec-kit-sdd-%E8%A6%8F%E6%A0%BC%E9%A9%85%E5%8B%95%E9%96%8B%E7%99%BC-f2df57cfdf3c



樹莓派 5 打造最強 AI 助理：OpenClaw 安裝、Gemini 模型設定與 Telegram 連動全攻略
https://vanix.github.io/2026/02/openclaw-on-raspberrypi-googleantigravity.html

Google Antigravity IDE 教學
https://luke.ninja/tutorials/antigravity-tutorial-1.html


用 agy-starter 體驗 Rules & Workflows
與其從理論開始，不如直接動手試試。我們準備了一個完整的範例專案 `agy-starter`，讓你邊做邊學。
https://memo.jimmyliao.net/p/antigravity-rules-and-workflows-ai
https://github.com/AgentWorkshop/agy-starter

Google Antigravity 介紹含實作
https://medium.com/@simon3458/google-antigravity-ide-intro-2025-1-e8e6a4675a36

https://www.techbang.com/posts/127856-google-antigravity-n8n-workflow-optimize-debug


龍蝦
https://ohya.co/blog/openclaw-docker-deploy-guide

OpenClaw-AI助手入门教程-Docker+deepseek+飞书+nginx反向代理部署流程1
https://www.ncnynl.com/archives/202602/6875.html


conda
創建環境: conda create -n env_name python==3.X.X
列出環境: conda env list
進入環境: conda activate env_name
離開環境: conda deactivate
刪除環境: conda remove -n env_name --all
安裝包: pip install … or conda install …
列出所有安裝包: pip install or conda install

刪除資料夾
最常用的指令是 rm -rf 資料夾名稱


OneNote MCP 
https://mcp.aibase.com/zh/server/1475585820550504486
https://pgdash.io/blog/rag-with-postgresql.html
https://blog.csdn.net/qq_29929123/article/details/142706895

Visuval Studio Code With Agent Skilkls
https://code.visualstudio.com/docs/copilot/customization/agent-skills