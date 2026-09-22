# Q2 (part 2): Performance comparison table + graph

import time
import importlib.util
from pathlib import Path

import matplotlib.pyplot as plt

algorithm_path = Path(__file__).with_name("2_karatsuba.py")
spec = importlib.util.spec_from_file_location("karatsuba_algorithm", algorithm_path)
karatsuba_algorithm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(karatsuba_algorithm)

traditional = karatsuba_algorithm.traditional
karatsuba = karatsuba_algorithm.karatsuba
random_number = karatsuba_algorithm.random_number
pad_to_power_of_2 = karatsuba_algorithm.pad_to_power_of_2

sizes = [8, 16, 32, 64, 128, 256, 512, 1024]
trad_times = []
kara_times = []

print("%-10s %-18s %-18s %-8s" % ("digits", "Traditional (s)", "Karatsuba (s)", "Match"))
print("-" * 58)

for d in sizes:
    x = random_number(d)
    y = random_number(d)
    xp, yp = pad_to_power_of_2(x, y)

    t0 = time.time()
    r1 = traditional(xp, yp)
    t1 = time.time()
    r2 = karatsuba(xp, yp)
    t2 = time.time()

    trad_times.append(t1 - t0)
    kara_times.append(t2 - t1)
    print("%-10d %-18.6f %-18.6f %-8s" % (d, t1 - t0, t2 - t1, "YES" if r1 == r2 else "NO"))

plt.plot(sizes, trad_times, "o-", label="Traditional O(n^2)")
plt.plot(sizes, kara_times, "s-", label="Karatsuba O(n^1.585)")
plt.xlabel("Number of digits n")
plt.ylabel("Time (seconds)")
plt.title("Traditional vs Karatsuba Multiplication")
plt.legend()
plt.grid(True)
plt.savefig("karatsuba_graph.png")
print("\nGraph saved as karatsuba_graph.png")
plt.show()
