import random
import os


def Generate_Dataset_340(size_340):
    return [random.randint(0, size_340 * 10) for _ in range(size_340)]


def Save_Dataset_340(dataset_340, size_340, folder_340):
    file_path_340 = os.path.join(folder_340, f"dataset_340_{size_340}.txt")
    with open(file_path_340, "w") as file_340:
        file_340.write("\n".join(str(value_340) for value_340 in dataset_340))
    return file_path_340


def Main_340():
    input_sizes_340 = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]

    folder_340 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets_340")
    os.makedirs(folder_340, exist_ok=True)

    print(f"{'Input Size':>12} | {'Sample (first 5)':^40} | {'Saved To'}")
    print("-" * 90)

    for size_340 in input_sizes_340:
        dataset_340 = Generate_Dataset_340(size_340)
        file_path_340 = Save_Dataset_340(dataset_340, size_340, folder_340)
        sample_340 = str(dataset_340[:5])
        print(f"{size_340:>12} | {sample_340:^40} | {file_path_340}")


if __name__ == "__main__":
    Main_340()
