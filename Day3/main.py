import pandas as pd

# ---------- Part 1 ----------
def max_joltage_two_digits(bank: str) -> int:
    """Find the maximum two-digit joltage from a bank."""
    max_val = 0
    for i in range(len(bank)):
        for j in range(i+1, len(bank)):
            val = int(bank[i] + bank[j])  # form two-digit number
            max_val = max(max_val, val)
    return max_val

# ---------- Part 2 ----------
def max_joltage_twelve_digits(bank: str) -> int:
    """
    Find the maximum 12-digit joltage from a bank.
    Strategy: choose the lexicographically largest subsequence of length 12.
    """
    k = 12
    stack = []
    to_remove = len(bank) - k  # how many digits we can drop

    for digit in bank:
        while stack and to_remove > 0 and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)

    # Keep only first k digits
    result = "".join(stack[:k])
    return int(result)

# ---------- Main ----------
def solve_puzzle(filename: str):
    # Read input file
    df = pd.read_csv(filename, header=None, names=["bank"])

    # Part 1: two-digit joltage
    df["part1_max"] = df["bank"].apply(max_joltage_two_digits)
    total_part1 = df["part1_max"].sum()

    # Part 2: twelve-digit joltage
    df["part2_max"] = df["bank"].apply(max_joltage_twelve_digits)
    total_part2 = df["part2_max"].sum()

    print("Results per bank:")
    print(df)
    print("\nTotal output joltage (Part 1):", total_part1)
    print("Total output joltage (Part 2):", total_part2)


# Example run
if __name__ == "__main__":
    solve_puzzle("input.txt")