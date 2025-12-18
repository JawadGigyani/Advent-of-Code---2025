def parse_ranges(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f if line.strip()]
    
    ranges = []
    for line in lines:
        if '-' in line:
            start, end = map(int, line.split('-'))
            ranges.append((start, end))
        else:
            break  
    return ranges

def merge_ranges(ranges):
    ranges.sort()
    merged = []
    for start, end in ranges:
        if not merged or merged[-1][1] < start - 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged

def main():
    ranges = parse_ranges("input.txt")
    merged = merge_ranges(ranges)
    total_fresh = sum(end - start + 1 for start, end in merged)
    print(total_fresh)

if __name__ == "__main__":
    main()