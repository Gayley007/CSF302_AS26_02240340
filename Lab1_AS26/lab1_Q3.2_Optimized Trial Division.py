import time


def Is_Prime_Optimized_340(n_340):
    if n_340 < 2:
        return False
    for i_340 in range(2, int(n_340 ** 0.5) + 1):
        if n_340 % i_340 == 0:
            return False
    return True


def Generate_Primes_Optimized_340(limit_340):
    return [n_340 for n_340 in range(2, limit_340 + 1) if Is_Prime_Optimized_340(n_340)]


def Run_Test_340(limit_340):
    start_340 = time.perf_counter()
    primes_340 = Generate_Primes_Optimized_340(limit_340)
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
