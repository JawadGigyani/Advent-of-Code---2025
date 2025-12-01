import pandas as pd
import numpy as np
import os

df = pd.read_csv("Input.csv")

# 1. Parse the string data
df['direction'] = df['rotation'].str[0]
df['amount'] = df['rotation'].str[1:].astype(int)

# 2. Calculate the numeric change
df['change'] = df.apply(
    lambda row: row['amount'] if row['direction'] == 'R' else -row['amount'], 
    axis=1
)

# 3. Calculate absolute positions
start_position = 50
# The 'end' position of the current move
df['end_abs'] = start_position + df['change'].cumsum()
# The 'start' position of the current move (shift end_abs down, fill first with start_position)
df['start_abs'] = df['end_abs'].shift(1, fill_value=start_position)

# --- PART 1 CALCULATION ---
# Password is the number of times the dial lands on 0 (multiples of 100)
df['dial_position'] = df['end_abs'] % 100
part1_password = (df['dial_position'] == 0).sum()

# --- PART 2 CALCULATION (Method 0x434C49434B) ---
# We need to count how many multiples of 100 are crossed or landed on.

# Initialize hits column
df['zero_crossings'] = 0

# Vectorized calculation for Positive moves (R)
mask_pos = df['change'] > 0
df.loc[mask_pos, 'zero_crossings'] = (
    np.floor(df.loc[mask_pos, 'end_abs'] / 100) - 
    np.floor(df.loc[mask_pos, 'start_abs'] / 100)
).astype(int)

# Vectorized calculation for Negative moves (L)
mask_neg = df['change'] < 0
df.loc[mask_neg, 'zero_crossings'] = (
    np.floor(-df.loc[mask_neg, 'end_abs'] / 100) - 
    np.floor(-df.loc[mask_neg, 'start_abs'] / 100)
).astype(int)

part2_password = df['zero_crossings'].sum()

# --- Output Results ---
print("-" * 30)
print(f"Analyzing {len(df)} rotations...")
print(f"Starting Position: {start_position}")
print("-" * 30)

print("First 10 steps trace:")
cols = ['rotation', 'start_abs', 'end_abs', 'zero_crossings']
print(df[cols].head(10))
print("-" * 30)

print(f"Part 1 Password (Lands on 0): {part1_password}")
print(f"Part 2 Password (Crosses 0): {part2_password}")
print("-" * 30)
