from flask import Flask
from surebet import scrapy
from book import predict
import pandas as pd

app = Flask(__name__)

def bet():
    jogos = pd.read_json('betfair')
    jogos['Previsão'] , na = predict(jogos,'model_log.pkl.z')
    jogos = jogos[['HomeTeam','AwayTeam','Previsão','Odd_Betfair']]

    aposta = []
    for x, y in zip(jogos.Odd_Betfair, jogos['Previsão']):
        if y == 0 and x > 2:
            aposta.append('-')
        elif y == 1 and x < 2:
            aposta.append('Lay')
        else:
            aposta.append('-')

    jogos['Aposta'] = aposta
    na['Aposta'] = 'Name Error'
    jogos['Previsão'] = jogos['Previsão'].map({0:'H',1:'NoH'})
    jogos = pd.concat([jogos,na],ignore_index=True)

    return jogos.to_html()

@app.route('/')
def index():
    return """<head><h1>Recomendador de Apostas</h1></head>
        < body >
        <h2> Ligas disponíveis:</h2>
        <p>B1 - Liga Belga\n
        D2 - Bundesliga 2 Alemã\n
        IT - Séria A Italiana\n
        P1 - Primeira Liga Portuguesa\n
        SC1 - Premiership Escocesa\n
        T1 - Liga 1 Turca</p>
        </body>"""

@app.route('/B1D2')
def B1D2():
    scrapy(['bélgica-first-division-a-apostas-89979','alemanha-bundesliga-2-apostas-61'])
    html = bet()
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 1.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/I1P1')
def I1P1():
    scrapy(['itália-série-a-apostas-81,portugal-primeira-liga-apostas-99'])
    html = bet()
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 1.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/SC1T1')
def SC1T1():
    scrapy(['escócia-premiership-apostas-105,turquia-super-league-apostas-194215'])
    html = bet()
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 1.0 por Bruno Brasil</center>
        </body>""".format(html)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

# flask run