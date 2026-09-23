# Discord Bot（最小可 Docker 部署示例）

基于 [discord.py](https://discordpy.readthedocs.io/en/stable/) v2 的最小机器人：
支持前缀命令（`!ping`、`!hello`）与 Slash 命令（`/ping`、`/info`），启动时自动同步 slash 命令。
Token 等敏感信息通过 `.env` 注入，**不会**被提交到 git、也不会写入镜像。

## 项目结构

```
├── bot.py              # 机器人主程序
├── requirements.txt    # Python 依赖
├── Dockerfile          # 容器镜像定义
├── docker-compose.yml  # 一键部署
├── .env.example        # 环境变量模板（可提交）
├── .env                # 真实 token（已被 .gitignore 忽略）
└── .gitignore / .dockerignore
```

## 一、创建 Discord 应用

1. 打开 <https://discord.com/developers/applications> → **New Application**
2. 左侧 **Bot** → **Reset Token**，复制 token
3. 同一页面开启 **Privileged Gateway Intents** 中的 **MESSAGE CONTENT INTENT**（本 bot 读取消息内容必需）
4. 左侧 **OAuth2 → URL Generator**：勾选 scope `bot` + `applications.commands`，
   Bot Permissions 至少勾 `Send Messages`、`Read Message History`，
   用生成的 URL 邀请 bot 进你的服务器

## 二、本地运行（不用 Docker）

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # 然后编辑 .env 填入 DISCORD_TOKEN
python bot.py
```

## 三、Docker 部署

```bash
cp .env.example .env      # 填入 DISCORD_TOKEN
docker compose up -d --build    # 构建并后台启动
docker compose logs -f          # 查看日志，看到 "已登录: ..." 即成功
docker compose down             # 停止
```

不使用 compose 的等价命令：

```bash
docker build -t discord-bot .
docker run -d --restart unless-stopped --env-file .env --name discord-bot discord-bot
```

## 四、Portainer 部署（Stacks）

> 注意：`.env` 不会提交到 git，所以 Portainer 从仓库拉代码后目录里没有 `.env`。
> 变量请在 Portainer 界面里配置，compose 已改为 `${VAR}` 插值方式读取。

1. **Stacks → Add stack**，命名如 `discord-bot`
2. Build method 选 **Repository**：
   - Repository: `https://github.com/Wersd234/Deepseek-Harness-Test.git`
   - Branch: `main`
3. 在页面下方的 **Environment variables** 区域添加：
   - `DISCORD_TOKEN` = 你的 bot token（**不要**勾选 "New secret"，普通环境变量即可）
   - `COMMAND_PREFIX` = `!`（可选，不填默认 `!`）
4. **Deploy the stack**
5. 在 Stack 的日志里看到 `已登录: xxx` 与 `已同步 2 个 slash 命令` 即成功
6. 以后更新代码后：进入 Stack → **Re-deploy the stack**（勾选 *Re-pull image and redeploy* 如有）

如果误删了 Stack 里的变量，容器启动会在日志中打印
`缺少 DISCORD_TOKEN：请复制 .env.example 为 .env 并填入 Bot Token`，补上变量重新部署即可。


## 五、命令列表

| 命令 | 类型 | 说明 |
| ---- | ---- | ---- |
| `!ping` / `/ping` | 前缀 / Slash | 返回延迟 |
| `!hello` | 前缀 | 打招呼 |
| `/info` | Slash | 机器人信息（Embed） |

## 安全提示

- `.env` 已在 `.gitignore` / `.dockerignore` 中，**永远不要把真实 token 提交到 git**
- 若 token 泄露，立即到开发者门户 Reset Token
