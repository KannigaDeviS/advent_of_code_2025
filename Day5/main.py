def parse_input(filename):
    with open(filename, "r") as f:
        raw_lines = f.read().splitlines()

    blank_index = raw_lines.index("")

    ranges = raw_lines[:blank_index]
    ids = raw_lines[blank_index+1:]

    ranges = [tuple(map(int, r.split("-"))) for r in ranges]
    ids = [int(i) for i in ids]

    return ranges, ids


def count_fresh_available(ranges, ids):
    """Part One: Count how many available IDs are fresh."""
    fresh_count = 0
    for ingredient in ids:
        if any(start <= ingredient <= end for start, end in ranges):
            fresh_count += 1
    return fresh_count


def count_all_fresh_ids(ranges):
    """Part Two: Count all unique IDs considered fresh by ranges (optimized)."""
    # Sort ranges by start
    ranges.sort()
    merged = []

    for start, end in ranges:
        if not merged or start > merged[-1][1]:
            # no overlap, add new interval
            merged.append([start, end])
        else:
            # overlap, extend the last interval
            merged[-1][1] = max(merged[-1][1], end)

    # Sum lengths of merged intervals
    total = sum(end - start + 1 for start, end in merged)
    return total, merged


if __name__ == "__main__":
    ranges, ids = parse_input("input.txt")

    # Part One
    part1_result = count_fresh_available(ranges, ids)
    print("Part One: Number of fresh available ingredients =", part1_result)

    # Part Two
    part2_count, merged_ranges = count_all_fresh_ids(ranges)
    print("Part Two: Number of IDs considered fresh =", part2_count)
    print("Merged ranges:", merged_ranges)
