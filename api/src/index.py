from flask import Flask

app = Flask(__name__)

@app.route('/api/number')
def getNumber():
    return {"number":3}