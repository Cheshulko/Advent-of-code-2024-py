#!/usr/bin/env python3

import collections
import itertools
from typing import Iterable

class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [list("." * width) for _ in range(height)]

    def __contains__(self, point: complex) -> bool:
        y, x = int(point.real), int(point.imag)

        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])

    def __getitem__(self, point: complex) -> int:
        return self.grid[int(point.real)][int(point.imag)]
    
    def __setitem__(self, point: complex, value: str):
        assert point in self

        self.grid[int(point.real)][int(point.imag)] = value

    def set_bytes(self, bytes: list[complex]):
        self.grid = [list("." * self.width) for _ in range(self.height)]
        for byte in bytes:
            self[byte] = "#"

    def get_neighbors(self, point: complex) -> Iterable[tuple[complex, int]]:
        for dir in [1, -1, 1j, -1j]:
            to_point = point + dir
            if to_point in self and self[to_point] != "#":
                yield to_point

    def bfs(self) -> int:
        queue = collections.deque([(0, 0)])
        seen = set([0])

        while queue:
            (cur, dist) = queue.popleft()

            if cur == self.height - 1 + 1j * (self.width - 1):
                return dist

            for neighbor in self.get_neighbors(cur):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append((neighbor, dist + 1))

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()
    
def parse_bytes(input: list[str]) -> Iterable[complex]:
    for point in input:
        x, y = point.split(",")
        yield int(x) + 1j* int(y)

def solve_part_1(input: list[str], count: int, width: int, height: int):
    grid = Grid(width, height)
    bytes = list(itertools.islice(parse_bytes(input), count))

    grid.set_bytes(bytes)

    return grid.bfs()

def solve_part_2(input: list[str], width: int, height: int):
    grid = Grid(width, height)
    bytes = list(parse_bytes(input))

    low = 0
    high = len(bytes)
    while high - low > 1:
        mid = (high + low) >> 1
        grid.set_bytes(bytes[:mid + 1])

        if grid.bfs() is not None:
            low = mid
        else:
            high = mid

    return f"{int(bytes[high].real)},{int(bytes[high].imag)}"

def check():
    input_small = read_and_parse("assets/day18/in_small.txt")

    part_1_answer = solve_part_1(input_small, count = 12, width = 7, height = 7)
    assert part_1_answer == 22
    part_2_answer = solve_part_2(input_small, width = 7, height = 7)
    assert part_2_answer == "6,1"

def main():
    input = read_and_parse("assets/day18/in.txt")
    
    part_1_answer = solve_part_1(input, count = 1024, width = 71, height = 71)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 324
    part_2_answer = solve_part_2(input, width = 71, height = 71)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == "46,23"

if __name__ == "__main__":
    check()
    main()