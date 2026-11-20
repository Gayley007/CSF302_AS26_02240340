# Lab 7 - Q2: Huffman coding
# Run with:  python lab7_q2_huffman.py
#
# Steps for each file:
#   1. count how often each character appears
#   2. build the Huffman tree with a priority queue (heapq)
#   3. read the code of each character from the tree
#   4. encode the text into a string of 0s and 1s, then decode it back
#   5. compare the size with 8 bits per character

import heapq

# The tree is made of nested tuples:
#   a leaf is just the character itself, e.g. "a"
#   an inner node is a pair (left, right)


def count_frequencies(text):
    freq = {}
    for ch in text:
        if ch in freq:
            freq[ch] += 1
        else:
            freq[ch] = 1
    return freq


def build_tree(freq):
    # Each heap entry is (frequency, number, tree).
    # "number" is just a counter so that two equal frequencies never
    # need to compare the trees themselves.
    heap = []
    number = 0
    for ch in freq:
        heapq.heappush(heap, (freq[ch], number, ch))
        number += 1

    # keep joining the two smallest trees until only one is left
    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)       # smallest
        f2, _, right = heapq.heappop(heap)      # second smallest
        heapq.heappush(heap, (f1 + f2, number, (left, right)))
        number += 1

    return heap[0][2]                           # the root of the tree


def make_codes(tree, prefix, codes):
    # walk down the tree: going left adds "0", going right adds "1"
    if isinstance(tree, str):                   # a leaf (one character)
        if prefix == "":
            prefix = "0"                        # text with only one kind of character
        codes[tree] = prefix
    else:
        make_codes(tree[0], prefix + "0", codes)
        make_codes(tree[1], prefix + "1", codes)
    return codes


def encode(text, codes):
    parts = []
    for ch in text:
        parts.append(codes[ch])
    return "".join(parts)


def decode(bits, tree):
    # start at the root, follow 0 = left / 1 = right,
    # and when we reach a leaf, write that character and go back to the root
    if isinstance(tree, str):                   # only one kind of character
        return tree * len(bits)
    result = []
    node = tree
    for b in bits:
        if b == "0":
            node = node[0]
        else:
            node = node[1]
        if isinstance(node, str):
            result.append(node)
            node = tree
    return "".join(result)


def show_char(ch):
    # make spaces and newlines visible in the code table
    if ch == " ":
        return "' '"
    if ch == "\n":
        return "\\n"
    if ch == "\t":
        return "\\t"
    return ch


def run(filename, print_table):
    with open(filename, encoding="utf-8") as f:
        text = f.read()

    freq = count_frequencies(text)
    tree = build_tree(freq)
    codes = make_codes(tree, "", {})

    if print_table:
        print("  Code table (most common first):")
        print("    char  freq  code")
        order = sorted(freq, key=freq.get, reverse=True)
        for ch in order:
            print("    " + show_char(ch).ljust(5) + str(freq[ch]).rjust(5) + "  " + codes[ch])

    bits = encode(text, codes)
    back = decode(bits, tree)

    fixed_bits = 8 * len(text)                 # 8 bits per character
    huffman_bits = len(bits)
    print("  characters      :", len(text))
    print("  different chars :", len(freq))
    print("  decoded == original?", back == text)
    print("  8-bit size      :", fixed_bits, "bits")
    print("  Huffman size    :", huffman_bits, "bits")
    print("  average bits/char:", round(huffman_bits / len(text), 3))
    print("  compression ratio (8-bit / Huffman):", round(fixed_bits / huffman_bits, 3))
    print("  space saved     :", str(round(100 * (1 - huffman_bits / fixed_bits), 1)) + "%")
    return back == text


if __name__ == "__main__":
    files = ["story.txt", "lab7_q1_greedy.py", "dna.txt"]
    for name in files:
        print("=== " + name + " ===")
        # the full table is long, so only print it for the first file
        run(name, name == "story.txt")
        print()
