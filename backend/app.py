import json

import networkx
from flask import Flask, request
from flask_cors import CORS
from networkx import DiGraph

from backend.weigthCalc import predict_connections

app = Flask(__name__)
CORS = CORS(app, resources={r"/*": {"origins": "*"}})


# graph = create_graph(routes=read_routes_to_graph(), date="2023-01-13")
@app.route("/predict")
def predict():
    global graph
    # graph = create_graph(routes=read_routes_to_graph(), date="2023-01-13")
    destination = request.args.get('dest')
    start = request.args.get('start')
    date_now = request.args.get('date')
    with open("../out.json") as f:
        G: DiGraph = networkx.node_link_graph(json.load(f))
    result = predict_connections(graph_struct=G, start=int(start), dest=int(destination))
    return json.dumps(result).encode("utf8")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
