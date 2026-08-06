import random
import time

def Bubble_Sort_340(list_340):
    n_340 = len(list_340)
    for i_340 in range(n_340 - 1):
        swapped_340 = False
        for j_340 in range(n_340 - 1 - i_340):
            if list_340[j_340] > list_340[j_340 + 1]:
                list_340[j_340], list_340[j_340 + 1] = list_340[j_340 + 1], list_340[j_340]
                swapped_340 = True
        if not swapped_340:
            break
    return list_340


def Generate_Data_340(size_340):
    return [random.randint(0, size_340 * 10) for _ in range(size_340)]

def Run_Test_340(size_340):
    data_340 = Generate_Data_340(size_340)

    start_340 = time.perf_counter()
    Bubble_Sort_340(data_340)
    end_340 = time.perf_counter()

    time_taken_340 = end_340 - start_340
    return time_taken_340

def Main_340():
    input_sizes_340 = [100, 500, 1000, 2000, 4000, 8000]

    print(f"{'Input Size':>12} | {'Time Taken (s)':>15}")
    print("-" * 32)

    for size_340 in input_sizes_340:
        time_taken_340 = Run_Test_340(size_340)
        print(f"{size_340:>12} | {time_taken_340:>15.6f}")


if __name__ == "__main__":
    Main_340()
