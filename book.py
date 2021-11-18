times ={
  'Coritiba':'Coritiba',
  'Corinthians':'Corinthians',
  'Palmeiras':'Palmeiras',
  'Fluminense':'Fluminense',
  'Internacional':'Internacional',
  'Cruzeiro':'Cruzeiro',
  'Sport Recife':'Sport Recife',
  'Bahia':'Bahia',
  'Vasco':'Vasco',
  'Portuguesa':'Portuguesa',
  'Chapecoense-SC':'Chapecoense-SC',
  'Ponte Preta':'Ponte Preta',
  'Fortaleza':'Fortaleza',
  'Figueirense':'Figueirense',
  'Santos':'Santos',
  'Bragantino':'Bragantino',
  'CSA':'CSA',
  'Santa Cruz':'Santa Cruz',
  'Joinville':'Joinville',
  'Juventude':'Juventude',
  'Flamengo RJ':'Flamengo',
  'Atletico-MG':'Atlético-MG',
  'Sao Paulo': 'São Paulo',
  'Gremio': 'Grêmio',
  'Botafogo RJ': 'Botafogo',
  'Atletico-PR': 'Athletico-PR',
  'Vitoria': 'Vitória',
  'Goias':'Goiás',
  'Ceara':'Ceará',
  'Atletico GO': 'Atlético-GO',
  'Avai': 'Avaí',
  'Athletico-PR': 'Athletico-PR',
  'America MG': 'América-MG',
  'Nautico':'Náutico',
  'Criciuma':'Criciúma',
  'Parana':'Paraná',
  'Cuiaba': 'Cuiabá'}
import pandas as pd
import numpy as np
from sklearn import preprocessing
from scipy.sparse import hstack
from sklearn.linear_model import LogisticRegression
import joblib

book = pd.read_csv('https://www.football-data.co.uk/new/BRA.csv')
book.drop(['Time', 'PH', 'PD', 'PA', 'MaxH', 'MaxD', 'MaxA'], axis=1, inplace=True)
book.dropna(inplace=True)  # Chape vs Atletico Mg em 2016 teve um W.O.
book.Home = book.Home.map(times)
book.Away = book.Away.map(times)
book.reset_index(drop=True)


def predict(home, away, modelo):
    mybook = pd.concat([book, pd.DataFrame([[home, away]], columns=['Home', 'Away'])], ignore_index=True)

    # Criando colunas com média de gols
    mybook['MediagolsH'] = 0
    mybook['MediagolsA'] = 0

    # loop com a crianção da média de gols antes da ocorrência do jogo
    for time in mybook.Home.unique():
        i = mybook[mybook['Home'] == time].index.tolist()
        mediagols = mybook[mybook['Home'] == time].HG.cumsum() / (
                    mybook[mybook['Home'] == time].reset_index(drop=True).index + 1)
        mediagols = [0] + mediagols.tolist()[:-1]
        mediagols = pd.Series(mediagols, index=i)
        mybook.MediagolsH[i] = mediagols

    for time in mybook.Away.unique():
        i = mybook[mybook['Away'] == time].index.tolist()
        mediagols = mybook[mybook['Away'] == time].AG.cumsum() / (
                    mybook[mybook['Away'] == time].reset_index(drop=True).index + 1)
        mediagols = [0] + mediagols.tolist()[:-1]
        mediagols = pd.Series(mediagols, index=i)
        mybook.MediagolsA[i] = mediagols

    mybook['g_3'] = mybook.MediagolsH.apply(lambda x: x ** 2)
    X = mybook[['Home', 'Away', 'g_3']]
    # Lidando com dados categóricos com OneHotEnconder e padronizado valores numéricos
    # dados em array
    std = preprocessing.StandardScaler()

    # separando dados numéricos
    a = X.drop(['Home', 'Away'], axis=1).values

    # separando dados categóricos
    features = [f for f in X.columns if f in (['Home', 'Away'])]

    # preprocessando dados categóricos no formato sparse matrix
    ohe = preprocessing.OneHotEncoder(sparse=True)
    X = ohe.fit_transform(X[features])

    # Adicionando dados numéricos padronizados
    dados_std = std.fit_transform(a)

    # Inserindo dentro da matriz

    X = hstack([X, dados_std])
    X = X.tocsr()[-1]

    model = joblib.load(modelo)

    y_pred = model.predict(X)
    y_prob = model.predict_proba(X)

    return y_pred[0], round(1 / y_prob[0][0], 2)