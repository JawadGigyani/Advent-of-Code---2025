import bisect

def parse_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f if line.strip()]

    # Split at the first line that is not a range (i.e., doesn't contain '-')
    split_idx = 0
    while split_idx < len(lines) and '-' in lines[split_idx]:
        split_idx += 1

    range_lines = lines[:split_idx]
    id_lines = lines[split_idx:]

    ranges = []
    for line in range_lines:
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

    ids = [int(line) for line in id_lines]
    return ranges, ids

def merge_ranges(ranges):
    # Sort ranges by start
    ranges.sort()
    merged = []
    for start, end in ranges:
        if not merged or merged[-1][1] < start - 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged

def is_fresh(merged_ranges, id_):
    # Use bisect to find the right interval
    # merged_ranges is a list of [start, end], sorted by start
    idx = bisect.bisect_right(merged_ranges, [id_, float('inf')]) - 1
    if idx >= 0:
        start, end = merged_ranges[idx]
        if start <= id_ <= end:
            return True
    return False

def main():
    ranges, ids = parse_input("input.txt")
    merged_ranges = merge_ranges(ranges)
    fresh_count = sum(1 for id_ in ids if is_fresh(merged_ranges, id_))
    print(fresh_count)

if __name__ == "__main__":
    main()