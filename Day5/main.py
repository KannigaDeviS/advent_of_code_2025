def parse_input(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip() != ""]

    # Split into ranges and ingredient IDs
    # Find the index of the blank line in the original file
    with open(filename, "r") as f:
        raw_lines = f.read().splitlines()

    blank_index = raw_lines.index("")
    ranges = raw_lines[:blank_index]
    ids = raw_lines[blank_index+1:]

    # Convert ranges into tuples of integers
    ranges = [tuple(map(int, r.split("-"))) for r in ranges]

    # Convert ids into integers
    ids = [int(i) for i in ids]

    return ranges, ids


def count_fresh(ranges, ids):
    fresh_count = 0
    for ingredient in ids:
        # Check if ingredient falls in any range
        if any(start <= ingredient <= end for start, end in ranges):
            fresh_count += 1
    return fresh_count


if __name__ == "__main__":
    ranges, ids = parse_input("input.txt")
    result = count_fresh(ranges, ids)
    print("Number of fresh ingredients:", result)
