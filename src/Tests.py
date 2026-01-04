import numpy as np
import time
from src.algorithms import brute_force_tsp, greedy_tsp  # Ensure these algorithms are defined in your algorithms.py
from src.utils import CITY_INDEX_MAP


def get_random_cities(num_cities):
    """Get a random sample of cities from the CITY_INDEX_MAP."""
    city_names = list(CITY_INDEX_MAP.keys())
    selected_cities = np.random.choice(city_names, size=num_cities, replace=False)
    return selected_cities


def run_tests(num_tests=10, num_cities=5):
    """Run multiple tests to compare brute force and greedy algorithms."""
    results = []

    for _ in range(num_tests):
        # Randomly select a set of cities for this test
        selected_cities = get_random_cities(num_cities)
        start_city = selected_cities[0]
        end_city = selected_cities[-1]  # or you can choose any other logic for start and end

        # Test Brute Force Algorithm
        start_time = time.time()
        bf_route, bf_distance = brute_force_tsp(selected_cities, start_city, end_city)
        bf_time = time.time() - start_time

        # Test Greedy Algorithm
        start_time = time.time()
        greedy_route, greedy_distance = greedy_tsp(selected_cities, start_city, end_city)
        greedy_time = time.time() - start_time

        # Accuracy Check
        accuracy = "Correct" if greedy_distance <= bf_distance else "Incorrect"

        # Store results
        results.append({
            'test': len(results) + 1,
            'bf_time': bf_time,
            'bf_distance': bf_distance,
            'greedy_time': greedy_time,
            'greedy_distance': greedy_distance,
            'accuracy': accuracy,
            'selected_cities': selected_cities.tolist()  # Store the selected cities for reference
        })

    # Print results summary
    print("Test Results Summary:")
    for result in results:
        print(f"Test {result['test']}: "
              f"Brute Force Time: {result['bf_time']:.4f}s, "
              f"Brute Force Distance: {result['bf_distance']}, "
              f"Greedy Time: {result['greedy_time']:.4f}s, "
              f"Greedy Distance: {result['greedy_distance']}, "
              f"Accuracy: {result['accuracy']}, "
              f"Cities: {result['selected_cities']}")

    # Analyze the results to find average times/distances, etc.
    analyze_results(results)


def analyze_results(results):
    """Analyze and print average results."""
    bf_times = [result['bf_time'] for result in results]
    bf_distances = [result['bf_distance'] for result in results]
    greedy_times = [result['greedy_time'] for result in results]
    greedy_distances = [result['greedy_distance'] for result in results]

    print("\nAverage Results:")
    print(f"Average Brute Force Time: {np.mean(bf_times):.4f}s")
    print(f"Average Brute Force Distance: {np.mean(bf_distances)}")
    print(f"Average Greedy Time: {np.mean(greedy_times):.4f}s")
    print(f"Average Greedy Distance: {np.mean(greedy_distances)}")

    # Consider the number of correct predictions
    correct_count = sum(1 for result in results if result['accuracy'] == "Correct")
    print(f"Greedy Algorithm Accuracy: {correct_count}/{len(results)} tests correct.")


if __name__ == "__main__":
    run_tests(num_tests=100, num_cities=15)  # Adjust the number of tests and cities as needed

    # Note: The implementation is without Ant Colony Optimization (ACO) algorithm
