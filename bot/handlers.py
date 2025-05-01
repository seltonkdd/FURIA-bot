from telegram.ext import CommandHandler, ContextTypes
from telegram import Update, MenuButtonCommands

from .utils import (
    get_latest_matches,
    get_lineup,
    get_next_matches,
    get_next_tournaments
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hellooooo')

async def latests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_latest_matches()
    await update.message.reply_text(message, parse_mode='Markdown')

async def lineup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_lineup()
    await update.message.reply_text(message, parse_mode='Markdown')

async def next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_next_matches()
    await update.message.reply_text(message, parse_mode='Markdown')

async def tournaments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_next_tournaments()
    await update.message.reply_text(message, parse_mode='Markdown')


def setup_handler(application):

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ultimas', latests))
    application.add_handler(CommandHandler('equipe', lineup))
    application.add_handler(CommandHandler('proximas', next))
    application.add_handler(CommandHandler('torneios', tournaments))