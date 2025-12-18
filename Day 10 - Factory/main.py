
from __future__ import annotations

import re
from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, List, Sequence, Tuple


PAREN_GROUP_RE = re.compile(r"\(([^)]*)\)")
BRACKET_RE = re.compile(r"\[([^\]]+)\]")
BRACE_RE = re.compile(r"\{([^}]*)\}")


@dataclass(frozen=True)
class LightMachine:
	light_count: int
	target_mask: int
	button_masks: tuple[int, ...]


def _pattern_to_mask(pattern: str) -> int:
	mask = 0
	for i, ch in enumerate(pattern):
		if ch == "#":
			mask |= 1 << i
	return mask


def parse_factory_line(line: str) -> tuple[str, list[list[int]], list[int]]:
	line = line.strip()
	if not line:
		raise ValueError("Empty machine line")

	bracket_match = BRACKET_RE.search(line)
	if not bracket_match:
		raise ValueError(f"Missing [pattern] in line: {line}")

	brace_match = BRACE_RE.search(line)
	if not brace_match:
		raise ValueError(f"Missing {{targets}} in line: {line}")

	pattern = bracket_match.group(1).strip()

	targets_raw = brace_match.group(1).strip()
	targets = [int(x.strip()) for x in targets_raw.split(",") if x.strip()]

	buttons: list[list[int]] = []
	for raw in PAREN_GROUP_RE.findall(line):
		raw = raw.strip()
		if not raw:
			buttons.append([])
			continue
		buttons.append([int(x.strip()) for x in raw.split(",") if x.strip()])

	if not buttons:
		raise ValueError(f"No buttons found in line: {line}")

	return pattern, buttons, targets


def parse_light_machine(line: str) -> LightMachine:
	pattern, buttons, _targets = parse_factory_line(line)
	light_count = len(pattern)
	target_mask = _pattern_to_mask(pattern)

	button_masks: List[int] = []
	for indices in buttons:
		mask = 0
		for idx in indices:
			if idx < 0 or idx >= light_count:
				raise ValueError(
					f"Button index {idx} out of range for pattern length {light_count}: {line.strip()}"
				)
			mask |= 1 << idx
		button_masks.append(mask)

	return LightMachine(light_count=light_count, target_mask=target_mask, button_masks=tuple(button_masks))


def min_presses_lights(machine: LightMachine) -> int:
	n = machine.light_count
	if n <= 0:
		return 0

	start = 0
	target = machine.target_mask
	if start == target:
		return 0

	max_state = 1 << n
	dist = [-1] * max_state
	dist[start] = 0
	q: deque[int] = deque([start])

	while q:
		state = q.popleft()
		next_dist = dist[state] + 1
		for button in machine.button_masks:
			nxt = state ^ button
			if dist[nxt] != -1:
				continue
			if nxt == target:
				return next_dist
			dist[nxt] = next_dist
			q.append(nxt)

	raise ValueError("Target configuration is unreachable for a machine")


def _rref_augmented(
	A: Sequence[Sequence[int]],
	b: Sequence[int],
	col_order: Sequence[int],
) -> tuple[list[list[Fraction]], list[Fraction], list[int], list[int]]:
	m = len(A)
	n = len(A[0]) if m else 0

	M: list[list[Fraction]] = [
		[Fraction(A[r][c]) for c in col_order] + [Fraction(b[r])] for r in range(m)
	]

	pivot_cols: list[int] = []
	row = 0
	for col in range(n):
		pivot_row = None
		for r in range(row, m):
			if M[r][col] != 0:
				pivot_row = r
				break
		if pivot_row is None:
			continue

		M[row], M[pivot_row] = M[pivot_row], M[row]
		pivot_val = M[row][col]
		for j in range(col, n + 1):
			M[row][j] /= pivot_val

		for r in range(m):
			if r != row and M[r][col] != 0:
				factor = M[r][col]
				for j in range(col, n + 1):
					M[r][j] -= factor * M[row][j]

		pivot_cols.append(col)
		row += 1
		if row == m:
			break

	for r in range(m):
		if all(M[r][c] == 0 for c in range(n)) and M[r][n] != 0:
			raise ValueError("No solution for this machine (inconsistent equations)")

	pivot_set = set(pivot_cols)
	free_cols = [c for c in range(n) if c not in pivot_set]
	rhs = [M[r][n] for r in range(m)]
	coeffs = [row[:n] for row in M]
	return coeffs, rhs, pivot_cols, free_cols


def min_presses_joltage(targets: Sequence[int], buttons: Sequence[Sequence[int]]) -> int:
	b = list(targets)
	m = len(b)
	if m == 0:
		return 0

	raw_buttons: list[list[int]] = []
	for idxs in buttons:
		clean: list[int] = []
		for i in idxs:
			if i < 0 or i >= m:
				raise ValueError(f"Button index {i} out of range for counter count {m}")
			clean.append(i)
		raw_buttons.append(clean)

	kept_buttons: list[list[int]] = [btn for btn in raw_buttons if btn]
	if not kept_buttons:
		if all(v == 0 for v in b):
			return 0
		raise ValueError("No effective buttons available to reach nonzero targets")

	n = len(kept_buttons)
	A: list[list[int]] = [[0] * n for _ in range(m)]
	for j, idxs in enumerate(kept_buttons):
		for i in idxs:
			A[i][j] = 1

	ub: list[int] = [min(b[i] for i in idxs) for idxs in kept_buttons]

	col_order = sorted(range(n), key=lambda j: ub[j], reverse=True)
	inv_order = [0] * n
	for new, old in enumerate(col_order):
		inv_order[old] = new

	coeffs, rhs, pivot_cols, free_cols = _rref_augmented(A, b, col_order)

	pivot_vars = [col_order[c] for c in pivot_cols]
	free_vars = [col_order[c] for c in free_cols]

	if len(free_vars) > 3:
		raise ValueError(f"Too many degrees of freedom ({len(free_vars)}) for brute enumeration")

	pivot_exprs: list[tuple[int, Fraction, list[tuple[int, Fraction]]]] = []
	for row_idx, piv_col in enumerate(pivot_cols):
		piv_var = col_order[piv_col]
		terms: list[tuple[int, Fraction]] = []
		for free_col in free_cols:
			c = coeffs[row_idx][free_col]
			if c != 0:
				terms.append((col_order[free_col], c))
		pivot_exprs.append((piv_var, rhs[row_idx], terms))

	best: int | None = None

	if not free_vars:
		free_assign: dict[int, int] = {}
		x = [0] * n
		for var, val in free_assign.items():
			x[var] = val
		total = 0
		for piv_var, const, terms in pivot_exprs:
			val = const
			for free_var, c in terms:
				val -= c * x[free_var]
			if val < 0 or val.denominator != 1:
				break
			ival = int(val)
			if ival < 0 or ival > ub[piv_var]:
				break
			x[piv_var] = ival
		else:
			total = sum(x)
			best = total
	elif len(free_vars) == 1:
		f0 = free_vars[0]
		for v0 in range(ub[f0] + 1):
			x = [0] * n
			x[f0] = v0
			ok = True
			for piv_var, const, terms in pivot_exprs:
				val = const
				for free_var, c in terms:
					val -= c * x[free_var]
				if val < 0 or val.denominator != 1:
					ok = False
					break
				ival = int(val)
				if ival < 0 or ival > ub[piv_var]:
					ok = False
					break
				x[piv_var] = ival
			if not ok:
				continue
			total = sum(x)
			if best is None or total < best:
				best = total
	elif len(free_vars) == 2:
		f0, f1 = free_vars
		for v0 in range(ub[f0] + 1):
			for v1 in range(ub[f1] + 1):
				x = [0] * n
				x[f0] = v0
				x[f1] = v1
				ok = True
				for piv_var, const, terms in pivot_exprs:
					val = const
					for free_var, c in terms:
						val -= c * x[free_var]
					if val < 0 or val.denominator != 1:
						ok = False
						break
					ival = int(val)
					if ival < 0 or ival > ub[piv_var]:
						ok = False
						break
					x[piv_var] = ival
				if not ok:
					continue
				total = sum(x)
				if best is None or total < best:
					best = total
	else:
		f0, f1, f2 = free_vars
		for v0 in range(ub[f0] + 1):
			for v1 in range(ub[f1] + 1):
				for v2 in range(ub[f2] + 1):
					x = [0] * n
					x[f0] = v0
					x[f1] = v1
					x[f2] = v2
					ok = True
					for piv_var, const, terms in pivot_exprs:
						val = const
						for free_var, c in terms:
							val -= c * x[free_var]
						if val < 0 or val.denominator != 1:
							ok = False
							break
						ival = int(val)
						if ival < 0 or ival > ub[piv_var]:
							ok = False
							break
						x[piv_var] = ival
					if not ok:
						continue
					total = sum(x)
					if best is None or total < best:
						best = total

	if best is None:
		raise ValueError("No nonnegative integer solution found")
	return best


def solve_part1(lines: Iterable[str]) -> int:
	total = 0
	for line in lines:
		line = line.strip()
		if not line:
			continue
		machine = parse_light_machine(line)
		total += min_presses_lights(machine)
	return total


def solve_part2(lines: Iterable[str]) -> int:
	total = 0
	for line in lines:
		line = line.strip()
		if not line:
			continue
		_pattern, buttons, targets = parse_factory_line(line)
		total += min_presses_joltage(targets, buttons)
	return total


def main() -> None:
	with open("input.txt", "r", encoding="utf-8") as f:
		print(solve_part2(f))


if __name__ == "__main__":
	main()
