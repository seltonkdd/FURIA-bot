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
            'role': 'system', 'content': '''Voce é um assistente que irá receber um json com uma chave "type" e uma chave "md_content".
            O valor da chave "type" contém o tipo de tarefa que voce irá realizar.
            E o valor da chave "md_content" contém o conteudo html estilizado como markdown de um site no qual você irá buscar as informações.
            O conteudo do site é informações sobre o time de CS Furia, suas partidas ou sua line-up.
            Você deve responder diretamente apenas o que lhe for atribuido.
            Sua resposta deve ser um JSON.

            Se o "type" for 'GET_LATEST_MATCHES', o response_type deve ser 'latestMatches' e a resposta deve ser uma lista de json com as informações das partidas como data, hora, torneio, oponente e score.
            Se o "type" for 'GET_LINEUP', o response_type deve ser 'lineUp' e a resposta deve ser uma lista de json com os nomes dos jogadores.

            Exemplo de perguntas:
            {'type': 'GET_LASTEST_MATCHES', 'md_content': 
            'Resultados
            ----------

            📅 quarta-feira, 9 de abril de 2025

            [09:50 ![Image 8: 330](https://api.draft5.gg/teams/330/logo)FURIA 0 ![Image 9: 2635](https://api.draft5.gg/teams/2635/logo)The MongolZ 2 MD3 PGL Bucharest 2025 Reveja os lances](https://draft5.gg/partida/36342-FURIA-vs-The-MongolZ-PGL-Bucharest-2025)'
            }
            {type': 'GET_LINEUP': 'md_content':
            Line-up Titular
            ---------------

            ![Image 1: KZ](https://static.draft5.gg/assets/flags/KZ.svg)MOLODOY 

            ![Image 2: LV](https://static.draft5.gg/assets/flags/LV.svg)YEKINDAR

            ![Image 3: BR](https://static.draft5.gg/assets/flags/BR.svg)FalleN

            ![Image 4: BR](https://static.draft5.gg/assets/flags/BR.svg)KSCERATO

            ![Image 5: BR](https://static.draft5.gg/assets/flags/BR.svg)yuurih

            Reservas
            --------

            ![Image 6: BR](https://static.draft5.gg/assets/flags/BR.svg)skullz

            ![Image 7: BR](https://static.draft5.gg/assets/flags/BR.svg)chelo
            }

            Exemplo de resposta:
            {'latestMatches': [
                {'date': '2025/04/09 - 09:50 BRT',
                    'tournament': 'Bucharest 2025',
                    'opponent': 'MongolZ',
                    'score': '0:2',
                    'win': 'false'}
                    ]
            }

            {'lineUp': [
                    {'titular': [
                            'MOLODOY',
                            'YEKINDAR',
                            'FalleN',
                            ...
                        ]
                    },
                    {'reserva': [
                            'skullz',
                            ...
                        ]
                    }
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