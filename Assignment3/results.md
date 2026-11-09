# Assignment 3 results

Python 3.11.5, recursion limit 1000, best of 3 runs, times in seconds.

## C1. Time vs n for three input types

### Input: random

| n | quicksort_basic | quicksort_improved |
|---|---|---|
| 1,000 | 0.0006 | 0.0008 |
| 2,000 | 0.0013 | 0.0018 |
| 4,000 | 0.0032 | 0.0042 |
| 8,000 | 0.0065 | 0.0087 |
| 16,000 | 0.0145 | 0.0176 |
| 32,000 | 0.0284 | 0.0397 |
| 64,000 | 0.0635 | 0.0958 |

### Input: sorted

| n | quicksort_basic | quicksort_improved |
|---|---|---|
| 1,000 | RecursionError | 0.0008 |
| 2,000 | RecursionError | 0.0016 |
| 4,000 | RecursionError | 0.0038 |
| 8,000 | RecursionError | 0.0077 |
| 16,000 | RecursionError | 0.0173 |
| 32,000 | RecursionError | 0.0406 |
| 64,000 | RecursionError | 0.0844 |

### Input: duplicates

| n | quicksort_basic | quicksort_improved |
|---|---|---|
| 1,000 | 0.0030 | 0.0002 |
| 2,000 | 0.0111 | 0.0004 |
| 4,000 | 0.0444 | 0.0008 |
| 8,000 | 0.1678 | 0.0016 |
| 16,000 | RecursionError | 0.0030 |
| 32,000 | RecursionError | 0.0058 |
| 64,000 | RecursionError | 0.0104 |

## C2. quicksort_basic on sorted input with a raised recursion limit

Recursion limit raised to 100,000 and run in a thread with a 200 MB stack, so the worst case can be timed instead of crashing.

| n | time (s) | time / n^2 (x 1e-8) | time / previous |
|---|---|---|---|
| 1,000 | 0.0273 | 2.735 | - |
| 2,000 | 0.1136 | 2.840 | 4.15 |
| 4,000 | 0.4435 | 2.772 | 3.90 |
| 8,000 | 1.6727 | 2.614 | 3.77 |
| 16,000 | 6.6901 | 2.613 | 4.00 |

## C3. quicksort_improved cutoff, n = 100,000 random values

| cutoff | time (s) |
|---|---|
| 1 | 0.1786 |
| 4 | 0.1552 |
| 8 | 0.1430 |
| 16 | 0.1422 |
| 32 | 0.1371 |
| 64 | 0.1531 |

Best cutoff: **32**

## C4. quicksort_improved (cutoff=32) vs Python sorted()

| input (n = 100,000) | quicksort_improved | sorted() | ratio |
|---|---|---|---|
| random | 0.1497 | 0.0115 | 13x slower |
| sorted | 0.1353 | 0.0005 | 280x slower |
| duplicates | 0.0202 | 0.0047 | 4x slower |

