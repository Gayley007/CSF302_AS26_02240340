# Lab 7 - Q4: Randomized algorithms
# Run with:  python lab7_q4_randomized.py
#   Part 1: randomized quickselect vs sort-then-index
#   Part 2: Miller-Rabin vs trial division on 12-digit numbers
#   Part 3: Miller-Rabin (1 round) on the Carmichael number 561

import random
import time

random.seed(7)


# ===============================================================
# Part 1: Randomized quickselect - the k-th smallest (k = 0 is the smallest)
# ===============================================================

def quickselect(a, k):
    while True:
        pivot = random.choice(a)          # random pivot -> expected O(n)
        smaller = []
        equal = []
        bigger = []
        for x in a:                       # split into three groups
            if x < pivot:
                smaller.append(x)
            elif x == pivot:
                equal.append(x)
            else:
                bigger.append(x)

        if k < len(smaller):              # answer is in the smaller group
            a = smaller
        elif k < len(smaller) + len(equal):
            return pivot                  # answer is the pivot itself
        else:                             # answer is in the bigger group
            k = k - len(smaller) - len(equal)
            a = bigger


def sort_select(a, k):
    return sorted(a)[k]                   # O(n log n)


# ===============================================================
# Part 2: Primality tests
# ===============================================================

def trial_division(n):
    # try every odd divisor up to sqrt(n)
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def miller_rabin(n, rounds):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # write n - 1 = 2^s * d with d odd
    s = 0
    d = n - 1
    while d % 2 == 0:
        d = d // 2
        s += 1

    for _ in range(rounds):
        a = random.randint(2, n - 2)      # random base
        x = pow(a, d, n)                  # a^d mod n (fast)
        if x == 1 or x == n - 1:
            continue                      # this base says "maybe prime"
        found = False
        for _ in range(s - 1):            # square up to s-1 times
            x = pow(x, 2, n)
            if x == n - 1:
                found = True
                break
        if not found:
            return False                  # definitely composite
    return True                           # probably prime


if __name__ == "__main__":
    print("=== Part 1: quickselect vs sort-then-index (median, best of 3) ===")
    print("  n          quickselect (s)  sort (s)   same answer?")
    for n in [10**4, 10**5, 10**6]:
        a = []
        for _ in range(n):
            a.append(random.randint(0, 10**9))
        k = n // 2                        # find the median
        q_times = []
        s_times = []
        for _ in range(3):
            start = time.perf_counter()
            q = quickselect(a, k)
            q_times.append(time.perf_counter() - start)
            start = time.perf_counter()
            s = sort_select(a, k)
            s_times.append(time.perf_counter() - start)
        print("  " + str(n).ljust(10) + format(min(q_times), ".4f").rjust(14)
              + format(min(s_times), ".4f").rjust(11) + "     " + str(q == s))

    # check quickselect on many small lists, every k
    ok = True
    for _ in range(1000):
        a = []
        for _ in range(random.randint(1, 30)):
            a.append(random.randint(0, 20))        # small range -> many repeats
        for k in range(len(a)):
            if quickselect(a, k) != sorted(a)[k]:
                ok = False
    print("  correct on 1,000 small random lists (every k):", ok)

    print("\n=== Part 2: Miller-Rabin (20 rounds) vs trial division ===")
    print("  number          trial  MR     trial (s)  MR (s)")
    agree = 0
    primes = 0
    for _ in range(20):
        n = random.randint(10**11, 10**12 - 1)     # a random 12-digit number
        start = time.perf_counter()
        t = trial_division(n)
        t_time = time.perf_counter() - start
        start = time.perf_counter()
        m = miller_rabin(n, 20)
        m_time = time.perf_counter() - start
        if t == m:
            agree += 1
        if t:
            primes += 1
        print("  " + str(n) + "  " + str(t).ljust(6) + " " + str(m).ljust(6)
              + format(t_time, ".5f").rjust(9) + format(m_time, ".5f").rjust(9))
    print("  agree on", agree, "of 20 numbers;", primes, "of them are prime")

    # random numbers are mostly composite with small factors, so trial
    # division finishes early. Primes are its worst case - test 5 of them.
    print("\n  Five 12-digit PRIMES (worst case for trial division):")
    print("  number          trial  MR     trial (s)  MR (s)")
    found = 0
    while found < 5:
        n = random.randint(10**11, 10**12 - 1)
        if not miller_rabin(n, 20):
            continue
        found += 1
        start = time.perf_counter()
        t = trial_division(n)
        t_time = time.perf_counter() - start
        start = time.perf_counter()
        m = miller_rabin(n, 20)
        m_time = time.perf_counter() - start
        print("  " + str(n) + "  " + str(t).ljust(6) + " " + str(m).ljust(6)
              + format(t_time, ".5f").rjust(9) + format(m_time, ".5f").rjust(9))

    print("\n=== Part 3: Miller-Rabin with 1 round on 561 = 3 x 11 x 17 ===")
    says_prime = 0
    for _ in range(1000):
        if miller_rabin(561, 1):
            says_prime += 1
    print("  answered 'prime'", says_prime, "times out of 1000 ("
          + str(says_prime / 10) + "%)")

    # which bases fool it? (try every base once)
    liars = []
    for a in range(2, 560):
        x = pow(a, 35, 561)               # 560 = 2^4 * 35
        fooled = (x == 1 or x == 560)
        for _ in range(3):
            if fooled:
                break
            x = pow(x, 2, 561)
            if x == 560:
                fooled = True
        if fooled:
            liars.append(a)
    print("  bases from 2 to 559 that fool the test:", liars)
    print("  expected rate =", len(liars), "/ 558 =",
          str(round(100 * len(liars) / 558, 2)) + "%")
    # compare with the simpler Fermat test (a^(n-1) = 1 mod n means "prime")
    fermat_liars = 0
    for a in range(2, 560):
        if pow(a, 560, 561) == 1:
            fermat_liars += 1
    print("  Fermat test for comparison: bases with a^560 = 1 (mod 561):",
          fermat_liars, "of 558")
