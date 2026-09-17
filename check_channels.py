import os
import sys
import discord
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        print(f"Guild: {guild.name}")
        for ch_name in ["👋・apresente-se", "💡・sugestoes-e-ideias"]:
            ch = discord.utils.get(guild.channels, name=ch_name)
            if ch:
                async for msg in ch.history(limit=2):
                    btn_labels = []
                    for row in msg.components:
                        for comp in getattr(row, "children", []):
                            btn_labels.append(getattr(comp, "label", ""))
                    print(f"[{ch.name}] Msg: '{msg.embeds[0].title if msg.embeds else msg.content}' | Botões: {btn_labels}")
    await client.close()

client.run(TOKEN)
