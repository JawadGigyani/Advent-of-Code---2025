# Advent of Code 2025 – My Journey

Welcome to my Advent of Code 2025 repo. This year, I challenged myself to solve every puzzle, every day, and document not just the solutions, but the journey, my thought process, struggles, and little victories along the way.

![Advent of Code 2025 - All Stars](Completion%20Pictures/AOC-Home.png)

![Completion Message](Completion%20Pictures/AOC-Completion.png)

## Why Advent of Code?

Advent of Code is a December tradition for programmers: a new puzzle drops every midnight, and thousands of coders around the world race to solve it. For me, it’s a chance to sharpen my problem-solving skills, learn new algorithms, and have fun with code; sometimes late into the night!

## How I Approached It

- **Language:** Python (my go-to for quick prototyping and clarity)
- **Philosophy:**
  - Always get the example working first—if it doesn’t pass, I don’t move on.
  - For big/real inputs, I try to find the most efficient approach, even if it means rewriting everything.
  - I document my reasoning, and final strategies in each day’s README.
- **Techniques I Used:**
  - Everything from greedy and BFS/DFS to dynamic programming, bitmasking, graph theory, and even some linear algebra.
  - For the really tough (NP-hard) ones, I sometimes combined brute force for small cases with clever shortcuts for big ones.

## What’s in This Repo?

- Each day has its own folder: `Day N - [Theme]/`
- Inside each folder:
  - `main.py` – My solution code (usually for both parts)
  - `input.txt` or `Input.csv` – The puzzle input
  - `README.md` – My writeup: problem summary, approaches I tried, and what finally worked

## How to Run My Solutions

1. Put the puzzle input in the day’s folder as `input.txt` (or `Input.csv` for Day 1)
2. Run:
   ```bash
   python main.py
   ```
3. The script prints the answers for both parts

## What I Learned

- Sometimes the first idea is wrong, and that’s okay—iteration is key
- Reading the problem carefully saves hours of debugging
- Python’s standard library is powerful, but sometimes you need numpy or pandas for speed

## Dependencies

- Python 3.8+
- Some days: `pandas` and `numpy`
- Most days: just the Python standard library

## Attribution

- Puzzles © [Advent of Code](https://adventofcode.com/2025) by Eric Wastl
- Solutions and writeups © [JawadGigyani](https://github.com/JawadGigyani)
