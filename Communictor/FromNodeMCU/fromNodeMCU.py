from flask import Flask, request

app = Flask(__name__)

@app.route('/endpoint', methods=['POST'])
def handle_data():
    data = request.json
    print(data)

    return 'Data received'

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)