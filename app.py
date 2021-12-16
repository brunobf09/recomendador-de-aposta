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
    return """"<head><h1>Recomendador de Apostas</h1></head>
        < body >
        <h1> Ligas disponíveis: <h1>
        <p>B1 - Liga Belga<p>"""
    

@app.route('/B1D1')
def pag1():
    scrapy(['bélgica-first-division-a-apostas-89979','alemanha-bundesliga-2-apostas-61]')
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