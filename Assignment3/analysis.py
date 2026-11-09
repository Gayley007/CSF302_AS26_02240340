# Assignment 3 - Part C: timing experiments
# Run with:  python analysis.py
# It prints all tables, saves them in results.md, and saves 4 graphs (PNG).

import random
import sys
import time
import matplotlib.pyplot as plt
from sorts import quicksort_basic, quicksort_improved

random.seed(340)    # same random numbers every run

# Everything we print is also saved here and written to results.md at the end.
output_lines = []


def show(text=""):
    print(text)
    output_lines.append(text)


def make_list(kind, n):
    # Build one of the three input types.
    if kind == "random":
        return [random.randint(0, 1000000) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "duplicates":
        return [random.randint(0, 9) for _ in range(n)]   # only values 0..9


def time_sort(sort_function, data):
    # Run the sort 3 times on fresh copies and keep the fastest time.
    # If it crashes with RecursionError, return the text "RecursionError".
    best = None
    for _ in range(3):
        my_list = data.copy()
        start = time.perf_counter()
        try:
            sort_function(my_list)
        except RecursionError:
            return "RecursionError"
        seconds = time.perf_counter() - start
        if best is None or seconds < best:
            best = seconds
    return best


def as_text(t):
    # Turn a time into text for the table (crashes stay as text).
    if t == "RecursionError":
        return t
    return f"{t:.4f}"


# =====================================================================
# C1. Basic vs improved on random, sorted and duplicate inputs
# =====================================================================
sizes = [1000, 2000, 4000, 8000, 16000, 32000, 64000]
kinds = ["random", "sorted", "duplicates"]

show("# Assignment 3 results")
show(f"Python {sys.version.split()[0]}, recursion limit {sys.getrecursionlimit()}, "
     "best of 3 runs, times in seconds.")
show()
show("## C1. Time for each input type")

basic_times = {}       # e.g. basic_times["sorted"] = [time for each n]
improved_times = {}

for kind in kinds:
    basic_times[kind] = []
    improved_times[kind] = []
    show()
    show(f"### Input: {kind}")
    show("| n | quicksort_basic | quicksort_improved |")
    show("|---|---|---|")
    for n in sizes:
        data = make_list(kind, n)
        tb = time_sort(quicksort_basic, data)
        ti = time_sort(quicksort_improved, data)
        basic_times[kind].append(tb)
        improved_times[kind].append(ti)
        show(f"| {n} | {as_text(tb)} | {as_text(ti)} |")

# Graph 1: one small chart per input type.
plt.figure(figsize=(15, 4.5))
for number, kind in enumerate(kinds):
    plt.subplot(1, 3, number + 1)

    # Only plot the basic times that did NOT crash.
    ok_sizes = []
    ok_times = []
    for n, t in zip(sizes, basic_times[kind]):
        if t != "RecursionError":
            ok_sizes.append(n)
            ok_times.append(t)

    plt.plot(ok_sizes, ok_times, marker="o", label="quicksort_basic (missing points = crash)")
    plt.plot(sizes, improved_times[kind], marker="s", label="quicksort_improved")
    plt.title(f"Input: {kind}")
    plt.xlabel("n (number of items)")
    plt.ylabel("Time (seconds)")
    plt.grid(True)
    plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig("graph1_input_types.png")
plt.close()


# =====================================================================
# C2. Show that quicksort_basic is O(n^2) on sorted input.
#     We raise the recursion limit so it can finish instead of crashing.
# =====================================================================
sys.setrecursionlimit(20000)

show()
show("## C2. quicksort_basic on sorted input (recursion limit raised to 20000)")
show()
show("| n | time (s) | time / previous time |")
show("|---|---|---|")

worst_sizes = [1000, 2000, 4000, 8000, 16000]
worst_times = []
for n in worst_sizes:
    my_list = list(range(n))                 # already sorted = worst case
    start = time.perf_counter()
    quicksort_basic(my_list)
    worst_times.append(time.perf_counter() - start)

for k in range(len(worst_sizes)):
    if k == 0:
        ratio = "-"
    else:
        ratio = f"{worst_times[k] / worst_times[k - 1]:.2f}"   # about 4 means O(n^2)
    show(f"| {worst_sizes[k]} | {worst_times[k]:.4f} | {ratio} |")

sys.setrecursionlimit(1000)                  # back to normal

# Graph 2: measured times and a c*n^2 curve for comparison.
c = worst_times[-1] / worst_sizes[-1] ** 2
n_squared_curve = [c * n * n for n in worst_sizes]
plt.figure(figsize=(7, 4.5))
plt.plot(worst_sizes, worst_times, marker="o", label="quicksort_basic on sorted input")
plt.plot(worst_sizes, n_squared_curve, "--", label="c * n^2")
plt.title("C2: worst case is O(n^2)")
plt.xlabel("n (number of items)")
plt.ylabel("Time (seconds)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("graph2_worst_case.png")
plt.close()


# =====================================================================
# C3. Which cutoff is best? (n = 100,000 random values)
# =====================================================================
show()
show("## C3. Cutoff test, n = 100000 random values")
show()
show("| cutoff | time (s) |")
show("|---|---|")

cutoffs = [1, 4, 8, 16, 32, 64]
cutoff_times = []
data = make_list("random", 100000)
for cutoff in cutoffs:
    best = None
    for _ in range(5):                       # 5 runs, keep the fastest
        my_list = data.copy()
        start = time.perf_counter()
        quicksort_improved(my_list, cutoff)
        seconds = time.perf_counter() - start
        if best is None or seconds < best:
            best = seconds
    cutoff_times.append(best)
    show(f"| {cutoff} | {best:.4f} |")

best_cutoff = cutoffs[cutoff_times.index(min(cutoff_times))]
show()
show(f"Best cutoff: {best_cutoff}")

# Graph 3
plt.figure(figsize=(7, 4.5))
plt.plot([str(c) for c in cutoffs], cutoff_times, marker="o")
plt.title("C3: time for each cutoff (n = 100,000)")
plt.xlabel("cutoff")
plt.ylabel("Time (seconds)")
plt.grid(True)
plt.tight_layout()
plt.savefig("graph3_cutoff.png")
plt.close()


# =====================================================================
# C4. Our best quicksort vs Python's sorted()
# =====================================================================
def best_quicksort(a):
    quicksort_improved(a, best_cutoff)


def python_sorted(a):
    sorted(a)


show()
show(f"## C4. quicksort_improved (cutoff {best_cutoff}) vs sorted(), n = 100000")
show()
show("| input | quicksort_improved | sorted() | how many times slower |")
show("|---|---|---|---|")

mine = []
python = []
for kind in kinds:
    data = make_list(kind, 100000)
    t1 = time_sort(best_quicksort, data)
    t2 = time_sort(python_sorted, data)
    mine.append(t1)
    python.append(t2)
    show(f"| {kind} | {t1:.4f} | {t2:.4f} | {t1 / t2:.0f}x |")

# Graph 4: bar chart (log scale because sorted() is so much faster)
positions = [0, 1, 2]
plt.figure(figsize=(7, 4.5))
plt.bar([p - 0.2 for p in positions], mine, width=0.4, label="quicksort_improved")
plt.bar([p + 0.2 for p in positions], python, width=0.4, label="sorted()")
plt.xticks(positions, kinds)
plt.yscale("log")
plt.title("C4: our quicksort vs sorted() (n = 100,000)")
plt.ylabel("Time (seconds, log scale)")
plt.legend()
plt.tight_layout()
plt.savefig("graph4_vs_sorted.png")
plt.close()


# Save all tables to results.md
with open("results.md", "w") as f:
    f.write("\n".join(output_lines) + "\n")
print("\nSaved results.md and 4 graphs.")
