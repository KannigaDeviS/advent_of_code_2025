import re
import math

def parse_blocks(lines):
    max_w = max(len(line) for line in lines)
    grid = [line.rstrip('\n').ljust(max_w) for line in lines]
    h, w = len(grid), max_w
    op_row = grid[-1]

    blocks = []
    c = 0
    while c < w:
        while c < w and all(row[c] == ' ' for row in grid):
            c += 1
        if c >= w:
            break
        start = c
        while c < w and any(row[c] != ' ' for row in grid):
            c += 1
        end = c - 1
        blocks.append((start, end))
    return grid, blocks, op_row


def solve_part1(grid, blocks, op_row):
    h = len(grid)
    total = 0
    for start, end in blocks:
        nums = []
        for r in range(h - 1):
            segment = grid[r][start:end + 1]
            m = re.search(r'\d+', segment)
            if m:
                nums.append(int(m.group(0)))
        op_segment = op_row[start:end + 1]
        if '+' in op_segment:
            result = sum(nums)
        elif '*' in op_segment:
            result = math.prod(nums)
        else:
            raise ValueError("No operator found")
        total += result
    return total


def solve_part2(grid, blocks, op_row):
    h = len(grid)
    total = 0
    for start, end in blocks:
        # Each column inside the block is a number
        nums = []
        for c in range(start, end + 1):
            digits = []
            for r in range(h - 1):  # exclude operator row
                ch = grid[r][c]
                if ch.isdigit():
                    digits.append(ch)
            if digits:
                nums.append(int(''.join(digits)))
        op_segment = op_row[start:end + 1]
        if '+' in op_segment:
            result = sum(nums)
        elif '*' in op_segment:
            result = math.prod(nums)
        else:
            raise ValueError("No operator found")
        total += result
    return total


def main():
    with open('input.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    grid, blocks, op_row = parse_blocks(lines)

    part1_total = solve_part1(grid, blocks, op_row)
    part2_total = solve_part2(grid, blocks, op_row)

    print("Part 1 total:", part1_total)
    print("Part 2 total:", part2_total)


if __name__ == '__main__':
    main()
