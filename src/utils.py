import numpy as np

#costants - do not change
DISTANCE_MATRIX = np.load('/Users/amit/PycharmProjects/Tsp Project/data/distance_matrix.npy')
CITY_INDEX_MAP = np.load('/Users/amit/PycharmProjects/Tsp Project/data/city_index.npy', allow_pickle=True).item()


def get_distance(city1, city2):
    city1 = city1.capitalize()
    city2 = city2.capitalize()
    if city1 not in CITY_INDEX_MAP or city2 not in CITY_INDEX_MAP:
        raise ValueError(f"One or both cities not found: {city1}, {city2}")

    return DISTANCE_MATRIX[CITY_INDEX_MAP[city1], CITY_INDEX_MAP[city2]]


# Function to calculate the total distance of a given route
def calculate_total_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[CITY_INDEX_MAP[route[i]]][CITY_INDEX_MAP[route[i + 1]]]
    return total_distance
