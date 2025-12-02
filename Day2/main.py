def is_invalid_id(n: int) -> bool:
    s = str(n)
    if len(s) % 2 != 0:  # must be even length
        return False
    half = len(s) // 2
    return s[:half] == s[half:]


def sum_invalid_ids_from_file(filename: str) -> int:
    with open(filename, "r") as f:
        data = f.read().strip()

    total = 0
    ranges = data.split(",")
    for r in ranges:
        if not r:
            continue
        start, end = map(int, r.split("-"))
        for n in range(start, end + 1):
            if is_invalid_id(n):
                total += n
    return total


# Example usage:
print(sum_invalid_ids_from_file("input.txt"))
