from flask import Flask, request, jsonify
import time
import json

app = Flask(__name__)

host_url = '192.168.1.4'

@app.route("/")
def hello_world():
    return "<p>Routes: </p> <p> /json1 : Receive json from ESP </p> <p> /json2 : Post json to ESP </p>"

@app.route('/json1', methods=['GET','POST'])
def handle_data():
    data = request.json
    print(data)
    return jsonify(data)

@app.route('/json2', methods=['GET','POST'])
def send_data():
    f = open("toNodeMCU.txt", "r")
    data_to_send = f.read()
    f.close()
    if data_to_send:
        send_data = {"data": data_to_send}
        return jsonify(send_data)
    else:
        return ""

if __name__ == '__main__':
    app.run(host=host_url,port=80)