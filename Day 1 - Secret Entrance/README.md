# Advent of Code 2025 - Day 1: Secret Entrance

[View the full puzzle on Advent of Code](https://adventofcode.com/2025/day/1)

## 🎄 Problem Description

The Elves have lost the password to the North Pole secret entrance! We are presented with a safe dial (0-99) that starts at position **50**. We are given a list of rotations (e.g., `R10`, `L5`).

### Part 1

The password is the number of times the dial **lands exactly on 0** after a rotation is complete.

### Part 2

We discover "Method 0x434C49434B". The password is the number of times the dial **touches or crosses 0** at any point during the rotations (including the final resting spot).

## 🧠 Solution Logic

My solution uses **Python** and **Pandas** to process the rotations efficiently using vectorized operations.

### Key Concept: Linearizing the Dial

Instead of simulating the circular dial (0-99) step-by-step, I track the **absolute cumulative position**.

- A rotation of `R10` adds 10.
- A rotation of `L10` subtracts 10.
- The dial is circular with size 100.

By tracking the total accumulated value, the "dial position" is simply `absolute_position % 100`.

### Part 1: Landing on Zero

We calculate the absolute position at the end of every move.

```python
df['dial_position'] = df['end_abs'] % 100
part1_password = (df['dial_position'] == 0).sum()
```

### Part 2: Crossing Zero

This is the tricky part! Since 0 is equivalent to any multiple of 100 (0, 100, 200, -100...), counting how many times we cross 0 is equivalent to counting how many **multiples of 100** exist between the start and end of a move.

I used a mathematical trick involving the `floor` function:

- The number of 100s in a number X is `floor(X / 100)`.
- The difference between the floor of the end position and the floor of the start position tells us how many "100 boundaries" were crossed.

**For positive moves (Right):**

```
Crossings = floor(End / 100) - floor(Start / 100)
```

**For negative moves (Left):**

```
Crossings = floor(-End / 100) - floor(-Start / 100)
```

The logic for negative moves is inverted to handle the direction correctly.

## 🚀 How to Run

1. Ensure you have `pandas` and `numpy` installed:
   ```bash
   pip install pandas numpy
   ```
2. Place your puzzle input in `Input.csv` (with a header `rotation`).
3. Run the script:
   ```bash
   python main.py
   ```
