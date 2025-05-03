from dotenv import load_dotenv
import os

load_dotenv()

ID_FILE = 'alert_on_chats.txt'
TOKEN = os.getenv('TELEGRAM_TOKEN')
CACHE_FOLDER = 'cache/'
