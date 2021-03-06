from flask import Flask
from surebet import scrapy
from book import predict
import pandas as pd


app = Flask(__name__)

def bet(modelo, back=True, lay=True, back_inverse=False):
    jogos = pd.read_json('betfair')
    jogos['Previsão'], na = predict(jogos, modelo)

    jogos = jogos[['Date','HomeTeam','AwayTeam','Previsão','Odd_Betfair']]

    aposta = []
    for x, y in zip(jogos.Odd_Betfair, jogos['Previsão']):
        if back == True and y == 0 and x > 2:
            aposta.append('Back')
        elif lay == True and y == 1 and x < 2:
            aposta.append('Lay')
        elif back_inverse == True and y == 0 and x < 2:
            aposta.append('Back')
        else:
            aposta.append('-')

    jogos['Aposta'] = aposta
    na['Aposta'] = 'Name Error'
    jogos['Previsão'] = jogos['Previsão'].map({0:'H',1:'NoH'})
    jogos = pd.concat([jogos,na],ignore_index=True)

    return jogos.to_html()

# def bet2():
#     jogos = pd.read_json('betfair_tw')
#     jogos['Previsão'] = predict2(jogos)
#     jogos = jogos[['HomeTeam', 'AwayTeam', 'Previsão', 'Odd_Betfair', 'League']]
#     aposta = []
#     back = ["D1","D2","E1","E2","E3","EC","SC2","SP1","SP2"]
#     lay = ["B1","D1","D2","E1","E2","E3","EC","I2","N1","SC2","SC3","SP1","SP2","T1"]

#     for x, y, b in zip(jogos.Odd_Betfair, jogos['Previsão'],jogos.League):
#         if y == 0 and x > 2 and b in back:
#             aposta.append('Back')
#         elif y == 1 and x < 2 and b in lay:
#             aposta.append('Lay')
#         else:
#             aposta.append('-')
#     jogos = jogos[['League','HomeTeam','AwayTeam','Odd_Betfair']]
#     jogos['Aposta'] = aposta

#     return jogos.to_html()

@app.route('/')
def index():
    return """<head><title>Recomendador de Apostas</title></head>
        <body>
        <h2> Ligas disponíveis:</h2>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/A1">  A1 - Copa da Superliga Argentina </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/A2">  A2 - Austria Bundesliga </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/B1">  B1 - Divisão A Belga </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/D1">  D1 - Bundesliga 1 Alemã </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/D2"> D2 - Bundesliga 2 Alemã </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/E1"> E1 - EFL Championship </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/E2"> E2 - Inglaterra Liga 1 </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/E3"> E3 - Inglaterra Liga 2 </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/EC"> EC - National League </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/I2">  I2 - Séria B Italiana </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/N1">  N1 - Eredivisie Neerlandês </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/P1"> P1 - Primeira Liga Portuguesa </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/SC2"> SC2 - Primeira Divisão Escocesa </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/SC3"> SC3 - Segunda Divisão Escocesa </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/SP1"> SP1 - La Liga Espanhola </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/SP2"> SP2 - Segunda Divisão Espanhola </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/SW1"> SW1 - Allsvenskan Sueca </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/SW2"> SW2 - Challenge League Suíça </a></p>
        <p><a href="https://recomendador-de-aposta.herokuapp.com/T1"> T1 -Super Liga Turca </a></p>
        </body>"""

@app.route('/A1')
def A1():
    scrapy(['argentina-copa-da-superliga-apostas-12225162'])
    modelo = 'model_Argentina.pkl.z'
    html = bet(modelo, back=False)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/A2')
def A2():
    scrapy(['áustria-bundesliga-apostas-10479956'])
    modelo = 'model_Austria.pkl.z'
    html = bet(modelo, back=False)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/B1')
def B1():
    scrapy(['bélgica-first-division-a-apostas-89979'])
    modelo = 'model_B1.pkl.z'
    html = bet(modelo, back=False)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/D1')
def D1():
    scrapy(['bundesliga-alemã-apostas-59'])
    modelo = 'model_D1.pkl.z'
    html = bet(modelo)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/D2')
def D2():
    scrapy(['alemanha-bundesliga-2-apostas-61'])
    modelo = 'model_D2.pkl.z'
    html = bet(modelo)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/E1')
def E1():
    scrapy(['inglaterra-championship-apostas-7129730'])
    modelo = 'model_E1.pkl.z'
    html = bet(modelo)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/E2')
def E2():
    scrapy(['inglaterra-league-1-apostas-35'])
    modelo = 'model_E2.pkl.z'
    html = bet(modelo)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/E3')
def E3():
    scrapy(['inglaterra-league-two-apostas-37'])
    modelo = 'model_E3.pkl.z'
    html = bet(modelo)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/EC')
def EC():
    scrapy(['inglaterra-national-league-apostas-11086347'])
    modelo = 'model_EC.pkl.z'
    html = bet(modelo)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/F1')
def F1():
    scrapy(['frança-ligue-1-apostas-55'])
    modelo = 'model_F1.pkl.z'
    html = bet(modelo, back=False)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/I1')
def I1():
    scrapy(['itália-série-a-apostas-81'])
    modelo = 'model_I1.pkl.z'
    html = bet(modelo, back=False)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/I2')
def I2():
    scrapy(['itália-série-b-apostas-12199689'])
    modelo = 'model_I2.pkl.z'
    html = bet(modelo, back=False)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/N1')
def N1():
    scrapy(['holanda-eredivisie-apostas-9404054'])
    modelo = 'model_N1.pkl.z'
    html = bet(modelo, back=False)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/P1')
def P1():
    scrapy(['portugal-primeira-liga-apostas-99'])
    modelo = 'model_P1.h5'
    html = bet(modelo, back=False , back_inverse=True)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/SC2')
def SC2():
    scrapy(['escócia-league-one-apostas-109'])
    modelo = 'model_SC2.pkl.z'
    html = bet(modelo)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/SC3')
def SC3():
    scrapy(['escócia-league-2-apostas-111'])
    modelo = 'model_SC3.pkl.z'
    html = bet(modelo, back=False)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/SP1')
def SP1():
    scrapy(['espanha-la-liga-apostas-117'])
    modelo = 'model_SP1.pkl.z'
    html = bet(modelo)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/SP2')
def SP2():
    scrapy(['espanha-segunda-divisão-apostas-12204313'])
    modelo = 'model_SP2.pkl.z'
    html = bet(modelo)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/SW1')
def SW1():
    scrapy(['suécia-allsvenskan-apostas-129'])
    modelo = 'model_Sweden.pkl.z'
    html = bet(modelo, back=False)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/SW2')
def SW2():
    scrapy(['suíça-challenge-league-apostas-133'])
    modelo = 'model_Switzerland.pkl.z'
    html = bet(modelo, back=False)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/T1')
def T1():
    scrapy(['turquia-super-league-apostas-194215'])
    modelo = 'model_T1.pkl.z'
    html = bet(modelo, back=False)
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 2.0 por Bruno Brasil</center>
        </body>""".format(html)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

# flask run
