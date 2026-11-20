# Assignment 2 - Results

## C2. Running times (seconds)

| n | brute force (s) | divide & conquer (s) | brute / D&C |
|---|---|---|---|
| 1000 | 0.076 | 0.0028 | 27x |
| 2000 | 0.329 | 0.0065 | 50x |
| 4000 | 1.323 | 0.0134 | 98x |
| 8000 | 5.298 | 0.0318 | 167x |
| 16000 | 19.907 | 0.0702 | 284x |
| 32000 | 76.656 | 0.1271 | 603x |
| 64000 | (skipped, over 60 s) | 0.3240 | - |

### What happens when n doubles

| n | brute: time / previous time | D&C: time / previous time |
|---|---|---|
| 2000 | 4.31 | 2.34 |
| 4000 | 4.02 | 2.06 |
| 8000 | 4.00 | 2.36 |
| 16000 | 3.76 | 2.21 |
| 32000 | 3.85 | 1.81 |
| 64000 | - | 2.55 |

(Theta(n^2) should give about 4.00. Theta(n log n) should give a bit over 2.00.)

Slope of the log-log line: brute force = 1.99, divide & conquer = 1.14

## C3. Crossover point

| n | brute force (microseconds) | divide & conquer (microseconds) | faster |
|---|---|---|---|
| 2 | 0.5 | 1.1 | brute |
| 5 | 2.4 | 5.4 | brute |
| 10 | 8.3 | 13.8 | brute |
| 20 | 33.3 | 30.7 | D&C |
| 30 | 68.8 | 51.1 | D&C |
| 40 | 119.4 | 67.6 | D&C |
| 50 | 199.9 | 93.1 | D&C |
| 60 | 260.7 | 113.5 | D&C |
| 70 | 360.2 | 137.9 | D&C |
| 80 | 472.7 | 158.3 | D&C |
| 90 | 625.0 | 176.3 | D&C |
| 100 | 736.0 | 197.6 | D&C |
| 125 | 1142.1 | 277.5 | D&C |
| 150 | 2012.8 | 419.9 | D&C |

First n where divide and conquer is faster: 18
Smallest n from which divide and conquer is ALWAYS faster (n up to 150): 18
