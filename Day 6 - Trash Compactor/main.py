def parse_problems_from_transposed(lines):
    maxlen = max(len(line) for line in lines)
    padded = [line.ljust(maxlen) for line in lines]
    columns = [''.join(row[i] for row in padded) for i in range(maxlen)]

    problems = []
    i = 0
    while i < len(columns):
        if all(c == ' ' for c in columns[i]):
            i += 1
            continue
        start = i
        while i < len(columns) and not all(c == ' ' for c in columns[i]):
            i += 1
        end = i  
        problems.append(columns[start:end])
    return problems

def solve_problem_cephalopod(problem_cols):
    rows = len(problem_cols[0])
    op = ''.join(col[rows - 1] for col in problem_cols).strip()
    numbers = []
    for col in reversed(problem_cols):  
        num = ''.join(col[r] for r in range(rows - 1)).strip()
        if num:
            numbers.append(int(num))
    if op == '+':
        return sum(numbers)
    elif op == '*':
        result = 1
        for n in numbers:
            result *= n
        return result
    else:
        raise ValueError(f"Unknown operation: {op}")

def main():
    with open("input.txt") as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]
    problems = parse_problems_from_transposed(lines)
    total = sum(solve_problem_cephalopod(p) for p in problems)
    print(total)

if __name__ == "__main__":
    main()