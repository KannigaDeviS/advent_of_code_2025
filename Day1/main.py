def count_password_hits(rotations, start=50, method="part1"):
    """
    rotations: list of strings like ["L68", "R48", ...]
    start: starting position of the dial (default 50)
    method: "part1" or "part2"
    """
    position = start
    count_zero = 0

    for rotation in rotations:
        direction = rotation[0]  # 'L' or 'R'
        steps = int(rotation[1:])  # number after L/R

        if method == "part1":
            # Just move and check final position
            if direction == 'L':
                position = (position - steps) % 100
            elif direction == 'R':
                position = (position + steps) % 100

            if position == 0:
                count_zero += 1

        elif method == "part2":
            # Count every click that lands on 0
            if direction == 'L':
                for _ in range(steps):
                    position = (position - 1) % 100
                    if position == 0:
                        count_zero += 1
            elif direction == 'R':
                for _ in range(steps):
                    position = (position + 1) % 100
                    if position == 0:
                        count_zero += 1
        else:
            raise ValueError("Invalid method: choose 'part1' or 'part2'")

    return count_zero


# Example from the puzzle
example_rotations = ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"]

print("Part 1 example password:", count_password_hits(example_rotations, method="part1"))  # should be 3
print("Part 2 example password:", count_password_hits(example_rotations, method="part2"))  # should be 6

# To solve your actual input file:
with open("input.txt") as f:
    rotations = [line.strip() for line in f if line.strip()]

print("Actual Part 1 password:", count_password_hits(rotations, method="part1"))
print("Actual Part 2 password:", count_password_hits(rotations, method="part2"))
