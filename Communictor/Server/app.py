from flask import Flask, request, jsonify
import time
import json
from main import process_image, calculate_expression, process_image_for_whiteboard

app = Flask(__name__)

host_url = '192.168.1.4'

@app.route("/")
def hello_world():
    return "<p>Routes: </p> <p> /json1 : Image from raspberry pi </p>"

@app.route('/json1', methods=['GET','POST'])
def handle_data():
    data = request.json
    f = open("fromNodeMCU.txt", "w")
    f.write(json.dumps(data))
    f.close()
    return jsonify(data)

@app.route('/image', methods=['GET','POST'])
def image_route():
    if 'file' not in request.files:
        return jsonify({"error":"No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error":"No selected file"})
    if not file:
        return jsonify({"error":"No file part"})
    file.save("img.png")
    result = process_image("img.png")
    try:
        ans = calculate_expression(result)
    except:
        ans = ["Error in processing the image"]
    return jsonify({"result":ans})

@app.route('/image_whiteboard', methods=['GET','POST'])
def image_route_whiteboard():
    if 'file' not in request.files:
        return jsonify({"error":"No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error":"No selected file"})
    if not file:
        return jsonify({"error":"No file part"})
    file.save("img.png")
    result = process_image_for_whiteboard("img.png")
    return jsonify({"result":result})

if __name__ == '__main__':
    app.run(host=host_url,port=80)