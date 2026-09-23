"""
最小可 Docker 部署的 Discord Bot
- token 等敏感配置从 .env 读取（python-dotenv）
- 同时支持前缀命令 (!ping / !hello) 与 Slash 命令 (/ping / /info)，
  slash 命令在启动时的 setup_hook 中自动同步（兼容全部 discord.py 2.x）
"""

import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # 读取 .env

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("COMMAND_PREFIX", "!")

if not TOKEN:
    raise SystemExit("缺少 DISCORD_TOKEN：请复制 .env.example 为 .env 并填入 Bot Token")

# 意图：default() 已包含 guilds 等；读取消息内容必须显式开启 message_content，
# 并且要在 Discord 开发者门户 (https://discord.com/developers/applications) 里同步打开
intents = discord.Intents.default()
intents.message_content = True


class Bot(commands.Bot):
    """启动时自动同步 slash 命令的 Bot。"""

    async def setup_hook(self) -> None:
        # 全局同步，约 1 秒生效；如需仅测试服务器可传 guild=...
        synced = await self.tree.synchronize()
        print(f"已同步 {len(synced)} 个 slash 命令")


bot = Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"已登录: {bot.user} (ID: {bot.user.id})")
    print(f"所在服务器数: {len(bot.guilds)}")


# ---------- 前缀命令 ----------

@bot.command(help="测试机器人延迟")
async def ping(ctx: commands.Context):
    latency_ms = round(bot.latency * 1000)
    await ctx.send(f"Pong! 延迟 {latency_ms} ms")


@bot.command(help="打招呼")
async def hello(ctx: commands.Context):
    await ctx.send(f"你好, {ctx.author.mention}!")


# ---------- Slash 命令 ----------

@bot.tree.command(name="ping", description="测试机器人延迟")
async def ping_slash(interaction: discord.Interaction):
    latency_ms = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! 延迟 {latency_ms} ms")


@bot.tree.command(name="info", description="查看机器人信息")
async def info_slash(interaction: discord.Interaction):
    embed = discord.Embed(title="Bot 信息", color=discord.Color.blurple())
    embed.add_field(name="名称", value=str(bot.user), inline=True)
    embed.add_field(name="服务器数", value=len(bot.guilds), inline=True)
    embed.add_field(name="延迟", value=f"{round(bot.latency * 1000)} ms", inline=True)
    await interaction.response.send_message(embed=embed)


def main():
    discord.utils.setup_logging(level=logging.INFO)
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
