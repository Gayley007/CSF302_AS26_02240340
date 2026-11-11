# Lab 5 - Q2: Counting Sort and Radix Sort
# Compared with merge sort (same merge sort as Lab 1).

import os
import random
import time
import matplotlib.pyplot as plt


# ---------------------------------------------------------------
# 1. Stable counting sort for integers in range 0..k
# ---------------------------------------------------------------
def counting_sort(arr, k):
    count = [0] * (k + 1)
    for x in arr:                       # step 1: count each value
        count[x] += 1
    for v in range(1, k + 1):           # step 2: prefix sums
        count[v] += count[v - 1]        # count[v] = how many values are <= v
    output = [0] * len(arr)
    # step 3: go from the END of the array backwards.
    # Equal values are placed from right to left, so they keep
    # their original order -> this is what makes it STABLE.
    for i in range(len(arr) - 1, -1, -1):
        x = arr[i]
        count[x] -= 1
        output[count[x]] = x
    return output


# Same counting sort, but on (key, original_index) pairs.
# Sorts only by the key. Used to PROVE stability.
def counting_sort_pairs(pairs, k):
    count = [0] * (k + 1)
    for key, index in pairs:
        count[key] += 1
    for v in range(1, k + 1):
        count[v] += count[v - 1]
    output = [None] * len(pairs)
    for i in range(len(pairs) - 1, -1, -1):
        key = pairs[i][0]
        count[key] -= 1
        output[count[key]] = pairs[i]
    return output


# ---------------------------------------------------------------
# 2. LSD radix sort (uses counting sort on each digit)
# ---------------------------------------------------------------
def counting_sort_by_digit(arr, exp, base):
    # The "digit" of x is (x // exp) % base.
    # Example base 10, exp 100: digit of 4567 is 5 (the hundreds digit).
    count = [0] * base
    for x in arr:
        count[(x // exp) % base] += 1
    for d in range(1, base):
        count[d] += count[d - 1]
    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):     # backwards = stable
        d = (arr[i] // exp) % base
        count[d] -= 1
        output[count[d]] = arr[i]
    return output


def radix_sort(arr, base):
    if len(arr) == 0:
        return arr
    biggest = max(arr)
    exp = 1                       # 1st pass: last digit, then next digit, ...
    while biggest // exp > 0:
        arr = counting_sort_by_digit(arr, exp, base)
        exp = exp * base
    return arr


# ---------------------------------------------------------------
# 3. Merge sort (from Lab 1)
# ---------------------------------------------------------------
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    merged = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def time_it(start):
    return time.perf_counter() - start


if __name__ == "__main__":
    folder = os.path.dirname(os.path.abspath(__file__))

    # ---------- Correctness check ----------
    test = [random.randint(0, 1000) for _ in range(20)]
    print("Input            :", test)
    print("Counting sort    :", counting_sort(test, 1000))
    print("Radix base 10    :", radix_sort(test, 10))
    print("Radix base 256   :", radix_sort(test, 256))
    print("All correct?     :", counting_sort(test, 1000) == radix_sort(test, 10)
          == radix_sort(test, 256) == sorted(test))

    # ---------- Stability check ----------
    # Make pairs (key, original index). Keys repeat a lot (only 0..4).
    keys = [3, 1, 4, 1, 0, 3, 2, 4, 1, 0]
    pairs = []
    for i in range(len(keys)):
        pairs.append((keys[i], i))
    result = counting_sort_pairs(pairs, 4)
    print("\nStability test")
    print("Before :", pairs)
    print("After  :", result)
    # Stable means: for the same key, the original indexes are still increasing.
    stable = True
    for i in range(1, len(result)):
        if result[i][0] == result[i - 1][0] and result[i][1] < result[i - 1][1]:
            stable = False
    print("Stable?:", stable)

    # ---------- Experiment A: n fixed, k changes (counting sort) ----------
    n = 100000
    k_values = [10, 10**3, 10**5, 10**7]
    count_times = []
    merge_times_a = []
    print(f"\nExperiment A: n = {n:,}, k changes")
    print(f"{'k':>12} | {'counting (s)':>12} | {'merge (s)':>10}")
    for k in k_values:
        data = [random.randint(0, k) for _ in range(n)]
        start = time.perf_counter()
        counting_sort(data, k)
        count_times.append(time_it(start))
        start = time.perf_counter()
        merge_sort(data)
        merge_times_a.append(time_it(start))
        print(f"{k:>12,} | {count_times[-1]:>12.4f} | {merge_times_a[-1]:>10.4f}")

    plt.figure()
    plt.plot(k_values, count_times, marker="o", label="Counting sort O(n + k)")
    plt.plot(k_values, merge_times_a, marker="s", label="Merge sort O(n log n)")
    plt.xscale("log")
    plt.xlabel("Range of values k")
    plt.ylabel("Time (seconds)")
    plt.title(f"Counting sort vs Merge sort (n = {n:,})")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(folder, "q2_graph_counting_vs_k.png"))

    # ---------- Experiment B: k = 10^9 fixed, n changes (radix vs merge) ----------
    k = 10**9
    n_values = [10000, 50000, 100000, 250000, 500000, 1000000]
    radix10_times = []
    radix256_times = []
    merge_times_b = []
    print(f"\nExperiment B: k = 10^9, n changes")
    print(f"{'n':>10} | {'radix b10 (s)':>13} | {'radix b256 (s)':>14} | {'merge (s)':>10}")
    for n in n_values:
        data = [random.randint(0, k) for _ in range(n)]
        start = time.perf_counter()
        radix_sort(data, 10)
        radix10_times.append(time_it(start))
        start = time.perf_counter()
        radix_sort(data, 256)
        radix256_times.append(time_it(start))
        start = time.perf_counter()
        merge_sort(data)
        merge_times_b.append(time_it(start))
        print(f"{n:>10,} | {radix10_times[-1]:>13.4f} | {radix256_times[-1]:>14.4f} | {merge_times_b[-1]:>10.4f}")

    plt.figure()
    plt.plot(n_values, radix10_times, marker="o", label="Radix sort base 10 (10 passes)")
    plt.plot(n_values, radix256_times, marker="^", label="Radix sort base 256 (4 passes)")
    plt.plot(n_values, merge_times_b, marker="s", label="Merge sort")
    plt.xlabel("Input size n")
    plt.ylabel("Time (seconds)")
    plt.title("Radix sort vs Merge sort (k = 10^9)")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(folder, "q2_graph_radix_vs_merge.png"))
    plt.show()
