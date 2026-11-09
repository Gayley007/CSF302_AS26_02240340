# Assignment 3 - Part A
# Two quicksorts. Both sort the list "a" in place (they change the list itself)
# from smallest to largest. We do NOT use sorted() or list.sort() here.

import random


# =====================================================================
# 1. BASIC QUICKSORT  (last element is the pivot)
# =====================================================================

def partition_basic(a, low, high):
    # Lomuto partition: use the LAST element as the pivot.
    # After this, everything <= pivot is on the left of the pivot,
    # and everything > pivot is on the right.
    pivot = a[high]
    i = low - 1                      # i = end of the "small" part

    for j in range(low, high):       # look at every element except the pivot
        if a[j] <= pivot:            # small element found
            i = i + 1
            a[i], a[j] = a[j], a[i]  # move it into the "small" part

    # put the pivot just after the "small" part
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1                     # final position of the pivot


def quicksort_basic_helper(a, low, high):
    if low < high:                               # 2 or more elements left
        p = partition_basic(a, low, high)        # pivot is now at index p
        quicksort_basic_helper(a, low, p - 1)    # sort the left part
        quicksort_basic_helper(a, p + 1, high)   # sort the right part


def quicksort_basic(a):
    # PROBLEM: if the list is already sorted, the last element is always
    # the biggest, so the right part is always empty. Each call removes
    # only one element: T(n) = T(n-1) + n  ->  O(n^2) time,
    # and n nested calls -> Python gives RecursionError.
    quicksort_basic_helper(a, 0, len(a) - 1)


# =====================================================================
# 2. IMPROVED QUICKSORT
#    Fix 1: random pivot            -> sorted input is no longer a bad case
#    Fix 2: insertion sort on small parts (size <= cutoff) -> fewer calls
#    Fix 3: recurse on the smaller part, loop on the bigger part
#           -> at most log2(n) nested calls, so no RecursionError
#    Fix 4: three-way partition (< pivot | = pivot | > pivot)
#           -> many repeated values are handled in one pass
# =====================================================================

def insertion_sort(a, low, high):
    # Sort a[low..high] like sorting cards in your hand.
    for i in range(low + 1, high + 1):
        key = a[i]                        # the card we want to place
        j = i - 1
        while j >= low and a[j] > key:    # shift bigger cards one step right
            a[j + 1] = a[j]
            j = j - 1
        a[j + 1] = key                    # drop the card into the gap


def partition_three_way(a, low, high):
    # Pick a RANDOM pivot, then split a[low..high] into three groups:
    #   a[low .. lt-1]   smaller than pivot
    #   a[lt .. gt]      equal to pivot      (already in the right place)
    #   a[gt+1 .. high]  bigger than pivot
    pivot = a[random.randint(low, high)]
    lt = low        # next place for a small element
    i = low         # element we are looking at now
    gt = high       # next place for a big element

    while i <= gt:
        if a[i] < pivot:                   # small: swap to the front
            a[lt], a[i] = a[i], a[lt]
            lt = lt + 1
            i = i + 1
        elif a[i] > pivot:                 # big: swap to the back
            a[i], a[gt] = a[gt], a[i]
            gt = gt - 1                    # (do not move i: new a[i] is unchecked)
        else:                              # equal: leave it in the middle
            i = i + 1

    return lt, gt


def quicksort_improved_helper(a, low, high, cutoff):
    # Keep going while the part is bigger than the cutoff.
    while high - low + 1 > cutoff:
        lt, gt = partition_three_way(a, low, high)

        left_size = lt - low          # size of the "smaller than pivot" part
        right_size = high - gt        # size of the "bigger than pivot" part

        if left_size < right_size:
            # Left part is smaller: sort it with a recursive call...
            quicksort_improved_helper(a, low, lt - 1, cutoff)
            # ...and handle the right part in the next loop round.
            low = gt + 1
        else:
            # Right part is smaller: sort it with a recursive call...
            quicksort_improved_helper(a, gt + 1, high, cutoff)
            # ...and handle the left part in the next loop round.
            high = lt - 1

    # The part left over is small, so insertion sort is fast here.
    insertion_sort(a, low, high)


def quicksort_improved(a, cutoff=16):
    if cutoff < 1:
        cutoff = 1
    quicksort_improved_helper(a, 0, len(a) - 1, cutoff)


# Small demo when you run:  python sorts.py
if __name__ == "__main__":
    data = [5, 3, 9, 1, 5, 0, -2, 7, 3, 3]

    x = data.copy()
    quicksort_basic(x)

    y = data.copy()
    quicksort_improved(y)

    print("input:              ", data)
    print("quicksort_basic:    ", x)
    print("quicksort_improved: ", y)
