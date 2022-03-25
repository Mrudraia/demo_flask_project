from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to redhat"
    
@app.route("/greet", methods=["GET"])
def greet():
    response = {"message":"welcome to redhat, enjoy the opensource culture"}
    return jsonify(response)

@app.route('/post_json', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
