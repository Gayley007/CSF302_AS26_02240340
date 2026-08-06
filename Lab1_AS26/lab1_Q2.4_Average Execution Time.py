import os
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


def Load_Array_340(file_path_340):
    with open(file_path_340, "r") as file_340:
        return [int(line_340) for line_340 in file_340]


def Average_Time_340(sort_func_340, array_340, runs_340=10):
    total_time_340 = 0.0

    for _ in range(runs_340):
        data_340 = array_340[:]
        start_340 = time.perf_counter()
        sort_func_340(data_340)
        end_340 = time.perf_counter()
        total_time_340 += (end_340 - start_340)

    return total_time_340 / runs_340

def Main_340():
    input_sizes_340 = [100, 500, 1000, 2000, 4000, 8000]
    runs_340 = 10

    script_dir_340 = os.path.dirname(os.path.abspath(__file__))
    arrays_folder_340 = os.path.join(script_dir_340, "arrays_340")

    print(f"{'Input Size':>12} | {'Bubble Avg (s)':>15} | {'Merge Avg (s)':>15}")
    print("-" * 50)

    for size_340 in input_sizes_340:
        array_path_340 = os.path.join(arrays_folder_340, f"array_340_{size_340}.txt")
        array_340 = Load_Array_340(array_path_340)

        bubble_avg_340 = Average_Time_340(Bubble_Sort_340, array_340, runs_340)
        merge_avg_340 = Average_Time_340(Merge_Sort_340, array_340, runs_340)

        print(f"{size_340:>12} | {bubble_avg_340:>15.6f} | {merge_avg_340:>15.6f}")


if __name__ == "__main__":
    Main_340()
