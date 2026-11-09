# Assignment 3 - Part C: timing experiments
# Run with:  python analysis.py
# Writes results.md (tables) and four PNG graphs into this folder.

import os
import random
import sys
import threading
import time

import matplotlib.pyplot as plt

from sorts import quicksort_basic, quicksort_improved

HERE = os.path.dirname(os.path.abspath(__file__))
SIZES = [1000, 2000, 4000, 8000, 16000, 32000, 64000]
REPEATS = 3          # best of 3 runs for each measurement
random.seed(340)


def make_input(kind, n):
    if kind == "random":
        return [random.randint(0, 10**6) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "duplicates":
        return [random.randint(0, 9) for _ in range(n)]
    raise ValueError(kind)


def time_sort(sort_fn, data, repeats=REPEATS, **kwargs):
    """Best time over `repeats` runs, or the name of the error if it crashed."""
    best = float("inf")
    for _ in range(repeats):
        a = list(data)
        start = time.perf_counter()
        try:
            sort_fn(a, **kwargs)
        except RecursionError:
            return "RecursionError"
        best = min(best, time.perf_counter() - start)
    return best


def fmt(t):
    return t if isinstance(t, str) else f"{t:.4f}"


lines = []          # markdown output


def out(text=""):
    print(text)
    lines.append(text)


# ---------------------------------------------------------------------------
# C1. Basic vs improved on three input types (default recursion limit)
# ---------------------------------------------------------------------------
out(f"# Assignment 3 results\n\nPython {sys.version.split()[0]}, "
    f"recursion limit {sys.getrecursionlimit()}, best of {REPEATS} runs, times in seconds.\n")
out("## C1. Time vs n for three input types\n")

results = {}   # (sort name, kind) -> list of times / error strings
for kind in ["random", "sorted", "duplicates"]:
    out(f"### Input: {kind}\n")
    out("| n | quicksort_basic | quicksort_improved |")
    out("|---|---|---|")
    for n in SIZES:
        data = make_input(kind, n)
        tb = time_sort(quicksort_basic, data)
        ti = time_sort(quicksort_improved, data)
        results.setdefault(("basic", kind), []).append(tb)
        results.setdefault(("improved", kind), []).append(ti)
        out(f"| {n:,} | {fmt(tb)} | {fmt(ti)} |")
    out()

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
for ax, kind in zip(axes, ["random", "sorted", "duplicates"]):
    for name, marker in [("basic", "o"), ("improved", "s")]:
        ts = results[(name, kind)]
        xs = [n for n, t in zip(SIZES, ts) if not isinstance(t, str)]
        ys = [t for t in ts if not isinstance(t, str)]
        crashed = [n for n, t in zip(SIZES, ts) if isinstance(t, str)]
        label = f"quicksort_{name}"
        if crashed:
            label += f" (RecursionError for n >= {crashed[0]:,})"
        ax.plot(xs, ys, marker=marker, label=label)
    ax.set_title(f"Input: {kind}")
    ax.set_xlabel("n (number of items)")
    ax.set_ylabel("Time (seconds)")
    ax.grid(True)
    ax.legend(fontsize=8)
fig.suptitle("C1: quicksort_basic vs quicksort_improved")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "graph1_input_types.png"), dpi=120)
plt.close(fig)


# ---------------------------------------------------------------------------
# C2. Show the Theta(n^2) worst case of quicksort_basic on sorted input.
#     The recursion limit is raised (in a thread with a big stack) so the
#     sort can finish instead of crashing.
# ---------------------------------------------------------------------------
out("## C2. quicksort_basic on sorted input with a raised recursion limit\n")
out("Recursion limit raised to 100,000 and run in a thread with a 200 MB stack, "
    "so the worst case can be timed instead of crashing.\n")
out("| n | time (s) | time / n^2 (x 1e-8) | time / previous |")
out("|---|---|---|---|")

worst_sizes = [1000, 2000, 4000, 8000, 16000]
worst_times = []


def worst_case_run():
    sys.setrecursionlimit(100_000)
    for n in worst_sizes:
        worst_times.append(time_sort(quicksort_basic, list(range(n)), repeats=1))


threading.stack_size(200 * 1024 * 1024)
t = threading.Thread(target=worst_case_run)
t.start()
t.join()
sys.setrecursionlimit(1000)

prev = None
for n, tm in zip(worst_sizes, worst_times):
    ratio = "-" if prev is None else f"{tm / prev:.2f}"
    out(f"| {n:,} | {tm:.4f} | {tm / n**2 * 1e8:.3f} | {ratio} |")
    prev = tm
out()

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(worst_sizes, worst_times, marker="o", label="quicksort_basic, sorted input (measured)")
c = worst_times[-1] / worst_sizes[-1] ** 2
ax.plot(worst_sizes, [c * n**2 for n in worst_sizes], "--", label="c * n^2 (fitted)")
ax.set_xlabel("n (number of items)")
ax.set_ylabel("Time (seconds)")
ax.set_title("C2: worst case T(n) = T(n-1) + Theta(n) = Theta(n^2)")
ax.grid(True)
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(HERE, "graph2_worst_case.png"), dpi=120)
plt.close(fig)


# ---------------------------------------------------------------------------
# C3. Choosing the cutoff (n = 100,000 random values)
# ---------------------------------------------------------------------------
out("## C3. quicksort_improved cutoff, n = 100,000 random values\n")
out("| cutoff | time (s) |")
out("|---|---|")
N = 100_000
data = make_input("random", N)
cutoffs = [1, 4, 8, 16, 32, 64]
cut_times = []
for cutoff in cutoffs:
    tm = time_sort(quicksort_improved, data, repeats=5, cutoff=cutoff)
    cut_times.append(tm)
    out(f"| {cutoff} | {tm:.4f} |")
best_cutoff = cutoffs[cut_times.index(min(cut_times))]
out(f"\nBest cutoff: **{best_cutoff}**\n")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(cutoffs, cut_times, marker="o")
ax.set_xscale("log", base=2)
ax.set_xticks(cutoffs)
ax.set_xticklabels([str(c) for c in cutoffs])
ax.set_xlabel("cutoff (largest part sorted by insertion sort)")
ax.set_ylabel("Time (seconds)")
ax.set_title("C3: effect of cutoff, n = 100,000 random values")
ax.grid(True)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "graph3_cutoff.png"), dpi=120)
plt.close(fig)


# ---------------------------------------------------------------------------
# C4. Best version vs Python's sorted()
# ---------------------------------------------------------------------------
out(f"## C4. quicksort_improved (cutoff={best_cutoff}) vs Python sorted()\n")
out("| input (n = 100,000) | quicksort_improved | sorted() | ratio |")
out("|---|---|---|---|")
cmp_rows = []
for kind in ["random", "sorted", "duplicates"]:
    data = make_input(kind, N)
    ti = time_sort(quicksort_improved, data, cutoff=best_cutoff)
    ts = time_sort(lambda a: sorted(a), data)
    cmp_rows.append((kind, ti, ts))
    out(f"| {kind} | {ti:.4f} | {ts:.4f} | {ti / ts:.0f}x slower |")
out()

fig, ax = plt.subplots(figsize=(7, 4.5))
kinds = [r[0] for r in cmp_rows]
x = range(len(kinds))
ax.bar([i - 0.2 for i in x], [r[1] for r in cmp_rows], width=0.4,
       label=f"quicksort_improved (cutoff={best_cutoff})")
ax.bar([i + 0.2 for i in x], [r[2] for r in cmp_rows], width=0.4, label="sorted() (Timsort, C)")
ax.set_xticks(list(x))
ax.set_xticklabels(kinds)
ax.set_yscale("log")
ax.set_ylabel("Time (seconds, log scale)")
ax.set_title("C4: best quicksort vs sorted(), n = 100,000")
ax.grid(True, axis="y")
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(HERE, "graph4_vs_sorted.png"), dpi=120)
plt.close(fig)

with open(os.path.join(HERE, "results.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("\nSaved results.md and graph1-4 PNGs.")
