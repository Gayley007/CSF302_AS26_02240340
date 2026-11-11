# Lab 5: Sorting Algorithms (Results)

Files:
- `lab5_q1_quicksort.py`: Q1, four quicksort variants
- `lab5_q2_counting_radix.py`: Q2, counting sort, radix sort and merge sort
- `lab5_q3_inversions.py`: Q3, brute force and merge-based inversion counting
- `lab5_q3_kendall_tau.py`: Q3 part 5, Kendall tau for two users' movie rankings (keyboard input)

---

## Q1: Quicksort Variants

- **Lomuto**: the pivot is the last element.
- **Hoare**: the pivot is the first element. It uses two pointers that move toward each other.
- **Randomised**: the pivot is a random element, then Lomuto partition is used.
- **Three-way**: uses a random pivot. It splits the array into `< pivot`, `= pivot` and `> pivot`.

All four sorts recurse on the **smaller** part and loop on the **bigger** part. This keeps the recursion depth at about log n, so sorted input of size 16,000 does not crash with a recursion error.

### Comparisons (time in seconds in brackets)

**Random input**

| n | Lomuto | Hoare | Random | 3-way |
|---|---|---|---|---|
| 1000 | 10,555 (0.0012) | 15,774 (0.0014) | 11,475 (0.0017) | 16,812 (0.0017) |
| 2000 | 25,531 (0.0030) | 35,035 (0.0027) | 23,581 (0.0034) | 39,391 (0.0053) |
| 4000 | 54,706 (0.0073) | 73,267 (0.0061) | 53,410 (0.0070) | 88,346 (0.0093) |
| 8000 | 116,159 (0.0110) | 157,144 (0.0119) | 122,202 (0.0173) | 197,526 (0.0230) |
| 16000 | 275,984 (0.0263) | 354,537 (0.0226) | 260,410 (0.0231) | 416,633 (0.0361) |

**Sorted input**

| n | Lomuto | Hoare | Random | 3-way |
|---|---|---|---|---|
| 1000 | 499,500 (0.0351) | 501,498 (0.0215) | 10,528 (0.0010) | 17,822 (0.0015) |
| 2000 | 1,999,000 (0.1609) | 2,002,998 (0.1100) | 24,211 (0.0025) | 37,430 (0.0033) |
| 4000 | 7,998,000 (0.6345) | 8,005,998 (0.3192) | 51,736 (0.0041) | 88,422 (0.0060) |
| 8000 | 31,996,000 (2.3096) | 32,011,998 (1.2512) | 115,467 (0.0093) | 189,732 (0.0137) |
| 16000 | 127,992,000 (8.8889) | 128,023,998 (5.0537) | 259,214 (0.0198) | 403,156 (0.0440) |

**Reverse sorted input**

| n | Lomuto | Hoare | Random | 3-way |
|---|---|---|---|---|
| 1000 | 499,500 (0.0291) | 501,998 (0.0196) | 11,048 (0.0010) | 18,175 (0.0014) |
| 2000 | 1,999,000 (0.1102) | 2,003,998 (0.0772) | 26,866 (0.0022) | 39,783 (0.0031) |
| 4000 | 7,998,000 (0.4165) | 8,007,998 (0.3074) | 53,595 (0.0043) | 86,985 (0.0063) |
| 8000 | 31,996,000 (1.6887) | 32,015,998 (1.4640) | 126,925 (0.0116) | 174,031 (0.0161) |
| 16000 | 127,992,000 (7.1925) | 128,031,998 (5.5596) | 251,196 (0.0227) | 417,179 (0.0292) |

**Many duplicates (values 0 to 9)**

| n | Lomuto | Hoare | Random | 3-way |
|---|---|---|---|---|
| 1000 | 56,707 (0.0041) | 14,334 (0.0009) | 52,973 (0.0041) | 5,572 (0.0003) |
| 2000 | 208,660 (0.0149) | 26,654 (0.0018) | 206,618 (0.0153) | 10,676 (0.0007) |
| 4000 | 814,587 (0.0587) | 64,992 (0.0042) | 812,636 (0.0643) | 25,902 (0.0016) |
| 8000 | 3,230,788 (0.2268) | 134,046 (0.0082) | 3,235,431 (0.2299) | 47,245 (0.0027) |
| 16000 | 12,856,006 (0.9249) | 276,702 (0.0178) | 12,860,622 (0.9451) | 88,998 (0.0054) |

### Which variant becomes Θ(n²), and why

- **Lomuto and Hoare on sorted and reverse sorted input.** The pivot is the first or last element, which is the smallest or largest value in the range. So every partition splits the array into a part of size 0 and a part of size n−1. The total work is (n−1) + (n−2) + … + 1 = n(n−1)/2. For n = 1000 that is exactly 499,500, which matches Lomuto's count. When n doubles, the comparisons grow about 4 times, which is the sign of n².
- **Lomuto and Randomised on many duplicates.** Lomuto puts values that are `<=` the pivot on one side. When a block is all the same value, every element goes to one side, so the split is 0 and n−1 again. A random pivot does not help because every value in the block is equal. The comparisons grow about 4 times when n doubles, so this is Θ(n²) too.
- **Hoare on duplicates is fine.** Its pointers stop on elements *equal* to the pivot and swap them, so equal values are shared out between both sides and the splits stay balanced.
- **Randomised on sorted or reverse input is fine.** A random pivot is almost never the smallest or largest value, so the expected time stays O(n log n) for any order.
- **Three-way is the best on duplicates.** All values equal to the pivot are put in the middle and never touched again. With only 10 different values, it finishes after about 10 levels, so the work is close to O(n) (only 88,998 comparisons for n = 16,000).
- On random input all four are about O(n log n). Three-way does slightly more comparisons, because it makes two checks per element (`<` and `>`).

---

## Q2: Counting Sort and Radix Sort

**Stability proof.** We sorted (key, original index) pairs by key only:

```
Before : [(3,0), (1,1), (4,2), (1,3), (0,4), (3,5), (2,6), (4,7), (1,8), (0,9)]
After  : [(0,4), (0,9), (1,1), (1,3), (1,8), (2,6), (3,0), (3,5), (4,2), (4,7)]
Stable?: True
```

Equal keys keep their original order (key 1 → indexes 1, 3, 8). This works because the last loop goes through the array **backwards** and fills each key's area from right to left.

### Experiment A: counting sort, n = 100,000, k changes

| k | Counting sort (s) | Merge sort (s) |
|---|---|---|
| 10 | 0.0093 | 0.1621 |
| 1,000 | 0.0096 | 0.1664 |
| 100,000 | 0.0364 | 0.1828 |
| 10,000,000 | 0.7177 | 0.1751 |

Graph: `q2_graph_counting_vs_k.png`

### Experiment B: k = 10⁹, n changes

| n | Radix base 10 (s) | Radix base 256 (s) | Merge sort (s) |
|---|---|---|---|
| 10,000 | 0.0131 | 0.0055 | 0.0149 |
| 50,000 | 0.0700 | 0.0303 | 0.0865 |
| 100,000 | 0.1556 | 0.0645 | 0.1921 |
| 250,000 | 0.4232 | 0.1967 | 0.5017 |
| 500,000 | 0.9645 | 0.4326 | 1.2156 |
| 1,000,000 | 2.3887 | 1.0903 | 2.1253 |

Graph: `q2_graph_radix_vs_merge.png`

### When the linear-time sorts win and when they lose

- Counting sort takes **O(n + k)** time. When k is small (k ≤ n), it is about 15 times faster than merge sort. When k = 10⁷ (100 times bigger than n), the count array of size k takes most of the time, so counting sort becomes **slower** than merge sort and also uses a lot of memory. **Counting sort wins only when k is not much bigger than n.**
- Radix sort takes **O(d · (n + b))** time, where d is the number of digits and b is the base. For k = 10⁹:
  - Base 10 needs d = 10 passes. That is about the same as log₂ n ≈ 20 for merge sort, so radix base 10 is only a little faster, and at n = 1,000,000 it was even slower.
  - Base 256 needs only d = 4 passes, so it was about **2 times faster** than merge sort at every size.
- Linear sorts lose when (1) k is huge compared with n (counting sort), (2) the numbers have many digits, so d is large (radix sort), or (3) the data are not integers. They also need extra memory for the count and output arrays. Merge sort works on any data that can be compared.

---

## Q3: Counting Inversions

The merge-based method adds `len(left) - i` when an element from the right half is smaller than `left[i]`. The left half is sorted, so that element is also smaller than every element still left in the left half.

**Check:** both methods gave the same answer on 50 random arrays of size 1 to 2,000 → `All results match: True`.

| n | Brute force O(n²) (s) | Merge based O(n log n) (s) | Inversions |
|---|---|---|---|
| 1,000 | 0.0163 | 0.0012 | 251,293 |
| 2,000 | 0.0673 | 0.0027 | 982,754 |
| 5,000 | 0.3998 | 0.0078 | 6,178,403 |
| 10,000 | 1.7262 | 0.0162 | 25,096,613 |
| 20,000 | 6.0405 | 0.0323 | 100,536,132 |
| 50,000 | 38.5320 | 0.0897 | 626,003,916 |
| 100,000 | > 60 (stopped) | 0.1819 | 2,506,984,325 |
| 500,000 | skipped | 1.0878 | 62,591,851,076 |
| 1,000,000 | skipped | 2.4789 | 250,164,007,677 |

Graph: `q3_graph_inversions.png`

When n doubles, the brute force time grows about 4 times (n²), and the merge-based time grows about 2 times (n log n). For a random array, the number of inversions is about n²/4 (for example 1000²/4 = 250,000).

### Kendall tau distance (movie rankings)

The Kendall tau distance is the number of movie pairs that the two users rank in a different order. To find it, we go through user A's list and write down where user B placed each movie. The number of inversions in that list is the distance.

Sample run:

```
User A: 1 2 3 4 5 6 7 8 9 10
User B: 2 1 3 4 5 6 7 8 10 9
Kendall tau distance : 2 out of 45 pairs disagree
Similarity           : 0.96  (1 = identical, 0 = reversed)
```

If user B gives the exact reverse of user A, the distance is 45 out of 45 and the similarity is 0.
