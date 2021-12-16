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
    return """<head><title>Recomendador de Apostas</title></head>
        <body>
        <h2> Ligas disponíveis:</h2>
        <p>B1 - Liga Belga </p>
        <p>D2 - Bundesliga 2 Alemã </p>
        <p>I1 - Séria A Italiana </p>
        <p>P1 - Primeira Liga Portuguesa </p>
        <p>SC1 - Premiership Escocesa </p>
        <p>T1 - Super Liga Turca</p>
        </body>"""

@app.route('/B1')
def B1():
    scrapy(['bélgica-first-division-a-apostas-89979'])
    html = bet()
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 1.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/D2')
def D2():
    scrapy(['alemanha-bundesliga-2-apostas-61'])
    html = bet()
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 1.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/I1')
def I1():
    scrapy(['itália-série-a-apostas-81'])
    html = bet()
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 1.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/P1')
def P1():
    scrapy(['portugal-primeira-liga-apostas-99'])
    html = bet()
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 1.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/SC1')
def SC1():
    scrapy(['escócia-premiership-apostas-105'])
    html = bet()
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
        <body>
        <center><table>
                 {}
        </table></center>
        <center> Versão 1.0 por Bruno Brasil</center>
        </body>""".format(html)

@app.route('/T1')
def T1():
    scrapy(['turquia-super-league-apostas-194215'])
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
