import random
import numpy as np
from utils import CITY_INDEX_MAP


def generate_city_list(size):
    city_names = list(CITY_INDEX_MAP.keys())

    if size > len(city_names):
        raise ValueError("Requested size exceeds available city list")

    random.shuffle(city_names)
    cities = city_names[:size]
    start_city = random.choice(cities)
    end_city = random.choice(cities)

    return cities, start_city, end_city

