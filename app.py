from flask import Flask
import pandas as pd


app = Flask(__name__)

@app.route('/')
def aposta():
    html = bet()
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

# flask run
