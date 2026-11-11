# Lab 6 - Q4 (Optional): Optimal Binary Search Tree
# p[i] = chance we search for key ki        (i = 1..n)
# q[i] = chance we search for a missing value between keys (dummy di, i = 0..n)

p = [0, 0.15, 0.10, 0.05, 0.10, 0.20]       # p[0] not used
q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]
n = 5


# ---------------------------------------------------------------
# Bottom-up DP  ->  O(n^3)   (same as CLRS)
#   e[i][j]    = expected cost of the best tree for keys ki..kj
#   w[i][j]    = sum of all probabilities p[i..j] and q[i-1..j]
#   root[i][j] = which key is the root of that best tree
# e[i][i-1] = q[i-1] means an "empty" tree: just the dummy leaf d(i-1)
# ---------------------------------------------------------------
def optimal_bst(p, q, n):
    e = [[0.0] * (n + 1) for _ in range(n + 2)]
    w = [[0.0] * (n + 1) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            e[i][j] = float("inf")
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            for r in range(i, j + 1):              # try every key as root
                # Putting the subtrees one level deeper adds w[i][j] to the cost
                cost = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if cost < e[i][j]:
                    e[i][j] = cost
                    root[i][j] = r
    return e, root


# Print the tree sideways using indentation (children are indented more)
def print_tree(root, i, j, label, depth):
    space = "    " * depth
    if j == i - 1:                      # no keys left -> dummy leaf d(j)
        print(f"{space}{label}d{j}")
        return
    r = root[i][j]
    print(f"{space}{label}k{r}")
    print_tree(root, i, r - 1, "left:  ", depth + 1)
    print_tree(root, r + 1, j, "right: ", depth + 1)


if __name__ == "__main__":
    e, root = optimal_bst(p, q, n)
    print(f"Expected search cost = {e[1][n]:.2f}")    # should be 2.75
    print("\nOptimal tree structure:")
    print_tree(root, 1, n, "root:  ", 0)
