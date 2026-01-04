import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Load the city data
cities_df = pd.read_csv('/Users/amit/PycharmProjects/Tsp Project/data/cities.csv')

# Extract latitudes, longitudes, and city names
latitudes = cities_df['Latitude'].values
longitudes = cities_df['Longitude'].values
city_names = cities_df['Capital City'].values

# Number of cities
n = len(city_names)

# Create a 2D matrix to store distances (n x n)
distance_matrix = np.zeros((n, n))

# Calculate distances between each pair of cities
for i in range(n):
    for j in range(i, n):  # Only compute the upper triangle (symmetrical matrix)
        if i != j:
            city1 = (latitudes[i], longitudes[i])
            city2 = (latitudes[j], longitudes[j])
            distance = geodesic(city1, city2).kilometers  # Calculate distance in kilometers
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance  # Symmetric matrix

# Print the distance matrix (Optional)
print(distance_matrix)

# Save the distance matrix to a file for future use
np.save('/Users/amit/PycharmProjects/Tsp Project/data/distance_matrix.npy', distance_matrix)

# Save city index mapping
city_to_index = {city: index for index, city in enumerate(city_names)}
np.save('/Users/amit/PycharmProjects/Tsp Project/data/city_index.npy', city_to_index)