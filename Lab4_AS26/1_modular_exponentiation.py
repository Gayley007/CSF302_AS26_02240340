# Topic 6: Efficient Modular Exponentiation  (a^b mod m)


def check_input(a, b, m):
    """Handles bad or special inputs before calculating."""
    if m <= 0:
        raise ValueError("modulus must be positive")
    a = a % m                       # negative base: -3 mod 7 becomes 4
    if b < 0:
        a = pow(a, -1, m)           # negative exponent: use the inverse of a (error if none)
        b = -b
    return a, b                     # zero exponent needs nothing special: loops below just return 1


# 1. Naive: multiply by a, b times  ->  O(b)
def naive_power(a, b, m):
    a, b = check_input(a, b, m)
    result = 1 % m
    for i in range(b):
        result = (result * a) % m
    return result


# 2. Binary (square and multiply)  ->  O(log b)
def binary_power(a, b, m):
    a, b = check_input(a, b, m)
    result = 1 % m
    while b > 0:
        if b % 2 == 1:              # exponent is odd
            result = (result * a) % m
        a = (a * a) % m
        b = b // 2
    return result


# 3. Binary using bitwise operations
def bitwise_power(a, b, m):
    a, b = check_input(a, b, m)
    result = 1 % m
    while b > 0:
        if b & 1:                   # same as b % 2 == 1
            result = (result * a) % m
        a = (a * a) % m
        b = b >> 1                  # same as b // 2
    return result


if __name__ == "__main__":
    print("Compare outputs")
    tests = [(2, 10, 1000), (3, 200, 13), (7, 0, 5), (-3, 5, 7), (3, -2, 7), (123456, 7890, 1000000007)]
    for a, b, m in tests:
        n1 = naive_power(a, b, m)
        n2 = binary_power(a, b, m)
        n3 = bitwise_power(a, b, m)
        print(f"{a}^{b} mod {m}:  naive={n1}  binary={n2}  bitwise={n3}  match={n1 == n2 == n3}")

    print("\nInput validation")
    tests = [(9, 0, 4), (-2, 3, 5), (2, -1, 7), (2, -1, 4), (2, 3, 0), (2, 3, -5)]
    for a, b, m in tests:
        try:
            print(f"{a}^{b} mod {m} = {bitwise_power(a, b, m)}")
        except ValueError as e:
            print(f"{a}^{b} mod {m} -> Error: {e}")
