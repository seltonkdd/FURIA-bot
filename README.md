# FURIA Bot

Esse projeto foi desenvolvido para um desafio técnico da [FURIA](https://www.furia.gg)

A ideia foi desenvolver um bot do telegram em que fãs do time de CS da FURIA possam receber as informações do time e notificações das partidas em tempo real.

# Tecnologias

- [Python](https://www.python.org) - Linguagem principal do projeto
- [JINA IA](https://jina.ai) - Auxílio em scraping
- [GROQ API](https://console.groq.com/home) - Interpretação e via IA

# Implementações

- Raspagem de dados (webscraping) utilizando IA
- Serialização desses dados em formato JSON
- Dados armazenados em cache para melhor performance
- Dados processados e enviados como mensagens no telegram pelo bot

# Funcionalidades

- Lista as partidas mais recentes da FURIA
- Informa a LINEUP completa da FURIA
- Informa as próximas partidas marcadas pela FURIA e disponibiliza links de transmissão
- Procura os proximos torneios que a FURIA irá participar
- Notificações automáticas para fãs que quiserem ser alertados 15 minutos antes da partida começar

# Uso

> ## Pré requisitos

Python 3.10+

#### Clone o projeto:

    git clone https://github.com/seltonkdd/FURIA-bot

Entre no diretório do projeto

#### Instale as dependências:

    pip install -r requirements.txt

#### Configure suas variaveis de ambiente:

Crie um arquivo `.env` e adicione sua chaves privadas da Groq API e o token de bot do telegram (BotFather)

    GROQ_KEY=
    TELEGRAM_TOKEN=

#### Rode no terminal:

    python main.py

#### Alguns exemplos de comandos:
`/start` Da inicio ao bot
`/on` Ativa as notificações automaticas
`/off` Desativa as notificações automáticas

Acesse seu bot e utilze-o
