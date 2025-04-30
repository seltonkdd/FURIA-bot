import requests

from client import call_model

def get_latest_matches(chunk_size=805):
    url = 'https://r.jina.ai/https://liquipedia.net/counterstrike/FURIA/Matches'

    response = requests.get(url, stream=True)
    response.raise_for_status()
    html_content = ''

    for chunk in response.iter_content(chunk_size=chunk_size):
        html_content += chunk.decode('utf-8')
        break

    user_message = '{"type": "GET_LATEST_MATCHES", "html_content": ' + html_content + '}'
    response = call_model(user_message)

    print(response)

get_latest_matches()