# Assignment 2 - Part A: Closest Camera Traps
#
# Input : a list of n >= 2 points (x, y)
# Output: (d, i, j) = the smallest distance d, and the indices i < j
#         of the two points that are that close.
#
# Example: [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
#          -> (1.414..., 0, 5)   because (2, 3) and (3, 4) are closest.
#
# Note: inside the code we compare SQUARED distances (dx*dx + dy*dy).
# This avoids calling sqrt again and again, and it gives the same
# winner because a smaller distance always has a smaller square.
# We only take the square root once, at the very end.

import math


def squared_distance(p, q):
    # p and q are (x, y, ...) - we only use the first two values
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


# ------------------------------------------------------------------
# 1. Brute force: check every pair.  Theta(n^2)
# ------------------------------------------------------------------

def closest_pair_brute(points):
    n = len(points)
    best = None                  # smallest squared distance so far
    best_i = 0
    best_j = 1

    for i in range(n):
        for j in range(i + 1, n):          # j > i, so every pair once
            d = squared_distance(points[i], points[j])
            if best is None or d < best:
                best = d
                best_i = i
                best_j = j

    return (math.sqrt(best), best_i, best_j)


# ------------------------------------------------------------------
# 2. Divide and conquer.  Theta(n log n)
# ------------------------------------------------------------------
#
# Plan:
#   - Sort the points by x ONCE at the start.
#   - solve(part) works on a list sorted by x and returns two things:
#       (a) the best pair in that part, as (squared_distance, i, j)
#       (b) the same points sorted by y   (we build this like merge sort)
#   - Split at the middle, solve the left half and the right half.
#   - delta = the best distance found in either half.
#   - A closer pair could still cross the dividing line, so we look at
#     the "strip": the points whose x is within delta of the line
#     (so the strip is 2*delta wide). Because the strip is sorted by y,
#     each point only needs to be compared with the next few points
#     above it (we stop as soon as the y gap is already >= delta).

def closest_pair(points):
    # remember each point's original index: (x, y, index)
    labelled = []
    for index in range(len(points)):
        x, y = points[index]
        labelled.append((x, y, index))

    # sort by x (and by y when x is the same)
    by_x = sorted(labelled)

    best, by_y = solve(by_x)
    d_squared, i, j = best

    # the question wants i < j
    if i > j:
        i, j = j, i
    return (math.sqrt(d_squared), i, j)


def solve(by_x):
    n = len(by_x)

    # ----- base case: 3 or fewer points, just check every pair -----
    if n <= 3:
        best = None
        for a in range(n):
            for b in range(a + 1, n):
                d = squared_distance(by_x[a], by_x[b])
                if best is None or d < best[0]:
                    best = (d, by_x[a][2], by_x[b][2])
        # sort these few points by y (key = the y value)
        by_y = sorted(by_x, key=get_y)
        return best, by_y

    # ----- divide: split into left half and right half -----
    mid = n // 2
    mid_x = by_x[mid][0]          # x of the dividing line
    left = by_x[:mid]
    right = by_x[mid:]

    # ----- conquer: solve each half -----
    best_left, left_by_y = solve(left)
    best_right, right_by_y = solve(right)

    # best of the two halves
    if best_left[0] <= best_right[0]:
        best = best_left
    else:
        best = best_right

    # ----- combine step 1: merge the two y-sorted lists (like merge sort) -----
    by_y = merge_by_y(left_by_y, right_by_y)

    # ----- combine step 2: check the strip around the dividing line -----
    # keep the points whose x is closer than delta to the line
    # (we compare squares: (x - mid_x)^2 < delta^2)
    strip = []
    for p in by_y:
        dx = p[0] - mid_x
        if dx * dx < best[0]:
            strip.append(p)

    # strip is sorted by y. Compare each point with the points above it,
    # but stop once the y gap alone is already as big as delta.
    for a in range(len(strip)):
        b = a + 1
        while b < len(strip):
            dy = strip[b][1] - strip[a][1]
            if dy * dy >= best[0]:
                break                       # everything further up is too far
            d = squared_distance(strip[a], strip[b])
            if d < best[0]:
                best = (d, strip[a][2], strip[b][2])
            b = b + 1

    return best, by_y


def get_y(point):
    # used as the sort key: sort by y
    return point[1]


def merge_by_y(left, right):
    # merge two lists that are already sorted by y (same as in merge sort)
    result = []
    a = 0
    b = 0
    while a < len(left) and b < len(right):
        if left[a][1] <= right[b][1]:
            result.append(left[a])
            a = a + 1
        else:
            result.append(right[b])
            b = b + 1
    # one list is finished - copy what is left of the other one
    while a < len(left):
        result.append(left[a])
        a = a + 1
    while b < len(right):
        result.append(right[b])
        b = b + 1
    return result


# quick check when you run this file directly:  python closest.py
if __name__ == "__main__":
    example = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print("brute force      :", closest_pair_brute(example))
    print("divide & conquer :", closest_pair(example))
