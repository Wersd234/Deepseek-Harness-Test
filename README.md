# ptvbot（M0 环境壳）

基于 [discord.py](https://discordpy.readthedocs.io/en/stable/) v2 的最小机器人壳：仅 `/ping` 一个 slash 命令。
按 M0 要求**关闭全部 Privileged Intents**；设置 `DEV_GUILD_ID` 后 slash 命令秒级同步到 dev 测试服（主文档 §5.4），未设置则走 global 同步（最长 1 小时）。
Token / PTV 凭证通过 `.env` 注入，**不会**被提交到 git、也不会写入镜像。

## 里程碑状态

| 里程碑 | 状态 |
|---|---|
| [M0 — 环境与凭证](M0-environment-setup.md) | 🟡 进行中（代码与环境就绪；凭证填入与 /ping 实测待完成） |

## 项目结构

```
├── bot.py                # M0 最小 bot（仅 /ping）
├── scripts/verify_ptv.py # §11.1 PTV 凭证验证（curl 等价）
├── requirements.txt      # Python 依赖
├── Dockerfile            # 容器镜像定义
├── docker-compose.yml    # 一键部署
├── .env.example          # 环境变量模板（可提交）
├── .env                  # 真实凭证（已被 .gitignore 忽略）
└── .gitignore / .dockerignore
```

## 一、创建 Discord 应用（浏览器操作）

1. 打开 <https://discord.com/developers/applications> → **New Application**
2. 左侧 **Bot** → **Reset Token**，复制 token 填入 `.env` 的 `DISCORD_TOKEN`
3. **Privileged Gateway Intents 全部保持关闭**（本 bot 只读 slash 交互，不需要）
4. 左侧 **OAuth2 → URL Generator**：scope 勾 `bot` + `applications.commands`，
   Permissions 至少勾 `Send Messages`，用生成的 URL 把 bot 邀请进 dev 测试服
5. 客户端 设置 → 高级 → 开发者模式 打开后，右键测试服服务器名 → **复制服务器 ID**，填入 `.env` 的 `DEV_GUILD_ID`

## 二、本地运行

```powershell
python -m venv .venv
.venv\Scripts\activate         # Windows（Linux/macOS: source .venv/bin/activate）
pip install -r requirements.txt
copy .env.example .env         # 然后编辑 .env 填入凭证
python bot.py                  # 看到 "Logged in as ..." 即成功；测试服输入 /ping 验证
.venv\Scripts\python scripts\verify_ptv.py   # 验证 PTV 凭证（应返回 5 种 route_type）
```

## 三、Docker 部署

```bash
cp .env.example .env      # 填入凭证
docker compose up -d --build    # 构建并后台启动
docker compose logs -f          # 查看日志，看到 "Logged in as ..." 即成功
docker compose down             # 停止
```

## 安全提示

- `.env` 已在 `.gitignore` / `.dockerignore` 中，**永远不要把真实 token 提交到 git**
- 若 token 泄露，立即到开发者门户 Reset Token
