import time


def Sieve_Of_Eratosthenes_340(limit_340):
    is_prime_340 = [True] * (limit_340 + 1)
    is_prime_340[0:2] = [False, False]

    for i_340 in range(2, int(limit_340 ** 0.5) + 1):
        if is_prime_340[i_340]:
            for multiple_340 in range(i_340 * i_340, limit_340 + 1, i_340):
                is_prime_340[multiple_340] = False

    return [n_340 for n_340, prime_340 in enumerate(is_prime_340) if prime_340]


def Run_Test_340(limit_340):
    start_340 = time.perf_counter()
    primes_340 = Sieve_Of_Eratosthenes_340(limit_340)
    end_340 = time.perf_counter()

    time_taken_340 = end_340 - start_340
    return time_taken_340, len(primes_340)


def Main_340():
    input_sizes_340 = [10000, 50000, 100000, 500000, 1000000]

    print(f"{'Limit N':>12} | {'Time Taken (s)':>15} | {'Prime Count':>12}")
    print("-" * 46)

    for limit_340 in input_sizes_340:
        time_taken_340, count_340 = Run_Test_340(limit_340)
        print(f"{limit_340:>12} | {time_taken_340:>15.6f} | {count_340:>12}")


if __name__ == "__main__":
    Main_340()
