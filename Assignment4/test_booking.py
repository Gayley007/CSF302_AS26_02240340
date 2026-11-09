# Assignment 4 - Part B: tests
# Run with:  python -m pytest test_booking.py -v
#
# Idea: brute_force tries every possible subset, so it is always right
# (for small inputs). We compare our DP answer with it.

import random
from booking import (fits, greedy_earliest_finish, greedy_highest_fee,
                     best_schedule, brute_force)


def random_requests(n, same_fee=False):
    # make n random requests (start, finish, fee) with start < finish
    requests = []
    for _ in range(n):
        start = random.randint(0, 20)
        finish = start + random.randint(1, 6)
        if same_fee:
            fee = 1000
        else:
            fee = random.randint(1, 10) * 500
        requests.append((start, finish, fee))
    return requests


def is_valid(requests, total, chosen):
    # chosen must have no overlaps, and the fees must add up to total
    for a in range(len(chosen)):
        for b in range(a + 1, len(chosen)):
            if not fits(requests[chosen[a]], requests[chosen[b]]):
                return False
    money = 0
    for i in chosen:
        money = money + requests[i][2]
    return money == total


# ---------- The example from the assignment ----------

def test_assignment_example():
    requests = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000),
                (12, 14, 2500), (16, 18, 2000)]
    assert greedy_earliest_finish(requests) == (7500, [0, 3, 4])
    assert best_schedule(requests) == (10000, [1, 4])


# ---------- Test 1: DP vs brute force on 500 random inputs ----------

def test_dp_matches_brute_force_500_times():
    for _ in range(500):
        n = random.randint(0, 10)                 # 0 to 10 requests
        requests = random_requests(n)
        dp_total, dp_chosen = best_schedule(requests)
        bf_total, bf_chosen = brute_force(requests)
        assert dp_total == bf_total                          # same best money
        assert is_valid(requests, dp_total, dp_chosen)       # real schedule


def test_greedy_answers_are_valid_schedules():
    # greedy may not be the best, but it must never double-book the hall
    for _ in range(500):
        requests = random_requests(random.randint(0, 10))
        for rule in [greedy_earliest_finish, greedy_highest_fee]:
            total, chosen = rule(requests)
            assert is_valid(requests, total, chosen)
            assert total <= brute_force(requests)[0]         # never beats optimum


# ---------- Test 2: special cases ----------

def check_all(requests, expected_total):
    # helper: DP and brute force must both give expected_total
    assert best_schedule(requests)[0] == expected_total
    assert brute_force(requests)[0] == expected_total


def test_no_requests():
    assert best_schedule([]) == (0, [])
    assert brute_force([]) == (0, [])
    assert greedy_earliest_finish([]) == (0, [])
    assert greedy_highest_fee([]) == (0, [])


def test_one_request():
    requests = [(9, 12, 3000)]
    assert best_schedule(requests) == (3000, [0])
    assert greedy_earliest_finish(requests) == (3000, [0])
    assert greedy_highest_fee(requests) == (3000, [0])


def test_all_overlapping():
    # every request uses 10:00-11:00, so only one can be taken -> pick the biggest fee
    requests = [(9, 12, 3000), (10, 11, 5000), (8, 14, 2000), (10, 13, 4000)]
    check_all(requests, 5000)
    assert best_schedule(requests)[1] == [1]


def test_none_overlapping():
    # gaps between all events -> take all of them
    requests = [(1, 2, 100), (3, 4, 200), (5, 6, 300), (7, 8, 400)]
    check_all(requests, 1000)
    assert best_schedule(requests)[1] == [0, 1, 2, 3]


def test_back_to_back():
    # one ends at exactly the time the next starts -> they still fit
    requests = [(9, 12, 3000), (12, 15, 2000), (15, 18, 1000)]
    check_all(requests, 6000)
    assert best_schedule(requests)[1] == [0, 1, 2]
    assert greedy_earliest_finish(requests) == (6000, [0, 1, 2])


# ---------- Test 3: equal fees -> earliest finish is optimal ----------

def test_equal_fees_greedy_is_optimal():
    for _ in range(500):
        requests = random_requests(random.randint(0, 10), same_fee=True)
        assert greedy_earliest_finish(requests)[0] == brute_force(requests)[0]


# ---------- Part C1: the counterexamples really break the greedy rules ----------

def test_counterexample_earliest_finish():
    requests = [(0, 2, 1000), (1, 5, 5000)]
    assert greedy_earliest_finish(requests)[0] == 1000
    assert best_schedule(requests)[0] == 5000


def test_counterexample_highest_fee():
    requests = [(0, 10, 5000), (0, 5, 3000), (5, 10, 3000)]
    assert greedy_highest_fee(requests)[0] == 5000
    assert best_schedule(requests)[0] == 6000
