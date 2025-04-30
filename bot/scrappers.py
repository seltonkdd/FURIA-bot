import requests
import os
from bs4 import BeautifulSoup

from client import call_model
from utils import fetch_local_cache

CACHE_FOLDER = 'cache/'
URL = 'https://r.jina.ai/https://draft5.gg/equipe/330-FURIA'


def get_scrapped(context, cache_file, url=URL):
    response = None

    if not os.path.exists(cache_file):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        md_content = response.content.decode('utf-8')

        user_message = '{"type": ' + context + ', "md_content": ' + md_content + '}'
        response = call_model(user_message)
        response = response.replace('`', '').replace('json', '')

    data = fetch_local_cache(data=response, json_file=cache_file)
    if not data:
        data = 'Oops! Something wnt wrong, try again later'
        print(data)


def get_latest_matches():
    cache_file = CACHE_FOLDER + 'latest_matches.json'
    task_context = 'GET_LATEST_MATCHES'
    get_scrapped(task_context, cache_file)


def get_lineup():
    cache_file = CACHE_FOLDER + 'lineup.json'
    task_context = 'GET_LINEUP'
    get_scrapped(task_context, cache_file)


def get_next_matches():
    cache_file = CACHE_FOLDER + 'next_matches.json'
    task_context = 'GET_NEXT_MATCHES'
    get_scrapped(task_context, cache_file)

def get_next_tournaments():
    url = URL + '/campeonatos'
    cache_file = CACHE_FOLDER + 'next_tournaments.json'
    task_context = 'GET_NEXT_TOURNAMENTS'
    get_scrapped(task_context, cache_file, url=url)


get_next_tournaments()