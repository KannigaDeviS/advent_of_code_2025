def count_paths(graph, start, end):
    """Part 1: Count all paths from start to end."""
    memo = {}

    def dfs(node):
        if node == end:
            return 1
        if node in memo:
            return memo[node]

        total = 0
        for nxt in graph.get(node, []):
            total += dfs(nxt)

        memo[node] = total
        return total

    return dfs(start)


def find_paths_with_required_nodes(graph, start, end, must_visit):
    """Part 2: Find all paths from start to end that include all required nodes."""
    valid_paths = []

    def dfs(node, visited, path):
        path.append(node)

        if node == end:
            if all(req in visited for req in must_visit):
                valid_paths.append(path.copy())
            path.pop()
            return

        for nxt in graph.get(node, []):
            dfs(nxt, visited | {nxt}, path)

        path.pop()

    dfs(start, {start}, [])
    return valid_paths


def main():
    graph = {}

    # Load input
    with open("input.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, outs = line.split(":")
            outs = outs.strip().split()
            graph[name.strip()] = outs

    # --- Part 1 ---
    part1 = count_paths(graph, "you", "out")
    print("Part 1: Number of paths from 'you' to 'out':", part1)

    # --- Part 2 ---
    required = {"dac", "fft"}
    part2_paths = find_paths_with_required_nodes(graph, "svr", "out", required)
    print("Part 2: Number of paths from 'svr' to 'out' that include dac and fft:", len(part2_paths))


if __name__ == "__main__":
    main()
