from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import asyncio
import json
import os

from config import CACHE_FOLDER, ID_FILE
from .utils import (
    get_latest_matches,
    get_lineup,
    get_next_matches,
    get_next_tournaments
)


def run_async_job(coroutine, *args):
    asyncio.run(coroutine(*args))


def get_chats_id():
    with open(ID_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]
    

def get_match_date():
    try:
        with open(f'{CACHE_FOLDER}next_matches.json', 'r') as f:
            data = json.load(f)

        if data.get('nextMatches'):
            target_str = data.get('nextMatches')[0]['date'].replace('BRT', '').strip()
            target_date = datetime.strptime(target_str, '%Y/%m/%d - %H:%M')
            notify_time = target_date - timedelta(minutes=15)
            link = data.get('nextMatches')[0]['match_link']

            return notify_time, link

    except FileNotFoundError:
        return None, None
    

def delete_cache_files():
    cache_files = os.listdir(CACHE_FOLDER)
    if not cache_files:
        return
    for file in cache_files:
        os.remove(CACHE_FOLDER + file)


def create_cache_files():
    get_latest_matches(scheduled=True)
    get_lineup(scheduled=True)
    get_next_matches(scheduled=True)
    get_next_tournaments(scheduled=True)


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


def update_job(scheduler, token):
    notify_time, link = get_match_date()
    if notify_time and link:
        scheduler.remove_job('job_wrapper') if scheduler.get_job('job_wrapper') else None

        scheduler.add_job(
            job_wrapper,
            'date',
            run_date=notify_time,
            args=[token, link],
            id='job_wrapper'
        )


def start_scheduler(token):
    scheduler = BackgroundScheduler(timezone='America/Sao_Paulo')
    
    scheduler.add_job(
        delete_cache_files,
        'cron',
        hour=1,
        minute=0,
        id='delete_cache_files'
    )

    scheduler.add_job(
        create_cache_files,
        'cron',
        hour=1,
        minute=5,
        id='create_cache_files'
    )

    scheduler.add_job(
        update_job,
        'cron',
        hour=1,
        minute=10,
        args=[scheduler, token],
        id='update_job'
    )

    scheduler.start()
    print('Scheduler iniciado...')
