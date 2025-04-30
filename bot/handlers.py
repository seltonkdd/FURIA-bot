from telegram.ext import CommandHandler, ContextTypes
from telegram import Update


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hellooooo')



def setup_handler(application):

    application.add_handler(CommandHandler('start', start))