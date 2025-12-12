import re
import heapq
from itertools import product
from math import ceil


# -----------------------------
# Parsing
# -----------------------------
def parse_line(line):
    pattern = re.search(r"\[(.*?)\]", line).group(1)
    target_lights = [1 if c == "#" else 0 for c in pattern]

    buttons = [tuple(map(int, b.split(",")))
               for b in re.findall(r"\((.*?)\)", line)]

    jolts = list(map(int, re.search(r"\{(.*?)\}", line).group(1).split(",")))

    return target_lights, buttons, jolts


# -----------------------------
# Part 1: GF(2) minimum-weight solution
# -----------------------------
def gaussian_elimination_min_weight(A, b):
    m = len(A)
    n = len(A[0])

    aug = [A[i] + [b[i]] for i in range(m)]

    row = 0
    pivots = []
    for col in range(n):
        pivot = None
        for r in range(row, m):
            if aug[r][col] == 1:
                pivot = r
                break
        if pivot is None:
            continue

        aug[row], aug[pivot] = aug[pivot], aug[row]
        pivots.append((row, col))

        for r in range(m):
            if r != row and aug[r][col] == 1:
                aug[r] = [(aug[r][c] ^ aug[row][c]) for c in range(n + 1)]

        row += 1

    pivot_cols = {c for _, c in pivots}
    free_cols = [c for c in range(n) if c not in pivot_cols]

    def solve_with_free(free_assign):
        x = [0] * n
        for col, val in zip(free_cols, free_assign):
            x[col] = val

        for r, c in reversed(pivots):
            rhs = aug[r][n]
            for j in range(c + 1, n):
                rhs ^= (aug[r][j] & x[j])
            x[c] = rhs

        return x

    best = None
    for free_assign in product([0, 1], repeat=len(free_cols)):
        x = solve_with_free(free_assign)
        if best is None or sum(x) < sum(best):
            best = x

    return sum(best)


def solve_machine_part1(target, buttons):
    m = len(target)
    n = len(buttons)

    A = [[0] * n for _ in range(m)]
    for j, btn in enumerate(buttons):
        for light in btn:
            A[light][j] = 1

    return gaussian_elimination_min_weight(A, target)


# -----------------------------
# Part 2: A* search on counters
# -----------------------------
def solve_machine_part2(jolts, buttons):
    k = len(jolts)
    target = tuple(jolts)

    # Precompute button effect vectors on counters
    effects = []
    for btn in buttons:
        vec = [0] * k
        for idx in btn:
            vec[idx] += 1
        effects.append(tuple(vec))

    # Precompute max increment per dimension (usually 1)
    max_inc = [0] * k
    for eff in effects:
        for i in range(k):
            if eff[i] > max_inc[i]:
                max_inc[i] = eff[i]

    # If any dimension has max_inc[i] == 0 but target[i] > 0 → impossible
    for i in range(k):
        if max_inc[i] == 0 and target[i] > 0:
            raise RuntimeError("No solution: some target dimension never changes")

    def heuristic(state):
        # lower bound on presses needed from this state
        worst = 0
        for i in range(k):
            diff = target[i] - state[i]
            if diff <= 0:
                continue
            worst = max(worst, ceil(diff / max_inc[i]))
        return worst

    start = tuple([0] * k)
    # Priority queue of (f = g + h, g, state)
    pq = [(heuristic(start), 0, start)]
    best_g = {start: 0}

    while pq:
        f, g, state = heapq.heappop(pq)

        if state == target:
            return g

        # Skip if we've already found a better path
        if g > best_g.get(state, float("inf")):
            continue

        for eff in effects:
            nxt = tuple(state[i] + eff[i] for i in range(k))

            # Prune states that exceed target in any dimension
            if any(nxt[i] > target[i] for i in range(k)):
                continue

            new_g = g + 1
            if new_g < best_g.get(nxt, float("inf")):
                best_g[nxt] = new_g
                h = heuristic(nxt)
                heapq.heappush(pq, (new_g + h, new_g, nxt))

    raise RuntimeError("No solution found")


# -----------------------------
# Main
# -----------------------------
def main():
    total_part1 = 0
    total_part2 = 0

    with open("Input.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            target_lights, buttons, jolts = parse_line(line)

            total_part1 += solve_machine_part1(target_lights, buttons)
            total_part2 += solve_machine_part2(jolts, buttons)

    print("Part 1:", total_part1)
    print("Part 2:", total_part2)


if __name__ == "__main__":
    main()
