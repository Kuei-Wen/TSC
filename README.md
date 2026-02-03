
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

TypeScript 新手指南
https://willh.gitbook.io/typescript-tutorial

ECMAScript 6.0
https://wangdoc.com/es6/intro

使用 AutoGen 打造多 AI 工作流 — Two-Agent Chat 與 Group Chat
https://myapollo.com.tw/blog/autogen-two-agent-chat-group-chat/#google_vignette


Prompt 学习笔记
https://book.trumandu.top/ai/prompt%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0


使用 Docker 部署 Clawdbot（官方推荐方式）
三、获取 Clawdbot 源码
官方推荐直接从 GitHub 克隆源码：

代码语言：
Bash

自动换行
AI代码解释
git clone https://github.com/clawdbot/clawdbot.git
cd clawdbot
项目目录中已包含：

Dockerfile

docker-compose.yml（官方基础版，仅保证最小可运行）

.env.example

这些文件是 Docker 部署的基础，生产环境建议基于此扩展。

四、配置环境变量
1️⃣ 复制环境变量模板
代码语言：
Bash

自动换行
AI代码解释
# 测试场景
cp .env.example .env

# 生产场景（推荐）
cp .env.example .env.production
# 后续命令需指定 --env-file .env.production
2️⃣ 环境变量模板示例（.env.production.example）
展开
 
代码语言：
TXT

自动换行
AI代码解释
# 基础配置
NODE_ENV=production

# 数据库配置（⚠️ 生产环境必须替换为强密码）
DB_PASSWORD=请替换为随机强密码（长度≥16位，含大小写/数字/特殊符号）
DATABASE_URL=postgresql://clawdbot:${DB_PASSWORD}@db:5432/clawdbot

# Bot / Gateway 配置
BOT_TOKEN=请替换为真实的Bot Token
GATEWAY_PORT=3000

# 日志配置
LOG_LEVEL=info
LOG_DIR=/var/log/clawdbot

# 其他可选配置
WORKER_CONCURRENCY=4
3️⃣ 编辑环境变量文件
根据部署场景填写配置，生产环境务必修改所有默认凭证，并严格限制文件权限：

代码语言：
Bash

自动换行
AI代码解释
# 生产环境文件权限加固
chmod 600 .env.production
⚠️ 重要安全提示：

请勿使用示例中的弱密码，生产环境建议使用随机生成的强密码（长度≥16位，包含大小写字母、数字、特殊符号）

.env / .env.production 文件包含敏感凭证，禁止将其提交到公共代码仓库

企业级部署建议使用 Docker Secret 或第三方密钥管理系统替代环境变量文件

五、构建 Docker 镜像
Clawdbot 官方 Docker 方案 不使用远程镜像仓库，需要在本地构建镜像。

在项目根目录执行：

代码语言：
Bash

自动换行
AI代码解释
docker build -t clawdbot:latest .
构建完成后可通过以下命令确认：

代码语言：
Bash

自动换行
AI代码解释
docker images | grep clawdbot
六、初始化（Onboarding）
在首次运行前，需要执行一次初始化流程（创建数据库结构、基础配置等）。

代码语言：
Bash

自动换行
AI代码解释
# 测试场景
docker compose run --rm clawdbot-cli onboard

# 生产场景
docker compose --env-file .env.production run --rm clawdbot-cli onboard
ℹ️ 关键说明：

该步骤是 首次部署必需 的，成功后会看到初始化完成的提示信息

clawdbot-cli 为官方 docker-compose.yml 中定义的管理服务，用于执行初始化与维护命令

onboard 命令设计为幂等操作，重复执行不会破坏已有数据（仅会校验/补全基础配置）

七、启动 Clawdbot 服务
7.1 测试场景启动（快速体验）
代码语言：
Bash

自动换行
AI代码解释
docker compose up -d
7.2 生产场景启动（推荐配置）
首先创建/修改 docker-compose.prod.yml，补充生产级配置（适配普通 Docker Compose 非 Swarm 模式）：

展开
 
代码语言：
YAML

自动换行
AI代码解释
version: '3.8'

services:
  clawdbot-gateway:
    image: clawdbot:latest
    command: ["gateway"]
    ports:
      - "3000:3000"
    env_file: .env.production
    restart: unless-stopped  # 进程退出时自动重启（生产必需）
    # 健康检查配置（生产必需）
    healthcheck:
      # ⚠️ 以下为示例健康检查路径，请根据 Clawdbot 实际提供的健康接口调整
      # 若官方未提供健康接口，可替换为端口连通性检查：["CMD", "nc", "-z", "localhost", "3000"]
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    # Docker Compose（非 Swarm）资源限制（生产建议）
    cpus: "1.0"
    mem_limit: 1g
    # 日志轮转（生产建议）
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "5"
    volumes:
      - clawdbot-logs:/var/log/clawdbot

  clawdbot-worker:
    image: clawdbot:latest
    command: ["worker"]
    env_file: .env.production
    restart: unless-stopped
    healthcheck:
      # ⚠️ 以下为示例健康检查命令，请根据 Clawdbot 实际情况调整
      test: ["CMD", "node", "-e", "process.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
    # Docker Compose（非 Swarm）资源限制（生产建议）
    cpus: "1.0"
    mem_limit: 512m
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "5"
    volumes:
      - clawdbot-logs:/var/log/clawdbot

  db:
    image: postgres:15-alpine
    env_file: .env.production
    environment:
      - POSTGRES_USER=clawdbot
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=clawdbot
    volumes:
      - clawdbot-db-data:/var/lib/postgresql/data  # 数据持久化卷（生产必需）
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U clawdbot -d clawdbot"]
      interval: 10s
      timeout: 5s
      retries: 5
    # Docker Compose（非 Swarm）资源限制（生产建议）
    cpus: "0.5"
    mem_limit: 512m
    # 生产环境禁止暴露数据库端口到宿主机
    # ports:
    #   - "5432:5432"

volumes:
  clawdbot-db-data:  # 数据库持久化卷（核心，不可随意删除）
  clawdbot-logs:     # 日志持久化卷
ℹ️ 资源限制补充说明：
若使用 Docker Swarm 模式，可替换为以下配置（需删除上述 cpus/mem_limit）：

展开
 
代码语言：
YAML

自动换行
AI代码解释
> deploy:
>   resources:
>     limits:
>       cpus: '1'
>       memory: 1G
> # ⚠️ 注意：deploy.resources 仅在 Docker Swarm 模式下生效
>
启动生产环境服务：

代码语言：
Bash

自动换行
AI代码解释
docker compose -f docker-compose.prod.yml up -d
7.3 查看运行状态
展开
 
代码语言：
Bash

自动换行
AI代码解释
# 测试场景
docker compose ps
docker compose logs -f

# 生产场景
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f
常见服务包括：

clawdbot-gateway（仅该服务需对外暴露）

clawdbot-worker（内部服务，禁止公网访问）

db（数据库服务，禁止公网访问）

八、数据持久化与安全提示
⚠️ 高危提示（生产环境必看）：

PostgreSQL 数据存储在名为 clawdbot-db-data 的 Docker Volume 中，该 Volume 是数据唯一持久化载体

Docker Volume ≠ 备份：Volume 仅保证容器删除后数据不丢失，无法应对磁盘故障、误操作等场景，必须配合定期备份

禁止在生产环境执行 docker compose down -v（-v 参数会删除 Volume，导致数据永久丢失）

如需清理容器，生产环境请执行：docker compose down（仅删除容器，保留 Volume）

九、服务访问与防火墙配置
9.1 访问方式
Gateway 默认监听端口：3000

本地访问示例：http://localhost:3000

服务器访问示例：http://<服务器IP>:3000

9.2 防火墙/安全组配置（生产必需）
仅放行 3000 端口（Clawdbot Gateway），禁止放行 5432 端口（数据库）

建议限制 3000 端口的访问来源（如仅允许企业内网 IP）

云服务器需在厂商控制台配置安全组规则，物理机/虚拟机需配置 iptables/firewalld

十、数据库备份（生产必需）
10.1 手动备份
展开
 
代码语言：
Bash

自动换行
AI代码解释
# 测试场景
docker compose exec db pg_dump -U clawdbot -d clawdbot > clawdbot_backup_$(date +%Y%m%d).sql

# 生产场景
docker compose -f docker-compose.prod.yml exec -T db pg_dump -U clawdbot -d clawdbot > clawdbot_backup_$(date +%Y%m%d_%H%M%S).sql
# 备份文件权限加固
chmod 600 clawdbot_backup_*.sql
10.2 自动备份（推荐）
创建定时任务脚本 backup_clawdbot.sh：

展开
 
代码语言：
Bash

自动换行
AI代码解释
#!/bin/bash
# Clawdbot 数据库自动备份脚本（生产环境）
set -e

# 配置项
BACKUP_DIR="/data/clawdbot/backup"
COMPOSE_FILE="/path/to/clawdbot/docker-compose.prod.yml"
RETENTION_DAYS=7

# 创建备份目录
mkdir -p $BACKUP_DIR

# 执行备份
BACKUP_FILE="$BACKUP_DIR/clawdbot_backup_$(date +%Y%m%d_%H%M%S).sql"
docker compose -f $COMPOSE_FILE exec -T db pg_dump -U clawdbot -d clawdbot > $BACKUP_FILE

# 备份文件权限加固
chmod 600 $BACKUP_FILE

# 保留最近N天备份
find $BACKUP_DIR -name "clawdbot_backup_*.sql" -mtime +$RETENTION_DAYS -delete

# ⚠️ 建议：将备份文件同步至对象存储（OSS/S3/NAS）或异地服务器
# 示例：aws s3 cp $BACKUP_FILE s3://clawdbot-backup/
# 示例：rsync -avz $BACKUP_FILE backup@remote-server:/data/backup/
添加到 crontab（每日凌晨2点备份）：

代码语言：
Bash

自动换行
AI代码解释
chmod +x backup_clawdbot.sh
crontab -e
# 新增一行
0 2 * * * /path/to/backup_clawdbot.sh >> /var/log/clawdbot_backup.log 2>&1
十一、升级与维护
11.1 更新代码
代码语言：
Bash

自动换行
AI代码解释
cd clawdbot
git pull
11.2 重新构建镜像
代码语言：
Bash

自动换行
AI代码解释
docker build -t clawdbot:latest .
11.3 重启服务
展开
 
代码语言：
Bash

自动换行
AI代码解释
# 测试场景
docker compose down
docker compose up -d

# 生产场景
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d
11.4 升级注意事项
⚠️ 风险提示：

升级前必须备份数据库（避免 schema 变更导致数据丢失）

若版本包含数据库结构变更，需确认官方升级指引（部分版本需执行迁移命令）

升级后建议先查看日志，确认无报错后再对外提供服务

十二、架构说明
12.1 测试/单机部署架构
展开
 
代码语言：
TXT

自动换行
AI代码解释
graph TD
    A[用户浏览器/客户端] -->|HTTP :3000| B[clawdbot-gateway\nWeb/API 接入层]
    B -->|内部网络| C[clawdbot-worker\n后台任务处理]
    C -->|SQL| D[PostgreSQL\n数据持久化服务]
    style D fill:#f9f,stroke:#333,stroke-width:2px
    note[Docker Volume: clawdbot-db-data\n数据持久化载体] -.-> D

核心特征：

单 Docker 网络，组件间内部通信

仅 Gateway 暴露端口到外部

数据库数据存储在 Docker Volume 中

12.2 生产级单节点增强架构
展开
 
代码语言：
TXT

自动换行
AI代码解释
graph TD
    A[公网/内网] -->|防火墙/安全组| B[clawdbot-gateway<br/>- restart策略<br/>- 健康检查<br/>- 资源限制]
    B -->|内部Docker网络| C[clawdbot-worker<br/>- 无公网暴露<br/>- 资源限制]
    C -->|SQL| D[PostgreSQL<br/>- Volume持久化<br/>- 定期备份<br/>- 无公网端口]
    E[定时备份脚本<br/>- 权限加固<br/>- 异地存储] -.-> D
    F[日志卷: clawdbot-logs<br/>- 轮转策略<br/>- 权限控制] -.-> B
    F -.-> C
    style B fill:#9ff,stroke:#333,stroke-width:2px
    style D fill:#f9f,stroke:#333,stroke-width:2px
核心增强：

全组件配置重启策略、健康检查、资源限制

日志轮转+持久化，避免磁盘占满

数据库定期备份+权限加固+异地存储建议

Gateway 端口访问来源限制

敏感文件权限严格控制

十三、日志管理（生产建议）
13.1 日志持久化
通过 Docker Volume 将日志挂载到宿主机（已在 docker-compose.prod.yml 中配置），便于集中管理。

13.2 日志接入（企业级）
生产环境建议将日志接入专业日志系统：

ELK Stack（Elasticsearch + Logstash + Kibana）

Loki + Grafana

云厂商日志服务（如阿里云SLS、腾讯云CLS）

配置示例（以 Loki 为例）：

代码语言：
YAML

自动换行
AI代码解释
logging:
  driver: "loki"
  options:
    loki-url: "http://loki:3100/loki/api/v1/push"
    loki-external-labels: "service={{.Name}},env=production"
十四、常见问题说明
Q1：为什么没有 docker pull clawdbot/...？
Clawdbot 官方目前 未发布官方 Docker 镜像，主要原因包括：

配置高度定制化（Token DB Gateway）

避免通用镜像导致安全误用

鼓励用户自行构建、可控部署

Q2：可以自己发布镜像到私有仓库吗？
可以，流程如下：

代码语言：
Bash

自动换行
AI代码解释
docker tag clawdbot:latest registry.example.com/clawdbot:latest
docker push registry.example.com/clawdbot:latest
适合企业内部部署或 CI/CD 使用。

Q3：重复执行 onboard 命令会有风险吗？
不会。onboard 命令设计为幂等操作，重复执行仅会校验已有配置，不会删除/修改业务数据。

Q4：生产环境如何进一步提升安全性？
使用 Docker Secret 或第三方密钥管理系统存储敏感凭证（替代 .env 文件）

为 Gateway 配置 HTTPS（通过 Nginx 反向代理）

限制容器的 Linux 内核能力（capabilities）

使用非 root 用户运行容器

开启 Docker 守护进程的 TLS 认证

Q5：Docker Volume 备份和数据库备份有什么区别？
Docker Volume 备份：对整个数据目录打包，恢复速度快，但占用空间大，无法单表恢复

数据库逻辑备份（pg_dump）：SQL 文本格式，占用空间小，支持精细恢复，是生产环境首选

建议：两者结合使用，Volume 备份用于快速恢复，逻辑备份用于精细恢复和异地容灾

十五、总结
✅ 本文基于 Clawdbot 官方基础配置，补充了生产环境必需的安全、可靠、运维能力，与官方配置无冲突

✅ 测试部署：配置简化，适合功能验证，无需严格资源限制

✅ 单机生产部署：需补充数据持久化、重启策略、健康检查、资源限制、定期备份（核心）

⚠️ 企业级生产：需在单机生产基础上扩展多节点、监控、容灾等能力（本文不覆盖HA/多节点数据库）

❌ Docker Volume 不等于备份，生产环境必须配置定期数据库备份+异地存储

❌ 暂无官方预构建镜像，需自行构建保证配置可控

如需更高级的部署方式（K8s CI/CD 高可用），可在本文单机生产配置基础上进行扩展。

关键点回顾
Docker 环境安装提供两种方式：国内服务器推荐一键脚本（基于官方流程、优化国内访问），直连环境使用官方安装方式；

生产环境需区分 Docker Compose 资源限制参数（非 Swarm 用 cpus/mem_limit，Swarm 用 deploy.resources），并明确标注生效范围；

健康检查路径需标注为示例，避免用户照抄导致容器不健康；

数据库备份需加固权限、建议异地存储，且强调 Docker Volume ≠ 备份；

文档明确声明是“官方基础配置+生产增强”，且不覆盖HA/多节点场景。



WPF
https://youtu.be/lbyID3KXLOU?si=gdMd1V_RD4YU1Zrb





