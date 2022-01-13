import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
import json
import joblib

book = pd.read_csv('Europa.csv')
df = pd.read_excel('https://www.football-data.co.uk/mmz4281/2122/all-euro-data-2021-2022.xlsx',sheet_name=None)
df = pd.concat(df,ignore_index=True)
df = df[['Div', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR','B365H', 'B365D', 'B365A']]
df.fillna(0,inplace=True)
data = pd.concat([book,df],ignore_index=True)
bias = json.load(open('bias.json'))

def predict(jogos, modelo, xgb=False ):
  jogos['h5']  = jogos.AwayTeam.apply(lambda x: data[data.AwayTeam == x].FTHG.mean()**2)
  jogos['a3']  = jogos.AwayTeam.apply(lambda x: data[data.AwayTeam == x].FTAG.mean()**2)
  jogos['a5']  = jogos.HomeTeam.apply(lambda x: data[data.HomeTeam == x].FTAG.mean()**2)
  jogos['h4']  = jogos.HomeTeam.apply(lambda x: data[data.HomeTeam == x].FTHG.mean()) * jogos.AwayTeam.apply(lambda x: data[data.AwayTeam == x].FTHG.mean())

  bias = json.load(open('bias.json'))
  m5 = []
  for h,a in zip(jogos.HomeTeam,jogos.AwayTeam):
    if h not in bias:
      x = 1
    else:
      x = bias[h]
    if a not in bias:
      y = 1
    else:
      y = bias[a]
    m5.append((x+y)/2)

  jogos['m5'] = m5 * jogos.h4
  na_a5 = jogos[jogos.a5.isnull() == True]
  na_a3 = jogos[jogos.a3.isnull() == True]
  na = pd.concat([na_a5,na_a3],ignore_index=True)
  na.drop(['a5','a3','h5','h4','m5'],axis=1,inplace=True)
  jogos.dropna(inplace=True, axis=0)


  X = jogos[['m5','h5','a3','a5']]
  std = StandardScaler()
  X = std.fit_transform(X)
  X = csr_matrix(X)
  if xgb == True:
    model = XGBClassifier()
    model.load_model(modelo)
  else:
    model = joblib.load(modelo)

  y_pred = model.predict(X)

  return y_pred , na
