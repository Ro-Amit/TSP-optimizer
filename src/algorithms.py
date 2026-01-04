from src.utils import CITY_INDEX_MAP, DISTANCE_MATRIX, calculate_total_distance




# Recursive function to generate permutations of cities (helper for brute force)
def permute(cities, start=0):
   if start == len(cities) - 1:
       yield cities
   else:
       for i in range(start, len(cities)):
           cities[start], cities[i] = cities[i], cities[start]
           yield from permute(cities, start + 1)
           cities[start], cities[i] = cities[i], cities[start]  # backtrack




# Brute force TSP algorithm without itertools
def brute_force_tsp(cities, start_city, end_city):
   # Generate all permutations of the selected cities except the start and end cities
   selected_cities = [city for city in cities if city not in [start_city, end_city]]


   best_route = None
   min_distance = float('inf')


   # Handle both cases (start and end can be the same)
   if start_city == end_city:
       permutations = permute(selected_cities)


       for perm in permutations:
           route = [start_city] + list(perm) + [start_city]
           total_distance = calculate_total_distance(route, DISTANCE_MATRIX)
           if total_distance < min_distance:
               min_distance = total_distance
               best_route = route
   else:
       permutations = permute(selected_cities)


       for perm in permutations:
           route = [start_city] + list(perm) + [end_city]
           total_distance = calculate_total_distance(route, DISTANCE_MATRIX)
           if total_distance < min_distance:
               min_distance = total_distance
               best_route = route


   return best_route, min_distance




# Greedy TSP algorithm
def greedy_tsp(cities, start_city, end_city):
   current_city = start_city
   unvisited = set(cities) - {start_city}
   route = [current_city]
   total_distance = 0


   while unvisited:
       # Find the closest city
       next_city = min(unvisited, key=lambda city: DISTANCE_MATRIX[CITY_INDEX_MAP[current_city]][CITY_INDEX_MAP[city]])
       total_distance += DISTANCE_MATRIX[CITY_INDEX_MAP[current_city]][CITY_INDEX_MAP[next_city]]
       route.append(next_city)
       current_city = next_city
       unvisited.remove(next_city)


   if start_city != end_city:
       # Add the distance to the end city
       total_distance += DISTANCE_MATRIX[CITY_INDEX_MAP[current_city]][CITY_INDEX_MAP[end_city]]
       route.append(end_city)


   return route, total_distance

#cluster based algorithm

