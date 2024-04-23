from flask import Flask, request, jsonify
import time
import json

app = Flask(__name__)

RECEIVE_DATA = False
SEND_DATA = True
count = 0
data_to_send = "hello from pc"

@app.route("/")
def hello_world():
    return "<p>Routes: </p> <p> /json1 : Receive json from ESP </p> <p> /json2 : Post json to ESP </p>"

@app.route('/json1', methods=['GET','POST'])
def handle_data():
    if RECEIVE_DATA:
        data = request.json
        print(data)
        return jsonify(data)

@app.route('/json2', methods=['GET','POST'])
def send_data():
    if SEND_DATA:
        send_data = {"data": data_to_send}
        return jsonify(send_data)
    else:
        return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)