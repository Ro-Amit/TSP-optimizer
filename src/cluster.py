from src.utils import get_distance, calculate_total_distance, DISTANCE_MATRIX, CITY_INDEX_MAP
from src.algorithms import brute_force_tsp

# Maximum distance for clustering
MAX_DISTANCE = 1000


# Function to cluster cities based on a maximum distance threshold
def cluster_cities(cities):
    clusters = []
    visited = set()

    for city in cities:
        if city in visited:
            continue
        cluster = [city]
        visited.add(city)
        for other_city in cities:
            if other_city not in visited:
                try:
                    distance = get_distance(city, other_city)
                    if distance <= MAX_DISTANCE:
                        cluster.append(other_city)
                        visited.add(other_city)
                except ValueError as e:
                    print(f"Distance calculation error for cities {city} and {other_city}: {e}")
        clusters.append(cluster)

    print(f"Clusters formed: {clusters}")
    return clusters


# Function to solve TSP for a single cluster using brute force
def solve_tsp_for_cluster(cluster):
    if len(cluster) <= 1:
        return cluster
    route, _ = brute_force_tsp(cluster, cluster[0], cluster[0])
    print(f"Route for cluster {cluster}: {route}")
    return route


# Main cluster-based TSP function
def cluster_tsp(cities, start_city, end_city):
    # Helper function to format city names
    def format_city_name(city):
        return city.strip().title()

    # Ensure proper formatting of city names
    cities = [format_city_name(city) for city in cities]
    start_city = format_city_name(start_city)
    end_city = format_city_name(end_city)

    if start_city not in cities:
        cities.append(start_city)
    if end_city not in cities:
        cities.append(end_city)

    # Validate that all cities are in the CITY_INDEX_MAP
    for city in cities:
        if city not in CITY_INDEX_MAP:
            raise ValueError(f"City not found in CITY_INDEX_MAP: {city}")

    # Divide cities into clusters based on the maximum distance threshold
    clusters = cluster_cities([city for city in cities if city not in {start_city, end_city}])

    # Solve the TSP for each cluster
    all_cluster_routes = []
    for cluster in clusters:
        cluster_route = solve_tsp_for_cluster(cluster)
        all_cluster_routes.append(cluster_route)

    print(f"All cluster routes: {all_cluster_routes}")

    # Create "super cities" by picking the first city from each cluster
    super_cities = [cluster[0] for cluster in clusters]
    if start_city not in super_cities:
        super_cities.insert(0, start_city)
    if end_city not in super_cities:
        super_cities.append(end_city)
    print(f"Super cities: {super_cities}")

    # Solve the TSP for the super cities (including start and end cities)
    super_city_route, _ = brute_force_tsp(super_cities, start_city, end_city)
    print(f"Super city route: {super_city_route}")

    # Reassemble the final route by ordering the cluster routes based on the super city route
    final_route = []
    visited = set()

    for city in super_city_route:
        for cluster_route in all_cluster_routes:
            if city in cluster_route and city not in visited:
                # Ensure each city (except start and end) appears only once
                for cluster_city in cluster_route:
                    if cluster_city not in visited:
                        final_route.append(cluster_city)
                        visited.add(cluster_city)

    # Ensure the route starts and ends correctly
    if start_city != end_city:
        final_route.insert(0, start_city)  # Ensure start city is at the beginning
        final_route.append(end_city)  # Ensure end city is at the end
    else:
        final_route.append(start_city)  # Close the loop for the start-end city

    min_distance = calculate_total_distance(final_route, DISTANCE_MATRIX)
    print(f"Final route: {final_route}, Total distance: {min_distance}")

    return final_route, min_distance
