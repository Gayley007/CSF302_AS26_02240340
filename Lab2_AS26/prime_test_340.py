"""Q1: Compare naive and optimized prime-number testing algorithms."""

import time

import matplotlib.pyplot as plt


# Algorithm 1: check every possible divisor.
def is_prime_naive_340(n340):
    """Check primality by testing all divisors from 2 to n-1."""
    steps340 = 0
    if n340 < 2:
        return False, steps340
    for divisor340 in range(2, n340):
        steps340 += 1
        if n340 % divisor340 == 0:
            return False, steps340
    return True, steps340


# Algorithm 2: check divisors only up to the square root.
def is_prime_optimized_340(n340):
    """Check primality by testing divisors only up to sqrt(n)."""
    steps340 = 0
    if n340 < 2:
        return False, steps340
    divisor340 = 2
    while divisor340 * divisor340 <= n340:
        steps340 += 1
        if n340 % divisor340 == 0:
            return False, steps340
        divisor340 += 1
    return True, steps340


# Get at least 10 numbers from the user.
def get_input_numbers_340():
    numbers340 = []
    print("Enter numbers to test for primality (at least 10 required).")
    while len(numbers340) < 10:
        entry340 = input(f"Number {len(numbers340) + 1}: ").strip()
        try:
            numbers340.append(int(entry340))
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        more340 = input("Add another number? (y/n): ").strip().lower()
        if more340 != "y":
            break
        entry340 = input(f"Number {len(numbers340) + 1}: ").strip()
        try:
            numbers340.append(int(entry340))
        except ValueError:
            print("Invalid input. Please enter an integer.")
    return numbers340


def main_340():
    # Store the inputs and step counts for the graph.
    numbers340 = get_input_numbers_340()
    naive_steps_list340 = []
    optimized_steps_list340 = []

    print("\n" + "=" * 100)
    print(
        f"{'n':>8} | {'Naive Prime?':>12} | {'Naive Steps':>12} | "
        f"{'Naive Time(s)':>14} | {'Opt Prime?':>10} | "
        f"{'Opt Steps':>10} | {'Opt Time(s)':>12}"
    )
    print("=" * 100)

    # Test every number with both algorithms and measure the time.
    for n340 in numbers340:
        start340 = time.perf_counter()
        naive_result340, naive_steps340 = is_prime_naive_340(n340)
        naive_time340 = time.perf_counter() - start340

        start340 = time.perf_counter()
        optimized_result340, optimized_steps340 = is_prime_optimized_340(n340)
        optimized_time340 = time.perf_counter() - start340

        if naive_result340 != optimized_result340:
            raise RuntimeError(f"The algorithms disagree for {n340}.")

        naive_steps_list340.append(naive_steps340)
        optimized_steps_list340.append(optimized_steps340)

        print(
            f"{n340:>8} | {str(naive_result340):>12} | "
            f"{naive_steps340:>12} | {naive_time340:>14.8f} | "
            f"{str(optimized_result340):>10} | {optimized_steps340:>10} | "
            f"{optimized_time340:>12.8f}"
        )

    print("=" * 100)

    print("Naive method complexity: O(n)")
    print("Optimized method complexity: O(sqrt(n))")
    print("The optimized method is generally faster because it checks fewer divisors.")

    # Plot the step-count comparison and save the graph.
    plt.plot(numbers340, naive_steps_list340, marker="o", label="Naive Method")
    plt.plot(
        numbers340,
        optimized_steps_list340,
        marker="s",
        label="Optimized Method",
    )
    plt.xlabel("Input Number")
    plt.ylabel("Number of Steps")
    plt.title("Prime Testing: Naive vs Optimized Method")
    plt.legend()
    plt.grid(True)
    plt.savefig("prime_test_comparison_340.png")
    print("Graph saved as prime_test_comparison_340.png")


if __name__ == "__main__":
    main_340()