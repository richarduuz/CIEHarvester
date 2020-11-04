from flask import Flask, jsonify, request
import util
import json

app = Flask(__name__)

@app.errorhandler(500)
def internal_error(error):
    return str(error), 500

@app.route('/prices', methods=['GET', 'POST'])
def getPrices():
    crawler = util.Crawlers()
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        rawData = request.data.decode('utf-8')
        data = json.loads(rawData)
        result = crawler.crawlAllPrices(data['modelNumber'])
        return jsonify(result)

@app.route('/auth', methods=['POST'])
def authUsers():
    auther = util.Auther()
    try:
        if request.method == 'POST':
            rawData = request.data.decode('utf-8')
            data = json.loads(rawData)
            password = data['password']
            if auther.authUser(password):
                return jsonify({'status': 'Okay', 'message': 'right'})
            else:
                return jsonify({'status': 'Okay', 'message': 'wrong'})
        else:
            pass
    except Exception as e:
        internal_error(str(e))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)