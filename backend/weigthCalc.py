import math

import networkx
import networkx as nx
from fontTools.varLib.plot import stops
from networkx import Graph, DiGraph
# from graph import BUS_STOP_DETAILS
from datetime import datetime, timedelta
import requests
from collections import OrderedDict

from backend.distance import calc_time


DEPURTE_TIME = 2
WALKING_BONUS_TIME = 1
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
    for key in graph_struct.nodes.keys():
        graph_struct.nodes[key]["connections"] = sorted(graph_struct.nodes[key]["connections"], key=lambda x: x["estimatedDepartureTime"])
    path = networkx.dijkstra_path(graph_struct, start, dest, create_func(graph_struct))
    routes = []
    for i in range(len(path) - 1):
        routes.append(graph_struct.edges[path[i],path[i+1]]["chosen_line"])
    print(path)
    return routes


def create_func(G: Graph):
    now = datetime.fromisocalendar(2023,2,5)

    def weight_cost_func(u, v, d):
        relative_time = now + timedelta(minutes=G.nodes[u].get("relative_time", 0))
        if "routes" not in d:
            travel_time = d["walkTime"] + WALKING_BONUS_TIME
            chosen_line = ("W", travel_time, relative_time)
        else:
            connection_B = G.nodes[v].get("connections", [])

            departure_times = []


            for route in connection_B:
                time_diff = (datetime.strptime(route["estimatedDepartureTime"], "%Y-%m-%dT%H:%M:%S") - relative_time).seconds/60
                if time_diff >= 0 and route["routeId"] in d["routes"]:
                    departure_times.append((route["routeId"], time_diff + d["time"], route["estimatedDepartureTime"]))
            if departure_times:
                soonest_departure = min(departure_times, key=lambda x: x[TRAVEL_TIME])
                travel_time = math.ceil(soonest_departure[TRAVEL_TIME])
            else:
                soonest_departure = ("neverUSEDDD", 6969, datetime.now())
                travel_time = 999999
            walk_travel_time = d.get("walkTime", 999999)
            if walk_travel_time < travel_time:
                chosen_line = ("W", walk_travel_time, relative_time)
            else:
                chosen_line = (soonest_departure[ID], travel_time, soonest_departure[DEPURTE_TIME])

        new_relative = G.nodes[u].get("relative_time", 0) + travel_time
        if new_relative <=  G.nodes[v].get("relative_time", 9999999999):
            G.nodes[v]["relative_time"] = new_relative
            d["chosen_line"] = chosen_line

        return travel_time

    return weight_cost_func

def nodage_parserage(edges):
    pass




if __name__ == "__main__":
    import json
    import networkx
    from networkx.readwrite import json_graph

    with open("../out.json") as f:
        G: DiGraph = networkx.node_link_graph(json.load(f))
        #G = G.subgraph([2021, 2019, 2017, 2072])
        print(run_dijktra(G, 2072, 2021))

    #update_departure_times(graph_struct=Graph)