import random
import time


def Binary_Search_340(list_340, target_340):
    low_340 = 0
    high_340 = len(list_340) - 1

    while low_340 <= high_340:
        mid_340 = (low_340 + high_340) // 2
        if list_340[mid_340] == target_340:
            return mid_340
        elif list_340[mid_340] < target_340:
            low_340 = mid_340 + 1
        else:
            high_340 = mid_340 - 1

    return -1


def Generate_Data_340(size_340):
    return sorted(random.randint(0, size_340 * 10) for _ in range(size_340))


def Run_Test_340(size_340):
    data_340 = Generate_Data_340(size_340)
    target_340 = -1  # worst case: target not in list, forces full search range

    start_340 = time.perf_counter()
    result_340 = Binary_Search_340(data_340, target_340)
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
