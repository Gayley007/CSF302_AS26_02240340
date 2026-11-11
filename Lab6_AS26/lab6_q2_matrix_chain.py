# Lab 6 - Q2: Matrix Chain Multiplication
# Matrix Ai has size p[i-1] x p[i].  There are n = len(p) - 1 matrices.

import random


# ---------------------------------------------------------------
# 1. Bottom-up DP  ->  O(n^3)
#    m[i][j] = least multiplications to compute Ai...Aj
#    s[i][j] = where to split Ai...Aj for that best cost
# ---------------------------------------------------------------
def matrix_chain_order(p):
    n = len(p) - 1
    # make (n+1) x (n+1) tables so we can use 1-based indexes like the notes
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):              # chain length 2, 3, ..., n
        for i in range(1, n - length + 2):
            j = i + length - 1
            m[i][j] = float("inf")
            for k in range(i, j):               # try every split point
                # cost = left part + right part + multiply the two results
                cost = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    return m, s


# 2. Build the brackets string from the s table, e.g. ((A1(A2A3))A4)
def parens(s, i, j):
    if i == j:
        return "A" + str(i)
    k = s[i][j]
    return "(" + parens(s, i, k) + parens(s, k + 1, j) + ")"


# ---------------------------------------------------------------
# 3. Brute force: recursion that tries every split, NO saving  ->  exponential
# ---------------------------------------------------------------
def brute_force(p, i, j):
    if i == j:
        return 0
    best = float("inf")
    for k in range(i, j):
        cost = brute_force(p, i, k) + brute_force(p, k + 1, j) + p[i - 1] * p[k] * p[j]
        best = min(best, cost)
    return best


# Left to right order: ((A1A2)A3)A4 ...
# The running result is always p[0] x p[i], times next matrix p[i] x p[i+1].
def left_to_right_cost(p):
    n = len(p) - 1
    cost = 0
    for i in range(1, n):
        cost += p[0] * p[i] * p[i + 1]
    return cost


def run_test(name, p):
    n = len(p) - 1
    m, s = matrix_chain_order(p)
    print(f"\n{name}: p = {p}  ({n} matrices)")
    print(f"  Optimal cost       : {m[1][n]:,}")
    print(f"  Optimal brackets   : {parens(s, 1, n)}")
    print(f"  Left-to-right cost : {left_to_right_cost(p):,}")
    if n <= 8:
        bf = brute_force(p, 1, n)
        print(f"  Brute force cost   : {bf:,}   match = {bf == m[1][n]}")


if __name__ == "__main__":
    run_test("Test 1", [30, 35, 15, 5, 10, 20, 25])     # expected 15,125
    run_test("Test 2", [5, 4, 6, 2, 7])

    random.seed(6)      # fixed seed so the "random" chains are the same every run
    for t in range(1, 6):
        n = random.randint(3, 8)                         # 3 to 8 matrices
        p = [random.randint(5, 50) for _ in range(n + 1)]
        run_test(f"Random {t}", p)
