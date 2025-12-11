#!/usr/bin/env python3
import sys
from collections import Counter

def parse_points(path):
    pts = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) != 3:
                raise ValueError(f"Invalid line: {line}")
            x, y, z = map(int, parts)
            pts.append((x, y, z))
    return pts

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, a):
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

def squared_dist(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    dz = p[2] - q[2]
    return dx*dx + dy*dy + dz*dz

def build_sorted_edges(points):
    n = len(points)
    edges = []
    for i in range(n):
        pi = points[i]
        for j in range(i + 1, n):
            d2 = squared_dist(pi, points[j])
            edges.append((d2, i, j))
    edges.sort(key=lambda e: e[0])
    return edges

def part1_product_of_top3(dsu):
    reps = [dsu.find(i) for i in range(len(dsu.parent))]
    counts = Counter(reps)
    sizes = sorted(counts.values(), reverse=True)
    while len(sizes) < 3:
        sizes.append(1)
    return sizes[0] * sizes[1] * sizes[2]

def solve(path="input.txt", K=1000):
    points = parse_points(path)
    n = len(points)
    if n == 0:
        return 0, 0

    edges = build_sorted_edges(points)

    # Part 1: apply first K closest pairs
    dsu1 = DSU(n)
    for idx in range(min(K, len(edges))):
        _, i, j = edges[idx]
        dsu1.union(i, j)
    part1_ans = part1_product_of_top3(dsu1)

    # Part 2: continue until a single component
    dsu2 = DSU(n)
    last_pair_x_product = 0
    # We must re-run from the beginning to guarantee correct order for part 2.
    for _, i, j in edges:
        if dsu2.union(i, j):
            # This was an effective connection
            if dsu2.components == 1:
                xi, xj = points[i][0], points[j][0]
                last_pair_x_product = xi * xj
                break

    return part1_ans, last_pair_x_product

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    part1, part2 = solve(path, K)
    print(part1)
    print(part2)

if __name__ == "__main__":
    main()
