from telegram.ext import ApplicationBuilder

from dotenv import load_dotenv
import os

from bot.handlers import setup_handler

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')

app = ApplicationBuilder().token(TOKEN).build()
setup_handler(app)

if __name__ == '__main__':
    print('Bot iniciado...')
    app.run_polling()