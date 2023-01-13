import math

import networkx
import networkx as nx
from fontTools.varLib.plot import stops
from networkx import Graph
# from graph import BUS_STOP_DETAILS
from datetime import datetime, timedelta
import requests
from collections import OrderedDict

DEPURTE_TIME = 2

ID = 0

TRAVEL_TIME = 1


def predict_connections(graph_struct: Graph, start: int, dest: int):
    update_departure_times(graph_struct=graph_struct)
    run_dijktra(graph_struct, start, dest)
        

def update_departure_times(graph_struct):
    pass
    # for stop in BUS_STOP_DETAILS.keys():
    #     print(stop)
        

def run_dijktra(graph_struct: Graph, start: int, dest: int):

    path = networkx.dijkstra_path(graph_struct, start, dest, create_func(graph_struct))
    routes = []
    for i in range(len(path) - 1):
        routes.append(graph_struct.edges[path[i],path[i+1]]["chosen_line"])
    return routes


def create_func(G: Graph):
    now = datetime.now()

    def weight_cost_func(u, v, d):
        connection_B = G.nodes[v].get("connections")

        departure_times = []
        relative_time = now + timedelta(minutes=G.nodes[u].get("relative_time", 0))

        for route in connection_B:
            time_diff = (datetime.strptime(route["estimatedDepartureTime"], "%Y-%m-%dT%H:%M:%S") - relative_time).seconds/60
            if time_diff >= 0 and route["routeId"] in d["routes"]:
                departure_times.append((route["routeId"], time_diff + d["time"], route["estimatedDepartureTime"]))

        soonest_departure = min(departure_times, key=lambda x: x[TRAVEL_TIME])

        d["chosen_line"] = (soonest_departure[ID], soonest_departure[DEPURTE_TIME])
        travel_time = math.ceil(soonest_departure[TRAVEL_TIME])
        G.nodes[v]["relative_time"] = min(G.nodes[u].get("relative_time", 0) + travel_time, G.nodes[v].get("relative_time", 9999999999))
        return travel_time

    return weight_cost_func

def nodage_parserage(edges):
    pass

if __name__ == "__main__":
    import json
    import networkx
    from networkx.readwrite import json_graph

    with open("../out.json") as f:
        G: Graph = networkx.node_link_graph(json.load(f))
        # G = G.subgraph([1013,1025])
        print(run_dijktra(G, 2021, 1017))

    #update_departure_times(graph_struct=Graph)