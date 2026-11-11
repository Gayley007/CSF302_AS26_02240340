# Lab 6 - Q1: Rod Cutting
# Three versions: naive recursion, top-down memoization, bottom-up table.

import time

# price[i] = price of a piece of length i  (price[0] is not used)
price = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
# extend the table: p[i] = 3 * i for i > 10, up to length 25
for i in range(11, 26):
    price.append(3 * i)

calls = 0     # counts how many times a recursive function is called


# ---------------------------------------------------------------
# 1. Naive recursion  ->  O(2^n)
#    Try every first piece i, then solve the rest (n - i) again.
# ---------------------------------------------------------------
def cut_rod_naive(n):
    global calls
    calls += 1
    if n == 0:
        return 0
    best = -1
    for i in range(1, n + 1):
        best = max(best, price[i] + cut_rod_naive(n - i))
    return best


# ---------------------------------------------------------------
# 2. Top-down with memoization  ->  O(n^2)
#    Same as naive, but each answer is saved in memo[] and reused.
# ---------------------------------------------------------------
def cut_rod_memo(n):
    memo = [-1] * (n + 1)          # -1 means "not solved yet"
    return memo_helper(n, memo)


def memo_helper(n, memo):
    global calls
    calls += 1
    if memo[n] >= 0:               # already solved -> just return it
        return memo[n]
    if n == 0:
        best = 0
    else:
        best = -1
        for i in range(1, n + 1):
            best = max(best, price[i] + memo_helper(n - i, memo))
    memo[n] = best
    return best


# ---------------------------------------------------------------
# 3. Bottom-up  ->  O(n^2), no recursion at all
#    Solve length 1, then 2, then 3 ... each uses the smaller ones.
#    first_cut[j] remembers the best first piece for length j.
# ---------------------------------------------------------------
def cut_rod_bottom_up(n):
    revenue = [0] * (n + 1)
    first_cut = [0] * (n + 1)
    for j in range(1, n + 1):
        best = -1
        for i in range(1, j + 1):
            if price[i] + revenue[j - i] > best:
                best = price[i] + revenue[j - i]
                first_cut[j] = i
        revenue[j] = best
    return revenue, first_cut


def get_pieces(n, first_cut):
    # Follow first_cut: cut off the best first piece, repeat on what is left.
    pieces = []
    while n > 0:
        pieces.append(first_cut[n])
        n = n - first_cut[n]
    return pieces


if __name__ == "__main__":
    # ---------- n = 1 to 10: best revenue and pieces ----------
    revenue, first_cut = cut_rod_bottom_up(10)
    print(f"{'n':>3} | {'revenue':>7} | {'naive':>5} | {'memo':>5} | pieces")
    for n in range(1, 11):
        print(f"{n:>3} | {revenue[n]:>7} | {cut_rod_naive(n):>5} | {cut_rod_memo(n):>5} | "
              f"{get_pieces(n, first_cut)}")

    # ---------- Calls and time for bigger n ----------
    print(f"\n{'n':>3} | {'naive calls':>12} {'time(s)':>9} | {'memo calls':>10} {'time(s)':>9} | "
          f"{'bottom-up calls':>15} {'time(s)':>9} | revenue")
    for n in [5, 10, 15, 20, 25]:
        calls = 0
        start = time.perf_counter()
        r1 = cut_rod_naive(n)
        t1 = time.perf_counter() - start
        naive_calls = calls

        calls = 0
        start = time.perf_counter()
        r2 = cut_rod_memo(n)
        t2 = time.perf_counter() - start
        memo_calls = calls

        start = time.perf_counter()
        revenue, first_cut = cut_rod_bottom_up(n)
        t3 = time.perf_counter() - start
        # bottom-up makes 0 recursive calls (it only uses loops)

        print(f"{n:>3} | {naive_calls:>12,} {t1:>9.5f} | {memo_calls:>10,} {t2:>9.5f} | "
              f"{0:>15} {t3:>9.5f} | {r1} {r2} {revenue[n]}")
