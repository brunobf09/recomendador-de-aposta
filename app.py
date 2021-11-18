from flask import Flask


app = Flask(__name__)

@app.route('/')
def aposta():
    return """<head><center><h1>Recomendador de Apostas</h1></head></center>
    
if __name__ == '__main__':
    app.run()

# flask run
