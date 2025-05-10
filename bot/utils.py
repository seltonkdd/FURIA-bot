import json

from .scrappers import get_scrapped
from config import CACHE_FOLDER


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
        except (json.JSONDecodeError, Exception) as e:
            print(f'Error processing the cache... {e}')

    return json_cache


def create_reply_message(api_data, json_key):
    try:
        match json_key:
            case 'latestMatches':
                latest_matches = api_data.get('latestMatches', [])
                if not latest_matches:
                    return 'Nenhuma partida encontrada ‼️'

                message = '🎯 *Partidas anteriores da FURIA:*\n\n'
                for match in latest_matches:
                    opponent = match.get('opponent')
                    score = match.get('score')
                    tournament = match.get('tournament')
                    win = match.get('win')
                    date = match.get('date')
                    symbol = '✔️' if win == 'true' else '❌'
                    message += (
                        f"🕹️ *{tournament}*\n"
                        f"📆 {date}\n"
                        f"⚔️ *FURIA vs {opponent}*\n"
                        f"🏁 {score}\n"
                        f"Vitória: {symbol}\n\n"
                    )
                return message.strip()

            case 'lineUp':
                lineup = api_data.get('lineUp', [])
                if not lineup:
                    return 'Nenhuma equipe encontrada ‼️'

                message = '👾 *Lineup da FURIA:*\n'
                for team in lineup:
                    for key, members in team.items():
                        message += f'\n🎖️ *{key.upper()}*\n\n'
                        message += '\n'.join(members) + '\n'
                return message.strip()

            case 'nextMatches':
                next_matches = api_data.get('nextMatches', [])
                if not next_matches:
                    return 'Nenhuma partida encontrada ‼️'

                message = '🎯 *Próximas partidas da FURIA:*\n\n'
                for match in next_matches:
                    opponent = match.get('opponent')
                    tournament = match.get('tournament')
                    date = match.get('date')
                    link = match.get('match_link')
                    message += (
                        f"🕹️ *{tournament}*\n"
                        f"📆 {date}\n"
                        f"⚔️ *FURIA vs {opponent}*\n"
                        f"🎥 Link da transmissão: {link}\n\n"
                    )
                return message.strip()

            case 'nextTournaments':
                tournaments = api_data.get('nextTournaments', [])
                if not tournaments:
                    return 'Nenhum torneio encontrado ‼️'

                message = '🏆 *Próximos torneios da FURIA*:\n\n'
                for t in tournaments:
                    message += f"*{t.get('name')}*\n{t.get('date')}\n\n"
                return message.strip()
    except Exception as e:
        return f'{e}'


def get_latest_matches(scheduled=False):
    url = 'https://r.jina.ai/https://draft5.gg/equipe/330-FURIA/resultados'
    cache_file = CACHE_FOLDER + 'latest_matches.json'
    task_context = 'GET_LATEST_MATCHES'
    response = get_scrapped(task_context, cache_file, url=url)
    data = fetch_local_cache(data=response, json_file=cache_file)
    if data and not scheduled:
        return create_reply_message(data, 'latestMatches')
    elif data and scheduled:
        return
    elif not data:
        return 'Oops! Something went wrong, try again later'


def get_lineup(scheduled=False):
    cache_file = CACHE_FOLDER + 'lineup.json'
    task_context = 'GET_LINEUP'
    response = get_scrapped(task_context, cache_file)
    data = fetch_local_cache(data=response, json_file=cache_file)
    if data and not scheduled:
        return create_reply_message(data, 'lineUp')
    elif data and scheduled:
        return
    elif not data:
        return 'Oops! Something went wrong, try again later'


def get_next_matches(scheduled=False):
    url = 'https://r.jina.ai/https://draft5.gg/equipe/330-FURIA/proximas-partidas'
    cache_file = CACHE_FOLDER + 'next_matches.json'
    task_context = 'GET_NEXT_MATCHES'
    response = get_scrapped(task_context, cache_file, url=url)
    data = fetch_local_cache(data=response, json_file=cache_file)
    if data and not scheduled:
        return create_reply_message(data, 'nextMatches')
    elif data and scheduled:
        return
    elif not data:
        return 'Oops! Something went wrong, try again later'


def get_next_tournaments(scheduled=False):
    url = 'https://r.jina.ai/https://draft5.gg/equipe/330-FURIA/campeonatos'
    cache_file = CACHE_FOLDER + 'next_tournaments.json'
    task_context = 'GET_NEXT_TOURNAMENTS'
    response = get_scrapped(task_context, cache_file, url=url)
    data = fetch_local_cache(data=response, json_file=cache_file)
    if data and not scheduled:
        return create_reply_message(data, 'nextTournaments')
    elif data and scheduled:
        return
    elif not data:
        return 'Oops! Something went wrong, try again later'
