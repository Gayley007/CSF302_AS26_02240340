import random
import time

def Merge_Sort_340(list_340):
    if len(list_340) <= 1:
        return list_340

    mid_340 = len(list_340) // 2
    left_340 = Merge_Sort_340(list_340[:mid_340])
    right_340 = Merge_Sort_340(list_340[mid_340:])

    return Merge_340(left_340, right_340)


def Merge_340(left_340, right_340):
    merged_340 = []
    i_340 = 0
    j_340 = 0

    while i_340 < len(left_340) and j_340 < len(right_340):
        if left_340[i_340] <= right_340[j_340]:
            merged_340.append(left_340[i_340])
            i_340 += 1
        else:
            merged_340.append(right_340[j_340])
            j_340 += 1

    merged_340.extend(left_340[i_340:])
    merged_340.extend(right_340[j_340:])
    return merged_340


def Generate_Data_340(size_340):
    return [random.randint(0, size_340 * 10) for _ in range(size_340)]


def Run_Test_340(size_340):
    data_340 = Generate_Data_340(size_340)

    start_340 = time.perf_counter()
    Merge_Sort_340(data_340)
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
