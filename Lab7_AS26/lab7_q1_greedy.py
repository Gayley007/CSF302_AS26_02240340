# Lab 7 - Q1: Activity selection and knapsack (greedy)
# Run with:  python lab7_q1_greedy.py

import random

random.seed(7)       # fixed seed, so the same results every run


# ===============================================================
# Part 1 and 2: Activity selection
# An activity is (start, finish). Two activities fit together if
# one finishes no later than the other starts.
# ===============================================================

def read_activities(filename):
    # each line of the file is "start finish", e.g. "1 4"
    activities = []
    with open(filename) as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2:
                activities.append((int(parts[0]), int(parts[1])))
    return activities


def pick_in_order(activities, order):
    # Go through the activities in the given order.
    # Take an activity if it does not overlap anything already taken.
    chosen = []
    for a in order:
        ok = True
        for c in chosen:
            # overlap if a starts before c finishes AND c starts before a finishes
            if a[0] < c[1] and c[0] < a[1]:
                ok = False
                break
        if ok:
            chosen.append(a)
    chosen.sort()                       # print them in time order
    return chosen


def get_finish(a):
    return a[1]


def get_start(a):
    return a[0]


def get_length(a):
    return a[1] - a[0]


def earliest_finish(activities):
    # the correct greedy rule: sort by finish time.
    # After sorting we only need to compare with the LAST activity taken.
    order = sorted(activities, key=get_finish)
    chosen = []
    last_finish = None
    for a in order:
        if last_finish is None or a[0] >= last_finish:
            chosen.append(a)
            last_finish = a[1]
    return chosen


def earliest_start(activities):
    return pick_in_order(activities, sorted(activities, key=get_start))


def shortest_duration(activities):
    return pick_in_order(activities, sorted(activities, key=get_length))


def random_activities(n):
    # n random activities: start 0..20, length 1..8
    acts = []
    for _ in range(n):
        start = random.randint(0, 20)
        acts.append((start, start + random.randint(1, 8)))
    return acts


def find_counterexample(rule, name):
    # Try random inputs until the rule picks FEWER activities than
    # earliest finish. Start with small inputs so the example is easy to read.
    for tries in range(1, 100001):
        n = random.randint(2, 5)
        acts = random_activities(n)
        good = earliest_finish(acts)
        bad = rule(acts)
        if len(bad) < len(good):
            print("  " + name + " (found after " + str(tries) + " random tries)")
            print("    activities      :", acts)
            print("    " + name + " picks :", bad, "->", len(bad))
            print("    earliest finish picks:", good, "->", len(good))
            return
    print("  no counterexample found for", name)


# ===============================================================
# Part 3: Fractional knapsack - take items by best value/weight first.
# An item is (value, weight). We may take part of the last item.
# ===============================================================

def get_ratio(item):
    return item[0] / item[1]


def fractional_knapsack(items, capacity):
    order = sorted(items, key=get_ratio, reverse=True)   # best ratio first
    total = 0.0
    room = capacity
    taken = []                              # (item, fraction taken)
    for item in order:
        if room == 0:
            break
        value, weight = item
        if weight <= room:                  # the whole item fits
            total += value
            room -= weight
            taken.append((item, 1.0))
        else:                               # take only the part that fits
            fraction = room / weight
            total += value * fraction
            taken.append((item, round(fraction, 3)))
            room = 0
    return total, taken


# ===============================================================
# Part 4: 0/1 knapsack - greedy (best ratio first, whole items only)
# compared with the correct DP answer.
# ===============================================================

def greedy_01(items, capacity):
    order = sorted(items, key=get_ratio, reverse=True)
    total = 0
    room = capacity
    for value, weight in order:
        if weight <= room:                  # take it only if it fits completely
            total += value
            room -= weight
    return total


def dp_01(items, capacity):
    # best[w] = best value using capacity w (one row, filled backwards
    # so each item is used at most once)
    best = [0] * (capacity + 1)
    for value, weight in items:
        for w in range(capacity, weight - 1, -1):
            if best[w - weight] + value > best[w]:
                best[w] = best[w - weight] + value
    return best[capacity]


if __name__ == "__main__":
    print("=== Part 1: earliest finish time ===")
    activities = read_activities("activities.txt")
    print("  activities (from activities.txt):", activities)
    chosen = earliest_finish(activities)
    print("  selected  :", chosen, "->", len(chosen), "activities")

    print("\n=== Part 2: other greedy rules (random search) ===")
    find_counterexample(earliest_start, "earliest start")
    find_counterexample(shortest_duration, "shortest duration")

    # also count how often each rule loses on 10,000 bigger random inputs
    lose_start = 0
    lose_short = 0
    for _ in range(10000):
        acts = random_activities(10)
        best = len(earliest_finish(acts))
        if len(earliest_start(acts)) < best:
            lose_start += 1
        if len(shortest_duration(acts)) < best:
            lose_short += 1
    print("  On 10,000 random inputs of 10 activities:")
    print("    earliest start loses   ", lose_start, "times")
    print("    shortest duration loses", lose_short, "times")

    print("\n=== Part 3: fractional knapsack ===")
    items = [(60, 10), (100, 20), (120, 30)]          # (value, weight)
    total, taken = fractional_knapsack(items, 50)
    print("  items (value, weight):", items, " capacity = 50")
    print("  taken (item, fraction):", taken)
    print("  total value =", total)

    print("\n=== Part 4: greedy vs DP on 0/1 knapsack ===")
    print("  same items, 0/1 version: greedy =", greedy_01(items, 50),
          " DP =", dp_01(items, 50))

    worst = 1.0
    worst_case = None
    for _ in range(10000):
        n = random.randint(1, 8)
        items = []
        for _ in range(n):
            items.append((random.randint(1, 50), random.randint(1, 20)))
        capacity = random.randint(5, 40)
        best = dp_01(items, capacity)
        if best == 0:
            continue                       # nothing fits, ratio not defined
        ratio = greedy_01(items, capacity) / best
        if ratio < worst:
            worst = ratio
            worst_case = (items, capacity, greedy_01(items, capacity), best)
    print("  10,000 random inputs (1-8 items)")
    print("  worst greedy/optimal ratio =", round(worst, 3))
    print("  worst input: items =", worst_case[0], " capacity =", worst_case[1])
    print("  greedy =", worst_case[2], " DP =", worst_case[3])

    # a hand-made input that makes greedy as bad as we like
    items = [(2, 1), (100, 100)]
    print("  hand-made: items =", items, " capacity = 100 -> greedy =",
          greedy_01(items, 100), " DP =", dp_01(items, 100))
