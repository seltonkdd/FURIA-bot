import requests
import json

from .scrappers import get_scrapped

CACHE_FOLDER = 'cache/'


def fetch_local_cache(data, json_file: str):
    json_cache = None

    try:
        with open(json_file, 'r') as file:
            json_cache = json.load(file)
            print('fetched local cache')
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f'No local cache found... ({e})')

    if json_cache is None:
        try:
            json_cache = json.loads(data)
            with open(json_file, 'w') as file:
                json.dump(json_cache, file, indent=4)
            print('Local cache stored')
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f'Error processing the cache... {e}')

    return json_cache


def create_reply_message(api_data: dict):
    latest_matches = api_data.get('latestMatches', [])
    lineup = api_data.get('lineUp', [])
    next_matches = api_data.get('nextMatches', [])
    tournaments = api_data.get('nextTournaments', [])

    if latest_matches:
        message = '🎯 *Partidas anteriores da FURIA:*\n\n'
        for matches in latest_matches:
            opponent = matches.get('opponent')
            score = matches.get('score')
            tournament = matches.get('tournament')
            win = matches.get('win')
            date = matches.get('date')

            if win == 'true':
                symbol = '✔️'
            else:
                symbol = '❌'
            message += f"🕹️ *{tournament}*\n 📆 {date}\n ⚔️ *FURIA vs {opponent}*\n 🏁 {score}\n Vitória: {symbol}\n\n"

    return message.strip()


def get_latest_matches():
    cache_file = CACHE_FOLDER + 'latest_matches.json'
    task_context = 'GET_LATEST_MATCHES'
    response = get_scrapped(task_context, cache_file)
    data = fetch_local_cache(data=response, json_file=cache_file)
    if not data:
        data = 'Oops! Something went wrong, try again later'
    return create_reply_message(data)


def get_lineup():
    cache_file = CACHE_FOLDER + 'lineup.json'
    task_context = 'GET_LINEUP'
    response = get_scrapped(task_context, cache_file)
    data = fetch_local_cache(data=response, json_file=cache_file)
    if not data:
        data = 'Oops! Something went wrong, try again later'
    return data

def get_next_matches():
    cache_file = CACHE_FOLDER + 'next_matches.json'
    task_context = 'GET_NEXT_MATCHES'
    response = get_scrapped(task_context, cache_file)
    data = fetch_local_cache(data=response, json_file=cache_file)
    if not data:
        data = 'Oops! Something went wrong, try again later'
    return data

def get_next_tournaments():
    url = 'https://r.jina.ai/https://draft5.gg/equipe/330-FURIA/campeonatos'
    cache_file = CACHE_FOLDER + 'next_tournaments.json'
    task_context = 'GET_NEXT_TOURNAMENTS'
    response = get_scrapped(task_context, cache_file)
    data = fetch_local_cache(data=response, json_file=cache_file, url=url)
    if not data:
        data = 'Oops! Something went wrong, try again later'
    return data
