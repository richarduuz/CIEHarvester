from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.errorhandler(500)
def internal_error(error):
    return str(error), 500

@app.route('/prices', methods=['GET', 'POST'])
def getPrices():
    import util
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
    import util
    auther = util.Auther()
    try:
        if request.method == 'POST':
            rawData = request.data.decode('utf-8')
            data = json.loads(rawData)
            result = {'status': 'Okay', 'message': 'wrong'}
            if 'password' in data.keys():
                password = data['password']
                result['isAdmin'] = False
            else:
                password = data['adminPassword']
                result['isAdmin'] = True
            if auther.authUser(password, result['isAdmin']):
                result['message'] = 'right'
            return jsonify(result)
        else:
            pass
    except Exception as e:
        internal_error(str(e))

@app.route('/password', methods=['POST'])
def resetPaw():
    try:
        import util
        auther = util.Auther()
        rawData = request.data.decode('utf-8')
        data = json.loads(rawData)
        password = data['newPassword']
        if auther.resetPsw(password):
            return jsonify({'status': 'Okay'})
        else:
            return jsonify({'status': "Wrong"})
    except Exception as e:
        internal_error(str(e))

@app.route('/test', methods=["GET"])
def getTest():
    if request.method == 'GET':
        return jsonify({'status': 'Just for test'})
    else:
        internal_error("Wrong http requests")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)