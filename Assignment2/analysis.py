# Assignment 2 - Part C: timing analysis
# Run with:  python analysis.py
# It prints the results, writes them to results.md, and saves
# graph_loglog.png and graph_crossover.png.
# (Brute force takes a few minutes in total for the big sizes.)

import math
import random
import time
import matplotlib.pyplot as plt
from closest import closest_pair, closest_pair_brute

random.seed(340)          # fixed seed, so the same points every run

lines = []                # text that goes into results.md


def report(text):
    # print a line and also keep it for results.md
    print(text, flush=True)
    lines.append(text)


def random_points(n):
    # n camera traps on a 1,000,000 x 1,000,000 grid
    points = []
    for _ in range(n):
        points.append((random.randint(0, 1000000), random.randint(0, 1000000)))
    return points


def time_once(function, points):
    # how many seconds one call takes
    start = time.perf_counter()
    function(points)
    return time.perf_counter() - start


# ---------- C2: time both functions for n = 1,000 ... 64,000 ----------

report("# Assignment 2 - Results\n")
report("## C2. Running times (seconds)\n")
report("| n | brute force (s) | divide & conquer (s) | brute / D&C |")
report("|---|---|---|---|")

sizes = [1000, 2000, 4000, 8000, 16000, 32000, 64000]
brute_times = []          # only filled while brute force is still running
dc_times = []
brute_stopped = False     # becomes True after brute force takes > 60 s

for n in sizes:
    points = random_points(n)

    # divide and conquer is fast, so take the best of 3 runs
    dc = min(time_once(closest_pair, points),
             time_once(closest_pair, points),
             time_once(closest_pair, points))
    dc_times.append(dc)

    if brute_stopped:
        report("| " + str(n) + " | (skipped, over 60 s) | " + format(dc, ".4f") + " | - |")
        continue

    brute = time_once(closest_pair_brute, points)
    brute_times.append(brute)

    report("| " + str(n) + " | " + format(brute, ".3f") + " | " + format(dc, ".4f")
           + " | " + format(brute / dc, ".0f") + "x |")

    if brute > 60:
        brute_stopped = True      # stop brute force for the bigger sizes

# growth: when n doubles, how many times longer does it take?
report("\n### What happens when n doubles\n")
report("| n | brute: time / previous time | D&C: time / previous time |")
report("|---|---|---|")
for k in range(1, len(sizes)):
    if k < len(brute_times):
        brute_ratio = format(brute_times[k] / brute_times[k - 1], ".2f")
    else:
        brute_ratio = "-"
    dc_ratio = format(dc_times[k] / dc_times[k - 1], ".2f")
    report("| " + str(sizes[k]) + " | " + brute_ratio + " | " + dc_ratio + " |")

report("\n(Theta(n^2) should give about 4.00. Theta(n log n) should give a bit over 2.00.)")

# slope of the log-log line from the first to the last point
brute_slope = math.log(brute_times[-1] / brute_times[0]) / \
    math.log(sizes[len(brute_times) - 1] / sizes[0])
dc_slope = math.log(dc_times[-1] / dc_times[0]) / math.log(sizes[-1] / sizes[0])
report("\nSlope of the log-log line: brute force = " + format(brute_slope, ".2f")
       + ", divide & conquer = " + format(dc_slope, ".2f") + "\n")

# log-log graph
plt.figure(figsize=(7, 5))
plt.loglog(sizes[:len(brute_times)], brute_times, "o-", label="brute force")
plt.loglog(sizes, dc_times, "s-", label="divide and conquer")
plt.xlabel("number of points n (log scale)")
plt.ylabel("time in seconds (log scale)")
plt.title("Closest pair: running time (log-log)")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.savefig("graph_loglog.png", dpi=120, bbox_inches="tight")
plt.close()


# ---------- C3: smallest n where divide and conquer wins ----------
# Small inputs run in microseconds, so we run each function many times
# and take the average. We try n = 2, 3, ..., 150.

def average_time(function, points, repeats):
    start = time.perf_counter()
    for _ in range(repeats):
        function(points)
    return (time.perf_counter() - start) / repeats


small_sizes = list(range(2, 151))
small_brute = []
small_dc = []
for n in small_sizes:
    # average over 20 different random inputs of size n
    brute_total = 0
    dc_total = 0
    for _ in range(20):
        points = random_points(n)
        brute_total += average_time(closest_pair_brute, points, 20)
        dc_total += average_time(closest_pair, points, 20)
    small_brute.append(brute_total / 20)
    small_dc.append(dc_total / 20)

# crossover = the smallest n from which D&C is faster for EVERY bigger n we tried
crossover = None
for k in range(len(small_sizes)):
    faster_from_here = True
    for m in range(k, len(small_sizes)):
        if small_dc[m] >= small_brute[m]:
            faster_from_here = False
            break
    if faster_from_here:
        crossover = small_sizes[k]
        break

# first n where D&C wins at all (it can flip back and forth near the crossover)
first_win = None
for k in range(len(small_sizes)):
    if small_dc[k] < small_brute[k]:
        first_win = small_sizes[k]
        break

report("## C3. Crossover point\n")
report("| n | brute force (microseconds) | divide & conquer (microseconds) | faster |")
report("|---|---|---|---|")
for n in [2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150]:
    k = small_sizes.index(n)
    if small_dc[k] < small_brute[k]:
        faster = "D&C"
    else:
        faster = "brute"
    report("| " + str(n) + " | " + format(small_brute[k] * 1e6, ".1f") + " | "
           + format(small_dc[k] * 1e6, ".1f") + " | " + faster + " |")

report("\nFirst n where divide and conquer is faster: " + str(first_win))
report("Smallest n from which divide and conquer is ALWAYS faster (n up to 150): "
       + str(crossover))

plt.figure(figsize=(7, 5))
plt.plot(small_sizes, [t * 1e6 for t in small_brute], label="brute force")
plt.plot(small_sizes, [t * 1e6 for t in small_dc], label="divide and conquer")
if crossover is not None:
    plt.axvline(crossover, color="gray", linestyle="--",
                label="crossover n = " + str(crossover))
plt.xlabel("number of points n")
plt.ylabel("time in microseconds")
plt.title("Closest pair: small n (where is the crossover?)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig("graph_crossover.png", dpi=120, bbox_inches="tight")
plt.close()

with open("results.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("\nSaved results.md, graph_loglog.png and graph_crossover.png")
