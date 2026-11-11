# Lab 5 - Q3 (part 5): Kendall tau distance between two users' movie rankings
# Kendall tau distance = number of movie pairs the two users put in a different order.
# This is exactly an inversion count, so we reuse merge_count from Q3.

from lab5_q3_inversions import count_inversions

MOVIES = ["Inception", "Titanic", "Avatar", "Interstellar", "Joker",
          "Frozen", "Coco", "Up", "Parasite", "Gladiator"]


def read_ranking(user_name):
    # Ask until the user types 10 different movie numbers from 1 to 10
    while True:
        text = input(f"\n{user_name}: enter your ranking (best first) as 10 movie numbers: ")
        parts = text.split()
        ok = True
        ranking = []
        for p in parts:
            if not p.isdigit():
                ok = False
            else:
                ranking.append(int(p))
        if ok and sorted(ranking) == list(range(1, 11)):
            return ranking
        print("Invalid! Use each number 1-10 exactly once, separated by spaces.")


def kendall_tau_distance(rank_a, rank_b):
    # position_in_b[m] = where user B placed movie m (0 = top)
    position_in_b = {}
    for pos in range(len(rank_b)):
        position_in_b[rank_b[pos]] = pos
    # Go through movies in user A's order and write down B's position.
    # If B agreed fully, this list would be 0,1,2,...,9 (no inversions).
    # Each inversion = one pair the users disagree on.
    seq = []
    for movie in rank_a:
        seq.append(position_in_b[movie])
    return count_inversions(seq)


if __name__ == "__main__":
    print("Movies:")
    for i in range(len(MOVIES)):
        print(f"  {i + 1:>2}. {MOVIES[i]}")

    rank_a = read_ranking("User A")
    rank_b = read_ranking("User B")

    distance = kendall_tau_distance(rank_a, rank_b)
    n = len(rank_a)
    total_pairs = n * (n - 1) // 2               # 45 pairs for 10 movies
    similarity = 1 - distance / total_pairs       # 1 = same order, 0 = exact opposite
    tau = 1 - 2 * distance / total_pairs          # Kendall tau coefficient (-1 to 1)

    print("\nUser A:", [MOVIES[m - 1] for m in rank_a])
    print("User B:", [MOVIES[m - 1] for m in rank_b])
    print(f"Kendall tau distance : {distance} out of {total_pairs} pairs disagree")
    print(f"Similarity           : {similarity:.2f}  (1 = identical, 0 = reversed)")
    print(f"Kendall tau coeff.   : {tau:.2f}  (1 = identical, -1 = reversed)")
