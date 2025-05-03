from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import asyncio
import json

from config import CACHE_FOLDER, ID_FILE


def run_async_job(coroutine, *args):
    asyncio.run(coroutine(*args))


def get_chats_id():
    with open(ID_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]


async def schedule_msg(token, id_list, link):
    from telegram import Bot

    bot = Bot(token=token)
    message = f"""Faltam 15 minutos para a partida da FURIA começar ‼️\n
Link da transmissão: {link}"""

    if id_list is not None:
        for id in id_list:
            await bot.send_message(chat_id=id, text=message)


def job_wrapper(token, link):
    ids = get_chats_id()
    run_async_job(schedule_msg, token, ids, link)


def start_scheduler(token):
    scheduler = BackgroundScheduler(timezone='America/Sao_Paulo')

    try:
        with open(f'{CACHE_FOLDER}next_matches.json', 'r') as f:
            data = json.load(f)

        target_str = data.get('nextMatches')[0]['date'].replace('BRT', '').strip()
        target_date = datetime.strptime(target_str, '%Y/%m/%d - %H:%M')
        notify_time = target_date - timedelta(minutes=15)

        link = data.get('nextMatches')[0]['match_link']
    except:
        return

    scheduler.add_job(
        job_wrapper,
        'cron',
        year=notify_time.year,
        month=notify_time.month,
        day=notify_time.day,
        hour=notify_time.hour,
        minute=notify_time.minute,
        args=[token, link],
    )

    scheduler.start()
