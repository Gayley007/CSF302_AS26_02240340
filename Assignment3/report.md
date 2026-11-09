# Assignment 3: Fixing a Slow Quicksort

**CSF302 – Unit 5 · Student ID: 02240340**

Files: `sorts.py` (Part A), `test_sorts.py` (Part B), `analysis.py` (Part C, produces `results.md` and the four graphs).
Set-up: Python 3.11.5, Windows 11, default recursion limit 1000, each time is the best of 3 runs.

---

## 1. Implementation (Part A)

**`quicksort_basic(a)`** – Lomuto partition with `a[hi]` as the pivot, then two recursive calls.

**`quicksort_improved(a, cutoff=16)`** – four changes:

| Change | Why | 
|---|---|
| Random pivot (`random.randint(lo, hi)`) | Sorted or reverse-sorted input no longer gives the worst split; the expected time is O(n log n) for *every* input. |
| Insertion sort when a part has ≤ `cutoff` items | Avoids many recursive calls on tiny parts, where insertion sort is faster. |
| Recurse on the smaller part, loop on the larger | The smaller part has at most n/2 items, so the depth is at most log₂ n (≈ 17 for n = 100,000). No `RecursionError`. |
| Three-way partition (`< p`, `= p`, `> p`) | With a 2-way Lomuto partition, a run of equal values is still split 1 vs n−1 (all equal items go to one side). The 3-way partition removes every copy of the pivot in one pass, so the "many duplicates" input becomes very fast. |

## 2. Testing (Part B)

`python -m pytest test_sorts.py -v` → **4 passed** (each test loops over many sub-cases):

- 500 random lists (length 0–200, values −1000…1000) for **each** sort, compared with `sorted()`.
- `quicksort_improved` with every cutoff 1, 4, 8, 16, 32, 64 (100 lists each).
- Special cases for both sorts: empty, one element, two elements, all equal, already sorted, reverse sorted, negative numbers, many duplicates.
- `quicksort_improved` on 100,000 sorted, reverse, duplicate and all-equal items (the inputs that break the basic sort).
- Each test also checks the sort works **in place** (returns `None`, the list itself is changed).

## 3. Timing results (Part C1)

Times in seconds. "RecursionError" means the program crashed.

| n | basic – random | improved – random | basic – sorted | improved – sorted | basic – dup. (0–9) | improved – dup. (0–9) |
|---|---|---|---|---|---|---|
| 1,000 | 0.0006 | 0.0008 | RecursionError | 0.0008 | 0.0030 | 0.0002 |
| 2,000 | 0.0013 | 0.0018 | RecursionError | 0.0016 | 0.0111 | 0.0004 |
| 4,000 | 0.0032 | 0.0042 | RecursionError | 0.0038 | 0.0444 | 0.0008 |
| 8,000 | 0.0065 | 0.0087 | RecursionError | 0.0077 | 0.1678 | 0.0016 |
| 16,000 | 0.0145 | 0.0176 | RecursionError | 0.0173 | RecursionError | 0.0030 |
| 32,000 | 0.0284 | 0.0397 | RecursionError | 0.0406 | RecursionError | 0.0058 |
| 64,000 | 0.0635 | 0.0958 | RecursionError | 0.0844 | RecursionError | 0.0104 |

![C1 graph](graph1_input_types.png)

**Observations.**
- *Random:* both are O(n log n) (doubling n roughly doubles the time). The basic version is about 1.3–1.5× faster here, because the improved one pays for `random.randint` and the 3-way partition does more swaps. That cost is small compared with what the improved version saves on the other inputs.
- *Sorted:* the basic version crashes for all sizes, even n = 1,000, because it needs n nested calls and Python allows about 1,000. The improved version stays O(n log n).
- *Duplicates:* the basic version is quadratic (each doubling of n gives ≈ 4× the time: 0.0111 → 0.0444 → 0.1678) and crashes from n = 16,000. With only 10 values, the parts quickly become blocks of equal numbers, about n/10 long, and each block is split one item at a time. That is a depth of about 1,600 at n = 16,000, which is over the limit. The improved version is the *fastest* case, because the 3-way partition finishes each value in one step.

## 4. Why the basic quicksort is slow on sorted data (Part C2)

On sorted input the last element is the **largest**, so Lomuto puts all other n − 1 items on the left and nothing on the right. Each call therefore does Θ(n) work to partition and then makes one call of size n − 1:

T(n) = T(n − 1) + cn
  = cn + c(n − 1) + c(n − 2) + … + c·1
  = c · n(n + 1)/2 = **Θ(n²)**.

The recursion depth is also n, which explains the `RecursionError`. To time the slow case without crashing, I raised the recursion limit to 100,000 and ran the sort in a thread with a 200 MB stack:

| n | time (s) | time / n² (× 10⁻⁸) | time ÷ previous |
|---|---|---|---|
| 1,000 | 0.0273 | 2.74 | – |
| 2,000 | 0.1136 | 2.84 | 4.15 |
| 4,000 | 0.4435 | 2.77 | 3.90 |
| 8,000 | 1.6727 | 2.61 | 3.77 |
| 16,000 | 6.6901 | 2.61 | 4.00 |

Doubling n multiplies the time by about **4**, and time/n² stays almost constant, which is what Θ(n²) predicts. At n = 16,000 the basic sort takes 6.7 s, while the improved sort takes 0.017 s (about 390× faster). At n = 64,000 the basic sort would take about 16 × 6.7 ≈ 107 s.

![C2 graph](graph2_worst_case.png)

## 5. Choosing the cutoff (Part C3)

`quicksort_improved` on n = 100,000 random values, best of 5 runs:

| cutoff | 1 | 4 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|---|
| time (s) | 0.1786 | 0.1552 | 0.1430 | 0.1422 | **0.1371** | 0.1531 |

![C3 graph](graph3_cutoff.png)

**Chosen cutoff: 32.** The time goes down as the cutoff grows from 1 to 32 (about 23 % faster than cutoff = 1), then goes up again at 64, where the Θ(k²) cost of insertion sort starts to matter. The values for 8, 16 and 32 are close, so any cutoff from 8 to 32 is a good choice. In Python the best cutoff is a bit larger than the 10–20 often given for C, because a function call is expensive in Python compared with one step of the insertion-sort loop.

## 6. Comparison with Python's `sorted()` (Part C4)

n = 100,000, `quicksort_improved(cutoff=32)`:

| input | quicksort_improved (s) | sorted() (s) | improved is … |
|---|---|---|---|
| random | 0.1497 | 0.0115 | 13× slower |
| already sorted | 0.1353 | 0.0005 | 280× slower |
| duplicates (0–9) | 0.0202 | 0.0047 | 4× slower |

![C4 graph](graph4_vs_sorted.png)

`sorted()` uses **Timsort**, written in C. It is faster on every input, and much faster on sorted data, because Timsort finds the existing sorted run and finishes in O(n) time.

---

## 7. Critical reflection (Part D, ≈ 365 words excluding the question headings)

**Q1. Why did the basic quicksort fail on sorted data, and which assumption did real data break?**
The average-case result of about 1.39 n log₂ n comparisons assumes the input is in *random order*, so that each pivot is equally likely to be any rank. Then a bad split is rare and the splits are balanced on average. The bank's data breaks this assumption: it is already sorted, so the last element is always the maximum and every split is (n − 1, 0). That gives T(n) = T(n − 1) + Θ(n) = Θ(n²), and my table in Section 4 confirms it, with the time growing 4× each time n doubles. The second problem is depth. n nested calls go over Python's recursion limit, so the program crashed at only n = 1,000. Repeated amounts (Nu 100, Nu 500) cause the same problem, because Lomuto sends all items equal to the pivot to one side. A random pivot makes the order of the input irrelevant. Recursing on the smaller side fixes the depth. The 3-way partition fixes the duplicates.

**Q2. Insertion sort is Θ(n²). Why does it make quicksort faster?**
Θ(n²) describes how the cost grows for large n. For a part of 32 items the constant matters more. Insertion sort uses one tight loop with no function calls, no random numbers and no extra swaps. Quicksort on the same part would make about 2 × 32 recursive calls, and each call is expensive in Python. Insertion sort is also very fast on parts that are already nearly sorted. My results show that cutoff = 32 was 23 % faster than cutoff = 1. Beyond that, the k² term takes over and cutoff = 64 was slower again.

**Q3. Why is `sorted()` still faster, and how much is algorithm vs language?**
On random data `sorted()` was 13× faster. Timsort does about n log₂ n comparisons and quicksort about 1.39 n log₂ n, so the algorithm explains only about 1.4×. The remaining ≈ 9× comes from the language. Every step of my code runs through the Python interpreter, while Timsort is compiled C working directly on the list. On sorted data the gap grows to 280×. Here the algorithm matters much more: Timsort detects the sorted run in O(n), which saves about a log₂ n ≈ 17× factor, and the language accounts for the remaining ≈ 16×. So on random data the gap comes mostly from the language, and on structured data mostly from the algorithm.
