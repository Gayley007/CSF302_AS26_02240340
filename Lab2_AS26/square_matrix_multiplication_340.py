"""Q3: Square Matrix Multiplication with step/frequency count analysis."""

import random


matrix_a = []
matrix_b = []
DEFAULT_RANDOM_LOW = 0
DEFAULT_RANDOM_HIGH = 9


def is_power_of_two(n):
    """Return True when n is a power of 2 (2, 4, 8, ...)."""
    return n > 0 and (n & (n - 1)) == 0


def read_power_of_two_size():
    """Read and validate matrix size n where n must be a power of 2."""
    while True:
        try:
            n = int(input("Enter matrix size n (power of 2, e.g., 2, 4, 8): "))
        except ValueError:
            print("Invalid input. Please enter an integer.")
            continue

        if not is_power_of_two(n):
            print("n must be a power of 2 (2, 4, 8, ...). Try again.")
            continue
        return n


def generate_random_matrix(n, low, high):
    """Generate an n x n matrix with random integers in [low, high]."""
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]


def input_matrix_manual(name, n):
    """Input an n x n matrix manually from user input."""
    print(f"Enter values for Matrix {name} row by row:")
    matrix = []
    for i in range(n):
        while True:
            row_input = input(f"Row {i + 1} ({n} integers separated by spaces): ").strip()
            parts = row_input.split()
            if len(parts) != n:
                print(f"Please enter exactly {n} integers.")
                continue
            try:
                row = [int(x) for x in parts]
            except ValueError:
                print("Invalid row. Please enter integers only.")
                continue
            matrix.append(row)
            break
    return matrix


def print_matrix(matrix, title):
    """Print a matrix in aligned table form."""
    print(f"\n{title}")
    for row in matrix:
        print(" ".join(f"{value:>6}" for value in row))


def multiply_matrices(a, b):
    """Multiply two square matrices and return (result, step_count)."""
    n = len(a)
    result = [[0 for _ in range(n)] for _ in range(n)]
    steps = 0

    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                product = a[i][k] * b[k][j]
                steps += 1  # multiplication
                total += product
                steps += 1  # addition into accumulator
            result[i][j] = total
            steps += 1  # assignment into result matrix

    return result, steps


def generate_matrices_random():
    """Create both matrices using random values."""
    global matrix_a, matrix_b
    n = read_power_of_two_size()

    matrix_a = generate_random_matrix(n, DEFAULT_RANDOM_LOW, DEFAULT_RANDOM_HIGH)
    matrix_b = generate_random_matrix(n, DEFAULT_RANDOM_LOW, DEFAULT_RANDOM_HIGH)
    print(
        f"Matrices A and B generated using default range "
        f"[{DEFAULT_RANDOM_LOW}, {DEFAULT_RANDOM_HIGH}]."
    )


def generate_matrices_manual():
    """Create both matrices by manual input."""
    global matrix_a, matrix_b
    n = read_power_of_two_size()
    matrix_a = input_matrix_manual("A", n)
    matrix_b = input_matrix_manual("B", n)
    print("Matrices A and B stored.")


def display_matrices():
    """Display both input matrices if available."""
    if not matrix_a or not matrix_b:
        print("Matrices are not ready. Choose option 1 or 2 first.")
        return

    print_matrix(matrix_a, "Matrix A:")
    print_matrix(matrix_b, "Matrix B:")


def multiply_and_display():
    """Multiply current matrices and display result with step count."""
    if not matrix_a or not matrix_b:
        print("Matrices are not ready. Choose option 1 or 2 first.")
        return

    result, steps = multiply_matrices(matrix_a, matrix_b)
    print_matrix(matrix_a, "Matrix A:")
    print_matrix(matrix_b, "Matrix B:")
    print_matrix(result, "Result (A x B):")
    print(f"\nStep/frequency count: {steps}")


def print_menu():
    """Display available menu options."""
    print("\n----- SQUARE MATRIX MULTIPLICATION MENU -----")
    print("1. Generate matrices randomly")
    print("2. Input matrices manually")
    print("3. Display matrices A and B")
    print("4. Multiply matrices and display result")
    print("5. Exit")


def main():
    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            generate_matrices_random()
        elif choice == "2":
            generate_matrices_manual()
        elif choice == "3":
            display_matrices()
        elif choice == "4":
            multiply_and_display()
        elif choice == "5":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
