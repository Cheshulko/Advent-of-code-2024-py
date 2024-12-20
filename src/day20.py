#!/usr/bin/env python3

import collections
from typing import Iterable, Optional

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
        for dir in [1, -1, 1j, -1j]:
            to_point = point + dir
            if to_point in self and self[to_point] not in obstacles:
                yield to_point

    def find(self, value) -> Optional[complex]:
        for i, row in enumerate(self.grid):
            for j, c in enumerate(row):
                if c == value:
                    return i + 1j * j

    def bfs(self, source: complex):
        queue = collections.deque([(source, 0)])
        seen = set([source])

        distance = Grid([
            list([None] * self.width) 
            for _ in range(self.height)
        ])
        distance[source] = 0

        while queue:
            (cur, dist) = queue.popleft()

            for neighbor in self.get_neighbors(cur, obstacles = ["#"]):
                if neighbor not in seen:
                    seen.add(neighbor)
                    distance[neighbor] = dist  + 1
                    queue.append((neighbor, dist + 1))

        return distance

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()

def solve(input: list[str], cheat_dist: int, wanna_cheat_at_least: int):
    grid = Grid([list(line) for line in input])

    source, dest = grid.find("S"), grid.find("E")

    from_source = grid.bfs(source)
    from_dest = grid.bfs(dest)

    no_cheating = from_source[dest]

    points = [
        i + 1j* j 
        for i, row in enumerate(grid.grid) 
        for j, point in enumerate(row) 
        if point != "#" 
    ]

    def manhattan_distance(num1, num2):
        return abs(num1.real - num2.real) + abs(num1.imag - num2.imag)

    ans = 0
    for i, point1 in enumerate(points):
        for point2 in points[i + 1:]:
            dist = manhattan_distance(point1, point2)
            if dist <= cheat_dist:
                ans += (no_cheating - (from_source[point1] + from_dest[point2] + dist)) >= wanna_cheat_at_least
                ans += (no_cheating - (from_source[point2] + from_dest[point1] + dist)) >= wanna_cheat_at_least

    return ans

def check():
    input_small = read_and_parse("assets/day20/in_small.txt")

    part_1_answer = solve(input_small, cheat_dist = 2, wanna_cheat_at_least = 2)
    assert part_1_answer == 44
    part_2_answer = solve(input_small, cheat_dist = 20, wanna_cheat_at_least = 50)
    assert part_2_answer == 285

def main():
    input = read_and_parse("assets/day20/in.txt")
    
    part_1_answer = solve(input, cheat_dist = 2, wanna_cheat_at_least = 100)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 1_358
    part_2_answer = solve(input, cheat_dist = 20, wanna_cheat_at_least = 100)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 1_005_856

if __name__ == "__main__":
    check()
    main()