import numpy as np
from src.utils import CITY_INDEX_MAP, DISTANCE_MATRIX


def validate_city_index_map(city_index_map):
    # Check for consistent formatting
    for city in city_index_map:
        if city != city.strip().title():
            print(f"Inconsistent formatting found: {city}")

    # Check for duplicates
    city_names = list(city_index_map.keys())
    if len(city_names) != len(set(city_names)):
        print("Duplicate city names found in CITY_INDEX_MAP")

    print("CITY_INDEX_MAP validation complete.")


def validate_distance_matrix(distance_matrix, city_index_map):
    num_cities = len(city_index_map)

    # Check dimensions
    if distance_matrix.shape != (num_cities, num_cities):
        print(f"Incorrect dimensions: {distance_matrix.shape}, expected: ({num_cities}, {num_cities})")

    # Check symmetry and non-negative values
    for i in range(num_cities):
        for j in range(num_cities):
            if distance_matrix[i, j] != distance_matrix[j, i]:
                print(f"Asymmetry found between indices {i} and {j}")
            if distance_matrix[i, j] < 0:
                print(f"Negative distance found between indices {i} and {j}")

    # Check self-distances
    for i in range(num_cities):
        if distance_matrix[i, i] != 0:
            print(f"Non-zero self-distance found at index {i}")

    print("DISTANCE_MATRIX validation complete.")


# Perform validations
validate_city_index_map(CITY_INDEX_MAP)
validate_distance_matrix(DISTANCE_MATRIX, CITY_INDEX_MAP)
