from flask import Flask
import surebet
from book import predict
import pandas as pd


app = Flask(__name__)


def bet():
    jogos = pd.read_json('betfair')
    p = []

    for i in range(jogos.shape[0]):
        try:
            p.append(predict(jogos.Home[i], jogos.Away[i], 'model_log.pkl.z'))
        except:
            p.append(None)

    df = pd.DataFrame(p,columns=['Previsão','Odd_Modelo'])
    jogos = jogos.join(df, rsuffix='Odd_Betfair')
    jogos = jogos[['Home','Away','Previsão','Odd_Betfair']]

    aposta = []
    for x, y in zip(jogos.Odd_Betfair, jogos['Previsão']):
        if y == 0 and x > 2:
            aposta.append('Back')
        elif y == 1 and x < 2:
            aposta.append('Lay')
        else:
            aposta.append('-')

    jogos['Aposta'] = aposta
    jogos['Previsão'] = jogos['Previsão'].map({0:'NoH',1:'H'})

    return jogos.to_html()

jogos = bet()

@app.route('/')
def aposta():
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