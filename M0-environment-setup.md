# M0 — 环境与凭证

| | |
|---|---|
| 工作量 | 0.5 天 |
| 依赖 | 无 |
| 状态 | ⬜ 未开始 |

## 目标

把「能跑」之前的所有外部依赖一次性搞定：仓库、凭证、Discord 应用、Python 环境。

## 任务清单

- [ ] 初始化 git 仓库，提交 `.gitignore`（至少包含 `.env`、`__pycache__/`、`.venv/`、`data/ptvbot.json`）、`.env.example`、`requirements.txt`（主文档 §7）
- [ ] Discord Developer Portal 创建 Application → Bot，**关闭全部 Privileged Intents**，以 `bot` + `applications.commands` scope 邀请进 dev 测试服
- [ ] 按主文档 §11.1 的 curl 脚本验证 PTV devid / key（返回 5 种 route_type 即有效）
- [ ] `python -m venv .venv && pip install -r requirements.txt`
- [ ] 写一个 10 行的最小 bot（仅 `/ping`），在 dev guild 完成秒级命令同步（主文档 §5.4 的 `DEV_GUILD_ID` 机制）

## 产出

- 可运行的空壳仓库；
- 填好三组凭证的 `.env`（**不入库**）。

## 验收标准（DoD）

- [ ] 测试服里 `/ping` 可用
- [ ] curl 验证通过，返回 5 种 route_type
- [ ] `python bot.py` 启动无报错、日志可见 `Logged in as ...`

## 风险与对策

| 风险 | 对策 |
|---|---|
| PTV key 刚申请可能有激活延迟 | M0 第一件事就验证；不通过当天联系 PTV，不阻塞其余任务 |
| slash 命令同步后测试服看不到 | 确认走的是 dev guild 同步而非 global sync（global 最长 1 小时） |

## 收尾

- [ ] 打 git tag `m0`
- [ ] 更新 [README.md](README.md) 状态表为 ✅
