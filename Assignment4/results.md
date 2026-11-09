# Assignment 4 - Results

## C1. Counterexamples

Earliest finish: requests = [(0, 2, 1000), (1, 5, 5000)]
- greedy_earliest_finish = (1000, [0])
- best_schedule          = (5000, [1])

Highest fee: requests = [(0, 10, 5000), (0, 5, 3000), (5, 10, 3000)]
- greedy_highest_fee = (5000, [0])
- best_schedule      = (6000, [1, 2])

## C3. Greedy revenue / optimal revenue (1,000 inputs, 50 requests each)

| Rule | Average ratio | Worst ratio | Inputs where greedy was optimal |
|---|---|---|---|
| Earliest finish | 0.809 | 0.445 | 5 / 1000 |
| Highest fee | 0.870 | 0.459 | 63 / 1000 |
| DP (best_schedule) | 1.000 | 1.000 | 1000 / 1000 |
