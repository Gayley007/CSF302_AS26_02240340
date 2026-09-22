"""Q2: Menu-driven Merge Sort program with step/frequency count analysis."""

import random
import time

array = []


# Merge the two halves while counting comparisons and copies.
def merge_sort(arr):
    """Sort arr in ascending order using Merge Sort. Returns step count."""
    steps = 0
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        steps += merge_sort(left)
        steps += merge_sort(right)

        i = j = k = 0
        while i < len(left) and j < len(right):
            steps += 1
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            steps += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            steps += 1

    return steps


# Sort in descending order for menu option 4.
def bubble_sort_descending(arr):
    """Sort arr in descending order using Bubble Sort. Returns step count."""
    steps = 0
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            steps += 1
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return steps


# Generate the array used by the menu options.
def generate_array():
    global array
    n = int(input("Enter the number of elements (n): "))
    low = int(input("Enter lower bound of random numbers: "))
    high = int(input("Enter upper bound of random numbers: "))
    array = [random.randint(low, high) for _ in range(n)]
    print("Array generated.")


# Display the current array.
def display_array():
    if not array:
        print("Array is empty. Generate it first (option 1).")
    else:
        print("Array:", array)


# Sort the current array in ascending order using Merge Sort.
def sort_ascending():
    if not array:
        print("Array is empty. Generate it first (option 1).")
        return
    arr_copy = array.copy()
    start = time.perf_counter()
    steps = merge_sort(arr_copy)
    elapsed = time.perf_counter() - start
    print("Sorted (ascending):", arr_copy)
    print(f"Step count: {steps}, Time taken: {elapsed:.8f} seconds")


# Sort the current array in descending order using Bubble Sort.
def sort_descending():
    if not array:
        print("Array is empty. Generate it first (option 1).")
        return
    arr_copy = array.copy()
    start = time.perf_counter()
    steps = bubble_sort_descending(arr_copy)
    elapsed = time.perf_counter() - start
    print("Sorted (descending):", arr_copy)
    print(f"Step count: {steps}, Time taken: {elapsed:.8f} seconds")


# Test Merge Sort using random input.
def time_complexity_random():
    if not array:
        print("Array is empty. Generate it first (option 1).")
        return
    arr_copy = array.copy()
    start = time.perf_counter()
    steps = merge_sort(arr_copy)
    elapsed = time.perf_counter() - start
    print("\n" + "=" * 70)
    print("Random data - Merge Sort analysis")
    print(f"{'Number of elements':<25}: {len(arr_copy)}")
    print(f"{'Step/frequency count':<25}: {steps}")
    print(f"{'Time taken (seconds)':<25}: {elapsed:.8f}")
    print("=" * 70)


# Test Merge Sort using already sorted input.
def time_complexity_sorted():
    if not array:
        print("Array is empty. Generate it first (option 1).")
        return
    arr_copy = sorted(array)
    start = time.perf_counter()
    steps = merge_sort(arr_copy)
    elapsed = time.perf_counter() - start
    print("\n" + "=" * 70)
    print("Already ascending-sorted data - Merge Sort analysis")
    print(f"{'Number of elements':<25}: {len(arr_copy)}")
    print(f"{'Step/frequency count':<25}: {steps}")
    print(f"{'Time taken (seconds)':<25}: {elapsed:.8f}")
    print("=" * 70)


# Test Merge Sort using descending-sorted input.
def time_complexity_descending():
    if not array:
        print("Array is empty. Generate it first (option 1).")
        return
    arr_copy = sorted(array, reverse=True)
    start = time.perf_counter()
    steps = merge_sort(arr_copy)
    elapsed = time.perf_counter() - start
    print("\n" + "=" * 70)
    print("Descending-sorted data - Merge Sort analysis")
    print(f"{'Number of elements':<25}: {len(arr_copy)}")
    print(f"{'Step/frequency count':<25}: {steps}")
    print(f"{'Time taken (seconds)':<25}: {elapsed:.8f}")
    print("=" * 70)


# Display the conclusion for the report.
def print_analysis():
    print("\n" + "=" * 70)
    print("ANALYSIS / CONCLUSION")
    print("=" * 70)
    print("1. Merge Sort has time complexity O(n log n) in all cases:")
    print("   best, average, and worst case.")
    print("2. Its step count stays close to n*log2(n) for all input types.")
    print("3. Bubble Sort has O(n^2) complexity and is slower for large n.")
    print("Conclusion: Merge Sort is consistent and scalable for all inputs.")
    print("=" * 70)


# Display the available program choices.
def print_menu():
    print("\n----- MERGE SORT MENU -----")
    print("1. Generate n random numbers -> Array")
    print("2. Display Array")
    print("3. Sort in Ascending Order using Merge Sort")
    print("4. Sort in Descending Order (Bubble Sort)")
    print("5. Time Complexity for ascending random data")
    print("6. Time Complexity for ascending already-sorted data")
    print("7. Time Complexity for ascending descending-sorted data")
    print("8. Exit")


def main():
    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            generate_array()
        elif choice == "2":
            display_array()
        elif choice == "3":
            sort_ascending()
        elif choice == "4":
            sort_descending()
        elif choice == "5":
            time_complexity_random()
        elif choice == "6":
            time_complexity_sorted()
        elif choice == "7":
            time_complexity_descending()
        elif choice == "8":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")

    print_analysis()


if __name__ == "__main__":
    main()
