# Assignment 3 results
Python 3.11.5, recursion limit 1000, best of 3 runs, times in seconds.

## C1. Time for each input type

### Input: random
| n | quicksort_basic | quicksort_improved |
|---|---|---|
| 1000 | 0.0007 | 0.0010 |
| 2000 | 0.0016 | 0.0020 |
| 4000 | 0.0039 | 0.0048 |
| 8000 | 0.0082 | 0.0108 |
| 16000 | 0.0173 | 0.0243 |
| 32000 | 0.0360 | 0.0549 |
| 64000 | 0.1401 | 0.2086 |

### Input: sorted
| n | quicksort_basic | quicksort_improved |
|---|---|---|
| 1000 | RecursionError | 0.0011 |
| 2000 | RecursionError | 0.0022 |
| 4000 | RecursionError | 0.0043 |
| 8000 | RecursionError | 0.0140 |
| 16000 | RecursionError | 0.0208 |
| 32000 | RecursionError | 0.0384 |
| 64000 | RecursionError | 0.1120 |

### Input: duplicates
| n | quicksort_basic | quicksort_improved |
|---|---|---|
| 1000 | 0.0039 | 0.0003 |
| 2000 | 0.0155 | 0.0005 |
| 4000 | 0.0581 | 0.0012 |
| 8000 | 0.2432 | 0.0026 |
| 16000 | RecursionError | 0.0046 |
| 32000 | RecursionError | 0.0094 |
| 64000 | RecursionError | 0.0247 |

## C2. quicksort_basic on sorted input (recursion limit raised to 20000)

| n | time (s) | time / previous time |
|---|---|---|
| 1000 | 0.0377 | - |
| 2000 | 0.1459 | 3.87 |
| 4000 | 0.5163 | 3.54 |
| 8000 | 2.0893 | 4.05 |
| 16000 | 8.6314 | 4.13 |

## C3. Cutoff test, n = 100000 random values

| cutoff | time (s) |
|---|---|
| 1 | 0.2309 |
| 4 | 0.1856 |
| 8 | 0.1772 |
| 16 | 0.1577 |
| 32 | 0.1630 |
| 64 | 0.1708 |

Best cutoff: 16

## C4. quicksort_improved (cutoff 16) vs sorted(), n = 100000

| input | quicksort_improved | sorted() | how many times slower |
|---|---|---|---|
| random | 0.1563 | 0.0140 | 11x |
| sorted | 0.1474 | 0.0005 | 295x |
| duplicates | 0.0299 | 0.0063 | 5x |
