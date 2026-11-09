# Assignment 4 - Part C: analysis
# Run with:  python analysis.py
# It prints the results, writes them to results.md and saves graph_ratios.png.

import random
from booking import greedy_earliest_finish, greedy_highest_fee, best_schedule

random.seed(340)          # fixed seed, so we get the same numbers every run

lines = []                # text that goes into results.md


def report(text):
    # print a line and also keep it for results.md
    print(text)
    lines.append(text)


# ---------- C1: counterexamples ----------

report("# Assignment 4 - Results\n")
report("## C1. Counterexamples\n")

example1 = [(0, 2, 1000), (1, 5, 5000)]
report("Earliest finish: requests = " + str(example1))
report("- greedy_earliest_finish = " + str(greedy_earliest_finish(example1)))
report("- best_schedule          = " + str(best_schedule(example1)) + "\n")

example2 = [(0, 10, 5000), (0, 5, 3000), (5, 10, 3000)]
report("Highest fee: requests = " + str(example2))
report("- greedy_highest_fee = " + str(greedy_highest_fee(example2)))
report("- best_schedule      = " + str(best_schedule(example2)) + "\n")


# ---------- C3: revenue ratios on 1,000 random inputs of 50 requests ----------

def random_requests(n):
    # start between 0 and 100 hours, event lasts 1 to 20 hours,
    # fee between Nu 500 and Nu 10,000 (steps of 500)
    requests = []
    for _ in range(n):
        start = random.randint(0, 100)
        finish = start + random.randint(1, 20)
        fee = random.randint(1, 20) * 500
        requests.append((start, finish, fee))
    return requests


ratios_finish = []        # greedy_earliest_finish / optimal, for each input
ratios_fee = []           # greedy_highest_fee / optimal, for each input
times_finish_optimal = 0  # how many times each greedy rule hit the optimum
times_fee_optimal = 0

for _ in range(1000):
    requests = random_requests(50)
    best = best_schedule(requests)[0]
    g1 = greedy_earliest_finish(requests)[0]
    g2 = greedy_highest_fee(requests)[0]
    ratios_finish.append(g1 / best)
    ratios_fee.append(g2 / best)
    if g1 == best:
        times_finish_optimal = times_finish_optimal + 1
    if g2 == best:
        times_fee_optimal = times_fee_optimal + 1

report("## C3. Greedy revenue / optimal revenue (1,000 inputs, 50 requests each)\n")
report("| Rule | Average ratio | Worst ratio | Inputs where greedy was optimal |")
report("|---|---|---|---|")
report("| Earliest finish | %.3f | %.3f | %d / 1000 |"
       % (sum(ratios_finish) / 1000, min(ratios_finish), times_finish_optimal))
report("| Highest fee | %.3f | %.3f | %d / 1000 |"
       % (sum(ratios_fee) / 1000, min(ratios_fee), times_fee_optimal))
report("| DP (best_schedule) | 1.000 | 1.000 | 1000 / 1000 |")

with open("results.md", "w") as f:
    f.write("\n".join(lines) + "\n")


# ---------- Graph: how the ratios are spread out ----------

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 4.5))
bins = [0.40 + 0.025 * k for k in range(25)]       # 0.40 to 1.00
plt.hist(ratios_finish, bins=bins, alpha=0.6, label="Earliest finish")
plt.hist(ratios_fee, bins=bins, alpha=0.6, label="Highest fee")
plt.axvline(1.0, color="black", linestyle="--", label="Optimal (DP) = 1.0")
plt.xlabel("Greedy revenue / optimal revenue")
plt.ylabel("Number of inputs (out of 1,000)")
plt.title("How close each greedy rule gets to the best revenue (n = 50)")
plt.legend()
plt.tight_layout()
plt.savefig("graph_ratios.png", dpi=120)
print("Saved graph_ratios.png")
