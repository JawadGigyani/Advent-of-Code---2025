def is_invalid_id(n: int) -> bool:
    s = str(n)
    length = len(s)
    # Try all possible sequence lengths from 1 up to half the length
    for seq_len in range(1, length // 2 + 1):
        if length % seq_len != 0:
            continue
        chunk = s[:seq_len]
        if chunk * (length // seq_len) == s:
            return True
    return False

def parse_ranges(line: str):
    ranges = []
    for part in line.strip().split(','):
        part = part.strip()
        if not part:
            continue
        start, end = map(int, part.split('-'))
        ranges.append((start, end))
    return ranges

def main():
    with open("input.txt") as f:
        line = f.read()
    ranges = parse_ranges(line)
    invalid_ids = []
    for start, end in ranges:
        for n in range(start, end + 1):
            if is_invalid_id(n):
                invalid_ids.append(n)
    print(sum(invalid_ids))

if __name__ == "__main__":
    main()