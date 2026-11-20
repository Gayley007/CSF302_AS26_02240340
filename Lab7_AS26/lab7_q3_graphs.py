# Lab 7 - Q3: Shortest paths (Dijkstra) and minimum spanning trees
# (Kruskal and Prim)
# Run with:  python lab7_q3_graphs.py

import heapq
import random
import time

random.seed(7)


# ===============================================================
# Part 1: Dijkstra with a binary heap (heapq)
# graph = dictionary: vertex -> list of (neighbour, weight)
# ===============================================================

def read_graph(filename):
    graph = {}
    with open(filename) as f:
        for line in f:
            parts = line.split()
            if len(parts) != 3 or line.startswith("#"):
                continue                     # skip comments and empty lines
            u, v, w = parts[0], parts[1], int(parts[2])
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []
            graph[u].append((v, w))
    return graph


def dijkstra(graph, source):
    dist = {}
    prev = {}                    # prev[v] = the vertex we came from on the best path
    for v in graph:
        dist[v] = float("inf")
        prev[v] = None
    dist[source] = 0

    done = set()                 # vertices whose distance is final
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)       # closest vertex not finished yet
        if u in done:
            continue                     # an old, longer entry - skip it
        done.add(u)
        for v, w in graph[u]:
            if v in done:
                continue                 # Dijkstra never changes a finished vertex
            if d + w < dist[v]:          # found a shorter way to v
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, prev


def get_path(prev, target):
    # follow prev[] backwards from the target, then reverse it
    path = []
    v = target
    while v is not None:
        path.append(v)
        v = prev[v]
    path.reverse()
    return path


def bellman_ford(graph, source):
    # slower but works with negative edges: relax every edge V-1 times
    dist = {}
    for v in graph:
        dist[v] = float("inf")
    dist[source] = 0
    for _ in range(len(graph) - 1):
        for u in graph:
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
    return dist


# ===============================================================
# Part 2: Minimum spanning tree
# The graph is undirected, vertices are 0 .. V-1,
# edges is a list of (weight, u, v).
# ===============================================================

def find(parent, x):
    # find the leader of x's group, and make the path shorter as we go
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def kruskal(V, edges):
    parent = list(range(V))       # union-find: every vertex starts in its own group
    total = 0
    used = 0
    for w, u, v in sorted(edges):           # cheapest edge first
        root_u = find(parent, u)
        root_v = find(parent, v)
        if root_u != root_v:                # different groups -> no cycle
            parent[root_u] = root_v         # join the two groups
            total += w
            used += 1
            if used == V - 1:               # the tree is complete
                break
    return total


def prim(V, edges):
    # build an adjacency list first
    adj = []
    for _ in range(V):
        adj.append([])
    for w, u, v in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))

    in_tree = [False] * V
    total = 0
    heap = [(0, 0)]              # (edge weight, vertex) - start from vertex 0
    count = 0
    while heap and count < V:
        w, u = heapq.heappop(heap)          # cheapest edge leaving the tree
        if in_tree[u]:
            continue
        in_tree[u] = True
        total += w
        count += 1
        for w2, v in adj[u]:
            if not in_tree[v]:
                heapq.heappush(heap, (w2, v))
    return total


def random_connected_graph(V, E):
    # Step 1: connect vertex i to a random earlier vertex -> always connected.
    # Step 2: add random extra edges until there are E edges.
    edges = []
    seen = set()
    for i in range(1, V):
        j = random.randint(0, i - 1)
        edges.append((random.randint(1, 1000), i, j))
        seen.add((j, i))
    while len(edges) < E:
        u = random.randint(0, V - 1)
        v = random.randint(0, V - 1)
        if u == v:
            continue
        a = min(u, v)
        b = max(u, v)
        if (a, b) in seen:
            continue                        # no repeated edges
        seen.add((a, b))
        edges.append((random.randint(1, 1000), a, b))
    return edges


if __name__ == "__main__":
    print("=== Part 1: Dijkstra on graph.txt (source A) ===")
    graph = read_graph("graph.txt")
    dist, prev = dijkstra(graph, "A")
    for v in sorted(graph):
        if dist[v] == float("inf"):
            print("  " + v + ": not reachable")
        else:
            print("  " + v + ": distance " + str(dist[v]).rjust(3)
                  + "   path " + " -> ".join(get_path(prev, v)))

    print("\n=== Part 3: Kruskal vs Prim on 100 random connected graphs ===")
    same = 0
    for _ in range(100):
        V = random.randint(2, 60)
        max_edges = V * (V - 1) // 2
        E = random.randint(V - 1, max_edges)
        edges = random_connected_graph(V, E)
        if kruskal(V, edges) == prim(V, edges):
            same += 1
    print("  same total weight on", same, "out of 100 graphs")

    print("\n=== Part 4: timing, V = 1000 (best of 3 runs) ===")
    V = 1000
    for name, E in [("sparse (E = 3V)", 3 * V), ("dense (E = V^2/4)", V * V // 4)]:
        edges = random_connected_graph(V, E)
        k_times = []
        p_times = []
        for _ in range(3):
            start = time.perf_counter()
            k_total = kruskal(V, edges)
            k_times.append(time.perf_counter() - start)
            start = time.perf_counter()
            p_total = prim(V, edges)
            p_times.append(time.perf_counter() - start)
        print("  " + name + ": E = " + str(E))
        print("    Kruskal: " + format(min(k_times), ".4f") + " s   total weight " + str(k_total))
        print("    Prim   : " + format(min(p_times), ".4f") + " s   total weight " + str(p_total))

    print("\n=== Part 5: Dijkstra with one negative edge ===")
    small = {
        "A": [("B", 5), ("C", 2)],
        "B": [("C", -4)],          # the negative edge
        "C": [("D", 1)],
        "D": [],
    }
    print("  edges: A->B 5, A->C 2, B->C -4, C->D 1")
    d_dist, _ = dijkstra(small, "A")
    b_dist = bellman_ford(small, "A")
    for v in sorted(small):
        mark = "" if d_dist[v] == b_dist[v] else "   <- WRONG"
        print("  " + v + ": Dijkstra " + str(d_dist[v]).rjust(2)
              + "   correct (Bellman-Ford) " + str(b_dist[v]).rjust(2) + mark)
