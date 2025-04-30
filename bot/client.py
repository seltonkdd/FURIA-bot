from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv('./.env')

GROQ_KEY = os.getenv('GROQ_KEY')

model = Groq(api_key=GROQ_KEY)

def call_model(user_message):
    response_format = {'response_type': 'list_object'}
    messages = [
        {   
            'role': 'system', 'content': '''Voce é um assistente que irá receber um json com uma chave "type" e uma chave "html_content".
            O valor da chave "type" contém o tipo de tarefa que voce irá realizar.
            E o valor da chave "html_content" contém o conteudo html parseado de um site no qual você irá buscar as informações.
            O conteudo do site é informações sobre o time de CS Furia, suas partidas ou sua line-up.
            Você deve responder diretamente apenas o que lhe for atribuido.
            Sua resposta deve ser um JSON.
            Se o "type" for 'GET_LATEST_MATCHES', o response_type deve ser 'latestMatches' e a resposta deve ser uma lista de json com as informações das partidas como data, tier, tipo, torneio participante, oponente e score.

            Exemplo de perguntas:
            {'TYPE': 'GET_LASTEST_MATCH', 'HTML_CONTENT': 'Date  Tier  Type  Tournament  Participant  Score  vs.  Opponent  VOD(s)
            April 9, 2025 - 12:50 UTC+0  S-Tier  OfflinePGL  Bucharest 2025   FURIA   0 : 2    MongolZ'}

            Exemplo de resposta:
            {'latestMatches': [
                {'date': 'April 9, 2025 - 12:50 UTC+0',
                    'tier': 'S-Tier',
                    'type': 'offline',
                    'tournament': 'Bucharest 2025',
                    'opponent': 'MongolZ',
                    'score': '0:2',
                    'win': 'false'}
                    ...
                    ...
                    ...
                    ]
            }
            '''
        },
        {'role': 'user', 'content': user_message}
    ]

    response =  model.chat.completions.create(
        messages=messages,
        response_format=response_format,
        model='llama-3.3-70b-versatile',
        temperature=0.7
    )

    return response.choices[0].message.content