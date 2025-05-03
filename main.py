from telegram.ext import ApplicationBuilder

import os

from config import ID_FILE, TOKEN, CACHE_FOLDER
from bot.handlers import setup_handler

app = ApplicationBuilder().token(TOKEN).build()
setup_handler(app)
        
if __name__ == '__main__':
    if not os.path.exists(CACHE_FOLDER):
        os.mkdir(CACHE_FOLDER)
    if not os.path.exists(ID_FILE):
        with open(ID_FILE, 'w') as f:
            f.write('')

    print('Bot iniciado...')

    app.run_polling()
