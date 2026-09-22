# Q3: Binary Search vs Ternary Search (menu driven)

import random
import math

array = []          # the current sorted array


# - Algorithm 1: Binary Search -

def binary_search(arr, key):
    """Splits the range in two. One key-vs-element comparison per level.
       Recurrence: T(n) = T(n/2) + O(1)  ->  about log2(n) comparisons."""
    lo, hi = 0, len(arr) - 1
    count = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        count += 1                      # comparison with arr[mid]
        if arr[mid] == key:
            return mid, count
        elif key < arr[mid]:
            hi = mid - 1
        else:
            lo = mid + 1

    return -1, count


# - Algorithm 2: Ternary Search -

def ternary_search(arr, key):
    """Splits the range in three. Needs TWO key-vs-element comparisons
       per level (at mid1 and mid2).
       Recurrence: T(n) = T(n/3) + O(1)  ->  about log3(n) levels,
       so about 2*log3(n) comparisons."""
    lo, hi = 0, len(arr) - 1
    count = 0

    while lo <= hi:
        third = (hi - lo) // 3
        mid1 = lo + third
        mid2 = hi - third

        count += 1                      # comparison with arr[mid1]
        if arr[mid1] == key:
            return mid1, count

        if mid1 != mid2:
            count += 1                  # comparison with arr[mid2]
            if arr[mid2] == key:
                return mid2, count

        if key < arr[mid1]:
            hi = mid1 - 1
        elif key > arr[mid2]:
            lo = mid2 + 1
        else:
            lo = mid1 + 1
            hi = mid2 - 1

    return -1, count


# - Menu options -

def generate_array():
    global array
    n = int(input("Enter n (how many numbers): "))
    array = sorted(random.sample(range(1, n * 10 + 10), n))
    print("Generated a sorted array of %d numbers." % n)


def display_array():
    if not array:
        print("Array is empty. Use option 1 first.")
        return
    print("\nArray (%d elements):" % len(array))
    print(array)


def do_search(search_func, name):
    if not array:
        print("Array is empty. Use option 1 first.")
        return
    key = int(input("Enter the key to search: "))
    index, count = search_func(array, key)
    if index == -1:
        print("%s: key %d NOT FOUND." % (name, key))
    else:
        print("%s: key %d found at index %d." % (name, key, index))
    print("Step / frequency count (comparisons) = %d" % count)


def best_case():
    """Key present at the very first probe -> minimum comparisons."""
    if not array:
        print("Array is empty. Use option 1 first.")
        return
    n = len(array)

    # binary search probes the middle element first
    bkey = array[(n - 1) // 2]
    _, bc = binary_search(array, bkey)

    # ternary search probes the element at index (n-1)//3 first
    tkey = array[(n - 1) // 3]
    _, tc = ternary_search(array, tkey)

    print("\n--- BEST CASE (key found on the first probe), n = %d ---" % n)
    print("Binary  : key = %-8d comparisons = %d" % (bkey, bc))
    print("Ternary : key = %-8d comparisons = %d" % (tkey, tc))
    print("Both need only 1 comparison in the best case: O(1).")


def worst_case():
    """Key absent -> the search runs until the range becomes empty."""
    if not array:
        print("Array is empty. Use option 1 first.")
        return
    n = len(array)
    key = array[-1] + 1             # a value that is definitely absent

    _, bc = binary_search(array, key)
    _, tc = ternary_search(array, key)

    print("\n--- WORST CASE (key absent), n = %d ---" % n)
    print("Searching for key = %d (not present in the array)" % key)
    print("Binary  comparisons = %-6d (theory: log2(n)   = %.1f)" % (bc, math.log2(n)))
    print("Ternary comparisons = %-6d (theory: 2*log3(n) = %.1f)" % (tc, 2 * math.log(n, 3)))


def comparison_table():
    """Worst case comparison counts for increasing n, plus a graph."""
    sizes = [10, 100, 1000, 10000, 100000, 1000000]

    print("\n%-10s %-10s %-10s %-12s %-12s" %
          ("n", "Binary", "Ternary", "log2(n)", "2*log3(n)"))
    print("-" * 58)

    bin_counts, ter_counts = [], []

    for n in sizes:
        arr = list(range(1, n + 1))     # sorted array 1..n
        key = n + 1                     # absent key -> worst case

        _, bc = binary_search(arr, key)
        _, tc = ternary_search(arr, key)
        bin_counts.append(bc)
        ter_counts.append(tc)

        print("%-10d %-10d %-10d %-12.2f %-12.2f" %
              (n, bc, tc, math.log2(n), 2 * math.log(n, 3)))

    print("\nBinary Search always makes FEWER comparisons.")
    print("T(n)=T(n/2)+O(1) gives log2(n) levels with 1 comparison each,")
    print("T(n)=T(n/3)+O(1) gives log3(n) levels but 2 comparisons each.")
    print("2*log3(n) = 2*log2(n)/log2(3) = 1.26*log2(n)  >  log2(n)")

    try:
        import matplotlib.pyplot as plt
        plt.plot(sizes, bin_counts, "o-", label="Binary Search ~ log2(n)")
        plt.plot(sizes, ter_counts, "s-", label="Ternary Search ~ 2*log3(n)")
        plt.xscale("log")
        plt.xlabel("Array size n (log scale)")
        plt.ylabel("Number of comparisons (worst case)")
        plt.title("Binary vs Ternary Search - Step / Frequency Count")
        plt.legend()
        plt.grid(True)
        plt.savefig("search_graph.png")
        print("\nGraph saved as search_graph.png")
        plt.show()
    except ImportError:
        print("\n(matplotlib not installed - graph skipped)")


# - Main menu -

def main():
    while True:
        print("\n" + "=" * 50)
        print("   BINARY SEARCH vs TERNARY SEARCH")
        print("=" * 50)
        print("1. Generate n sorted random numbers")
        print("2. Display array")
        print("3. Search using Binary Search")
        print("4. Search using Ternary Search")
        print("5. Step count - BEST case")
        print("6. Step count - WORST case")
        print("7. Comparison table for increasing n")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            generate_array()
        elif choice == "2":
            display_array()
        elif choice == "3":
            do_search(binary_search, "Binary Search")
        elif choice == "4":
            do_search(ternary_search, "Ternary Search")
        elif choice == "5":
            best_case()
        elif choice == "6":
            worst_case()
        elif choice == "7":
            comparison_table()
        elif choice == "0":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()


# - Analysis / Conclusion -
# Step / frequency count = number of comparisons between the key and an
# array element.
#
# Binary Search : T(n) = T(n/2) + O(1)
#   Each level throws away half of the array and costs 1 comparison,
#   so the total is about log2(n) comparisons -> O(log2 n).
#
# Ternary Search: T(n) = T(n/3) + O(1)
#   Each level throws away two thirds of the array, so there are only
#   log3(n) levels - FEWER levels than binary search. But every level
#   costs 2 comparisons (one at mid1 and one at mid2), so the total is
#   about 2*log3(n) comparisons.
#
# Putting both in the same base:
#       2*log3(n) = 2*log2(n)/log2(3) = 2*log2(n)/1.585 = 1.26*log2(n)
#
# So ternary search makes about 26% MORE comparisons than binary search
# even though it needs fewer levels of recursion. Both are O(log n) -
# the base of the logarithm only changes the constant factor - but in
# practice BINARY SEARCH IS BETTER.
#
# Measured worst case (key absent), from menu option 7:
#   n        Binary   Ternary   log2(n)   2*log3(n)
#   10       4        4         3.32      4.19
#   100      7        8         6.64      8.38
#   1000     10       12        9.97      12.58
#   10000    14       17        13.29     16.77
#   100000   17       21        16.61     20.96
#   1000000  20       25        19.93     25.15
# The measured counts follow log2(n) and 2*log3(n) almost exactly, and
# the gap widens as n grows (equal at n=10, but 25 vs 20 at n=1000000).
#
# Best case for both is 1 comparison, i.e. O(1), which happens when the
# key sits exactly on the first probed position.
