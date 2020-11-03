from flask import Flask, jsonify, request
from config import settings

app = Flask(__name__)

@app.errorhandler(500)
def internal_error(error):
    return str(error), 500

@app.route('/prices', methods=['GET', 'POST'])
def getPrices():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        data = request.data.decode('utf-8')
        pass
    return 'Okay'

@app.route('/auth', methods=['POST'])
def authUsers():
    if request.method == 'POST':
        pass
    else:
        pass
    return jsonify({'result': 'Okay'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)