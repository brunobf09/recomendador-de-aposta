import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
import joblib


book = pd.read_csv('/content/Europa.csv')
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

def predict(home, away, modelo):
    mybook = pd.concat([data, pd.DataFrame([[home, away]], columns=['HomeTeam', 'AwayTeam'])], ignore_index=True)
    mybook.f_2[mybook.shape[0]-1] = mybook[mybook.HomeTeam == home].FTHG.mean()**2

    X = mybook[['HomeTeam', 'AwayTeam', 'f_2']]

    x = pipe.fit_transform(X)[-1]

    model = joblib.load(modelo)

    y_pred = model.predict(x.reshape(1,-1))

    return y_pred[0]