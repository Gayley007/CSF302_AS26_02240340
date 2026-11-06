# Topic 7 (part 2): Benchmark naive vs binary matrix exponentiation

import os
import time
import random
import importlib
import matplotlib.pyplot as plt

lab = importlib.import_module("2_matrix_exponentiation")

m = 1000000007
dimensions = [2, 5, 10]
exponents = [8, 16, 32, 64, 128, 256]

print("dim  exponent  naive (s)   binary (s)")
for d in dimensions:
    A = [[random.randint(0, 9) for j in range(d)] for i in range(d)]
    naive_times = []
    binary_times = []

    for n in exponents:
        start = time.perf_counter()
        lab.naive_matrix_power(A, n, m)
        naive_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        lab.binary_matrix_power(A, n, m)
        binary_times.append(time.perf_counter() - start)

        print(f"{d:<4} {n:<9} {naive_times[-1]:.6f}    {binary_times[-1]:.6f}")

    plt.plot(exponents, naive_times, marker="o", label=f"Naive d={d}")
    plt.plot(exponents, binary_times, marker="s", linestyle="--", label=f"Binary d={d}")

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Exponent n")
plt.ylabel("Time (seconds)")
plt.title("Naive vs Binary Matrix Exponentiation")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(os.path.dirname(__file__), "2_matrix_exp_graph.png"))
plt.show()
