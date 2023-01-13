import math

import networkx
import networkx as nx
from fontTools.varLib.plot import stops
from networkx import Graph
# from graph import BUS_STOP_DETAILS
from datetime import datetime, timedelta
import requests
from collections import OrderedDict

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
        connection_A = G.nodes[u].get("connections")
        connection_B = G.nodes[v].get("connections")
        possible_routes = dict()
        departure_times = []
        relative_time = now + timedelta(minutes=G.nodes[u].get("relative_time", 0))
        for route in connection_B:
            time_diff = (datetime.strptime(route["estimatedDepartureTime"], "%Y-%m-%dT%H:%M:%S") - relative_time).seconds/60
            if time_diff >= 0 and route["routeId"] in d["routes"]:
                departure_times.append((route["routeId"], time_diff + d["time"], route["estimatedDepartureTime"]))

            xd = False
            if time_diff >= -1 and route["routeId"] in (d.get("chosen_line", "WRONG") and d["routes"]):
                soonest_departure = (route["routeId"], time_diff+d["time"], route["estimatedDepartureTime"])
                xd = True
                break


        if not xd:
            found = False
            departure_times.sort(key=lambda x: x[1])
            # for i in range(5):
            #     if d.get("last_line", "xxx") == departure_times[i][0]:
            #         soonest_departure = departure_times[i]
            #         found = True

            if not found:
                soonest_departure = min(departure_times,key=lambda x: x[1])

        d["last_line"] = soonest_departure[0]
        d["chosen_line"] = (soonest_departure[0], soonest_departure[2])
        soonest_dep = math.ceil(soonest_departure[1])
        G.nodes[v]["relative_time"] = min(G.nodes[u].get("relative_time", 0) + soonest_dep, G.nodes[v].get("relative_time", 9999999999))
        return soonest_dep

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