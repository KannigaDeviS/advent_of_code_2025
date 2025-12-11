#!/usr/bin/env python3
from pathlib import Path
from typing import List, Tuple

def read_grid(path: str) -> List[str]:
    text = Path(path).read_text().splitlines()
    if not text:
        raise ValueError("Empty input.")
    # Validate consistent width
    width = len(text[0])
    for i, row in enumerate(text):
        if len(row) != width:
            raise ValueError(f"Inconsistent row width at line {i+1}.")
    return text

def find_start(grid: List[str]) -> Tuple[int, int]:
    for r, row in enumerate(grid):
        c = row.find('S')
        if c != -1:
            return r, c
    raise ValueError("No starting position 'S' found.")

def count_splits_classical(grid: List[str]) -> int:
    """
    Part 1: Classical manifold.
    Returns total number of splits encountered by all beams.
    """
    n_rows = len(grid)
    n_cols = len(grid[0])
    start_row, start_col = find_start(grid)

    active_cols = {start_col}
    total_splits = 0

    for r in range(start_row + 1, n_rows):
        row = grid[r]
        next_active = set()

        for col in active_cols:
            if col < 0 or col >= n_cols:
                continue
            cell = row[col]
            if cell == '.':
                next_active.add(col)
            elif cell == '^':
                total_splits += 1
                if col - 1 >= 0:
                    next_active.add(col - 1)
                if col + 1 < n_cols:
                    next_active.add(col + 1)
            else:
                # Treat unknown as empty space
                next_active.add(col)

        active_cols = next_active
        if not active_cols:
            break

    return total_splits

def count_timelines_quantum(grid: List[str]) -> int:
    """
    Part 2: Quantum manifold.
    Returns the number of distinct timelines after processing all rows.
    """
    n_rows = len(grid)
    n_cols = len(grid[0])
    start_row, start_col = find_start(grid)

    # counts[c] = number of timelines currently at column c on the current row
    counts = [0] * n_cols
    counts[start_col] = 1

    for r in range(start_row + 1, n_rows):
        row = grid[r]
        next_counts = [0] * n_cols

        for c, k in enumerate(counts):
            if k == 0:
                continue
            cell = row[c]
            if cell == '.':
                next_counts[c] += k
            elif cell == '^':
                if c - 1 >= 0:
                    next_counts[c - 1] += k
                if c + 1 < n_cols:
                    next_counts[c + 1] += k
            else:
                # Treat unknown as empty space
                next_counts[c] += k

        counts = next_counts
        if sum(counts) == 0:
            break

    return sum(counts)

def main():
    grid = read_grid("input.txt")
    part1 = count_splits_classical(grid)
    part2 = count_timelines_quantum(grid)
    print(part1)
    print(part2)

if __name__ == "__main__":
    main()
