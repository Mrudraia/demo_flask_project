from flask import Flask, jsonify, request, render_template_string, abort
from prometheus_client import generate_latest, REGISTRY, Counter, Gauge, Histogram
import random, time
import json

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



REQUESTS = Counter('http_requests_total', 'Total HTTP Requests (count)', ['method', 'endpoint', 'status_code'])
IN_PROGRESS = Gauge('http_requests_inprogress', 'Number of in progress HTTP requests')
TIMINGS = Histogram('http_requests_duration_seconds', 'HTTP request latency (seconds)')


@app.route("/")
@cross_origin()
@TIMINGS.time()
@IN_PROGRESS.track_inprogress()
def hello_world():
    REQUESTS.labels(method='GET', endpoint="/", status_code=200).inc()
    return "Welcome to redhat"
    
    
@app.route("/prometheus-course/<name>")
@cross_origin()
@IN_PROGRESS.track_inprogress()
@TIMINGS.time()
def greet():
    REQUESTS.labels(methos='GET', endpoint="/prometheus-course/jorn", status_code=200).inc()
    response = {"message":"welcome to redhat, enjoy the opensource culture"}
    return jsonify(response)


@app.route('/post_json', methods=['POST'])
@cross_origin()
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'
        
        
### Prometheus APIs
@app.route('/metrics')
@cross_origin()
@IN_PROGRESS.track_inprogress()
@TIMINGS.time()
def metrics():
    REQUESTS.labels(method='GET', endpoint="/metrics", status_code=200).inc()
    return generate_latest(REGISTRY)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
