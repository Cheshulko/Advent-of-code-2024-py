#!/usr/bin/env python3

Grid = list[str]

DIRS = [(di, dj) for di in range(-1, 2) for dj in range(-1, 2)]

DIAG_PRIMARY = [
    [(-1, -1), (0, 0), (1, 1)],
    [(1, 1), (0, 0), (-1, -1)],
]
DIAG_SECONDARY = [
    [(-1, 1), (0, 0), (1, -1)],
    [(1, -1), (0, 0), (-1, 1)],
]

XMAS = "XMAS"
MAS = "MAS"

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()
    
def is_valid(i: int, j: int, grid: Grid) -> bool:
    assert len(grid) != 0

    return 0 <= i < len(grid) and 0 <= j < len(grid[0])

def get_letter(i: int, j: int, grid: Grid) -> str:
    if is_valid(i, j, grid):
        return grid[i][j]
    else:
        return ""

def search_xmas(i: int, j: int, grid: Grid) -> int:
    cnt = 0
    for di, dj in DIRS:
        word = "".join(
            get_letter(i + step * di, j + step * dj, grid) 
            for step in range(len(XMAS))
        )
        
        if word == XMAS:
            cnt += 1

    return cnt

def search_x_mas(i: int, j: int, grid: Grid) -> int:
    diag_primary = False
    for diag in DIAG_PRIMARY:
        word = "".join(
            get_letter(i + di, j + dj, grid) 
            for di, dj in diag
        )
        diag_primary |= word == MAS

    diag_secondary = False
    for diag in DIAG_SECONDARY:
        word = "".join(
            get_letter(i + di, j + dj, grid) 
            for di, dj in diag
        )
        diag_secondary |= word == MAS

    return diag_primary and diag_secondary

def solve_part_1(grid: list[str]):
    return sum(
        search_xmas(i, j, grid) 
        for i in range(len(grid)) 
        for j in range(len(grid[0]))
    )

def solve_part_2(grid: list[str]):
    return sum(
        search_x_mas(i, j, grid) 
        for i in range(len(grid)) 
        for j in range(len(grid[0]))
    )

def check():
    input_small = read_and_parse("assets/day04/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 18
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 9

def main():
    input = read_and_parse("assets/day04/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 2_569
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 1_998

if __name__ == "__main__":
    check()
    main()