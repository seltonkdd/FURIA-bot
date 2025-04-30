from telegram.ext import CommandHandler, ContextTypes
from telegram import Update

from .utils import (
    get_latest_matches
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hellooooo')

async def latests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_latest_matches()
    await update.message.reply_text(message, parse_mode='Markdown')


def setup_handler(application):

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('latests', latests))