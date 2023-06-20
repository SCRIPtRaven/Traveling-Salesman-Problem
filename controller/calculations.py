import random
import math

from model import model_data


DATA_LIST = model_data.read_data_from_csv()


def calculate_distance(point1, point2):
    return math.sqrt((point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)


def calculate_route():
    if len(DATA_LIST) <= 2:
        return DATA_LIST

    # Create a copy of the data list to avoid modifying the original list
    remaining_points = DATA_LIST[:]

    # Start with the specified start location
    current_point = remaining_points.pop(0)
    route = [current_point]

    while remaining_points:
        if len(remaining_points) == 1:
            next_point = remaining_points.pop(0)
        else:
            # Select the next point based on the chosen method (Greedy or Random)
            method = method.get()
            if method == 1:  # Greedy
                next_point = find_nearest_neighbor(current_point, remaining_points)
            else:  # Random
                next_point = random.choice(remaining_points)

            remaining_points.remove(next_point)
        route.append(next_point)
        current_point = next_point

    return route


def find_nearest_neighbor(point, points):
    min_distance = float('inf')
    nearest_neighbor = None
    for neighbor in points:
        distance = calculate_distance(point, neighbor)
        if distance < min_distance:
            min_distance = distance
            nearest_neighbor = neighbor
    return nearest_neighbor


def calculate_total_distance(route):
    total_distance = 0
    for i in range(len(route)):
        point1 = route[i]
        point2 = route[(i + 1) % len(route)]
        distance = calculate_distance(point1, point2)
        total_distance += distance
    return total_distance