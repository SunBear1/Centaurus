import networkx
import networkx as nx
from fontTools.varLib.plot import stops
from networkx import Graph
from graph import BUS_STOP_DETAILS

def predict_connections(graph_struct: Graph, start: int, dest: int):
    update_departure_times(graph_struct=graph_struct)
    run_dijktra()
        

def update_departure_times(graph_struct):
    for stop in BUS_STOP_DETAILS.keys():
        print(stop)
        

def run_dijktra(graph_struct: Graph, start: int, dest: int):
    return networkx.dijkstra_path(Graph, start, dest)


def creat_func(G: Graph):
    NO
    def weight_cost_func(u, v, d):
        connection_A = G.nodes[u]["attr"].get("connections")
        connection_B = G.nodes[v]["attr"].get("connections")
        possible_routes = set()
        for route in connection_B:
            possible_routes = None
        print(G.nodes[u])
        print(connection_A)
        node_v_wt = G.nodes[v].get("node_weight", 1)
        edge_wt = d.get("weight", 1)
        return 1

    return weight_cost_func


if __name__ == "__main__":
    update_departure_times(graph_struct=Graph)