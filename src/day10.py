#!/usr/bin/env python3

from typing import Optional


Grid = list[list[int]]

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()

def build_grid(input: list[str]) -> Grid:
    return [[int(cell) for cell in line] for line in input]

def is_out(i: int, j: int, grid: Grid) -> bool:
    n = len(grid)
    m = len(grid[0])

    return i < 0 or j < 0 or i >= n or j >= m

def find_paths(i: int, j: int, grid: Grid, seen: Grid, final_points: Optional[set[tuple[int, int]]] = None) -> int:
    seen[i][j] = True
    cur = grid[i][j]

    if cur == 9:
        if final_points is not None:
            final_points.add((i, j))

        return 1

    ans = 0
    for di, dj in DIRS:
        to_i, to_j = i + di, j + dj

        if not is_out(to_i, to_j, grid) and grid[to_i][to_j] == cur + 1:
            ans += find_paths(to_i, to_j, grid, seen, final_points)

    return ans

def solve_part_1(input: list[str]):
    grid = build_grid(input)
    n = len(grid)
    m = len(grid[0])

    ans = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 0:
                seen = [[[False] * len(DIRS) for _ in range(m)] for _ in range(n)]
                final_points = set()
                _ = find_paths(i, j, grid, seen, final_points)
                ans += len(final_points)

    return ans

def solve_part_2(input: list[str]):
    grid = build_grid(input)
    n = len(grid)
    m = len(grid[0])

    ans = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 0:
                seen = [[[False] * len(DIRS) for _ in range(m)] for _ in range(n)]
                ans += find_paths(i, j, grid, seen)

    return ans

def check():
    input_small = read_and_parse("assets/day10/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 36
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 81

def main():
    input = read_and_parse("assets/day10/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 644
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 1_366

if __name__ == "__main__":
    check()
    main()