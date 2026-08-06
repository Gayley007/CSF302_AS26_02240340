import os
import time


def Load_Dataset_340(file_path_340):
    with open(file_path_340, "r") as file_340:
        return [int(line_340) for line_340 in file_340]


def Sort_Dataset_340(dataset_340):
    return sorted(dataset_340)


def Save_Sorted_Dataset_340(sorted_dataset_340, size_340, folder_340):
    file_path_340 = os.path.join(folder_340, f"sorted_dataset_340_{size_340}.txt")
    with open(file_path_340, "w") as file_340:
        file_340.write("\n".join(str(value_340) for value_340 in sorted_dataset_340))
    return file_path_340


def Main_340():
    input_sizes_340 = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]

    script_dir_340 = os.path.dirname(os.path.abspath(__file__))
    input_folder_340 = os.path.join(script_dir_340, "datasets_340")
    output_folder_340 = os.path.join(script_dir_340, "sorted_datasets_340")
    os.makedirs(output_folder_340, exist_ok=True)

    print(f"{'Input Size':>12} | {'Sort Time (s)':>15} | {'Saved To'}")
    print("-" * 90)

    for size_340 in input_sizes_340:
        input_path_340 = os.path.join(input_folder_340, f"dataset_340_{size_340}.txt")
        dataset_340 = Load_Dataset_340(input_path_340)

        start_340 = time.perf_counter()
        sorted_dataset_340 = Sort_Dataset_340(dataset_340)
        end_340 = time.perf_counter()
        sort_time_340 = end_340 - start_340

        output_path_340 = Save_Sorted_Dataset_340(sorted_dataset_340, size_340, output_folder_340)
        print(f"{size_340:>12} | {sort_time_340:>15.6f} | {output_path_340}")


if __name__ == "__main__":
    Main_340()
