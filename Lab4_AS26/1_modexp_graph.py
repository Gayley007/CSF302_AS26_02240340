# Topic 6 (part 2): Timing naive vs binary modular exponentiation

import os
import time
import importlib
import matplotlib.pyplot as plt

lab = importlib.import_module("1_modular_exponentiation")

a, m = 123456789, 1000000007
exponents = [10, 100, 1000, 10000, 100000, 1000000]
naive_times = []
binary_times = []

print("exponent    naive (s)     binary (s)")
for b in exponents:
    start = time.perf_counter()
    lab.naive_power(a, b, m)
    naive_times.append(time.perf_counter() - start)

    start = time.perf_counter()
    lab.binary_power(a, b, m)
    binary_times.append(time.perf_counter() - start)

    print(f"{b:<10}  {naive_times[-1]:.6f}      {binary_times[-1]:.6f}")

plt.plot(exponents, naive_times, marker="o", label="Naive O(b)")
plt.plot(exponents, binary_times, marker="s", label="Binary O(log b)")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Exponent b")
plt.ylabel("Time (seconds)")
plt.title("Naive vs Binary Modular Exponentiation")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(os.path.dirname(__file__), "1_modexp_graph.png"))
plt.show()
