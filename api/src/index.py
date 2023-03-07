from flask import Flask

app = Flask(__name__)

@app.route('/api/number')
def getNumber():
    return {"number":3}

@app.route('/api/letter')
def getLetter():
    return {"letter":'a'}