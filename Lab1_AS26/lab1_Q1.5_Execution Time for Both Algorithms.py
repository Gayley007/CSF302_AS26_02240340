import os
import time


def Linear_Search_340(list_340, target_340):
    for index_340 in range(len(list_340)):
        if list_340[index_340] == target_340:
            return index_340
    return -1


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


def Load_Dataset_340(file_path_340):
    with open(file_path_340, "r") as file_340:
        return [int(line_340) for line_340 in file_340]


def Average_Time_340(search_func_340, dataset_340, target_340, runs_340=10):
    total_time_340 = 0.0

    for _ in range(runs_340):
        start_340 = time.perf_counter()
        search_func_340(dataset_340, target_340)
        end_340 = time.perf_counter()
        total_time_340 += (end_340 - start_340)

    return total_time_340 / runs_340


def Main_340():
    input_sizes_340 = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    runs_340 = 10
    target_340 = -1  # worst case: target not in dataset

    script_dir_340 = os.path.dirname(os.path.abspath(__file__))
    unsorted_folder_340 = os.path.join(script_dir_340, "datasets_340")
    sorted_folder_340 = os.path.join(script_dir_340, "sorted_datasets_340")

    print(f"{'Input Size':>12} | {'Linear Avg (s)':>15} | {'Binary Avg (s)':>15}")
    print("-" * 50)

    for size_340 in input_sizes_340:
        unsorted_path_340 = os.path.join(unsorted_folder_340, f"dataset_340_{size_340}.txt")
        sorted_path_340 = os.path.join(sorted_folder_340, f"sorted_dataset_340_{size_340}.txt")

        unsorted_dataset_340 = Load_Dataset_340(unsorted_path_340)
        sorted_dataset_340 = Load_Dataset_340(sorted_path_340)

        linear_avg_340 = Average_Time_340(Linear_Search_340, unsorted_dataset_340, target_340, runs_340)
        binary_avg_340 = Average_Time_340(Binary_Search_340, sorted_dataset_340, target_340, runs_340)

        print(f"{size_340:>12} | {linear_avg_340:>15.6f} | {binary_avg_340:>15.6f}")


if __name__ == "__main__":
    Main_340()
