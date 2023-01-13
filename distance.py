import json
from math import radians, sin, cos
from math import atan2, sqrt


def calc_time(geolocationA: dict, geolocationB: dict) -> float:
    R = 6373.0
    walking_speed_minutes_per_kilometr = 15

    lat1 = radians(geolocationA["Lat"])
    lon1 = radians(geolocationA["Lon"])
    lat2 = radians(geolocationB["Lat"])
    lon2 = radians(geolocationB["Lon"])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance * walking_speed_minutes_per_kilometr


# data = json.load(open("busStops.json"))
# result = {stop_id: {stop_id: 0 for stop_id in data.keys() } for stop_id in data.keys() }
# for stop_id_A in result.keys():
#     for stop_id_B in result[stop_id_A].keys():
#         result[stop_id_A][stop_id_B] = calc_time(data[stop_id_A], data[stop_id_B])
# print(result)

if __name__ == "__main__":
    print("dupe")