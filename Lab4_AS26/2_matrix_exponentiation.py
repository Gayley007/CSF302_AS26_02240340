# Topic 7: Efficient Matrix Modular Exponentiation  (A^n mod m)


# 1. Multiply two square matrices, each element mod m
def multiply(A, B, m):
    d = len(A)
    C = [[0] * d for i in range(d)]
    for i in range(d):
        for j in range(d):
            for k in range(d):
                C[i][j] += A[i][k] * B[k][j]
            C[i][j] %= m
    return C


# 2. Identity matrix of size d
def identity(d):
    I = [[0] * d for i in range(d)]
    for i in range(d):
        I[i][i] = 1
    return I


# 3. Naive: multiply by A, n times  ->  O(n * d^3)
def naive_matrix_power(A, n, m):
    result = identity(len(A))
    for i in range(n):
        result = multiply(result, A, m)
    return result


# 4. Binary (repeated squaring)  ->  O(log n * d^3)
def binary_matrix_power(A, n, m):
    result = identity(len(A))
    while n > 0:
        if n % 2 == 1:
            result = multiply(result, A, m)
        A = multiply(A, A, m)
        n = n // 2
    return result


# 5. nth Fibonacci mod m:  [[1,1],[1,0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]]
def fibonacci(n, m):
    return binary_matrix_power([[1, 1], [1, 0]], n, m)[0][1]


# 6. Number of walks with exactly k edges from u to v = entry [u][v] of adj^k
def count_walks(adj, u, v, k, m):
    return binary_matrix_power(adj, k, m)[u][v]


if __name__ == "__main__":
    print("Compare naive and binary")
    tests = [
        ([[1, 1], [1, 0]], 10, 1000),
        ([[2, 3], [4, 5]], 0, 7),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 15, 97),
        ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 1, 2, 3], [4, 5, 6, 7]], 50, 1000000007),
    ]
    for A, n, m in tests:
        r1 = naive_matrix_power(A, n, m)
        r2 = binary_matrix_power(A, n, m)
        print(f"{len(A)}x{len(A)} matrix, n={n}, m={m}:  {r2}  match={r1 == r2}")

    print("\nFibonacci mod 1000000007")
    for n in [10, 50, 100]:
        print(f"F({n}) = {fibonacci(n, 1000000007)}")

    print("\nLarge Fibonacci (no earlier terms generated)")
    for n in [10**6, 10**12, 10**18]:
        print(f"F({n}) mod 1000000007 = {fibonacci(n, 1000000007)}")

    print("\nCounting walks")
    # edges: 0->1, 0->2, 1->2, 2->0, 2->3, 3->1
    adj = [[0, 1, 1, 0],
           [0, 0, 1, 0],
           [1, 0, 0, 1],
           [0, 1, 0, 0]]
    for k in [1, 2, 3, 4, 5, 10]:
        print(f"Walks from 0 to 2 with {k} edges = {count_walks(adj, 0, 2, k, 1000000007)}")
