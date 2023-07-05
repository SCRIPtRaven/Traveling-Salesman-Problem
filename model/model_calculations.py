import heapq
import random
import math

from model import model_data


DATA_LIST = model_data.read_data_from_csv()
METHOD = 1


def set_method(method):
    global METHOD
    METHOD = method


def get_method():
    return METHOD


def calculate_distance(point1, point2):
    x1, y1 = point1[1], point1[2]
    x2, y2 = point2[1], point2[2]
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


def calculate_route(contr):
    # use the appropriate method based on the checkbox value
    if METHOD == 1:
        return calculate_route_greedy(contr)
    else:
        return calculate_route_simplest(contr)


def calculate_route_simplest(contr):
    num_locations = len(DATA_LIST)
    distances = [[0.0] * num_locations for _ in range(num_locations)]
    for i in range(num_locations):
        for j in range(num_locations):
            distances[i][j] = calculate_distance(DATA_LIST[i], DATA_LIST[j])

    remaining_locations = set(range(num_locations)) - {contr.handle_position_selection()}
    current_location = contr.handle_position_selection()
    route = [current_location]

    while remaining_locations:
        # Get 10 closest locations from remaining locations.
        closest_locations = heapq.nsmallest(10, remaining_locations, key=lambda x: distances[current_location][x])
        # random.choice selects a random element from the closest_locations list
        next_location = random.choice(closest_locations)
        route.append(next_location)
        remaining_locations.remove(next_location)
        current_location = next_location

    return route


def calculate_route_greedy(contr):
    num_locations = len(DATA_LIST)
    distances = [[0.0] * num_locations for _ in range(num_locations)]
    for i in range(num_locations):
        for j in range(num_locations):
            distances[i][j] = calculate_distance(DATA_LIST[i], DATA_LIST[j])

    remaining_locations = set(range(num_locations)) - {contr.handle_position_selection()}
    current_location = contr.handle_position_selection()
    route = [current_location]

    while remaining_locations:
        nearest_location = min(remaining_locations, key=lambda x: distances[current_location][x])
        route.append(nearest_location)
        remaining_locations.remove(nearest_location)
        current_location = nearest_location

    return route


def calculate_total_distance(route):
    total_distance = 0
    for i in range(len(route) - 1):
        point1 = route[i]
        point2 = route[(i + 1) % len(route)]
        distance = calculate_distance(DATA_LIST[point1], DATA_LIST[point2])
        total_distance += distance
    return total_distance