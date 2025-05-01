from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from .utils import (
    get_latest_matches,
    get_lineup,
    get_next_matches,
    get_next_tournaments
)

start_message = '''*SEJA BEM VINDO AO FURIA BOT* ✨ !!!\n\n
O mais famoso bot de informações do seu time de CS favorito 🕹️😍\n
Aperte "MENU" para mostrar o menu de comandos.'''

menu_message = '''ESCOLHA UMA DAS SEGUINTES OPÇÕES:\n\n
*PARTIDAS RECENTES* - Mostra as 5 ultimas partidas da equipe!\n\n
*LINEUP* - Mostra o time completo da FURIA!\n\n
*PROXIMAS PARTIDAS* - Procura se há partidas marcadas!\n\n
*TORNEIOS* - Procura se há torneios por vir!'''

button = [[InlineKeyboardButton('MENU', callback_data='menu')]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   reply_markup=InlineKeyboardMarkup(button), 
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
                                   reply_markup=InlineKeyboardMarkup(button),
                                   text=message,
                                   parse_mode='Markdown')

async def lineup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_lineup()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   reply_markup=InlineKeyboardMarkup(button),
                                   text=message,
                                   parse_mode='Markdown')

async def next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_next_matches()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   reply_markup=InlineKeyboardMarkup(button),
                                   text=message,
                                   parse_mode='Markdown')
    
async def tournaments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = get_next_tournaments()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   reply_markup=InlineKeyboardMarkup(button),
                                   text=message,
                                   parse_mode='Markdown')

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
    application.add_handler(CallbackQueryHandler(query_handler))
