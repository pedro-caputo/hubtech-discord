import os
import sys
import asyncio
import discord
from discord.ext import commands
from discord import ui
from dotenv import load_dotenv
from aiohttp import web

# Configuração de UTF-8 no Windows Console para suportar emojis sem travar
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

# --- SERVIDOR WEB LEVE PARA MONITORAMENTO / CLOUD (RENDER HEALTH CHECK) ---
async def start_health_server():
    app = web.Application()
    async def ping(request):
        return web.Response(text="HubTech Bot 24/7 is Online and Healthy! 🚀")
    app.router.add_get("/", ping)
    app.router.add_get("/health", ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Servidor Web de Health Check ativo na porta {port}")

class HubTechBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Iniciar health check na nuvem
        asyncio.create_task(start_health_server())
        # Registrar views persistentes para funcionarem mesmo após reinicialização
        self.add_view(RoleSelectView())
        self.add_view(SuggestionView())
        self.add_view(ModerationView())

bot = HubTechBot()

# --- 1. CARGOS POR BOTÕES (INTERAÇÃO PERSISTENTE) ---
async def toggle_role(interaction: discord.Interaction, role_name: str):
    role = discord.utils.get(interaction.guild.roles, name=role_name)
    if not role:
        await interaction.response.send_message(f"Cargo `{role_name}` não encontrado.", ephemeral=True)
        return
    member = interaction.user
    if role in member.roles:
        await member.remove_roles(role)
        await interaction.response.send_message(f"❌ Cargo **{role_name}** removido do seu perfil.", ephemeral=True)
    else:
        await member.add_roles(role)
        await interaction.response.send_message(f"✅ Cargo **{role_name}** adicionado ao seu perfil!", ephemeral=True)

class RoleSelectView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Frontend", style=discord.ButtonStyle.primary, emoji="⚛️", custom_id="role_btn_frontend")
    async def frontend_btn(self, interaction: discord.Interaction, button: ui.Button):
        await toggle_role(interaction, "⚛️ Frontend")

    @ui.button(label="Backend", style=discord.ButtonStyle.success, emoji="⚙️", custom_id="role_btn_backend")
    async def backend_btn(self, interaction: discord.Interaction, button: ui.Button):
        await toggle_role(interaction, "⚙️ Backend")

    @ui.button(label="Mobile", style=discord.ButtonStyle.secondary, emoji="📱", custom_id="role_btn_mobile")
    async def mobile_btn(self, interaction: discord.Interaction, button: ui.Button):
        await toggle_role(interaction, "📱 Mobile")

    @ui.button(label="DevOps & Cloud", style=discord.ButtonStyle.primary, emoji="☁️", custom_id="role_btn_devops")
    async def devops_btn(self, interaction: discord.Interaction, button: ui.Button):
        await toggle_role(interaction, "☁️ DevOps & Cloud")

    @ui.button(label="IA & Dados", style=discord.ButtonStyle.secondary, emoji="🤖", custom_id="role_btn_ia")
    async def ia_btn(self, interaction: discord.Interaction, button: ui.Button):
        await toggle_role(interaction, "🤖 IA & Dados")

    @ui.button(label="Cybersecurity", style=discord.ButtonStyle.danger, emoji="🛡️", custom_id="role_btn_cyber")
    async def cyber_btn(self, interaction: discord.Interaction, button: ui.Button):
        await toggle_role(interaction, "🛡️ Cybersecurity")


# --- 2. MODAIS E TRIAGEM DE SUGESTÕES & VAGAS ---
async def send_to_moderation(interaction: discord.Interaction, category_type: str, title: str, link: str, details: str):
    guild = interaction.guild
    triagem_ch = discord.utils.get(guild.channels, name="📊・triagem-sugestoes")
    
    if not triagem_ch:
        await interaction.response.send_message("Canal de triagem não encontrado. Avise a moderação.", ephemeral=True)
        return

    embed = discord.Embed(
        title=f"Nova Submissão: {title}",
        description=details,
        color=0xF1C40F
    )
    embed.add_field(name="📌 Categoria", value=category_type, inline=True)
    embed.add_field(name="👤 Enviado por", value=interaction.user.mention, inline=True)
    if link and link.strip():
        embed.add_field(name="🔗 Link Informado", value=link, inline=False)
    embed.set_footer(text=f"Tipo: {category_type} | ID Autor: {interaction.user.id}")

    await triagem_ch.send(embed=embed, view=ModerationView())
    await interaction.response.send_message(
        "✨ **Sua sugestão foi enviada com sucesso para a moderação!**\n"
        "Assim que revisada por nossa equipe, ela será publicada no canal correspondente. Obrigado por fortalecer o HubTech! 🚀",
        ephemeral=True
    )

class CourseModal(ui.Modal, title="Sugerir Benefício ou Curso"):
    course_title = ui.TextInput(label="Título / Nome do Curso ou Benefício", placeholder="Ex: Imersão Go / Desconto Alura", max_length=100)
    link = ui.TextInput(label="Link de Acesso", placeholder="https://...", max_length=200, required=False)
    details = ui.TextInput(label="Detalhes / Por que vale a pena?", style=discord.TextStyle.paragraph, placeholder="Descreva brevemente o conteúdo, gratuidade ou detalhes do benefício...")

    async def on_submit(self, interaction: discord.Interaction):
        await send_to_moderation(interaction, "Curso / Benefício", self.course_title.value, self.link.value, self.details.value)

class JobModal(ui.Modal, title="Divulgar Oportunidade ou Vaga"):
    job_title = ui.TextInput(label="Cargo / Título da Vaga", placeholder="Ex: Desenvolvedor React Jr / Estágio Dados", max_length=100)
    company = ui.TextInput(label="Empresa & Modelo de Trabalho", placeholder="Ex: TechCorp • Remoto Brasil", max_length=100)
    link = ui.TextInput(label="Link da Vaga / Inscrição", placeholder="https://linkedin.com/jobs/... ou e-mail", max_length=200)
    details = ui.TextInput(label="Requisitos & Benefícios", style=discord.TextStyle.paragraph, placeholder="Requisitos principais, tecnologias e faixa salarial se souber...")

    async def on_submit(self, interaction: discord.Interaction):
        full_details = f"**Empresa & Modelo:** {self.company.value}\n\n{self.details.value}"
        await send_to_moderation(interaction, "Vaga de TI", self.job_title.value, self.link.value, full_details)

class SuggestionView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Sugerir Benefício / Curso", style=discord.ButtonStyle.primary, emoji="💡", custom_id="btn_sug_curso")
    async def sug_curso(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(CourseModal())

    @ui.button(label="Divulgar Vaga de TI", style=discord.ButtonStyle.success, emoji="💼", custom_id="btn_sug_vaga")
    async def sug_vaga(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(JobModal())

class ModerationView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Aprovar e Publicar", style=discord.ButtonStyle.success, emoji="✅", custom_id="mod_btn_approve")
    async def approve(self, interaction: discord.Interaction, button: ui.Button):
        is_staff = interaction.user.guild_permissions.administrator or any(
            r.name in ["👑 Fundador / ADM", "🛡️ Moderador"] for r in interaction.user.roles
        )
        if not is_staff:
            await interaction.response.send_message("Apenas membros da Staff podem aprovar!", ephemeral=True)
            return

        msg = interaction.message
        if not msg.embeds:
            await interaction.response.send_message("Embed não encontrado.", ephemeral=True)
            return

        orig_embed = msg.embeds[0]
        sub_type = orig_embed.footer.text if orig_embed.footer else ""
        guild = interaction.guild

        if "Vaga" in sub_type:
            target_ch = discord.utils.get(guild.channels, name="💼・vagas-e-oportunidades")
        else:
            target_ch = discord.utils.get(guild.channels, name="📚・cursos-e-recursos")

        if target_ch:
            pub_embed = discord.Embed.from_dict(orig_embed.to_dict())
            pub_embed.color = 0x1DD1A1
            pub_embed.set_footer(text="Aprovado pela Moderação • HubTech Comunidade")
            await target_ch.send(embed=pub_embed)

        orig_embed.color = 0x2ECC71
        orig_embed.title = f"✅ [APROVADO] {orig_embed.title}"
        orig_embed.set_footer(text=f"Aprovado por {interaction.user.display_name}")
        await msg.edit(embed=orig_embed, view=None)
        await interaction.response.send_message(f"✅ Publicado oficialmente em {target_ch.mention if target_ch else 'canal'}!", ephemeral=True)

    @ui.button(label="Recusar", style=discord.ButtonStyle.danger, emoji="❌", custom_id="mod_btn_reject")
    async def reject(self, interaction: discord.Interaction, button: ui.Button):
        is_staff = interaction.user.guild_permissions.administrator or any(
            r.name in ["👑 Fundador / ADM", "🛡️ Moderador"] for r in interaction.user.roles
        )
        if not is_staff:
            await interaction.response.send_message("Apenas membros da Staff podem recusar!", ephemeral=True)
            return

        msg = interaction.message
        if msg.embeds:
            orig_embed = msg.embeds[0]
            orig_embed.color = 0xE74C3C
            orig_embed.title = f"❌ [RECUSADO] {orig_embed.title}"
            orig_embed.set_footer(text=f"Recusado por {interaction.user.display_name}")
            await msg.edit(embed=orig_embed, view=None)
        await interaction.response.send_message("❌ Sugestão recusada e arquivada.", ephemeral=True)


# --- 3. EVENTOS DE BOAS-VINDAS E STARTUP ---
@bot.event
async def on_member_join(member: discord.Member):
    print(f"[Novo Membro] {member.name} ({member.display_name}) entrou no servidor.")
    
    # 1. Atribuir automaticamente o cargo 'Membro HubTech'
    role = discord.utils.get(member.guild.roles, name="🚀 Membro HubTech")
    if role:
        try:
            await member.add_roles(role, reason="Auto-role ao entrar no HubTech")
            print(f"  -> Cargo {role.name} atribuído com sucesso.")
        except Exception as e:
            print(f"  -> Erro ao atribuir cargo: {e}")

    # 2. Publicar mensagem estilizada de boas-vindas no #chat-geral
    welcome_ch = discord.utils.get(member.guild.channels, name="💬・chat-geral")
    regras_ch = discord.utils.get(member.guild.channels, name="📌・regras-e-diretrizes")
    apresente_ch = discord.utils.get(member.guild.channels, name="👋・apresente-se")
    showcase_ch = discord.utils.get(member.guild.channels, name="🛠️・showcase-projetos")
    
    if welcome_ch:
        embed = discord.Embed(
            title=f"🎉 Bem-vindo(a) ao HubTech!",
            description=(
                f"Olá {member.mention}, que honra ter você na nossa comunidade de tecnologia! 🚀\n\n"
                f"**Primeiros passos recomendados:**\n"
                f"• 📜 Dê uma olhada em {regras_ch.mention if regras_ch else '#regras'}\n"
                f"• 🎯 Escolha suas tecnologias e apresente-se em {apresente_ch.mention if apresente_ch else '#apresente-se'}\n"
                f"• 🛠️ Compartilhe o que está construindo em {showcase_ch.mention if showcase_ch else '#showcase-projetos'}\n\n"
                f"Sinta-se em casa para trocar ideias, tirar dúvidas e programar junto!"
            ),
            color=0x00D2D3
        )
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text="HubTech • Conectando tecnologia, projetos e pessoas")
        await welcome_ch.send(content=f"👋 Olá {member.mention}!", embed=embed)


async def setup_interactive_panels(guild):
    print(f"Configurando painéis interativos no servidor: {guild.name}")
    
    # 1. Painel de Cargos em #apresente-se
    apresente_ch = discord.utils.get(guild.channels, name="👋・apresente-se")
    if apresente_ch:
        has_panel = False
        async for m in apresente_ch.history(limit=5):
            if m.author == bot.user and m.components:
                has_panel = True
                break
        if not has_panel:
            embed = discord.Embed(
                title="🎯 Escolha suas Stacks & Interesses",
                description=(
                    "Seja bem-vindo(a)! Clique nos botões abaixo para receber os cargos das tecnologias que você estuda ou trabalha.\n\n"
                    "• Clicar uma vez **adiciona** o cargo ao seu perfil.\n"
                    "• Clicar novamente **remove** o cargo.\n\n"
                    "💬 Aproveite este canal para mandar uma mensagem contando seu nome, o que está aprendendo e quais projetos quer construir!"
                ),
                color=0x54A0FF
            )
            embed.set_footer(text="HubTech • Personalização de Perfil")
            await apresente_ch.send(embed=embed, view=RoleSelectView())
            print("  -> Painel de cargos publicado em #apresente-se")

    # 2. Painel de Sugestões em #sugestoes-e-ideias
    sugestoes_ch = discord.utils.get(guild.channels, name="💡・sugestoes-e-ideias")
    if sugestoes_ch:
        has_panel = False
        async for m in sugestoes_ch.history(limit=5):
            if m.author == bot.user and m.components:
                has_panel = True
                break
        if not has_panel:
            embed = discord.Embed(
                title="💡 Central de Colaboração da Comunidade",
                description=(
                    "Ajude a comunidade HubTech a crescer com conteúdos de qualidade!\n\n"
                    "Clique nos botões abaixo para abrir o formulário correspondente:\n"
                    "• **💡 Sugerir Benefício / Curso:** Indique cursos gratuitos ou com desconto, certificações, livros ou parcerias.\n"
                    "• **💼 Divulgar Vaga de TI:** Compartilhe oportunidades de estágio, júnior, pleno ou sênior.\n\n"
                    "*(Todas as submissões passam por uma triagem rápida da Staff antes de serem publicadas nos canais oficiais).* "
                ),
                color=0x1DD1A1
            )
            embed.set_footer(text="HubTech • Comunidade Colaborativa")
            await sugestoes_ch.send(embed=embed, view=SuggestionView())
            print("  -> Painel de sugestões publicado em #sugestoes-e-ideias")


@bot.event
async def on_ready():
    print(f"🤖 HubTech Bot online como {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a comunidade HubTech 🚀"))
    for guild in bot.guilds:
        await setup_interactive_panels(guild)
    print("Pronto e aguardando novos membros e interações!")

if __name__ == "__main__":
    if not TOKEN:
        print("Erro: DISCORD_TOKEN não encontrado.")
    else:
        bot.run(TOKEN)
