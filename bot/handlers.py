from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from .utils import (
    get_latest_matches,
    get_lineup,
    get_next_matches,
    get_next_tournaments
)

from config import ID_FILE

start_message = '''*SEJA BEM VINDO AO FURIA BOT* ✨ !!!\n\n
O mais famoso bot de informações do seu time de CS favorito 🕹️😍\n
Aperte "MENU" para mostrar o menu de comandos.'''

menu_message = '''ESCOLHA UMA DAS SEGUINTES OPÇÕES:\n\n
*PARTIDAS RECENTES* - Mostra as 5 ultimas partidas da equipe!\n\n
*LINEUP* - Mostra o time completo da FURIA!\n\n
*PROXIMAS PARTIDAS* - Procura se há partidas marcadas!\n\n
*TORNEIOS* - Procura se há torneios por vir!'''

menu_button = [[InlineKeyboardButton('MENU', callback_data='menu')]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   reply_markup=InlineKeyboardMarkup(menu_button), 
                                   text=start_message, 
                                   parse_mode='Markdown')

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [
        [InlineKeyboardButton('PARTIDAS RECENTES', callback_data='latests')],
        [InlineKeyboardButton('LINEUP', callback_data='lineup')],
        [InlineKeyboardButton('PROXIMAS PARTIDAS', callback_data='next')],
        [InlineKeyboardButton('TORNEIOS', callback_data='tournaments')]
        ]
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   reply_markup=InlineKeyboardMarkup(buttons), 
                                   text=menu_message, 
                                   parse_mode='Markdown')


async def latests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_latest_matches()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   reply_markup=InlineKeyboardMarkup(menu_button),
                                   text=message,
                                   parse_mode='Markdown')

async def lineup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_lineup()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   reply_markup=InlineKeyboardMarkup(menu_button),
                                   text=message,
                                   parse_mode='Markdown')

async def next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_next_matches()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   reply_markup=InlineKeyboardMarkup(menu_button),
                                   text=message,
                                   parse_mode='Markdown')
    
async def tournaments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_next_tournaments()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   reply_markup=InlineKeyboardMarkup(menu_button),
                                   text=message,
                                   parse_mode='Markdown')
    
async def alert_on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = str(update.effective_chat.id)
    with open(ID_FILE, 'r+') as f:
        ids = [line.strip() for line in f if line.strip()]
        if chat_id not in ids:
            f.write(f'{chat_id}\n')

    await context.bot.send_message(chat_id=chat_id, text='_Notificações ativadas!_', parse_mode='Markdown')

async def alert_off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = str(update.effective_chat.id)
    with open(ID_FILE, 'r') as f:
        ids = [line.strip() for line in f if line.strip()]
    if chat_id in ids:
        ids.remove(chat_id)
        with open(ID_FILE, 'w') as f:
            f.writelines(f'{id}\n' for id in ids)

    await context.bot.send_message(chat_id=chat_id, text='_Notificações desativadas!_', parse_mode='Markdown')

async def query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query.data
    if query == 'menu':
        await handle_menu(update, context)
    elif query == 'latests':
        await latests(update, context)
    elif query == 'lineup':
        await lineup(update, context)
    elif query == 'next':
        await next(update, context)
    else:
        await tournaments(update, context)


def setup_handler(application):

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('alert_on', alert_on))
    application.add_handler(CommandHandler('alert_off', alert_off))
    application.add_handler(CallbackQueryHandler(query_handler))
