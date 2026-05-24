import random
import math

cities = {
    0: (2, 3),
    1: (5, 4),
    2: (1, 7),
    3: (6, 8),
    4: (9, 2),
    5: (4, 6),
    6: (8, 7),
    7: (3, 9)
}

POPULATION_SIZE = 30
GENERATIONS = 100
MUTATION_RATE = 0.05
TOURNAMENT_SIZE = 3


def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def total_distance(route, cities):
    dist = 0
    for i in range(len(route)):
        dist += distance(cities[route[i]], cities[route[(i + 1) % len(route)]])
    return dist


def fitness(route, cities):
    return 1 / total_distance(route, cities)


def initialize_population(size, num_cities):
    population = []
    base = list(range(num_cities))
    for _ in range(size):
        route = base[:]
        random.shuffle(route)
        population.append(route)
    return population


def roulette_wheel_selection(population, cities):
    scores = [fitness(r, cities) for r in population]
    total = sum(scores)
    pick = random.uniform(0, total)
    current = 0
    for route, score in zip(population, scores):
        current += score
        if current >= pick:
            return route
    return population[-1]


def tournament_selection(population, cities, k=3):
    selected = random.sample(population, k)
    selected.sort(key=lambda r: fitness(r, cities), reverse=True)
    return selected[0]


def select_parent(population, cities, method):
    if method == 'roulette':
        return roulette_wheel_selection(population, cities)
    else:
        return tournament_selection(population, cities, TOURNAMENT_SIZE)


def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size
    child[start:end] = parent1[start:end]

    pointer = 0
    for gene in parent2:
        if gene not in child:
            while child[pointer] is not None:
                pointer += 1
            child[pointer] = gene

    return child


def mutate(route, mutation_rate):
    route = route[:]
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]
    return route


def genetic_algorithm(cities, selection_method):
    num_cities = len(cities)
    population = initialize_population(POPULATION_SIZE, num_cities)
    best = min(population, key=lambda r: total_distance(r, cities))

    for gen in range(GENERATIONS):
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            p1 = select_parent(population, cities, selection_method)
            p2 = select_parent(population, cities, selection_method)
            child1 = crossover(p1[:], p2[:])
            child2 = crossover(p2[:], p1[:])
            child1 = mutate(child1, MUTATION_RATE)
            child2 = mutate(child2, MUTATION_RATE)
            new_population.extend([child1, child2])

        population = new_population[:POPULATION_SIZE]
        current_best = min(population, key=lambda r: total_distance(r, cities))
        if total_distance(current_best, cities) < total_distance(best, cities):
            best = current_best

        print(f"Generation {gen+1} | Best Distance: {total_distance(best, cities):.4f}")

    return best


def display_solution(best_route, cities, selection_method):
    print("\n--- Best Route Found ---")
    print(f"Selection Method: {selection_method}")
    print(f"Route: {best_route}")
    dist = total_distance(best_route, cities)
    print(f"Total Distance: {dist:.4f}")
    print(f"Fitness: {fitness(best_route, cities):.6f}")
    print("Route order:")
    for i in range(len(best_route)):
        city = best_route[i]
        next_city = best_route[(i + 1) % len(best_route)]
        print(f"  City {city} {cities[city]} -> City {next_city} {cities[next_city]}")


def main():
    print("Use default cities? (y/n): ", end="")
    choice = input().strip().lower()

    if choice == 'n':
        n = int(input("Enter number of cities: "))
        city_dict = {}
        for i in range(n):
            x, y = map(int, input(f"City {i} (x y): ").split())
            city_dict[i] = (x, y)
    else:
        city_dict = cities

    print("\nSelect selection method:")
    print("1. Roulette Wheel")
    print("2. Tournament")
    choice = input("Enter choice (1/2): ").strip()
    method = 'roulette' if choice == '1' else 'tournament'

    print(f"\nRunning GA for TSP with {method} selection...\n")
    best_route = genetic_algorithm(city_dict, method)
    display_solution(best_route, city_dict, method)


if __name__ == "__main__":
    main()
