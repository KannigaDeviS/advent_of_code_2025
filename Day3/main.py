import pandas as pd

def max_joltage_per_bank(bank: str) -> int:
    max_val = 0
    for i in range(len(bank)):
        for j in range(i+1, len(bank)):
            val = int(bank[i] + bank[j])  # form two-digit number
            max_val = max(max_val, val)
    return max_val

# Read input.txt using pandas
# Each line is a bank of batteries
df = pd.read_csv("input.txt", header=None, names=["bank"])

# Compute maximum joltage for each bank
df["max_joltage"] = df["bank"].apply(max_joltage_per_bank)

# Compute total output joltage
total_output = df["max_joltage"].sum()

print("Maximum joltage per bank:")
print(df)
print("\nTotal output joltage:", total_output)
