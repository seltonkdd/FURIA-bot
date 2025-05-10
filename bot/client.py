from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv('./.env')

GROQ_KEY = os.getenv('GROQ_KEY')

model = Groq(api_key=GROQ_KEY)

def call_model(user_message):
    response_format = {"type": "json_object"}
    messages = [
        {   
            'role': 'system', 'content': '''Voce é um assistente que irá receber um json com uma chave "type" e uma chave "md_content".
            O valor da chave "type" contém o tipo de tarefa que voce irá realizar.
            E o valor da chave "md_content" contém o conteudo html estilizado como markdown de um site no qual você irá buscar as informações.
            O conteudo do site é informações sobre o time de CS Furia, suas partidas ou sua line-up.
            Você deve responder diretamente apenas o que lhe for atribuido.
            Sua resposta deve ser APENAS um JSON DIRETO. Nada mais.
            Não comece com 'Para conseguirmos identificar..' ou coisas do tipo.

            Se o "type" for 'GET_LATEST_MATCHES', o response_type deve ser 'latestMatches' e a resposta deve ser uma lista de json com as informações das partidas como data, hora, torneio, oponente e score.
            Se o "type" for 'GET_LINEUP', o response_type deve ser 'lineUp' e a resposta deve ser uma lista de json com os nomes dos jogadores.
            Se o "type" for 'GET_NEXT_MATCHES', o response_type deve ser 'nextMatches' e a resposta deve ser uma lista de json com as informações das partidas.
            Se o "type" for 'GET_NEXT_TOURNAMENTS', o response_type deve ser 'nextTournaments' e a resposta deve ser uma lista de json contendo nome e data do torneio.

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

            {'type': 'GET_NEXT_MATCHES', 'md_content': 
            'Jogos
            ----------

            📅 quarta-feira, 9 de abril de 2025

            [09:50 ![Image 8: 330](https://api.draft5.gg/teams/330/logo)FURIA 0 ![Image 9: 2635](https://api.draft5.gg/teams/2635/logo)(algum time...) 0 MD3 (algum torneio...) Reveja os lances](algum link...)'
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

            {'nextTournaments': [
                        {
                            'name': 'PGL Astana 2025',
                            'date': '2025/05/10 - 2025/05/18'
                    }
                ]
            }
            
            Para o 'nextMatches', repita o formato de latestsMatches com excessao dos campos score e win... e adicione um novo campo que é o link da partida.
            Exemplo "match_link": 'https://draft5.gg/partida/...'
            
            Sempre crie JSON com formatos válidos, como as chaves contendo aspas duplas.

            Caso não encontrar qualquer uma das informações, preencha a resposta como null
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