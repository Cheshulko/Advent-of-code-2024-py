#!/usr/bin/env python3

from copy import copy
from functools import cache
from typing import Iterable, Optional
from itertools import permutations, pairwise

numeric_keypad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["#", "0", "A"],
]

directional_keypad = [
    ["#", "^", "A"],
    ["<", "v", ">"]
]

class Grid:
    def __init__(self, grid: list):
        self.grid = grid
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def __contains__(self, point: complex) -> bool:
        y, x = int(point.real), int(point.imag)

        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])

    def __getitem__(self, point: complex) -> int:
        return self.grid[int(point.real)][int(point.imag)]
    
    def __setitem__(self, point: complex, value):
        assert point in self

        self.grid[int(point.real)][int(point.imag)] = value

    def get_neighbors(self, point: complex, obstacles = []) -> Iterable[complex]:
        for dir in [1, -1j, 1j, -1]:
            to_point = point + dir
            if to_point in self and self[to_point] not in obstacles:
                yield to_point

    @cache
    def find(self, value) -> Optional[complex]:
        for i, row in enumerate(self.grid):
            for j, num_key in enumerate(row):
                if num_key == value:
                    return i + 1j * j
                
    @cache
    def paths(self, start: complex, end: complex) -> list[list[complex]]:
        seen = set([start])
        path = [start]
        results = []

        def dfs(cur: complex) -> int:
            if cur == end:
                results.append(copy(path))
                
                return len(path)
            
            best = 10**18
            for neighbor in self.get_neighbors(cur, obstacles = ["#"]):
                if neighbor not in seen:
                    seen.add(neighbor)
                    path.append(neighbor)
                    best = min(best, dfs(neighbor))
                    seen.remove(neighbor)
                    path.pop()

            return best

        best = dfs(start)

        return list(filter(lambda result: len(result) <= best, results))
    
def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()
    
def dir_to_key(dir: complex) -> str:
    match dir:
        case complex(real = 1, imag = 0): 
            return "v"
        case complex(real = 0, imag = 1): 
            return ">"
        case complex(real = -1, imag = 0): 
            return "^"
        case complex(real = 0, imag = -1): 
            return "<"

def solve(input: list[str], depth: int):
    result = 0
    
    directional_keypad_grid = Grid(directional_keypad)
    numeric_keypad_grid = Grid(numeric_keypad)

    @cache
    def count_moves(cur_key: str, dest_key: complex, depth = 1) -> int:
        cur_point = directional_keypad_grid.find(cur_key)
        dest_point = directional_keypad_grid.find(dest_key)

        if depth == 0:
            return int(
                abs(cur_point.real - dest_point.real) + 
                abs(cur_point.imag - dest_point.imag)
            ) + 1

        possible_points = []
        for _ in range(int(cur_point.imag), int(dest_point.imag)):
            possible_points.append(+0 + 1 * 1j)
        for _ in range(int(dest_point.imag), int(cur_point.imag)):
            possible_points.append(+0 - 1 * 1j)
        for _ in range(int(cur_point.real), int(dest_point.real)):
            possible_points.append(+1 + 0 * 1j)
        for _ in range(int(dest_point.real), int(cur_point.real)):
            possible_points.append(-1 + 0 * 1j)
        
        if not possible_points:
            return 1
        
        best = 10**20
        for points in permutations(possible_points):
            cur = cur_point
            steps = count_moves("A", dir_to_key(points[0]), depth - 1)

            for from_point, to_point in pairwise(points):
                steps += count_moves(dir_to_key(from_point), dir_to_key(to_point), depth - 1)
                cur += from_point
                if cur == 0 + 0 * 1j:
                    break
            else:
                steps += count_moves(dir_to_key(points[-1]), "A", depth - 1)
                best = min(best, steps)

        return best
    
    def solve_numeric_keypad(grid: Grid, input: list[str]) -> list[list[complex]]:
        cur_num_key = grid.find("A")
        numeric_pathes: list[list[complex]] = [[]]

        for num_key in input:
            num_key = grid.find(num_key)
            pathes = grid.paths(cur_num_key, num_key)
            numeric_pathes_upd = []
            for points in pathes:
                keys = []
                for from_point, to_point in pairwise(points):
                    dir = to_point - from_point
                    keys.append(dir_to_key(dir))
            
                for path in numeric_pathes:
                    numeric_pathes_upd.append(copy(path) + keys + ["A"])
            numeric_pathes = numeric_pathes_upd
            cur_num_key = num_key

        return numeric_pathes

    for code in input:
        numeric_pathes = solve_numeric_keypad(numeric_keypad_grid, code)

        ans = 10**20
        for numeric_path in numeric_pathes:
            path = ["A"] + numeric_path
            
            ans = min(ans, sum(
                count_moves(from_point, to_point, depth) 
                for from_point, to_point in pairwise(path)
            ))
 
        result += ans * int(code[:3])

    return result

def check():
    input_small = read_and_parse("assets/day21/in_small.txt")

    part_1_answer = solve(input_small, depth = 1)
    assert part_1_answer == 126_384
    part_2_answer = solve(input_small, depth = 24)
    assert part_2_answer == 154_115_708_116_294

def main():
    input = read_and_parse("assets/day21/in.txt")
    
    part_1_answer = solve(input, depth = 1)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 164_960
    part_2_answer = solve(input, depth = 24)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 205_620_604_017_764

if __name__ == "__main__":
    check()
    main()