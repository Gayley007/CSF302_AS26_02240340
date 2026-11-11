# Lab 6 - Q3: Longest Common Subsequence (LCS)

import os
import random
import time


# ---------------------------------------------------------------
# 1. Fill the LCS table bottom-up  ->  O(m * n)
#    c[i][j] = LCS length of the first i items of X and first j items of Y
#    Works for strings AND for lists of lines (used in the diff below).
# ---------------------------------------------------------------
def lcs_table(X, Y):
    m = len(X)
    n = len(Y)
    c = [[0] * (n + 1) for _ in range(m + 1)]   # row 0 and column 0 stay 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1           # match: diagonal + 1
            else:
                c[i][j] = max(c[i - 1][j], c[i][j - 1])  # no match: best of up / left
    return c


def print_table(X, Y, c):
    print("      " + "  ".join("-" + Y))         # header: - B D C A B A
    for i in range(len(X) + 1):
        if i == 0:
            label = "-"
        else:
            label = X[i - 1]
        row = "  ".join(str(v) for v in c[i])
        print(f"   {label}  {row}")


# ---------------------------------------------------------------
# 2. Rebuild one LCS by walking back from the bottom-right corner
# ---------------------------------------------------------------
def get_lcs(X, Y, c):
    i = len(X)
    j = len(Y)
    result = []
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:          # this char is in the LCS
            result.append(X[i - 1])
            i -= 1
            j -= 1
        elif c[i - 1][j] >= c[i][j - 1]:  # move to the bigger neighbour
            i -= 1
        else:
            j -= 1
    result.reverse()                       # we collected it backwards
    return "".join(result)


# ---------------------------------------------------------------
# 3. Space-saving version: keeps only 2 rows -> O(n) memory, length only
# ---------------------------------------------------------------
def lcs_length_two_rows(X, Y):
    n = len(Y)
    prev = [0] * (n + 1)          # row i-1
    for i in range(1, len(X) + 1):
        curr = [0] * (n + 1)      # row i
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr               # current row becomes the previous row
    return prev[n]


# ---------------------------------------------------------------
# 4. Brute force: try EVERY subsequence of X  ->  O(2^m * n)
# ---------------------------------------------------------------
def is_subsequence(s, Y):
    # walk through Y, ticking off the chars of s in order
    k = 0
    for ch in Y:
        if k < len(s) and s[k] == ch:
            k += 1
    return k == len(s)


def lcs_brute_force(X, Y):
    m = len(X)
    best = 0
    # Each number "mask" from 0 to 2^m - 1 picks one subsequence:
    # if bit i of mask is 1, we take X[i].  Example m=3, mask=5 (101) -> X[0] + X[2]
    for mask in range(2 ** m):
        sub = ""
        for i in range(m):
            if (mask >> i) & 1:
                sub += X[i]
        if len(sub) > best and is_subsequence(sub, Y):
            best = len(sub)
    return best


# ---------------------------------------------------------------
# 5. Line-by-line diff using LCS of the LINES
# ---------------------------------------------------------------
def diff(old_lines, new_lines):
    c = lcs_table(old_lines, new_lines)
    i = len(old_lines)
    j = len(new_lines)
    output = []
    # Walk back like get_lcs. Lines in the LCS are unchanged,
    # lines only in old are removed (-), lines only in new are added (+).
    while i > 0 or j > 0:
        if i > 0 and j > 0 and old_lines[i - 1] == new_lines[j - 1]:
            output.append("  " + old_lines[i - 1])
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or c[i][j - 1] >= c[i - 1][j]):
            output.append("+ " + new_lines[j - 1])
            j -= 1
        else:
            output.append("- " + old_lines[i - 1])
            i -= 1
    output.reverse()
    return output


def read_lines(filename):
    with open(filename) as f:
        return f.read().splitlines()


if __name__ == "__main__":
    folder = os.path.dirname(os.path.abspath(__file__))

    # ---------- Table + one LCS ----------
    X = "ABCBDAB"
    Y = "BDCABA"
    c = lcs_table(X, Y)
    print(f"LCS table for X = {X}, Y = {Y}\n")
    print_table(X, Y, c)
    print("\nLCS length          :", c[len(X)][len(Y)])
    print("One LCS             :", get_lcs(X, Y, c))
    print("Two-row length      :", lcs_length_two_rows(X, Y))
    print("Brute force length  :", lcs_brute_force(X, Y))

    # ---------- DP vs brute force timing ----------
    print(f"\n{'length':>6} | {'DP (s)':>9} | {'brute force (s)':>15} | {'LCS':>3} | match")
    for length in range(5, 19):
        A = "".join(random.choice("ABCD") for _ in range(length))
        B = "".join(random.choice("ABCD") for _ in range(length))
        start = time.perf_counter()
        dp = lcs_length_two_rows(A, B)
        t_dp = time.perf_counter() - start
        start = time.perf_counter()
        bf = lcs_brute_force(A, B)
        t_bf = time.perf_counter() - start
        print(f"{length:>6} | {t_dp:>9.6f} | {t_bf:>15.4f} | {dp:>3} | {dp == bf}")

    # ---------- Diff of two text files ----------
    old_lines = read_lines(os.path.join(folder, "old.txt"))
    new_lines = read_lines(os.path.join(folder, "new.txt"))
    print("\nDiff old.txt -> new.txt  ('-' removed, '+' added, '  ' unchanged)\n")
    for line in diff(old_lines, new_lines):
        print(line)
