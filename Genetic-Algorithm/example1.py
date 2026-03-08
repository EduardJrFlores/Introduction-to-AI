import random

TASKS = [
    {"name": "Team Standup",      "duration": 1},
    {"name": "Client Meeting",    "duration": 2},
    {"name": "Code Review",       "duration": 1},
    {"name": "Sprint Planning",   "duration": 2},
    {"name": "Design Review",     "duration": 1},
    {"name": "QA Testing",        "duration": 2},
    {"name": "Deployment",        "duration": 1},
]

TIME_SLOTS  = [8, 9, 10, 11, 13, 14, 15, 16, 17, 18]
SLOT_LABELS = {8:"8AM", 9:"9AM", 10:"10AM", 11:"11AM", 13:"1PM", 14:"2PM", 15:"3PM", 16:"4PM", 17:"5PM", 18:"6PM"}

POP_SIZE    = 20
GENERATIONS = 100
MUTATION_RATE = 0.2

def random_chromosome():
    return [random.choice(TIME_SLOTS) for _ in TASKS]


def fitness(chrom):
    score = 100
    slot_usage = {}
    for i, slot in enumerate(chrom):
        dur = TASKS[i]["duration"]
        occupied = list(range(slot, slot + dur))
        for hour in occupied:
            if hour in slot_usage:
                score -= 20
            slot_usage[hour] = slot_usage.get(hour, 0) + 1

    score += len(set(chrom)) * 3
    return max(score, 0)


def select(population, fitnesses):
    candidates = random.sample(list(zip(population, fitnesses)), 3)
    return max(candidates, key=lambda x: x[1])[0]


def crossover(parent1, parent2):
    point = random.randint(1, len(TASKS) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(chrom):
    chrom = chrom[:]
    for i in range(len(chrom)):
        if random.random() < MUTATION_RATE:
            chrom[i] = random.choice(TIME_SLOTS)
    return chrom


def genetic_algorithm():
    population = [random_chromosome() for _ in range(POP_SIZE)]
    best_ever = None
    best_fitness_ever = -1
    history = []

    for gen in range(GENERATIONS):
        fitnesses = [fitness(c) for c in population]
        best_idx = fitnesses.index(max(fitnesses))
        best_chrom = population[best_idx]
        best_fit   = fitnesses[best_idx]

        if best_fit > best_fitness_ever:
            best_fitness_ever = best_fit
            best_ever = best_chrom[:]

        history.append(best_fit)

        new_pop = [best_chrom[:]]
        while len(new_pop) < POP_SIZE:
            p1 = select(population, fitnesses)
            p2 = select(population, fitnesses)
            c1, c2 = crossover(p1, p2)
            new_pop.extend([mutate(c1), mutate(c2)])

        population = new_pop[:POP_SIZE]

    return best_ever, best_fitness_ever, history


random.seed(42)
best, score, history = genetic_algorithm()

print("Genetic Algorithm: Employee Task Scheduler")
print(f"Tasks: {len(TASKS)}  |  Time Slots: {len(TIME_SLOTS)}  |  Population: {POP_SIZE}  |  Generations: {GENERATIONS}")
print()

def print_gen(g, fitness):
    bar_len = int((fitness / 130) * 30)
    bar = "█" * bar_len + "░" * (30 - bar_len)
    print(f"  Generation {g:3d}  {bar}  {fitness}")

print("Fitness Progress (every 10 generations):")
print_gen(1, history[0])
for g in range(10, GENERATIONS + 1, 10):
    print_gen(g, history[g-1])

print()
print(f"Best Fitness Score : {score}")
print()

print("Optimal Schedule:")
print(f"  {'Time':<8}  {'Task':<22}  {'Duration'}")
print("  " + "─" * 42)
schedule = sorted(zip(best, TASKS), key=lambda x: x[0])
for slot, task in schedule:
    end = slot + task["duration"]
    end_label = SLOT_LABELS.get(end, f"{end}:00")
    print(f"  {SLOT_LABELS[slot]:<8}  {task['name']:<22}  {task['duration']}h  ({SLOT_LABELS[slot]} – {end_label})")

print()

slot_usage = {}
for i, slot in enumerate(best):
    dur = TASKS[i]["duration"]
    for hour in range(slot, slot + dur):
        slot_usage[hour] = slot_usage.get(hour, []) + [TASKS[i]["name"]]

conflicts = {h: tasks for h, tasks in slot_usage.items() if len(tasks) > 1}
if conflicts:
    print("Conflicts detected:")
    for hour, tasks in conflicts.items():
        print(f"  {hour}:00 — {', '.join(tasks)} overlap")
else:
    print("No conflicts — all tasks fit without overlap.")