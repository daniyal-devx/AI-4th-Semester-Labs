import random

items = [
    (2, 12), (1, 10), (3, 20), (2, 15), (4, 25),
    (5, 30), (7, 42), (6, 35), (3, 18), (2, 14),
    (8, 50), (9, 55), (4, 24), (5, 28), (1, 8),
    (6, 33), (7, 40), (3, 16), (2, 11), (4, 22),
    (10, 60), (9, 52), (5, 29), (6, 34), (2, 13),
    (1, 7), (8, 48), (7, 39), (3, 19), (4, 23)
]

MAX_WEIGHT = 60
POPULATION_SIZE = 30
MUTATION_RATE = 0.05
GENERATIONS = 50
TOURNAMENT_SIZE = 3


def get_user_input():
    print("Use default dataset? (y/n): ", end="")
    choice = input().strip().lower()
    if choice == 'y':
        return items, MAX_WEIGHT

    n = int(input("Enter number of items: "))
    custom_items = []
    for i in range(n):
        w, v = map(int, input(f"Item {i+1} (weight value): ").split())
        custom_items.append((w, v))
    cap = int(input("Enter knapsack capacity: "))
    return custom_items, cap


def initialize_population(size, num_items):
    return [[random.randint(0, 1) for _ in range(num_items)] for _ in range(size)]


def calculate_weight(chromosome, items):
    return sum(chromosome[i] * items[i][0] for i in range(len(items)))


def fitness(chromosome, items, max_weight):
    total_weight = calculate_weight(chromosome, items)
    if total_weight > max_weight:
        return 0
    return sum(chromosome[i] * items[i][1] for i in range(len(items)))


def roulette_wheel_selection(population, items, max_weight):
    scores = [fitness(c, items, max_weight) for c in population]
    total = sum(scores)
    if total == 0:
        return random.choice(population)
    pick = random.uniform(0, total)
    current = 0
    for chromosome, score in zip(population, scores):
        current += score
        if current >= pick:
            return chromosome
    return population[-1]


def tournament_selection(population, items, max_weight, k=3):
    selected = random.sample(population, k)
    selected.sort(key=lambda c: fitness(c, items, max_weight), reverse=True)
    return selected[0]


def select_parent(population, items, max_weight, method):
    if method == 'roulette':
        return roulette_wheel_selection(population, items, max_weight)
    else:
        return tournament_selection(population, items, max_weight, TOURNAMENT_SIZE)


def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]
    return chromosome


def genetic_algorithm(items, max_weight, selection_method):
    population = initialize_population(POPULATION_SIZE, len(items))
    best = max(population, key=lambda c: fitness(c, items, max_weight))

    for gen in range(GENERATIONS):
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            p1 = select_parent(population, items, max_weight, selection_method)
            p2 = select_parent(population, items, max_weight, selection_method)
            c1, c2 = crossover(p1[:], p2[:])
            c1 = mutate(c1, MUTATION_RATE)
            c2 = mutate(c2, MUTATION_RATE)
            new_population.extend([c1, c2])

        population = new_population[:POPULATION_SIZE]
        current_best = max(population, key=lambda c: fitness(c, items, max_weight))
        if fitness(current_best, items, max_weight) > fitness(best, items, max_weight):
            best = current_best

        print(f"Generation {gen+1} | Best Fitness: {fitness(best, items, max_weight)}")

    return best


def display_solution(solution, items, max_weight, selection_method):
    print("\n--- Best Solution ---")
    print(f"Selection Method: {selection_method}")
    print(f"Chromosome: {solution}")
    total_weight = calculate_weight(solution, items)
    total_value = fitness(solution, items, max_weight)
    print(f"Total Weight: {total_weight}")
    print(f"Total Value: {total_value}")
    print("Selected Items (index, weight, value):")
    for i in range(len(solution)):
        if solution[i] == 1:
            print(f"  Item {i+1}: weight={items[i][0]}, value={items[i][1]}")


def main():
    item_list, capacity = get_user_input()

    print("\nSelect selection method:")
    print("1. Roulette Wheel")
    print("2. Tournament")
    choice = input("Enter choice (1/2): ").strip()
    method = 'roulette' if choice == '1' else 'tournament'

    print(f"\nRunning Genetic Algorithm with {method} selection...\n")
    best = genetic_algorithm(item_list, capacity, method)
    display_solution(best, item_list, capacity, method)


if __name__ == "__main__":
    main()
