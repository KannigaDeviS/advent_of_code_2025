def is_invalid_part1(n: int) -> bool:
    """Part 1: invalid if digits repeated exactly twice."""
    s = str(n)
    if len(s) % 2 != 0:
        return False
    half = len(s) // 2
    return s[:half] == s[half:]


def is_invalid_part2(n: int) -> bool:
    """Part 2: invalid if digits repeated at least twice."""
    s = str(n)
    length = len(s)
    # Try all possible chunk sizes
    for k in range(1, length // 2 + 1):
        if length % k == 0:  # must divide evenly
            chunk = s[:k]
            if all(s[i:i + k] == chunk for i in range(0, length, k)):
                return True
    return False


def sum_invalid_ids(filename: str, part: int = 1) -> int:
    with open(filename, "r") as f:
        data = f.read().strip()

    total = 0
    ranges = data.split(",")
    for r in ranges:
        if not r:
            continue
        start, end = map(int, r.split("-"))
        for n in range(start, end + 1):
            if part == 1 and is_invalid_part1(n):
                total += n
            elif part == 2 and is_invalid_part2(n):
                total += n
    return total

print("Part 1 sum:", sum_invalid_ids("input.txt", part=1))
print("Part 2 sum:", sum_invalid_ids("input.txt", part=2))
