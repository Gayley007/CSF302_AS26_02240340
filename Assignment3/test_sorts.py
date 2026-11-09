# Assignment 3 - Part B: tests for sorts.py
# Run with:   python -m pytest test_sorts.py -v
#        or:  python test_sorts.py
#
# sorted() is used here only as the trusted answer (brute-force check).

import random
import unittest

from sorts import quicksort_basic, quicksort_improved

SORTS = [quicksort_basic, quicksort_improved]


def check(test, sort_fn, data, **kwargs):
    expected = sorted(data)
    a = list(data)
    result = sort_fn(a, **kwargs)
    test.assertIsNone(result, "sort should work in place and return None")
    test.assertEqual(a, expected, f"{sort_fn.__name__} failed on {data}")


class TestRandomLists(unittest.TestCase):
    def test_500_random_lists(self):
        rng = random.Random(302)
        for sort_fn in SORTS:
            for _ in range(500):
                n = rng.randint(0, 200)
                data = [rng.randint(-1000, 1000) for _ in range(n)]
                with self.subTest(sort=sort_fn.__name__, n=n):
                    check(self, sort_fn, data)

    def test_improved_with_every_cutoff(self):
        rng = random.Random(7)
        for cutoff in [1, 4, 8, 16, 32, 64]:
            for _ in range(100):
                data = [rng.randint(-50, 50) for _ in range(rng.randint(0, 300))]
                with self.subTest(cutoff=cutoff):
                    check(self, quicksort_improved, data, cutoff=cutoff)


class TestSpecialCases(unittest.TestCase):
    CASES = {
        "empty": [],
        "one element": [42],
        "two elements": [2, 1],
        "all equal": [7] * 50,
        "already sorted": list(range(100)),
        "reverse sorted": list(range(100, 0, -1)),
        "negative numbers": [-3, -1, -7, 0, -2, 5, -100, 4],
        "many duplicates (0-9)": [random.Random(1).randint(0, 9) for _ in range(300)],
    }

    def test_cases(self):
        for sort_fn in SORTS:
            for name, data in self.CASES.items():
                with self.subTest(sort=sort_fn.__name__, case=name):
                    check(self, sort_fn, data)


class TestLargeInputsImproved(unittest.TestCase):
    """The improved sort must handle the inputs that break the basic one."""

    def test_large_sorted_and_duplicates(self):
        n = 100_000
        for name, data in {
            "sorted": list(range(n)),
            "reverse": list(range(n, 0, -1)),
            "duplicates": [random.randint(0, 9) for _ in range(n)],
            "all equal": [5] * n,
        }.items():
            with self.subTest(case=name):
                check(self, quicksort_improved, data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
