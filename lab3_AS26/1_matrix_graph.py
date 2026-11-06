# Q1 (part 2): Performance comparison table + graph
# Runs both algorithms on random matrices of increasing size and plots the times.

import time
import importlib.util
from pathlib import Path

import matplotlib.pyplot as plt

algorithm_path = Path(__file__).with_name("1_matrix_multiplication.py")
spec = importlib.util.spec_from_file_location("matrix_multiplication", algorithm_path)
matrix_multiplication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(matrix_multiplication)

make_matrix = matrix_multiplication.make_matrix
traditional = matrix_multiplication.traditional
strassen = matrix_multiplication.strassen

sizes = [2, 4, 8, 16, 32, 64, 128]
trad_times = []
stra_times = []

print("%-8s %-18s %-18s %-8s" % ("n", "Traditional (s)", "Strassen (s)", "Match"))
print("-" * 56)

for n in sizes:
    A = make_matrix(n)
    B = make_matrix(n)

    t0 = time.time()
    C1 = traditional(A, B)
    t1 = time.time()
    C2 = strassen(A, B)
    t2 = time.time()

    trad_times.append(t1 - t0)
    stra_times.append(t2 - t1)
    print("%-8d %-18.6f %-18.6f %-8s" % (n, t1 - t0, t2 - t1, "YES" if C1 == C2 else "NO"))

plt.plot(sizes, trad_times, "o-", label="Traditional O(n^3)")
plt.plot(sizes, stra_times, "s-", label="Strassen O(n^2.81)")
plt.xlabel("Matrix size n")
plt.ylabel("Time (seconds)")
plt.title("Traditional vs Strassen Matrix Multiplication")
plt.legend()
plt.grid(True)
plt.savefig("matrix_graph.png")
print("\nGraph saved as matrix_graph.png")
plt.show()
