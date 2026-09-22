# Q1: Matrix Multiplication - Traditional (O(n^3)) vs Strassen's Algorithm

import random
import time

def make_matrix(n, manual=False, name="A"):
    """Create an n x n matrix, either typed by the user or random."""
    if manual:
        print("Enter %d rows of matrix %s (%d numbers per row, space separated):" % (n, name, n))
        return [[int(x) for x in input().split()] for _ in range(n)]
    return [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]


def display(M, name):
    print("\nMatrix %s:" % name)
    for row in M:
        print(" ".join("%6d" % v for v in row))


def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def split(M):
    """Split matrix into 4 equal quadrants."""
    n = len(M) // 2
    a11 = [row[:n] for row in M[:n]]
    a12 = [row[n:] for row in M[:n]]
    a21 = [row[:n] for row in M[n:]]
    a22 = [row[n:] for row in M[n:]]
    return a11, a12, a21, a22


def join(c11, c12, c21, c22):
    """Join 4 quadrants back into one matrix."""
    top = [c11[i] + c12[i] for i in range(len(c11))]
    bottom = [c21[i] + c22[i] for i in range(len(c21))]
    return top + bottom


# - Algorithm 1: Traditional -

def traditional(A, B):
    """Classic triple nested loop. Time complexity O(n^3)."""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total += A[i][k] * B[k][j]
            C[i][j] = total
    return C


# - Algorithm 2: Strassen -

def strassen(A, B):
    """Divide and conquer using only 7 multiplications per split.
       Time complexity O(n^2.81)."""
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    a11, a12, a21, a22 = split(A)
    b11, b12, b21, b22 = split(B)

    # The 7 products (instead of 8 in the naive divide and conquer)
    p1 = strassen(a11, sub(b12, b22))
    p2 = strassen(add(a11, a12), b22)
    p3 = strassen(add(a21, a22), b11)
    p4 = strassen(a22, sub(b21, b11))
    p5 = strassen(add(a11, a22), add(b11, b22))
    p6 = strassen(sub(a12, a22), add(b21, b22))
    p7 = strassen(sub(a11, a21), add(b11, b12))

    c11 = add(sub(add(p5, p4), p2), p6)
    c12 = add(p1, p2)
    c21 = add(p3, p4)
    c22 = sub(sub(add(p5, p1), p3), p7)

    return join(c11, c12, c21, c22)


# - Main program -

def main():
    print("=" * 55)
    print(" Q1: Traditional vs Strassen Matrix Multiplication")
    print("=" * 55)

    n = int(input("Enter matrix size n (power of 2, e.g. 2 4 8 16): "))
    if n & (n - 1) != 0:
        print("Error: n must be a power of 2.")
        return

    choice = input("Input matrices manually? (y/n): ").strip().lower()
    manual = (choice == "y")

    A = make_matrix(n, manual, "A")
    B = make_matrix(n, manual, "B")

    display(A, "A")
    display(B, "B")

    t0 = time.time()
    C1 = traditional(A, B)
    t1 = time.time()
    C2 = strassen(A, B)
    t2 = time.time()

    display(C1, "C (Traditional)")
    display(C2, "C (Strassen)")

    print("\nBoth results match!" if C1 == C2 else "\nResults DO NOT match!")
    print("Traditional time : %.6f seconds" % (t1 - t0))
    print("Strassen time    : %.6f seconds" % (t2 - t1))


if __name__ == "__main__":
    main()


# - Conclusion -
# Traditional method: 3 nested loops -> n*n*n multiplications = O(n^3).
# Strassen: splits each matrix into 4 quadrants and uses 7 recursive
# multiplications instead of 8, giving the recurrence
#       T(n) = 7*T(n/2) + O(n^2)   ->   T(n) = O(n^log2(7)) = O(n^2.81)
# So asymptotically Strassen does fewer multiplications and grows slower.
# However, for small n this Python version of Strassen is actually SLOWER
# because of the overhead of recursion and the many matrix additions /
# subtractions and list slicing it performs. The crossover point where
# Strassen wins appears only at large n (in an optimised language).
# Both algorithms always produce the same resultant matrix (verified above).
