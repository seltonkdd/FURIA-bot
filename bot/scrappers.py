import requests
import os

from .client import call_model


def get_scrapped(context, cache_file, url):
    response = None

    if not os.path.exists(cache_file):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        md_content = response.content.decode('utf-8')

        user_message = '{"type": ' + context + ', "md_content": ' + md_content + '}'
        response = call_model(user_message)
        response = response.replace('`', '').replace('json', '')

    return response
