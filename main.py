from telegram.ext import ApplicationBuilder
from telegram import Update

import os

from config import *
from bot.handlers import setup_handler
from bot.scheduler import start_scheduler

app = ApplicationBuilder().token(TOKEN).build()
setup_handler(app)

if __name__ == '__main__':
    if not os.path.exists(ID_FILE):
        with open(ID_FILE, 'w') as f:
            f.write('')

    print('Bot iniciado...')
    start_scheduler(TOKEN)
    print('Scheduler rodando...')
    app.run_polling()