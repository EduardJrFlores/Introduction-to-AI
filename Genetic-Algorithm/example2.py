import random
import string

TARGET      = "SirJoshIsTheBest"
CHARACTERS  = string.ascii_letters + string.digits + string.punctuation
POP_SIZE    = 100
MUTATION_RATE = 0.05

def random_chromosome():
    return [random.choice(CHARACTERS) for _ in TARGET]


def fitness(chrom):
    return sum(1 for a, b in zip(chrom, TARGET) if a == b)


def select(population, fitnesses):
    candidates = random.sample(list(zip(population, fitnesses)), 3)
    return max(candidates, key=lambda x: x[1])[0]


def crossover(parent1, parent2):
    point = random.randint(1, len(TARGET) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(chrom):
    return [
        random.choice(CHARACTERS) if random.random() < MUTATION_RATE else c
        for c in chrom
    ]


def genetic_algorithm():
    population = [random_chromosome() for _ in range(POP_SIZE)]
    history = []
    generation = 0

    while True:
        fitnesses = [fitness(c) for c in population]
        best_idx  = fitnesses.index(max(fitnesses))
        best_chrom = population[best_idx]
        best_fit   = fitnesses[best_idx]
        history.append((generation, best_fit, "".join(best_chrom)))

        if best_fit == len(TARGET):
            break

        new_pop = [best_chrom[:]]   # elitism
        while len(new_pop) < POP_SIZE:
            p1 = select(population, fitnesses)
            p2 = select(population, fitnesses)
            c1, c2 = crossover(p1, p2)
            new_pop.extend([mutate(c1), mutate(c2)])

        population = new_pop[:POP_SIZE]
        generation += 1

    return history

random.seed(42)
history = genetic_algorithm()
total_gens = history[-1][0]

print("Genetic Algorithm: Password Evolution")
print(f"Target     : {TARGET}")
print(f"Characters : a-z, A-Z, 0-9, punctuation ({len(CHARACTERS)} possible)")
print(f"Population : {POP_SIZE}  |  Mutation Rate: {MUTATION_RATE:.0%}")
print()

col = len(TARGET)

print("Evolution Progress:")
print(f"  {'Gen':>3}        {'Best Guess':<{col}}        {'Matched':<12}     {'Accuracy'}          {'Missing Characters'}")
print("--------------------------------------------------------------------------------------------")

milestones = set()
step = max(1, total_gens // 10)
for i in range(0, total_gens + 1, step):
    milestones.add(i)
milestones.add(total_gens)

for gen, fit, guess in history:
    if gen in milestones:
        accuracy = fit / len(TARGET)
        correct_chars = "".join(a if a == b else "·" for a, b in zip(guess, TARGET))
        print(f"  {gen:>3}     {guess:<{col}}      {fit:>2}/{len(TARGET)} characters       {accuracy:>4.0%}              {correct_chars}")

print()
print(f"Target reached at Generation : {total_gens}")
print(f"Final answer   : {''.join(history[-1][2])}")
print(f"Exact match    : {''.join(history[-1][2]) == TARGET}")