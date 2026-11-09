# Assignment 4 - Part A: Booking the Hall
#
# Each request is a tuple (start, finish, fee), for example (9, 12, 3000).
# Only one event can use the hall at a time.
# Two requests FIT together if one finishes no later than the other starts
# (an event ending at 12 and one starting at 12 both fit).
# We assume start < finish for every request.
#
# Every function returns (total_fee, chosen):
#   total_fee = money earned
#   chosen    = list of the indices (positions in "requests") we accepted,
#               sorted from smallest to largest.

from bisect import bisect_right
from itertools import combinations


def fits(a, b):
    # True if request a and request b do not overlap.
    # a[0] = start, a[1] = finish
    return a[1] <= b[0] or b[1] <= a[0]


# =====================================================================
# 1. GREEDY RULE 1: earliest finish first
#    Time: O(n log n) for the sort, then O(n) for the loop.
# =====================================================================

def greedy_earliest_finish(requests):
    # make a list of (finish, index) and sort it -> earliest finish first
    order = []
    for i in range(len(requests)):
        order.append((requests[i][1], i))
    order.sort()

    chosen = []
    total = 0
    last_finish = float("-inf")         # finish time of the last accepted event

    for finish, i in order:
        start = requests[i][0]
        fee = requests[i][2]
        if start >= last_finish:        # it starts after the last event ends -> fits
            chosen.append(i)
            total = total + fee
            last_finish = finish

    chosen.sort()
    return total, chosen


# =====================================================================
# 2. GREEDY RULE 2: highest fee first
#    Time: O(n log n) for the sort, then for each request we check it
#    against every accepted request -> O(n^2) in the worst case.
# =====================================================================

def greedy_highest_fee(requests):
    # make a list of (-fee, index) and sort it.
    # Using -fee means the BIGGEST fee comes first.
    order = []
    for i in range(len(requests)):
        order.append((-requests[i][2], i))
    order.sort()

    chosen = []
    total = 0

    for neg_fee, i in order:
        # check this request against every request we already accepted
        ok = True
        for j in chosen:
            if not fits(requests[i], requests[j]):
                ok = False
                break
        if ok:
            chosen.append(i)
            total = total + requests[i][2]

    chosen.sort()
    return total, chosen


# =====================================================================
# 3. DYNAMIC PROGRAMMING (always optimal)
#    Time: O(n log n)   (sort + one binary search per request)
#    Space: O(n)        (the OPT and p lists)
# =====================================================================

def best_schedule(requests):
    n = len(requests)

    # Step 1: sort the requests by finish time.
    # We use positions 1..n (position 0 means "no request").
    order = []
    for i in range(n):
        order.append((requests[i][1], requests[i][0], requests[i][2], i))
    order.sort()
    # order[k] = (finish, start, fee, original_index)

    finishes = []
    for k in range(n):
        finishes.append(order[k][0])    # sorted list of finish times

    # Step 2: p[j] = the last request (in sorted order) that fits before request j.
    # bisect_right(finishes, start) counts how many requests finish <= start.
    # Those are exactly the requests that end before j starts, so that count
    # is the position of the last one. p[j] = 0 means none fit.
    p = [0] * (n + 1)
    for j in range(1, n + 1):
        start_j = order[j - 1][1]
        p[j] = bisect_right(finishes, start_j)

    # Step 3: fill the table.
    # OPT[j] = best money using only the first j requests (in sorted order).
    # Either we SKIP request j          -> OPT[j-1]
    # or we TAKE request j              -> fee_j + OPT[p[j]]
    # OPT(j) = max(OPT(j-1), fee_j + OPT(p(j)))
    OPT = [0] * (n + 1)
    for j in range(1, n + 1):
        fee_j = order[j - 1][2]
        skip = OPT[j - 1]
        take = fee_j + OPT[p[j]]
        OPT[j] = max(skip, take)

    # Step 4: walk backwards through the table to find which requests we took.
    chosen = []
    j = n
    while j > 0:
        fee_j = order[j - 1][2]
        if fee_j + OPT[p[j]] > OPT[j - 1]:     # taking j was better
            chosen.append(order[j - 1][3])     # save its original index
            j = p[j]                           # jump to the last one that fits
        else:                                  # skipping j was as good or better
            j = j - 1

    chosen.sort()
    return OPT[n], chosen


# =====================================================================
# 4. BRUTE FORCE (only for checking, n <= 15)
#    Try every subset: 2^n subsets, and each check is O(n^2) pairs.
#    Time: O(2^n * n^2)
# =====================================================================

def brute_force(requests):
    n = len(requests)
    best_total = 0
    best_chosen = []

    for size in range(n + 1):                          # subsets of every size
        for subset in combinations(range(n), size):    # every subset of that size
            # check every pair in the subset fits
            ok = True
            for a in range(len(subset)):
                for b in range(a + 1, len(subset)):
                    if not fits(requests[subset[a]], requests[subset[b]]):
                        ok = False
            if ok:
                total = 0
                for i in subset:
                    total = total + requests[i][2]
                if total > best_total:
                    best_total = total
                    best_chosen = list(subset)

    return best_total, best_chosen


# Small demo using the example from the assignment
if __name__ == "__main__":
    requests = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000),
                (12, 14, 2500), (16, 18, 2000)]
    print("greedy_earliest_finish:", greedy_earliest_finish(requests))  # (7500, [0, 3, 4])
    print("greedy_highest_fee:    ", greedy_highest_fee(requests))
    print("best_schedule (DP):    ", best_schedule(requests))           # (10000, [1, 4])
    print("brute_force:           ", brute_force(requests))
