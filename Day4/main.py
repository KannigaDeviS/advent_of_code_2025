def count_accessible_rolls(filename="input.txt"):
    # Read grid from file
    with open(filename) as f:
        grid = [list(line.strip()) for line in f if line.strip()]

    rows, cols = len(grid), len(grid[0])
    accessible_count = 0

    # Directions: 8 neighbors
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

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
                    accessible_count += 1

    return accessible_count


if __name__ == "__main__":
    result = count_accessible_rolls("input.txt")
    print("Accessible rolls:", result)
