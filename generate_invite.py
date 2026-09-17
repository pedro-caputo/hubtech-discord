import os
import sys
import discord
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    for guild in client.guilds:
        # Priorizar canal de regras ou apresente-se para chegada
        target_channel = discord.utils.get(guild.channels, name="📌・regras-e-diretrizes") or guild.text_channels[0]
        # max_age=0 significa NUNCA expira, max_uses=0 significa USOS ILIMITADOS
        invite = await target_channel.create_invite(
            max_age=0,
            max_uses=0,
            unique=False,
            reason="Link de Convite Oficial e Permanente da Comunidade HubTech"
        )
        print(f"INVITE_URL: {invite.url}")
    await client.close()

client.run(TOKEN)
