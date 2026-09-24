"""M0 最小 bot：仅 /ping。
- 全部 Privileged Intents 关闭（discord.Intents.default() 不含特权意图）
- 设置 DEV_GUILD_ID 时走 guild 级同步（主文档 §5.4，秒级生效）；未设置则 global 同步（最长 1 小时）
"""
import logging
import os
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DEV_GUILD_ID = int(os.getenv("DEV_GUILD_ID") or 0)

if not TOKEN:
    sys.exit("缺少 DISCORD_TOKEN：请复制 .env.example 为 .env 并填入 Bot Token")

intents = discord.Intents.default()  # 全部 Privileged Intents 关闭
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.tree.command(name="ping", description="测试机器人延迟")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! 延迟 {round(bot.latency * 1000)} ms")


@bot.event
async def setup_hook():
    guild = discord.Object(id=DEV_GUILD_ID) if DEV_GUILD_ID else None
    scope = f"guild {DEV_GUILD_ID}" if guild else "global"
    try:
        if guild:
            bot.tree.copy_global_to(guild=guild)  # 把全局命令拷到 guild 作用域，再 guild 级同步（主文档 §5.4）
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} slash command to {scope}", flush=True)
    except Exception:
        import traceback
        traceback.print_exc()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})", flush=True)


if __name__ == "__main__":
    discord.utils.setup_logging(level=logging.INFO)
    bot.run(TOKEN)
