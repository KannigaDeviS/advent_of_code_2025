def read_grid(filename="input.txt"):
    with open(filename) as f:
        return [list(line.strip()) for line in f if line.strip()]

def count_accessible(grid):
    rows, cols = len(grid), len(grid[0])
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)
    ]
    accessible_positions = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "@":
                neighbor_rolls = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == "@":
                            neighbor_rolls += 1
                if neighbor_rolls < 4:
                    accessible_positions.append((r, c))
    return accessible_positions

def part1(grid):
    """Return number of accessible rolls in initial grid."""
    return len(count_accessible(grid))

def part2(grid):
    """Simulate removal process until no more rolls accessible."""
    total_removed = 0
    while True:
        accessible = count_accessible(grid)
        if not accessible:
            break
        # Remove them
        for r, c in accessible:
            grid[r][c] = "."
        total_removed += len(accessible)
    return total_removed

if __name__ == "__main__":
    grid = read_grid("input.txt")
    # Copy grid for part2 since part2 modifies it
    import copy
    grid_copy = copy.deepcopy(grid)

    result1 = part1(grid)
    result2 = part2(grid_copy)

    print("Part 1 - Accessible rolls initially:", result1)
    print("Part 2 - Total rolls removed:", result2)
