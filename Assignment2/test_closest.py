# Assignment 2 - Part B: tests
# Run with:  python -m pytest test_closest.py -v
#
# Idea: closest_pair_brute checks every pair, so it is always right.
# We compare the divide-and-conquer answer with it.
#
# When two different pairs are equally close, the two functions may
# pick different pairs. Both are correct, so we compare the DISTANCE,
# and we check that the pair returned really is that far apart.

import math
import random
from closest import closest_pair, closest_pair_brute


def check_answer(points, answer):
    # answer = (d, i, j). Check i < j and that points i and j are d apart.
    d, i, j = answer
    assert 0 <= i < j < len(points)
    real = math.dist(points[i], points[j])
    assert math.isclose(real, d)


def check_against_brute(points):
    # the divide-and-conquer distance must equal the brute-force distance
    fast = closest_pair(points)
    slow = closest_pair_brute(points)
    check_answer(points, fast)
    check_answer(points, slow)
    assert math.isclose(fast[0], slow[0])


def random_points(n, size):
    # n random points with whole-number x and y between 0 and size
    points = []
    for _ in range(n):
        points.append((random.randint(0, size), random.randint(0, size)))
    return points


# ---------- the example from the assignment ----------

def test_example():
    points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    d, i, j = closest_pair(points)
    assert math.isclose(d, math.sqrt(2))
    assert (i, j) == (0, 5)
    assert closest_pair_brute(points)[1:] == (0, 5)


# ---------- 500 random inputs of 2 to 50 points ----------

def test_500_random_inputs():
    random.seed(340)
    for _ in range(500):
        n = random.randint(2, 50)
        points = random_points(n, 1000)
        check_against_brute(points)


def test_500_random_inputs_small_grid():
    # a small grid (0..10) gives lots of equal x values, equal distances
    # and duplicate points, which are the tricky cases
    random.seed(341)
    for _ in range(500):
        n = random.randint(2, 50)
        points = random_points(n, 10)
        check_against_brute(points)


def test_500_random_inputs_decimals():
    # points with decimal coordinates
    random.seed(342)
    for _ in range(500):
        n = random.randint(2, 50)
        points = []
        for _ in range(n):
            points.append((random.uniform(-100, 100), random.uniform(-100, 100)))
        check_against_brute(points)


# ---------- special cases ----------

def test_exactly_two_points():
    points = [(0, 0), (3, 4)]
    assert closest_pair(points) == (5.0, 0, 1)
    assert closest_pair_brute(points) == (5.0, 0, 1)


def test_duplicate_points():
    # (7, 7) appears twice, at index 1 and index 3 -> distance 0
    points = [(1, 1), (7, 7), (20, 5), (7, 7), (0, 30)]
    assert closest_pair(points) == (0.0, 1, 3)


def test_all_points_the_same():
    points = [(5, 5)] * 10
    d, i, j = closest_pair(points)
    assert d == 0.0
    check_answer(points, (d, i, j))


def test_all_on_one_vertical_line():
    # every point has x = 4, so the dividing line goes through all of them
    points = [(4, 0), (4, 10), (4, 25), (4, 27), (4, 50), (4, 61), (4, 90)]
    assert closest_pair(points) == (2.0, 2, 3)


def test_vertical_line_random():
    random.seed(343)
    for _ in range(100):
        n = random.randint(2, 50)
        points = []
        for _ in range(n):
            points.append((7, random.randint(0, 1000)))
        check_against_brute(points)


def test_closest_pair_crosses_the_dividing_line():
    # 8 points, sorted by x the split is between x=10 and x=11.
    # Inside each half the points are at least 20 apart,
    # but (10, 50) on the left and (11, 50) on the right are only 1 apart.
    points = [(0, 0), (0, 100), (10, 50), (5, 25),
              (11, 50), (30, 0), (30, 100), (25, 75)]
    assert closest_pair(points) == (1.0, 2, 4)
    assert closest_pair_brute(points) == (1.0, 2, 4)


def test_large_input_against_brute():
    # one bigger input (2,000 points) to make sure the recursion is right
    random.seed(344)
    points = random_points(2000, 100000)
    check_against_brute(points)
