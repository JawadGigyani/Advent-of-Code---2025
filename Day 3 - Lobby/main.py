def max_joltage(bank: str) -> int:
    max_right = [0] * len(bank)
    # Build max_right: for each position, the largest digit to its right
    max_digit = '0'
    for i in range(len(bank) - 1, -1, -1):
        max_right[i] = max_digit
        if bank[i] > max_digit:
            max_digit = bank[i]
    # For each position, combine with largest digit to its right
    max_val = 0
    for i in range(len(bank) - 1):
        val = int(bank[i] + max_right[i])
        if val > max_val:
            max_val = val
    return max_val

def main():
    total = 0
    with open("input.txt") as f:
        for line in f:
            line = line.strip()
            if line:
                total += max_joltage(line)
    print(total)

if __name__ == "__main__":
    main()