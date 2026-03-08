import collections
import itertools

PLAYLISTS = [
    ["Kalapastangan", "Pahina", "I Just Might"],
    ["Pahina", "I Just Might"],
    ["Kalapastangan", "I Just Might", "Leonora"],
    ["Pahina", "Leonora"],
    ["Kalapastangan", "Pahina"],
    ["I Just Might", "Leonora", "Kahel na langit"],
    ["Pahina", "I Just Might", "Kahel na langit"],
    ["Kalapastangan", "Leonora"],
    ["Pahina", "Kahel na langit"],
    ["Kalapastangan", "Pahina", "Leonora"],
]

MIN_SUPPORT    = 0.30
MIN_CONFIDENCE = 0.60


def get_support(itemset, transactions):
    return sum(1 for t in transactions if itemset.issubset(t)) / len(transactions)


def apriori(playlists, min_sup, min_conf):
    transactions = [frozenset(p) for p in playlists]

    counts = collections.Counter(song for p in transactions for song in p)
    frequent = {}
    current = []
    for song, count in counts.items():
        sup = count / len(transactions)
        if sup >= min_sup:
            fs = frozenset([song])
            frequent[fs] = sup
            current.append(fs)

    k = 2
    while current:
        candidates = set()
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                union = current[i] | current[j]
                if len(union) == k:
                    candidates.add(union)

        next_level = {}
        for candidate in candidates:
            sup = get_support(candidate, transactions)
            if sup >= min_sup:
                next_level[candidate] = sup

        frequent.update(next_level)
        current = list(next_level.keys())
        k += 1

    rules = []
    for itemset, sup in frequent.items():
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for antecedent in map(frozenset, itertools.combinations(itemset, size)):
                consequent = itemset - antecedent
                ant_sup = frequent.get(antecedent, get_support(antecedent, transactions))
                cons_sup = frequent.get(consequent, get_support(consequent, transactions))
                confidence = sup / ant_sup
                lift = confidence / cons_sup
                if confidence >= min_conf:
                    rules.append((set(antecedent), set(consequent), sup, confidence, lift))

    return frequent, rules


frequent, rules = apriori(PLAYLISTS, MIN_SUPPORT, MIN_CONFIDENCE)

print("A-Priori: Streaming Music Playlists")
print(f"Transactions: {len(PLAYLISTS)}  |  Min Support: {MIN_SUPPORT:.0%}  |  Min Confidence: {MIN_CONFIDENCE:.0%}")
print()

print("Frequent Itemsets:")
for itemset, sup in sorted(frequent.items(), key=lambda x: -x[1]):
    print(f"  {set(itemset)}  ->  support = {sup:.2f} -- {sup:.0%}")

print()
print("Association Rules:")
for ant, cons, sup, conf, lift in sorted(rules, key=lambda x: -x[3]):
    print(
        f"  if they listen to {ant}, they might also listen to {cons}\n"
        f"    support = {sup:.0%}  confidence = {conf:.0%}  lift = {lift:.2f}\n"
    )