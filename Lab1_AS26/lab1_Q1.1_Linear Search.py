import random
import time


def Linear_Search_340(list_340, target_340):
    for index_340 in range(len(list_340)):
        if list_340[index_340] == target_340:
            return index_340
    return -1


def Generate_Data_340(size_340):
    return [random.randint(0, size_340 * 10) for _ in range(size_340)]


def Run_Test_340(size_340):
    data_340 = Generate_Data_340(size_340)
    target_340 = -1  # worst case: target not in list, forces full scan

    start_340 = time.perf_counter()
    result_340 = Linear_Search_340(data_340, target_340)
    end_340 = time.perf_counter()

    time_taken_340 = end_340 - start_340
    return result_340, time_taken_340


def Main_340():
    input_sizes_340 = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]

    print(f"{'Input Size':>12} | {'Result':>10} | {'Time Taken (s)':>15}")
    print("-" * 45)

    for size_340 in input_sizes_340:
        result_340, time_taken_340 = Run_Test_340(size_340)
        print(f"{size_340:>12} | {result_340:>10} | {time_taken_340:>15.6f}")


if __name__ == "__main__":
    Main_340()
