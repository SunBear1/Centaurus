import json
import networkx
from pyvis.network import Network
import requests
from datetime import datetime
from collections import OrderedDict
import matplotlib.pyplot as plt

BUS_STOP_DETAILS = {}


def update_node_estimated_departures(graph) -> list:
    for key in BUS_STOP_DETAILS.keys():
        graph.nodes(key)




def read_routes_to_graph() -> list:
    routes_url = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/22313c56-5acf-41c7-a5fd-dc5dc72b3851/download/routes.json"

    today = str(datetime.today().date())
    r = requests.get(routes_url)

    routes = r.json()[today]["routes"]

    routes_ids = [route["routeId"] for route in routes]

    return routes_ids


def get_bus_stop_details():
    URL = "https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/d3e96eb6-25ad-4d6c-8651-b1eb39155945/download/stopsingdansk.json"
    r = requests.get(URL)

    stops = r.json()["stops"]

    for stop in stops:
        details = {
            "name": stop["stopName"],
            "location": {"Lat": stop["stopLat"], "Long": stop["stopLon"]},
        }
        BUS_STOP_DETAILS[stop["stopId"]] = details


def create_graph(routes, date):
    j = 1
    connections = dict()
    G = networkx.DiGraph()
    for route in routes:
        r = requests.get(
            url=f"https://ckan2.multimediagdansk.pl/stopTimes?date={date}&routeId={route}"
        )
        response_data = r.json()
        for i in range(len(response_data["stopTimes"]) - 1):
            if response_data["stopTimes"][i]["passenger"]:
                if response_data["stopTimes"][i]["stopId"] not in connections:
                    connections[response_data["stopTimes"][i]["stopId"]] = [
                        {
                            "routeId": response_data["stopTimes"][i]["routeId"],
                            "scheduledDepartureTime": f'{date}T{response_data["stopTimes"][i]["departureTime"][12:]}',
                            "estimatedDepartureTime": f'{date}T{response_data["stopTimes"][i]["departureTime"][12:]}',
                        }
                    ]
                else:
                    connections[response_data["stopTimes"][i]["stopId"]].append(
                        {
                            "routeId": response_data["stopTimes"][i]["routeId"],
                            "scheduledDepartureTime": f'{date}T{response_data["stopTimes"][i]["departureTime"][12:]}',
                            "estimatedDepartureTime": f'{date}T{response_data["stopTimes"][i]["departureTime"][12:]}',
                        }
                    )

        bus_stops = OrderedDict()
        for i in range(len(response_data["stopTimes"]) - 1):
            stop_id = response_data["stopTimes"][i]["stopId"]
            if (
                    response_data["stopTimes"][i]["passenger"] == True
                    and stop_id in BUS_STOP_DETAILS
            ):
                bus_stops[stop_id] = {
                    "label": BUS_STOP_DETAILS[stop_id]["name"],
                    "connections": connections[response_data["stopTimes"][i]["stopId"]],
                    "dep_time": response_data["stopTimes"][i]["departureTime"],
                    "location": {
                        "Lat": BUS_STOP_DETAILS[stop_id]["location"]["Lat"],
                        "Long": BUS_STOP_DETAILS[stop_id]["location"]["Long"],
                    },
                }
        bus_stops = list(bus_stops.items())
        if j == 100:
            pass
        for i in range(len(bus_stops) - 1):
            G.add_node(
                bus_stops[i][0], **bus_stops[i][1]
            )
            G.add_node(
                bus_stops[i + 1][0],
                **bus_stops[i + 1][1]
            )
            if G.get_edge_data(bus_stops[i][0], bus_stops[i + 1][0]) is not None:
                routes_on_edge = [route] + G.get_edge_data(bus_stops[i][0], bus_stops[i + 1][0])["routes"]
            else:
                routes_on_edge = [route]

            G.add_edge(
                bus_stops[i][0],
                bus_stops[i + 1][0],
                routes=routes_on_edge,
                time=(
                        (
                                datetime.strptime(
                                    bus_stops[i + 1][1]["dep_time"], "%Y-%m-%dT%H:%M:%S"
                                )
                                - datetime.strptime(
                            bus_stops[i][1]["dep_time"], "%Y-%m-%dT%H:%M:%S"
                        )
                        ).seconds
                        / 60
                ),
            )
        print(f"{j}/{len(routes)}", " completed")
        j = j + 1
    return G


get_bus_stop_details()
G = create_graph(routes=read_routes_to_graph(), date="2023-01-13")
graph = json.dumps(networkx.node_link_data(G))

with open("../out.json", "w", encoding="utf-8") as outfile:
    outfile.write(graph)


# networkx.draw(G, with_labels=True)
# plt.savefig("filename.png")

net = Network(notebook=False)
net.from_nx(G)
net.show("example.html")
