import math

import networkx
import networkx as nx
from fontTools.varLib.plot import stops
from networkx import Graph, DiGraph
from graph import get_bus_stop_details
from datetime import datetime, timedelta
import requests
from collections import OrderedDict
from distance import calc_time


DEPURTE_TIME = 2
WALKING_BONUS_TIME = 1
ID = 0

TRAVEL_TIME = 1


def predict_connections(graph_struct: Graph, start: int, dest: int):
    update_departure_times(graph_struct=graph_struct)
    routes, path = run_dijktra(graph_struct, start, dest)
    return convert_data(routes, path, graph_struct)

        

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
    return routes, path


def create_func(G: Graph):
    now = datetime.now()

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
                converted_time = relative_time.strftime('%Y-%m-%dT%H:%M:%S')
                chosen_line = ("W", walk_travel_time, converted_time)
            else:
                chosen_line = (soonest_departure[ID], travel_time, soonest_departure[DEPURTE_TIME])

        new_relative = G.nodes[u].get("relative_time", 0) + travel_time
        if new_relative <=  G.nodes[v].get("relative_time", 9999999999):
            G.nodes[v]["relative_time"] = new_relative
            d["chosen_line"] = chosen_line

        return travel_time

    return weight_cost_func

def convert_data(routes, path, G):
    datastruct = [{"route": [], "departure_time": 3, "arrival_time": 15, "coordinates": []}]

    travel_time = 0
    for i, route in enumerate(routes):
        if i==0:
            if isinstance(route[2],str):
                datastruct[0]["departure_time"] = route[2]
            else:
                datastruct[0]["departure_time"] = route[2].strftime("%Y-%m-%dT%H:%M:%S")

        if i == len(routes) - 1:
            if isinstance(route[2], str):
                datastruct[0]["arrival_time"] = route[2]
            else:
                datastruct[0]["arrival_time"] = route[2].strftime("%Y-%m-%dT%H:%M:%S")
        #unikalne wartosci
        datastruct[0]["route"].append(route[0])
    datastruct[0]["route"] = list(dict.fromkeys(datastruct[0]["route"]))
    for stop in path:
        datastruct[0]["coordinates"].append([G.nodes[stop]["location"]["Long"], G.nodes[stop]["location"]["Lat"]])

    return datastruct


if __name__ == "__main__":
    import json
    import networkx
    from networkx.readwrite import json_graph

    with open("../out.json") as f:
        G: DiGraph = networkx.node_link_graph(json.load(f))
        #G = G.subgraph([2021, 2019, 2017, 2072])
    routes, path = run_dijktra(G, 2072, 2021)
    convert_data(routes, path, G)

    #update_departure_times(graph_struct=Graph)