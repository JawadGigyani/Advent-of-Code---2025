# Advent of Code 2025 - Day 2: Gift Shop

[View the full puzzle on Advent of Code](https://adventofcode.com/2025/day/2)

## 🎁 Problem Description

The North Pole gift shop database contains ranges of product IDs, but a young Elf has accidentally added a bunch of **invalid IDs**! Your task is to help the clerks identify and sum up all the invalid product IDs in the given ranges.

### Part 1

An ID is **invalid** if it consists of a sequence of digits repeated **exactly twice** (e.g., `55`, `6464`, `123123`).  
Your job: For each range, find all such IDs and sum them.

### Part 2

The definition expands: An ID is **invalid** if it consists of a sequence of digits repeated **at least twice** (e.g., `123123123`, `1212121212`, `1111111`).  
Your job: For each range, find all such IDs and sum them.

## 🧠 Solution Logic

The solution is implemented in **Python** and processes the ranges efficiently.

### Key Concept: Pattern Detection

For each number in a range:

- Convert the number to a string.
- For all possible sequence lengths (from 1 up to half the length of the number), check if the number is made by repeating a sequence at least twice.
- If so, it's invalid.

### Implementation

- **Input:** A single line in `input.txt` containing comma-separated ranges (e.g., `11-22,95-115,...`).
- **Output:** The sum of all invalid IDs found in the ranges.

#### Main Functions

- `parse_ranges(line)`: Parses the input line into a list of (start, end) tuples.
- `is_invalid_id(n)`: Checks if a number is invalid according to the current part's rules.
- `main()`: Reads input, finds invalid IDs, and prints their sum.

## 🚀 How to Run

1. Place puzzle input in `input.txt` (one line, comma-separated ranges).
2. Run the script:
   ```bash
   python main.py
   ```

## 📦 Files

- `main.py` — Solution code for both parts.
- `input.txt` — Puzzle input.
