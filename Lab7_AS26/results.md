# Lab 7: Greedy and Randomized Algorithms (Results)

Files:
- `lab7_q1_greedy.py`: Q1, activity selection (3 greedy rules), fractional knapsack, greedy vs DP for 0/1 knapsack
- `activities.txt`: the activities read in Q1 Part 1 (one `start finish` per line)
- `lab7_q2_huffman.py`: Q2, Huffman tree, code table, encode/decode, compression ratio
- `story.txt`, `dna.txt`: text files for Q2 (the third file is `lab7_q1_greedy.py` itself)
- `lab7_q3_graphs.py`: Q3, Dijkstra, Kruskal, Prim, timing, negative edge
- `graph.txt`: the weighted directed graph read by Dijkstra (`from to weight` per line)
- `lab7_q4_randomized.py`: Q4, quickselect, Miller-Rabin, Carmichael number 561

All scripts use `random.seed(7)`, so they give the same results every run (only the timings change a little).
Set-up: Python 3.11.5 on Windows 11.

---

## Q1: Activity Selection and Knapsack

### 1. Earliest finish time

Activities read from `activities.txt`:
(1,4) (3,5) (0,6) (5,7) (3,9) (5,9) (6,10) (8,11) (8,12) (2,14) (12,16)

**Selected: (1,4), (5,7), (8,11), (12,16), which is 4 activities.**

Sort by finish time. Take the first activity, then keep taking the next activity that starts at or after the last one finishes.

### 2. Other greedy rules (found by random testing)

The script tries random inputs of 2 to 5 activities until the rule picks fewer than earliest finish.

| Rule | Input found | Rule picks | Earliest finish picks |
|---|---|---|---|
| Earliest start | (9,12) (7,14) (12,20) | (7,14) → **1** | (9,12) (12,20) → **2** |
| Shortest duration | (18,21) (8,13) (0,3) (13,19) (19,25) | (0,3) (8,13) (18,21) → **3** | (0,3) (8,13) (13,19) (19,25) → **4** |

- **Earliest start** fails because one long activity that starts early, like (7,14), blocks everything else.
- **Shortest duration** fails because a short activity, like (18,21), can sit across two longer activities that would both fit.

On 10,000 random inputs of 10 activities, earliest start was worse **4,438** times and shortest duration was worse **480** times. Earliest finish is never beaten.

### 3. Fractional knapsack

Items (value, weight): (60,10), (100,20), (120,30). Capacity 50.

| Item | Value/weight | Taken |
|---|---|---|
| (60, 10) | 6.0 | all |
| (100, 20) | 5.0 | all |
| (120, 30) | 4.0 | 2/3 |

**Total value = 60 + 100 + 80 = 240.** For the fractional problem, best ratio first is always optimal.

### 4. Same greedy rule on 0/1 knapsack vs DP

On the same items with whole items only: **greedy = 160, DP = 220** (DP takes items 2 and 3).

| Test | Worst greedy / optimal |
|---|---|
| 10,000 random inputs (1–8 items, capacity 5–40) | **0.089** |
| Worst random input: items (4,1) (49,18) (28,15) (45,15), capacity 15 | greedy 4, DP 45 |
| Hand-made: items (2,1) (100,100), capacity 100 | greedy 2, DP 100 (ratio 0.02) |

In the worst random input, greedy takes the tiny item (4,1) first because it has the best ratio (4.0). That leaves only 14 space, so (45,15) no longer fits. With 0/1 items, greedy by ratio can be **as bad as we like**: in the hand-made case, making the big item bigger pushes the ratio towards 0.

---

## Q2: Huffman Coding

The tree is built with `heapq`. Each time, the two smallest trees are joined. Left = 0, right = 1.

**Code table for `story.txt`** (top 12 of 44 characters; the full table is printed by the script):

| Char | Freq | Code | | Char | Freq | Code |
|---|---|---|---|---|---|---|
| space | 256 | 00 | | o | 78 | 0111 |
| e | 125 | 1110 | | n | 72 | 0101 |
| a | 119 | 1101 | | r | 69 | 0100 |
| t | 107 | 1011 | | h | 68 | 11111 |
| s | 80 | 1000 | | i | 62 | 11110 |
| ... | | | | z | 1 | 0110001101 |

Common characters get short codes (space = 2 bits), and rare ones get long codes (z = 10 bits).

**Compression results (decoded text equals the original for all three files):**

| File | Characters | Different chars | 8-bit size (bits) | Huffman size (bits) | Bits/char | Ratio (8-bit / Huffman) | Saved |
|---|---|---|---|---|---|---|---|
| `story.txt` (English) | 1,404 | 44 | 11,232 | 6,044 | 4.31 | **1.86** | 46.2% |
| `lab7_q1_greedy.py` (code) | 7,558 | 67 | 60,464 | 33,780 | 4.47 | **1.79** | 44.1% |
| `dna.txt` (A, C, G, T) | 5,000 | 4 | 40,000 | 9,364 | 1.87 | **4.27** | 76.6% |

- **English and code** use 44–67 different characters, so Huffman needs about 4.3–4.5 bits per character. That is a bit less than half the size.
- **DNA** has only 4 letters, and A is much more common (40%), so it needs only 1.87 bits per character. This is even less than a fixed 2-bit code would need.
- Code compresses slightly worse than English because it uses more different symbols (brackets, `_`, `=`, digits).

(Note: `lab7_q1_greedy.py` is used as the code file, so its numbers will change if that file is edited.)

---

## Q3: Shortest Paths and Minimum Spanning Trees

### 1. Dijkstra on `graph.txt` (source A)

Edges: A→B 4, A→C 2, B→C 5, B→D 10, C→E 3, E→D 4, D→F 11, E→F 15, C→B 1, F→G 2, D→G 9

| Vertex | Distance | Path |
|---|---|---|
| A | 0 | A |
| B | 3 | A → C → B |
| C | 2 | A → C |
| D | 9 | A → C → E → D |
| E | 5 | A → C → E |
| F | 20 | A → C → E → F |
| G | 18 | A → C → E → D → G |

I checked these by hand. For example, B is 3 through C, which is shorter than the direct edge A→B 4.

### 2 and 3. Kruskal vs Prim

- **Kruskal:** sort all edges, then take the cheapest edge that does not make a cycle. Cycles are checked with union-find (`find` with path shortening).
- **Prim:** grow the tree from vertex 0. A heap gives the cheapest edge leaving the tree.

**Both gave the same total weight on 100 out of 100 random connected graphs** (2–60 vertices, any number of edges).

### 4. Timing, V = 1,000 (best of 3)

| Graph | E | Kruskal (s) | Prim (s) | Faster |
|---|---|---|---|---|
| Sparse (E = 3V) | 3,000 | 0.0012 | 0.0018 | Kruskal |
| Dense (E = V²/4) | 250,000 | 0.1388 | 0.2052 | Kruskal |

Both found the same weight (191,810 sparse, 2,838 dense).

**Why:**
- In theory, Kruskal is O(E log E) and Prim with a binary heap is O(E log V). log E ≤ 2 log V, so they are the same order. The winner depends on the constant factors.
- **Sparse graph:** there are few edges, so sorting is cheap. Kruskal's work is one sort plus a fast union-find loop, and it is faster. Prim has to build an adjacency list first and push many entries onto the heap.
- **Dense graph:** I expected Prim to do better here. Kruskal still won, because Python's `sorted()` runs in fast C code, and Kruskal **stops as soon as it has V−1 edges**. Prim (lazy version) pushes up to E entries onto the heap, and each push and pop goes through Python. It also builds a 250,000-edge adjacency list. Prim would win on a dense graph if it used an adjacency matrix with an O(V²) array instead of a heap, because that needs no sorting and no heap at all.

### 5. Dijkstra with a negative edge

Graph: A→B 5, A→C 2, **B→C −4**, C→D 1

| Vertex | Dijkstra | Correct (Bellman-Ford) |
|---|---|---|
| A | 0 | 0 |
| B | 5 | 5 |
| C | **2** | **1** (A → B → C = 5 − 4) |
| D | **3** | **2** (A → B → C → D) |

**Dijkstra is wrong for C and D.** It finishes C first, with distance 2, because 2 < 5. Later it finds the path through B, but C is already marked as final, so Dijkstra never changes it. D is also wrong, because it was computed from the wrong value of C. Dijkstra assumes that adding an edge can never make a path shorter, and a negative edge breaks that rule.

---

## Q4: Randomized Algorithms

### 1. Randomized quickselect vs sort-then-index (finding the median, best of 3)

| n | Quickselect (s) | Sort then index (s) | Same answer? |
|---|---|---|---|
| 10,000 | 0.0008 | 0.0011 | Yes |
| 100,000 | 0.0096 | 0.0126 | Yes |
| 1,000,000 | 0.1259 | 0.1888 | Yes |

Quickselect also gave the right answer on 1,000 small random lists for every k, including lists with many repeated values.

- Quickselect is **expected O(n)**. It picks a random pivot and keeps only the side that holds the answer, so the work is about n + n/2 + n/4 + … ≈ 2n.
- Sorting is O(n log n).
- Quickselect's time grows about ×10–13 when n grows ×10, which fits O(n). Sorting grows about ×12–15.
- The gap is small because `sorted()` is written in C while quickselect is plain Python. Even so, quickselect wins at every size, and the gap grows with n.

### 2. Miller-Rabin vs trial division on 20 random 12-digit numbers

**Both tests agreed on all 20 numbers.** 2 of them were prime: 650,724,328,063 and 599,043,109,937.

| Kind of number | Trial division (s) | Miller-Rabin, 20 rounds (s) |
|---|---|---|
| Composite (18 numbers) | 0.00000 – 0.00075 | about 0.00001 |
| Prime (2 random + 5 extra primes) | 0.014 – 0.027 | about 0.00012 |

- Most random numbers have a small factor (2, 3, 5, …), so trial division stops almost at once.
- **For primes, trial division is about 130–210 times slower.** It has to try every odd number up to √n ≈ 1,000,000, which is about 500,000 divisions.
- Miller-Rabin does only about 40 multiplications per round (`pow(a, d, n)`), so it takes O(k log³ n) time no matter whether the number is prime or not.

### 3. Miller-Rabin (1 round) on 561 = 3 × 11 × 17, run 1,000 times

**It answered "prime" 18 times out of 1,000 (1.8%).** The other 982 times it correctly said "composite".

- Checking every base from 2 to 559, exactly **8 bases fool the test**: 50, 101, 103, 256, 305, 458, 460 and 511. So the expected rate is 8/558 = **1.43%**. 18 out of 1,000 is close to the expected 14, given the randomness.
- For comparison, the simple **Fermat test** is fooled by **318 of the 558 bases** (57%). 561 is a Carmichael number, so every base that shares no factor with 561 passes the Fermat test.
- Miller-Rabin is much harder to fool, because it also checks the square roots of 1 along the way. Its error is at most 1/4 per round, so with 20 rounds the chance of a wrong "prime" is below (1/4)²⁰ ≈ 10⁻¹².
