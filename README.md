# 🚀 HubTech Discord Community & Bot Architecture

Repositório oficial de infraestrutura e automação do servidor Discord da comunidade **HubTech | UNICSUL**.

Este projeto contém tanto o script de provisionamento automatizado de canais, categorias e cargos, quanto o **HubTech Bot**, um assistente contínuo construído em Python (`discord.py`) focado em onboarding de novos membros, moderação interativa e autosserviço de cargos, pronto para rodar **24/7 na nuvem via Render + UptimeRobot**.

---

## 🌟 Visão Geral & Funcionalidades

### 1. 🏗️ Provisionamento Automático de Infraestrutura (`setup_server.py`)
* Criação de **6 categorias temáticas** e **20 canais** (texto e voz) com permissões pré-definidas.
* Configuração automática de canais institucionais de somente-leitura e categoria restrita para a equipe de moderação.
* Criação de **9 cargos** estruturados por hierarquia e stacks técnicas (`Frontend`, `Backend`, `Mobile`, `DevOps & Cloud`, `IA & Dados`, `Cybersecurity`).
* Publicação automática de mensagens institucionais em Embed com diretrizes da comunidade e apresentação de projetos parceiros (como o **Vektor**).

### 2. 🤖 Bot Interativo Contínuo 24/7 (`bot.py`)
* **Auto-Role & Boas-Vindas:** Atribui automaticamente o cargo base aos novos integrantes e dispara uma recepção personalizada no canal geral com foto de perfil e instruções.
* **Catch-up Retroativo:** Mecanismo resiliente que garante a entrega de cargos mesmo se um membro entrar durante reinicializações.
* **Painel de Cargos por Clique (Self-Role):** Interface com botões persistentes em `#apresente-se` para que os membros escolham suas áreas de atuação com um clique.
* **Sistema de Triagem de Vagas e Cursos via Modais:**
  * Formulários pop-up nativos dentro do Discord para envio de sugestões de benefícios/cursos e vagas de tecnologia.
  * Encaminhamento das submissões para um canal privado de moderação (`#triagem-sugestoes`) com botões de aprovação e recusa em tempo real.
  * Publicação automática formatada após a aprovação da Staff.
* **Servidor Web de Monitoramento Embutido:** Servidor leve `aiohttp` escutando a porta `$PORT` para verificações de integridade (Health Check) e integração com serviços de uptime.

---

## 📂 Estrutura do Projeto

```
hubtech-discord/
├── bot.py                # Aplicação contínua do bot (eventos, views persistentes, modais, auto-role e health server)
├── setup_server.py       # Script de provisionamento e layout inicial do servidor
├── generate_invite.py    # Gerador de convites permanentes oficiais da guilda
├── Dockerfile            # Containerização para deploy 24/7 na nuvem (Render)
├── requirements.txt      # Dependências do ecossistema Python
├── .env.example          # Modelo seguro de variáveis de ambiente
└── .gitignore            # Proteção contra vazamento de credenciais e tokens
```

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.11+**
* **discord.py 2.x** (Views persistentes, Modals e Gateway Intents)
* **aiohttp** (Engine assíncrona e servidor de health check para a nuvem)
* **Docker** (Container pronto para deploy contínuo)
* **Render + UptimeRobot** (Arquitetura 24/7 de alta disponibilidade com custo zero)

---

## 🔒 Segurança

As credenciais do bot são gerenciadas exclusivamente através de variáveis de ambiente (`.env`), garantindo que nenhum token de autenticação seja exposto publicamente no repositório.

---

## 👨‍💻 Autor & Concepção

* **Idealização e Gestão:** Pedro H. Caputo ([LinkedIn](https://linkedin.com) • [GitHub](https://github.com/pedro-caputo))
* **Projeto:** Comunidade HubTech | UNICSUL
* **Metodologia:** Desenvolvimento assistido por Inteligência Artificial e automação de código de ponta a ponta.
