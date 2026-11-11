# Lab 5 - Q1: Quicksort variants
# Lomuto, Hoare, Randomised and Three-way quicksort.
# We count comparisons and time each one on 4 kinds of input.

import random
import time

# Global counter for comparisons between elements.
# Every sort resets it to 0 before it starts.
comparisons = 0


# ---------------------------------------------------------------
# 1. Lomuto partition (pivot = LAST element)
# ---------------------------------------------------------------
def lomuto_partition(arr, low, high):
    global comparisons
    pivot = arr[high]
    i = low - 1                       # end of the "<= pivot" area
    for j in range(low, high):
        comparisons += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]   # put pivot in its final place
    return i + 1


def quicksort_lomuto(arr, low, high):
    # Recurse on the SMALLER side, loop on the BIGGER side.
    # This keeps recursion depth at most log n, so sorted input
    # does not crash with "maximum recursion depth exceeded".
    while low < high:
        p = lomuto_partition(arr, low, high)
        if p - low < high - p:
            quicksort_lomuto(arr, low, p - 1)    # left side is smaller
            low = p + 1                           # loop again on right side
        else:
            quicksort_lomuto(arr, p + 1, high)   # right side is smaller
            high = p - 1                          # loop again on left side


# ---------------------------------------------------------------
# 2. Hoare partition (pivot = FIRST element)
# ---------------------------------------------------------------
def hoare_partition(arr, low, high):
    global comparisons
    pivot = arr[low]
    i = low - 1
    j = high + 1
    while True:
        # move i right until we find an element >= pivot
        i += 1
        comparisons += 1
        while arr[i] < pivot:
            i += 1
            comparisons += 1
        # move j left until we find an element <= pivot
        j -= 1
        comparisons += 1
        while arr[j] > pivot:
            j -= 1
            comparisons += 1
        if i >= j:
            return j              # arr[low..j] <= pivot <= arr[j+1..high]
        arr[i], arr[j] = arr[j], arr[i]


def quicksort_hoare(arr, low, high):
    # Note: Hoare returns j, and j stays INSIDE the left part,
    # so the two parts are [low..p] and [p+1..high].
    while low < high:
        p = hoare_partition(arr, low, high)
        if p - low < high - p:
            quicksort_hoare(arr, low, p)
            low = p + 1
        else:
            quicksort_hoare(arr, p + 1, high)
            high = p


# ---------------------------------------------------------------
# 3. Randomised quicksort (random pivot, then Lomuto)
# ---------------------------------------------------------------
def quicksort_random(arr, low, high):
    while low < high:
        # pick a random index and swap it to the end,
        # then Lomuto uses it as the pivot
        r = random.randint(low, high)
        arr[r], arr[high] = arr[high], arr[r]
        p = lomuto_partition(arr, low, high)
        if p - low < high - p:
            quicksort_random(arr, low, p - 1)
            low = p + 1
        else:
            quicksort_random(arr, p + 1, high)
            high = p - 1


# ---------------------------------------------------------------
# 4. Three-way quicksort (Dutch national flag), random pivot
# ---------------------------------------------------------------
def quicksort_3way(arr, low, high):
    global comparisons
    while low < high:
        pivot = arr[random.randint(low, high)]
        # After the loop the array looks like:
        #   [low..lt-1] < pivot | [lt..gt] == pivot | [gt+1..high] > pivot
        lt = low       # next place for a "smaller" element
        i = low        # element we are looking at now
        gt = high      # next place for a "bigger" element
        while i <= gt:
            comparisons += 1
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            else:
                comparisons += 1
                if arr[i] > pivot:
                    arr[i], arr[gt] = arr[gt], arr[i]
                    gt -= 1          # do NOT move i: the swapped-in value is unchecked
                else:
                    i += 1           # equal to pivot, leave it in the middle
        # The middle (equal) part is already sorted, skip it.
        if lt - low < high - gt:
            quicksort_3way(arr, low, lt - 1)
            low = gt + 1
        else:
            quicksort_3way(arr, gt + 1, high)
            high = lt - 1


# ---------------------------------------------------------------
# Making the 4 input types
# ---------------------------------------------------------------
def make_input(kind, n):
    if kind == "random":
        return [random.randint(0, n * 10) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n, 0, -1))
    if kind == "duplicates":
        return [random.randint(0, 9) for _ in range(n)]   # only values 0..9


# Runs one sort on a copy of data, returns (comparisons, seconds)
def run_one(sort_function, data):
    global comparisons
    arr = data[:]                    # copy so every sort gets the same input
    comparisons = 0
    start = time.perf_counter()
    sort_function(arr, 0, len(arr) - 1)
    seconds = time.perf_counter() - start
    if arr != sorted(data):
        print("ERROR: array not sorted correctly!")
    return comparisons, seconds


if __name__ == "__main__":
    # quick correctness check on a small list
    test = [5, 2, 9, 1, 5, 6, 0, 3, 3, 8]
    for name, f in [("Lomuto", quicksort_lomuto), ("Hoare", quicksort_hoare),
                    ("Random", quicksort_random), ("3-way", quicksort_3way)]:
        arr = test[:]
        f(arr, 0, len(arr) - 1)
        print(f"{name:7} -> {arr}")

    sorts = [("Lomuto", quicksort_lomuto), ("Hoare", quicksort_hoare),
             ("Random", quicksort_random), ("3-way", quicksort_3way)]
    sizes = [1000, 2000, 4000, 8000, 16000]
    kinds = ["random", "sorted", "reverse", "duplicates"]

    for kind in kinds:
        print(f"\n=== Input: {kind} ===")
        print(f"{'n':>6} | {'Lomuto comps':>13} {'time(s)':>8} | {'Hoare comps':>13} {'time(s)':>8} | "
              f"{'Random comps':>13} {'time(s)':>8} | {'3-way comps':>13} {'time(s)':>8}")
        for n in sizes:
            data = make_input(kind, n)
            line = f"{n:>6} |"
            for name, f in sorts:
                comps, secs = run_one(f, data)
                line += f" {comps:>13,} {secs:>8.4f} |"
            print(line)
