# Lab 5 - Q3: Counting Inversions
# An inversion is a pair (i, j) with i < j but arr[i] > arr[j].

import os
import random
import time
import matplotlib.pyplot as plt

TIME_LIMIT = 60     # seconds; brute force stops after this


# ---------------------------------------------------------------
# 1. Brute force: check every pair  ->  O(n^2)
# ---------------------------------------------------------------
def brute_force_inversions(arr, time_limit=None):
    count = 0
    start = time.perf_counter()
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
        # check the clock once per row; give up if it is too slow
        if time_limit is not None and time.perf_counter() - start > time_limit:
            return None
    return count


# ---------------------------------------------------------------
# 2. Merge sort based  ->  O(n log n)
#    Returns (sorted list, number of inversions)
# ---------------------------------------------------------------
def merge_count(arr):
    if len(arr) <= 1:
        return arr, 0
    mid = len(arr) // 2
    left, left_inv = merge_count(arr[:mid])        # inversions inside left half
    right, right_inv = merge_count(arr[mid:])      # inversions inside right half

    merged = []
    split_inv = 0                                  # inversions across the halves
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            # right[j] is smaller than left[i].
            # left is sorted, so right[j] is also smaller than
            # EVERY element still left in "left" -> all are inversions.
            split_inv += len(left) - i
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, left_inv + right_inv + split_inv


def count_inversions(arr):
    sorted_arr, inv = merge_count(arr)
    return inv


if __name__ == "__main__":
    folder = os.path.dirname(os.path.abspath(__file__))

    # ---------- Small example ----------
    example = [2, 4, 1, 3, 5]
    print("Example:", example)
    print("Brute force:", brute_force_inversions(example))   # (2,1) (4,1) (4,3) = 3
    print("Merge based:", count_inversions(example))

    # ---------- Verify both agree on random arrays up to size 2000 ----------
    print("\nVerifying on 50 random arrays (size 1 to 2000)...")
    all_ok = True
    for test in range(50):
        size = random.randint(1, 2000)
        arr = [random.randint(0, 1000) for _ in range(size)]
        if brute_force_inversions(arr) != count_inversions(arr):
            all_ok = False
            print("Mismatch at size", size)
    print("All results match:", all_ok)

    # ---------- Timing ----------
    sizes = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 500000, 1000000]
    brute_sizes = []
    brute_times = []
    merge_times = []
    brute_stopped = False

    print(f"\n{'n':>10} | {'brute force (s)':>16} | {'merge based (s)':>15} | {'inversions':>16}")
    for n in sizes:
        arr = [random.randint(0, n) for _ in range(n)]

        start = time.perf_counter()
        inv = count_inversions(arr)
        merge_times.append(time.perf_counter() - start)

        if brute_stopped:
            brute_text = "skipped"
        else:
            start = time.perf_counter()
            result = brute_force_inversions(arr, TIME_LIMIT)
            seconds = time.perf_counter() - start
            if result is None:
                brute_text = "> 60 (stopped)"
                brute_stopped = True             # don't try bigger sizes
            else:
                brute_text = f"{seconds:.4f}"
                brute_sizes.append(n)
                brute_times.append(seconds)
        print(f"{n:>10,} | {brute_text:>16} | {merge_times[-1]:>15.4f} | {inv:>16,}")

    plt.plot(brute_sizes, brute_times, marker="o", label="Brute force O(n^2)")
    plt.plot(sizes, merge_times, marker="s", label="Merge based O(n log n)")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Input size n")
    plt.ylabel("Time (seconds)")
    plt.title("Counting inversions: brute force vs merge based")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(folder, "q3_graph_inversions.png"))
    plt.show()
