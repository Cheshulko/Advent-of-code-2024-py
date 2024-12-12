#!/usr/bin/env python3

import itertools
import collections

Grid = list[list[str]]

Region = collections.namedtuple(
    "Region", ["area", "perimeter", "sides"]
)

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()

def is_out(i: int, j: int, grid: Grid) -> bool:
    n = len(grid)
    m = len(grid[0])

    return i < 0 or j < 0 or i >= n or j >= m

def side_dirs(dir: int) -> int:
    assert dir >= 0 and dir <= 3

    return [DIRS[(dir + 1) % len(DIRS)], DIRS[(dir + 3) % len(DIRS)]]

def dfs(i: int, j: int, grid: Grid, seen: Grid, side_cells: set[tuple[int, int, int]]) -> Region:
    seen[i][j] = True

    area, perimeter, sides = 1, 0, 0

    for dir, (di, dj) in enumerate(DIRS):
        to_i, to_j = i + di, j + dj

        if (i, j, dir) not in side_cells and (
            is_out(to_i, to_j, grid) or grid[i][j] != grid[to_i][to_j]
        ):
            sides += 1
            for side_di, side_dj in side_dirs(dir):
                side_i = i
                side_j = j

                while not is_out(side_i, side_j, grid) and grid[side_i][side_j] == grid[i][j] and (
                    is_out(side_i + di, side_j + dj, grid) or grid[i][j] != grid[side_i + di][side_j + dj]
                ):
                    side_cells.add((side_i, side_j, dir))
                    side_i += side_di
                    side_j += side_dj

    for di, dj in DIRS:
        to_i, to_j = i + di, j + dj

        if is_out(to_i, to_j, grid):
            perimeter += 1
        else:
            if grid[i][j] != grid[to_i][to_j]:
                perimeter += 1
                
            elif not seen[to_i][to_j]:
                to_area, to_perimeter, to_sides = dfs(to_i, to_j, grid, seen, side_cells)
                area += to_area
                perimeter += to_perimeter
                sides += to_sides

    return area, perimeter, sides

def solve(grid: Grid) -> list[Region]:
    n = len(grid)
    m = len(grid[0])

    side_cells = set()
    seen = [[False for _ in range(m)] for _ in range(n)]

    result = list(
        dfs(i, j, grid, seen, side_cells) 
        for i, j in itertools.product(range(n), range(m)) 
        if not seen[i][j]
    )

    return result

def solve_part_1(input: list[str]):
    return sum(
        itertools.starmap(
            lambda area, perimeter, _: area * perimeter, 
            solve(input)
        )
    )

def solve_part_2(input: list[str]):
    return sum(
        itertools.starmap(
            lambda area, _, sides: area * sides, 
            solve(input)
        )
    )

def check():
    input_small = read_and_parse("assets/day12/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 1_930
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 1_206

def main():
    input = read_and_parse("assets/day12/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 1_473_276
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 901_100

if __name__ == "__main__":
    check()
    main()