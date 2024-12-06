#!/usr/bin/env python3

Grid = list[list[str]]

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()

def build_grid(input: list[str]) -> Grid:
    return [list(line) for line in input]

def is_out(i: int, j: int, grid: Grid) -> bool:
    n = len(grid)
    m = len(grid[0])

    return i < 0 or j < 0 or i >= n or j >= m

def is_obstacle(i: int, j: int, grid: Grid) -> bool:
    return grid[i][j] == "#"

def find_initial_pos(grid: Grid) -> tuple[int, int]:
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "^":
                return i, j

def traverse_path(dir: int, i: int, j: int, grid: Grid, seen: Grid) -> bool:
    while True:
        seen[i][j][dir] = True
        to_i, to_j = i + DIRS[dir][0], j + DIRS[dir][1]

        if is_out(to_i, to_j, grid):
            return True

        while is_obstacle(to_i, to_j, grid):
            dir = (dir + 1) % len(DIRS)
            to_i, to_j = i + DIRS[dir][0], j + DIRS[dir][1]

        assert not is_obstacle(to_i, to_j, grid)

        if not seen[to_i][to_j][dir]:
            i, j = to_i, to_j
        else:
            return False
        
def check_obstacle_at(i: int, j: int, st_i: int, st_j: int, g: bool, grid: Grid) -> bool:
    if grid[i][j] == "." and g:
        n = len(grid)
        m = len(grid[0])
        grid[i][j] = '#'
        seen = [[[False] * len(DIRS) for _ in range(m)] for _ in range(n)]
        loop = not traverse_path(0, st_i, st_j, grid, seen)
        grid[i][j] = '.'
        
        return loop
    else:
        return False

def solve_part_1(input: list[str]):
    grid = build_grid(input)
    n = len(grid)
    m = len(grid[0])

    seen = [[[False] * len(DIRS) for _ in range(m)] for _ in range(n)]
    st_i, st_j = find_initial_pos(grid)

    traverse_path(0, st_i, st_j, grid, seen)
    ans = sum(
        sum(map(any, line)) 
        for line in seen
    )

    return ans

def solve_part_2(input: list[str]):
    grid = build_grid(input)
    n = len(grid)
    m = len(grid[0])

    st_i, st_j = find_initial_pos(grid)
    initital = [[[False] * len(DIRS) for _ in range(m)] for _ in range(n)]
    traverse_path(0, st_i, st_j, grid, initital)

    ans = sum(
        check_obstacle_at(i, j, st_i, st_j, any(initital[i][j]), grid) 
        for j in range(m) 
        for i in range(n)
    )
                
    return ans

def check():
    input_small = read_and_parse("assets/day06/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 41
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 6

def main():
    input = read_and_parse("assets/day06/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 4_826
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 1_721

if __name__ == "__main__":
    check()
    main()