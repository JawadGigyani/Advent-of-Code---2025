# Advent of Code 2025 - Day 6: Trash Compactor

[View the full puzzle on Advent of Code](https://adventofcode.com/2025/day/6)

## 🦑 Problem Description

In the Trash Compactor, the protagonist encounters a family of cephalopods who need help with their math homework. The worksheet consists of a wide grid of numbers, with each problem's numbers arranged vertically and the operation (`+` or `*`) at the bottom. Problems are separated by a full column of spaces.

### Part 1

Each problem is solved by collecting all numbers in a vertical group and applying the operation at the bottom. The grand total is the sum of all problem results.

### Part 2

Cephalopod math is written right-to-left in columns. Each number is given in its own column, with the most significant digit at the top and the least significant at the bottom. Problems are still separated by a column of spaces, and the operation is at the bottom. The grand total is the sum of all problem results, reading numbers as described.

## 🧠 Solution Logic

The solution is implemented in **Python** and robustly parses the worksheet regardless of alignment or spacing.

### Key Concept: Transposing and Grouping Columns

- The worksheet is read into a 2D grid and transposed so columns become rows.
- For each group of contiguous non-space columns, numbers and the operation are extracted.
- In Part 1, numbers are read vertically; in Part 2, each number is a column, read top-to-bottom, right-to-left within the group.
- The operation is applied to the numbers, and the results are summed for the grand total.

### Implementation

- **Input:** Each line in `input.txt` is a row of the worksheet.
- **Output:**
  - Part 1: The grand total using standard vertical math.
  - Part 2: The grand total using cephalopod right-to-left column math.

#### Main Functions

- Transposes the worksheet and groups columns into problems.
- Extracts numbers and operations, applies the correct math, and sums results.

## 🚀 How to Run

1. Place the puzzle input in `input.txt` (one worksheet row per line).
2. Run the script:
   ```bash
   python main.py
   ```

## 📦 Files

- `main.py` — Solution code for both parts.
- `input.txt` — The puzzle input worksheet.
