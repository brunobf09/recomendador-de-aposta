import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
import joblib


book = pd.read_csv('https://www.dropbox.com/s/67nc28maycz4840/Europa.csv?dl=1')
df = pd.read_excel('https://www.football-data.co.uk/mmz4281/2122/all-euro-data-2021-2022.xlsx',sheet_name=None)
df = pd.concat(df,ignore_index=True)
df = df[['Div', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR','B365H', 'B365D', 'B365A']]
df.fillna(0,inplace=True)
data = pd.concat([book,df],ignore_index=True)

numeric = ['f_2']
categorical = ['HomeTeam', 'AwayTeam']

class Columns(BaseEstimator, TransformerMixin):
    def __init__(self, names=None):
        self.names = names

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X):
        return X[self.names]

pipe = Pipeline([
    ("features", FeatureUnion([
        ('categorical', make_pipeline(Columns(names=categorical), OneHotEncoder(sparse=False))),
        ('numeric', make_pipeline(Columns(names=numeric), StandardScaler()))

    ]))
])


def predict(jogos, modelo):
    jogos['f_2'] = jogos.HomeTeam.apply(lambda x: data[data.HomeTeam == x].FTHG.mean() ** 2)
    jogos['f_1'] = jogos.AwayTeam.apply(lambda x: data[data.AwayTeam == x].FTHG.mean())
    jogos.dropna(inplace=True, axis=0)
    mybook = pd.concat([data, jogos], ignore_index=True)

    X = mybook[['HomeTeam', 'AwayTeam', 'f_2']]

    x = pipe.fit_transform(X)[-len(jogos):]

    model = joblib.load(modelo)

    y_pred = model.predict(x)

    return y_pred
