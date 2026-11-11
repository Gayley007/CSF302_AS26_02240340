# Lab 6: Dynamic Programming (Results)

Files:
- `lab6_q1_rod_cutting.py`: Q1, naive, memoized and bottom-up rod cutting
- `lab6_q2_matrix_chain.py`: Q2, matrix chain DP, brackets, brute-force check
- `lab6_q3_lcs.py`: Q3, LCS table, rebuilding the LCS, two-row version, brute force, file diff
- `old.txt`, `new.txt`: two small text files used for the diff
- `lab6_q4_optimal_bst.py`: Q4 (optional), optimal binary search tree

---

## Q1: Rod Cutting

Prices: 1, 5, 8, 9, 10, 17, 17, 20, 24, 30 for lengths 1 to 10, and p[i] = 3i for i > 10.

| n | Max revenue | Pieces |
|---|---|---|
| 1 | 1 | [1] |
| 2 | 5 | [2] |
| 3 | 8 | [3] |
| 4 | 10 | [2, 2] |
| 5 | 13 | [2, 3] |
| 6 | 17 | [6] |
| 7 | 18 | [1, 6] |
| 8 | 22 | [2, 6] |
| 9 | 25 | [3, 6] |
| 10 | 30 | [10] |

All three versions give the same revenue.

### Recursive calls and time

| n | Naive calls | Naive time (s) | Memo calls | Memo time (s) | Bottom-up calls | Bottom-up time (s) |
|---|---|---|---|---|---|---|
| 5 | 32 | 0.00001 | 16 | 0.00000 | 0 | 0.00000 |
| 10 | 1,024 | 0.00018 | 56 | 0.00001 | 0 | 0.00000 |
| 15 | 32,768 | 0.00567 | 121 | 0.00002 | 0 | 0.00001 |
| 20 | 1,048,576 | 0.18786 | 211 | 0.00003 | 0 | 0.00001 |
| 25 | 33,554,432 | 6.13668 | 326 | 0.00005 | 0 | 0.00002 |

**Why they are different:**
- **Naive** makes exactly **2ⁿ** calls. It solves the same smaller rods again and again. For example, length 3 is solved many times inside length 5. Each extra unit of length doubles the work, so n = 25 takes about 6 seconds.
- **Memoized** saves each answer the first time it is solved. Later calls just return the saved answer. Calls = 1 + n(n+1)/2 (326 for n = 25), so it is **O(n²)**.
- **Bottom-up** makes **no recursive calls**. It fills the table from length 1 up to n with two loops. That is also O(n²), and it is the fastest because there is no function-call overhead.

---

## Q2: Matrix Chain Multiplication

| Test | p | Optimal cost | Optimal brackets | Left-to-right cost | Brute force agrees? |
|---|---|---|---|---|---|
| 1 | 30,35,15,5,10,20,25 | **15,125** | ((A1(A2A3))((A4A5)A6)) | 40,500 | Yes |
| 2 | 5,4,6,2,7 | 158 | ((A1(A2A3))A4) | 250 | Yes |
| Random 1 | 10,36,21,7,5,14,47,42 | 21,575 | ((A1(A2(A3A4)))((A5A6)A7)) | 36,400 | Yes |
| Random 2 | 28,25,6,22,36,17,31 | 20,994 | ((A1A2)(((A3A4)A5)A6)) | 61,964 | Yes |
| Random 3 | 39,48,11,17,41,40,49,21 | 88,187 | ((A1A2)((((A3A4)A5)A6)A7)) | 235,599 | Yes |
| Random 4 | 44,48,10,32,26,10,28,31,21 | 58,570 | ((A1A2)(((A3A4)A5)((A6A7)A8))) | 162,404 | Yes |
| Random 5 | 49,11,17,49,45,23,11 | 52,789 | (A1(A2(A3(A4(A5A6))))) | 221,137 | Yes |

The random chains use `random.seed(6)`, so they are the same every run. Each has 3 to 8 matrices with sizes from 5 to 50.

**Notes:**
- The DP fills `m[i][j]` for short chains first, then longer ones. It tries every split point k, so it takes O(n³) time.
- The brute force tries every split without saving answers, so its time grows exponentially. It always gave the same answer, so the DP is correct.
- Multiplying left to right was 1.5 to 4 times more expensive than the best order. The order of brackets matters a lot.

---

## Q3: Longest Common Subsequence

LCS table for X = ABCBDAB, Y = BDCABA:

```
      -  B  D  C  A  B  A
   -  0  0  0  0  0  0  0
   A  0  0  0  0  1  1  1
   B  0  1  1  1  1  2  2
   C  0  1  1  2  2  2  2
   B  0  1  1  2  2  3  3
   D  0  1  2  2  2  3  3
   A  0  1  2  2  3  3  4
   B  0  1  2  2  3  4  4
```

- LCS length = **4**, one LCS = **BCBA**
- The two-row version also gives 4. It keeps only the previous row and the current row, so it uses O(n) memory instead of O(m·n).

### DP vs brute force (random strings over A, B, C, D)

| Length | DP (s) | Brute force (s) |
|---|---|---|
| 5 | 0.000007 | 0.0000 |
| 8 | 0.000009 | 0.0001 |
| 10 | 0.000013 | 0.0006 |
| 12 | 0.000020 | 0.0041 |
| 14 | 0.000025 | 0.0154 |
| 16 | 0.000037 | 0.0968 |
| 17 | 0.000054 | 0.1852 |
| 18 | 0.000050 | 0.3410 |

All lengths from 5 to 18 were run, and both methods always gave the same answer. The brute force checks all **2ᵐ** subsequences of X, so its time roughly **doubles** for each extra character. The DP is O(m·n) and stays tiny. At length 18 the DP is about 7,000 times faster.

### Diff of `old.txt` → `new.txt`

```
  def greet(name):
-     print("Hello")
-     print(name)
+     print("Hello,", name)
      return None

  greet("Pema")
+ greet("Karma")
  print("done")
```

Each **line** is treated as one item. Lines in the LCS are unchanged. Lines that are only in the old file are marked `-` (removed), and lines that are only in the new file are marked `+` (added).

---

## Q4 (Optional): Optimal Binary Search Tree

p = 0.15, 0.10, 0.05, 0.10, 0.20 and q = 0.05, 0.10, 0.05, 0.05, 0.05, 0.10

**Expected search cost = 2.75** (matches the expected answer).

```
root:  k2
    left:  k1
        left:  d0
        right: d1
    right: k5
        left:  k4
            left:  k3
                left:  d2
                right: d3
            right: d4
        right: d5
```

The DP tries every key as the root of each range of keys. When a subtree goes one level deeper, every search inside it costs one more step. That is why `w[i][j]`, the total probability of that range, is added to the cost.
