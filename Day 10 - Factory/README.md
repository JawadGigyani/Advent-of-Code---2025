# Advent of Code 2025 - Day 10: Factory

[View the full puzzle on Advent of Code](https://adventofcode.com/2025/day/10)

## Problem Overview

The Factory consists of a series of machines, each with a set of indicator lights and a set of buttons. Each machine is described by:

- A target pattern for the indicator lights (e.g., `[.#..#]`),
- A list of buttons, each toggling a subset of the lights (e.g., `(1,3)`),
- A list of joltage requirements (e.g., `{3,5,4,7}`), which is ignored in Part 1 and used in Part 2.

### Part 1: Minimum Button Presses for Indicator Lights

Each machine starts with all lights off. Pressing a button toggles (XORs) the state of the specified lights. The goal is to reach the target pattern using the fewest button presses. Each button can be pressed at most once (since pressing twice cancels itself out).

**Approach:**

- Model the lights as a bitmask and each button as a bitmask toggle.
- Use BFS to find the shortest sequence of button presses (minimum Hamming weight) to reach the target pattern from all-off.
- Sum the minimum presses over all machines.

### Part 2: Minimum Button Presses for Joltage Counters

Now, each machine has a set of counters (one per joltage requirement in `{...}`), all starting at zero. Each button, when pressed, increases each listed counter by 1. The goal is to reach the exact target vector for the counters, using the fewest total button presses (buttons can be pressed any number of times).

**Approach:**

- Model the system as a set of linear equations: $A x = b$, where $A$ is the counters-affected-by-buttons matrix, $x$ is the vector of button press counts, and $b$ is the target vector.
- Find a nonnegative integer solution $x$ minimizing $\sum x_j$.
- For this input, the number of free variables is small (≤3), so the solution uses rational RREF (Gaussian elimination) to express all variables in terms of the free ones, then enumerates all possible assignments to the free variables within tight bounds to find the minimum.
- Sum the minimum presses over all machines.

## Implementation Notes

- The solution is implemented in Python in `main.py`.
- For Part 1, the code parses each machine, builds bitmasks, and runs BFS for each.
- For Part 2, the code parses the counters and button wiring, builds the system of equations, and solves for the minimum total presses using RREF and bounded enumeration.
- The code automatically detects which part to solve based on the current puzzle state.

## Example

Given the following machine:

```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
```

- **Part 1:** Find the minimum number of button presses to reach the light pattern `.##.` from all-off.
- **Part 2:** Find the minimum number of button presses (with repeats allowed) to reach counters `{3,5,4,7}`.

## Results

- On the provided input, the minimum total button presses for all machines in Part 2 is:

```
15132
```

## Strategy Justification

- BFS is optimal for Part 1 due to the small state space (lights ≤ 10).
- For Part 2, the bounded number of free variables (≤3) makes exact enumeration feasible and efficient after RREF.

## File Structure

- `main.py` — Solution code for both parts.
- `input.txt` — Puzzle input.
