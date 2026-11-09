# Assignment 3 - Part B: tests
# Run with:  python -m pytest test_sorts.py -v
#
# Idea: sorted() is our "correct answer". We sort a copy with our own
# quicksort and check that it gives exactly the same result.

import random
from sorts import quicksort_basic, quicksort_improved


def is_correct(sort_function, data):
    expected = sorted(data)      # the correct answer (only used for checking)
    my_list = data.copy()        # copy, so the original data is not changed
    sort_function(my_list)       # sort in place with our quicksort
    return my_list == expected


# ---------- Test 1: 500 random lists for each sort ----------

def test_basic_on_500_random_lists():
    for _ in range(500):
        n = random.randint(0, 200)                            # random length
        data = [random.randint(-1000, 1000) for _ in range(n)]
        assert is_correct(quicksort_basic, data)


def test_improved_on_500_random_lists():
    for _ in range(500):
        n = random.randint(0, 200)
        data = [random.randint(-1000, 1000) for _ in range(n)]
        assert is_correct(quicksort_improved, data)


# ---------- Test 2: special cases ----------

special_cases = [
    [],                              # empty list
    [42],                            # one element
    [7, 7, 7, 7, 7, 7, 7, 7],        # all equal
    list(range(100)),                # already sorted
    list(range(100, 0, -1)),         # reverse sorted
    [-3, -1, -7, 0, -2, 5, -100, 4], # negative numbers
]


def test_basic_special_cases():
    for data in special_cases:
        assert is_correct(quicksort_basic, data)


def test_improved_special_cases():
    for data in special_cases:
        assert is_correct(quicksort_improved, data)


# ---------- Test 3: every cutoff value gives the right answer ----------

def test_improved_all_cutoffs():
    for cutoff in [1, 4, 8, 16, 32, 64]:
        for _ in range(100):
            data = [random.randint(-50, 50) for _ in range(random.randint(0, 300))]
            my_list = data.copy()
            quicksort_improved(my_list, cutoff)
            assert my_list == sorted(data)


# ---------- Test 4: big inputs that break the basic sort ----------

def test_improved_big_inputs():
    n = 100000
    assert is_correct(quicksort_improved, list(range(n)))                         # sorted
    assert is_correct(quicksort_improved, list(range(n, 0, -1)))                  # reverse
    assert is_correct(quicksort_improved, [random.randint(0, 9) for _ in range(n)])  # duplicates
    assert is_correct(quicksort_improved, [5] * n)                                # all equal
