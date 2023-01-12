import json

from flask import Flask

from backend.graph import create_graph, read_routes_to_graph
from backend.weigthCalc import predict_connections

app = Flask(__name__)

graph = create_graph(routes=read_routes_to_graph(), date="2023-01-13")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/predict")
def predict():
    start = 1113
    destination = 1114
    result = predict_connections(graph_struct=graph, start=start, desc=destination)
    return json.dumps(result, encoding="utf-8")

