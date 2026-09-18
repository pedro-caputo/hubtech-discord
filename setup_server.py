import os
import sys
import asyncio
import discord
from dotenv import load_dotenv

# Garantir suporte a UTF-8 no Windows Console para emojis
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

ROLES_CONFIG = [
    {"name": "👑 Fundador / ADM", "color": discord.Color.gold(), "hoist": True, "mentionable": True, "admin": True},
    {"name": "🛡️ Moderador", "color": discord.Color.purple(), "hoist": True, "mentionable": True, "admin": False},
    {"name": "🚀 Membro HubTech", "color": discord.Color.blue(), "hoist": False, "mentionable": False, "admin": False},
    {"name": "⚛️ Frontend", "color": discord.Color.from_rgb(0, 210, 211), "hoist": False, "mentionable": True, "admin": False},
    {"name": "⚙️ Backend", "color": discord.Color.from_rgb(29, 209, 161), "hoist": False, "mentionable": True, "admin": False},
    {"name": "📱 Mobile", "color": discord.Color.from_rgb(255, 159, 67), "hoist": False, "mentionable": True, "admin": False},
    {"name": "☁️ DevOps & Cloud", "color": discord.Color.from_rgb(84, 160, 255), "hoist": False, "mentionable": True, "admin": False},
    {"name": "🤖 IA & Dados", "color": discord.Color.from_rgb(95, 39, 205), "hoist": False, "mentionable": True, "admin": False},
    {"name": "🛡️ Cybersecurity", "color": discord.Color.from_rgb(238, 82, 83), "hoist": False, "mentionable": True, "admin": False},
]

STRUCTURE = [
    {
        "category": "🌐 HUBTECH OFICIAL",
        "read_only": True,
        "channels": [
            {"name": "📌・regras-e-diretrizes", "type": "text", "topic": "Diretrizes e conduta da comunidade HubTech"},
            {"name": "📢・avisos-e-novidades", "type": "text", "topic": "Anúncios e novidades oficiais"},
            {"name": "🚀・plataforma-hubtech", "type": "text", "topic": "Link direto para o portal HubTech e atualizações do site"},
            {"name": "🤝・parceiros-vektor", "type": "text", "topic": "Destaque para o Vektor: Currículo inteligente e match de vagas"},
        ]
    },
    {
        "category": "👥 COMUNIDADE & GERAL",
        "read_only": False,
        "channels": [
            {"name": "👋・apresente-se", "type": "text", "topic": "Diga seu nome, stack e o que você está aprendendo!"},
            {"name": "💬・chat-geral", "type": "text", "topic": "Bate-papo livre sobre tecnologia e dia a dia"},
            {"name": "💼・networking", "type": "text", "topic": "Troque LinkedIn, GitHub e conexões profissionais"},
            {"name": "💡・sugestoes-e-ideias", "type": "text", "topic": "Sugira cursos, benefícios, parcerias e melhorias"},
        ]
    },
    {
        "category": "💻 TRILHAS TÉCNICAS",
        "read_only": False,
        "channels": [
            {"name": "⚛️・frontend", "type": "text", "topic": "React, Vue, Next.js, CSS, UI/UX e desenvolvimento web"},
            {"name": "⚙️・backend", "type": "text", "topic": "Node, Python, Java, Go, APIs, bancos de dados e arquitetura"},
            {"name": "📱・mobile", "type": "text", "topic": "Flutter, React Native, Kotlin, Swift e apps"},
            {"name": "☁️・devops-e-cloud", "type": "text", "topic": "Docker, Kubernetes, AWS, Linux, CI/CD e infraestrutura"},
            {"name": "🤖・ia-e-dados", "type": "text", "topic": "Modelos de IA, Data Science, LLMs e Engenharia de Dados"},
            {"name": "🛡️・seguranca-cyber", "type": "text", "topic": "Segurança da informação, autenticação, pentest e boas práticas"},
        ]
    },
    {
        "category": "🚀 PROJETOS & CARREIRA",
        "read_only": False,
        "channels": [
            {"name": "🛠️・showcase-projetos", "type": "text", "topic": "Mostre o que você está desenvolvendo e receba feedback"},
            {"name": "👥・colaboracao-e-equipes", "type": "text", "topic": "Encontre parceiros para projetos, hackathons ou open-source"},
            {"name": "💼・vagas-e-oportunidades", "type": "text", "topic": "Compartilhamento de vagas e oportunidades na área de TI"},
            {"name": "📚・cursos-e-recursos", "type": "text", "topic": "Cursos recomendados, livros, artigos e conteúdos gratuitos"},
        ]
    },
    {
        "category": "🔊 SALAS DE VOZ & COWORKING",
        "read_only": False,
        "channels": [
            {"name": "🎧・Coworking (Foco/Mudo)", "type": "voice", "topic": "Sala de estudo e programação focada"},
            {"name": "☕・Café & Bate-Papo", "type": "voice", "topic": "Conversa livre por áudio"},
            {"name": "🎵・Música & Lo-Fi", "type": "voice", "topic": "Sala para escutar música e codar junto"},
            {"name": "🎙️・Auditório / Apresentações", "type": "voice", "topic": "Workshops, palestras e demonstrações"},
        ]
    },
    {
        "category": "🛡️ STAFF & MODERAÇÃO",
        "private": True,
        "channels": [
            {"name": "📊・triagem-sugestoes", "type": "text", "topic": "Fila de moderação de sugestões e vagas"},
            {"name": "💬・staff-chat", "type": "text", "topic": "Discussão interna da moderação"},
        ]
    }
]

async def setup_guild(guild):
    print(f"=== Iniciando configuração no servidor: {guild.name} (ID: {guild.id}) ===")
    
    # 1. Configurar Cargos
    created_roles = {}
    for role_cfg in ROLES_CONFIG:
        existing = discord.utils.get(guild.roles, name=role_cfg["name"])
        if not existing:
            try:
                perms = discord.Permissions.all() if role_cfg["admin"] else discord.Permissions.none()
                role = await guild.create_role(
                    name=role_cfg["name"],
                    color=role_cfg["color"],
                    hoist=role_cfg["hoist"],
                    mentionable=role_cfg["mentionable"],
                    permissions=perms,
                    reason="Setup automático HubTech"
                )
                print(f"[Cargo Criado] {role.name}")
                created_roles[role_cfg["name"]] = role
            except Exception as e:
                print(f"[Erro ao criar cargo {role_cfg['name']}] {e}")
        else:
            print(f"[Cargo Existente] {existing.name}")
            created_roles[role_cfg["name"]] = existing

    adm_role = created_roles.get("👑 Fundador / ADM")
    mod_role = created_roles.get("🛡️ Moderador")

    # 2. Configurar Categorias e Canais
    channel_map = {}
    for cat_data in STRUCTURE:
        cat_name = cat_data["category"]
        is_private = cat_data.get("private", False)
        is_read_only = cat_data.get("read_only", False)
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        if is_read_only:
            overwrites[guild.default_role] = discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True)
            if adm_role:
                overwrites[adm_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            if mod_role:
                overwrites[mod_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        elif is_private:
            overwrites[guild.default_role] = discord.PermissionOverwrite(read_messages=False)
            if adm_role:
                overwrites[adm_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            if mod_role:
                overwrites[mod_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        category = discord.utils.get(guild.categories, name=cat_name)
        if not category:
            category = await guild.create_category(cat_name, overwrites=overwrites)
            print(f"[Categoria Criada] {category.name}")
        else:
            print(f"[Categoria Existente] {category.name}")

        for ch_data in cat_data["channels"]:
            ch_name = ch_data["name"]
            ch_type = ch_data["type"]
            ch_topic = ch_data.get("topic", "")

            existing_ch = discord.utils.get(category.channels, name=ch_name)
            if not existing_ch:
                if ch_type == "text":
                    channel = await category.create_text_channel(name=ch_name, topic=ch_topic, overwrites=overwrites)
                elif ch_type == "voice":
                    channel = await category.create_voice_channel(name=ch_name, overwrites=overwrites)
                print(f"  [Canal Criado] {channel.name}")
                channel_map[ch_name] = channel
            else:
                print(f"  [Canal Existente] {existing_ch.name}")
                channel_map[ch_name] = existing_ch

    # 3. Postar Embeds Oficiais Iniciais
    print("\n=== Postando Mensagens Oficiais Iniciais ===")
    
    # Canal Regras
    regras_ch = channel_map.get("📌・regras-e-diretrizes")
    if regras_ch:
        msgs = [m async for m in regras_ch.history(limit=1)]
        if len(msgs) == 0:
            embed = discord.Embed(
                title="📜 Diretrizes e Código de Conduta | HubTech",
                description="Bem-vindo(a) à comunidade **HubTech**! Nosso objetivo é criar um ecossistema saudável, colaborativo e de alto nível para desenvolvedores e entusiastas de tecnologia.",
                color=0x00D2D3
            )
            embed.add_field(name="1. Respeito Mútuo", value="Empatia e cordialidade são fundamentais. Toda dúvida é válida, respeite o momento de aprendizado de cada um.", inline=False)
            embed.add_field(name="2. Conteúdo e Canais Corretos", value="Utilize os canais adequados para cada assunto (Frontend, Backend, Mobile, Vagas, etc.). Evite spam e autopromoção desmedida.", inline=False)
            embed.add_field(name="3. Ajuda Construtiva", value="Ao pedir ajuda com código, envie trechos formatados, mensagens de erro e o que você já tentou.", inline=False)
            embed.add_field(name="4. Pirataria e Segurança", value="É proibido compartilhar links de conteúdo pirata, ferramentas maliciosas ou qualquer material ilícito.", inline=False)
            embed.set_footer(text="HubTech • Conectando tecnologia e pessoas")
            await regras_ch.send(embed=embed)
            print("[Embed Enviado] #regras-e-diretrizes")

    # Canal Plataforma HubTech
    hubtech_ch = channel_map.get("🚀・plataforma-hubtech")
    if hubtech_ch:
        msgs = [m async for m in hubtech_ch.history(limit=1)]
        if len(msgs) == 0:
            embed = discord.Embed(
                title="🌐 Conheça a Plataforma HubTech",
                description="O **HubTech** nasce como uma plataforma desenhada para centralizar recursos, trilhas de aprendizado, eventos e projetos do ecossistema tech.",
                color=0x54A0FF
            )
            embed.add_field(name="🚀 Status do Projeto", value="🟡 **Em fase final de preparação para Deploy!**\nAssim que o portal estiver no ar, o link oficial de acesso direto será fixado aqui.", inline=False)
            embed.add_field(name="✨ O que você vai encontrar", value="• Hub de Trilhas de Aprendizado\n• Catálogo de Ferramentas & Recursos\n• Integração com a Comunidade Discord", inline=False)
            embed.set_footer(text="Acesse em breve • hubtech")
            await hubtech_ch.send(embed=embed)
            print("[Embed Enviado] #plataforma-hubtech")

    # Canal Parceiros - Vektor
    vektor_ch = channel_map.get("🤝・parceiros-vektor")
    if vektor_ch:
        msgs = [m async for m in vektor_ch.history(limit=1)]
        if len(msgs) == 0:
            embed = discord.Embed(
                title="🤝 Projeto Parceiro: Vektor",
                description="Apresentamos com muito orgulho o **Vektor**, um projeto parceiro oficial da nossa comunidade!",
                color=0x9B59B6
            )
            embed.add_field(name="🎯 O que é o Vektor?", value="O **Vektor** é uma plataforma inovadora focada em **construção inteligente de currículos** e **match de vagas** sob medida para o perfil de cada profissional de tecnologia.", inline=False)
            embed.add_field(name="💡 Como ele te ajuda?", value="• Criação de currículos otimizados para ATS e recrutadores tech\n• Análise de compatibilidade do seu perfil com vagas do mercado\n• Recomendações de aprimoramento profissional", inline=False)
            embed.add_field(name="🔗 Acompanhe e Apoie", value="Acesse gratuitamente agora mesmo: https://vektor-career.vercel.app
            embed.set_footer(text="Parceria HubTech x Vektor")
            await vektor_ch.send(embed=embed)
            print("[Embed Enviado] #parceiros-vektor")

    # Canal Sugestões
    sugestoes_ch = channel_map.get("💡・sugestoes-e-ideias")
    if sugestoes_ch:
        msgs = [m async for m in sugestoes_ch.history(limit=1)]
        if len(msgs) == 0:
            embed = discord.Embed(
                title="💡 Central de Sugestões & Oportunidades",
                description="Tem sugestão de algum **benefício**, **curso de alto valor**, **parceria** ou **vaga** para compartilhar com a comunidade?",
                color=0x1DD1A1
            )
            embed.add_field(name="Como funciona a triagem?", value="Envie sua ideia aqui detalhando o benefício ou oportunidade. Nossa equipe de moderação fará a revisão para garantir que a comunidade receba sempre conteúdos verificados e de qualidade!", inline=False)
            embed.set_footer(text="Sua contribuição faz o HubTech crescer!")
            await sugestoes_ch.send(embed=embed)
            print("[Embed Enviado] #sugestoes-e-ideias")

    print("\n✅ Configuração do HubTech concluída com sucesso no Discord!")

@client.event
async def on_ready():
    print(f"Bot conectado como: {client.user} (ID: {client.user.id})")
    for guild in client.guilds:
        await setup_guild(guild)
    await client.close()

if __name__ == "__main__":
    if not TOKEN:
        print("Erro: DISCORD_TOKEN não encontrado no .env")
    else:
        client.run(TOKEN)
