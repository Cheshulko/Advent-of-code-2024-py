#!/usr/bin/env python3

Grid = list[str]

def read_and_parse(filename: str) -> Grid:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()
    
def is_valid(i: int, j: int, grid: Grid) -> bool:
    rows = len(grid)
    cols = len(grid[0])
    
    return i >= 0 and i < rows and j >= 0 and j < cols

def build_antennas(grid: Grid):
    antennas = {}

    for i, line in enumerate(grid):
       for j, cell in enumerate(line):
           if cell != ".":
               antennas.setdefault(cell, []).append((i, j))

    return antennas

def emit(start: tuple[int], step: tuple[int], grid: Grid, antinodes: list[list[bool]], one_step=True):
    cur_i, cur_j = start
    di, dj = step
    while is_valid(cur_i, cur_j, grid):
        antinodes[cur_i][cur_j] = True
        cur_i, cur_j = cur_i + di, cur_j + dj
        if one_step:
            break

def solve_part_1(grid: Grid):
    antennas = build_antennas(grid)
    antinodes = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for points in antennas.values():
        for i, point_1 in enumerate(points):
            for point_2 in points[i + 1:]:
                di, dj = point_1[0] - point_2[0], point_1[1] - point_2[1]

                emit((point_1[0] + di, point_1[1] + dj), (+di, +dj), grid, antinodes)
                emit((point_2[0] - di, point_2[1] - dj), (-di, -dj), grid, antinodes)

    ans = sum(sum(row) for row in antinodes)

    return ans

def solve_part_2(grid: Grid):
    antennas = build_antennas(grid)
    antinodes = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for points in antennas.values():
        for i, point_1 in enumerate(points):
            for point_2 in points[i + 1:]:
                di, dj = point_1[0] - point_2[0], point_1[1] - point_2[1]
                
                emit(point_2, (+di, +dj), grid, antinodes, one_step=False)
                emit(point_1, (-di, -dj), grid, antinodes, one_step=False)

    ans = sum(sum(row) for row in antinodes)

    return ans

def check():
    input_small = read_and_parse("assets/day08/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 14
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 34

def main():
    input = read_and_parse("assets/day08/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 222
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 884

if __name__ == "__main__":
    check()
    main()