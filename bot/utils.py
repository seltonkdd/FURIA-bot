import requests
import json


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
