# Assignment 3 (Unit 5): Fixing a Slow Quicksort
# Part A - two in-place quicksorts.
#
# Both functions sort the list `a` in place (ascending) and return None.
# They do not call sorted() or list.sort().

import random


# ---------------------------------------------------------------------------
# 1. Basic quicksort: Lomuto partition, last element as pivot
# ---------------------------------------------------------------------------

def lomuto_partition(a, lo, hi):
    """Partition a[lo..hi] around pivot a[hi]. Return the pivot's final index."""
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


def _quicksort_basic(a, lo, hi):
    if lo < hi:
        p = lomuto_partition(a, lo, hi)
        _quicksort_basic(a, lo, p - 1)
        _quicksort_basic(a, p + 1, hi)


def quicksort_basic(a):
    """Textbook quicksort (last element as pivot).

    Worst case: already-sorted input or many equal values. Every partition
    then splits n items into (n - 1) and 0, so T(n) = T(n - 1) + Theta(n),
    which is Theta(n^2) time and n levels of recursion (RecursionError).
    """
    _quicksort_basic(a, 0, len(a) - 1)


# ---------------------------------------------------------------------------
# 2. Improved quicksort
#    - random pivot
#    - insertion sort for parts of size <= cutoff
#    - recurse on the smaller part, loop on the larger part (depth O(log n))
#    - three-way partition (< pivot | == pivot | > pivot), so runs of equal
#      values are finished in one pass instead of one element at a time
# ---------------------------------------------------------------------------

def insertion_sort(a, lo, hi):
    """Sort a[lo..hi] (inclusive) in place with insertion sort."""
    for i in range(lo + 1, hi + 1):
        key = a[i]
        j = i - 1
        while j >= lo and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


def three_way_partition(a, lo, hi):
    """Partition a[lo..hi] around a random pivot (Dutch national flag).

    Returns (lt, gt) such that afterwards:
        a[lo..lt-1]  <  pivot
        a[lt..gt]    == pivot
        a[gt+1..hi]  >  pivot
    """
    r = random.randint(lo, hi)
    pivot = a[r]
    lt, i, gt = lo, lo, hi
    while i <= gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    return lt, gt


def _quicksort_improved(a, lo, hi, cutoff):
    while hi - lo + 1 > cutoff:
        lt, gt = three_way_partition(a, lo, hi)
        # Recurse on the smaller side, then loop on the larger side.
        # The smaller side has at most half the items, so the recursion
        # depth is at most log2(n).
        if (lt - lo) < (hi - gt):
            _quicksort_improved(a, lo, lt - 1, cutoff)
            lo = gt + 1
        else:
            _quicksort_improved(a, gt + 1, hi, cutoff)
            hi = lt - 1
    insertion_sort(a, lo, hi)


def quicksort_improved(a, cutoff=16):
    """Randomised quicksort with an insertion-sort cutoff for small parts."""
    if cutoff < 1:
        cutoff = 1
    _quicksort_improved(a, 0, len(a) - 1, cutoff)


if __name__ == "__main__":
    data = [5, 3, 9, 1, 5, 0, -2, 7, 3, 3]
    x, y = data[:], data[:]
    quicksort_basic(x)
    quicksort_improved(y)
    print("input:              ", data)
    print("quicksort_basic:    ", x)
    print("quicksort_improved: ", y)
