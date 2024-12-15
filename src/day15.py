#!/usr/bin/env python3

import functools
from typing import Optional
from collections import deque

@functools.total_ordering
class Point(tuple[int, int]):
    def key(self) -> tuple[int, int]:
        return (self[0], self[1])

    def __lt__(self, other) -> bool:
        return self.key() < other.key()

    def __eq__(self, other) -> bool:
        return self.key() == other.key()

    def __hash__(self) -> int:
        return hash(self.key())
    
    def __add__(self, other):
        return Point((self[0] + other[0], self[1] + other[1]))

    def __sub__(self, other):
        return Point((self[0] - other[0], self[1] - other[1]))

    def __iadd__(self, other):
        self = self + other

        return self

    def __isub__(self, other):
        self = self - other

        return self

class Grid:
    DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, input: str):
        grid = [list(line) for line in input.splitlines()]
        self.grid = grid

        self.robot = self._robot_point()

    def __getitem__(self, point: Point) -> str:
        x = point[0]
        y = point[1]
    
        return self.grid[x][y]
    
    def __setitem__(self, point: Point, value: str):
        x = point[0]
        y = point[1]
        self.grid[x][y] = value

    def robot_point(self) -> Point:
        return self.robot
    
    def double_width(self):
        doubled_grid = []
        for row in self.grid:
            doubled_row = []
            for c in row:
                match c:
                    case "#": 
                        doubled_row.append("#")
                        doubled_row.append("#")
                    case "O":
                        doubled_row.append("[")
                        doubled_row.append("]")
                    case "@":
                        doubled_row.append("@")
                        doubled_row.append(".")
                    case ".":
                        doubled_row.append(".")
                        doubled_row.append(".")
            doubled_grid.append(doubled_row)

        self.grid = doubled_grid
        self.robot = self._robot_point()

    def try_move(self, dir: Point) -> Point: 
        assert self.__getitem__(self.robot) == "@" 

        if (pushed_points := self._get_pushed_points(dir)) is not None:
            for point in pushed_points:
                
                self.__setitem__(point + dir, pushed_points[point])
                if point - dir not in pushed_points:
                    self.__setitem__(point, ".")

            self.robot += dir

    def score(self, symbol: str) -> int:
        ans = 0
        for i, row in enumerate(self.grid):
            for j, c in enumerate(row):
                if c == symbol:
                    ans += 100 * i + j

        return ans
    
    def _robot_point(self) -> Point:
        robot = Point((-1, -1))
        for i, row in enumerate(self.grid):
            for j, c in enumerate(row):
                if c == "@":
                    robot = Point((i, j))

        return robot
    
    def _is_obstacle(self, point: Point) -> bool:
        return self.__getitem__(point) == "#"
    
    def _get_pushed_points(self, dir: Point) -> Optional[dict[Point, str]]:
        robot = self.robot_point()

        pushed_points = dict()
        points_queue = deque()
        points_queue.append(robot)

        while points_queue:
            cur = points_queue.popleft()
            pushed_points[cur] = self.__getitem__(cur)
            next = cur + dir

            if self._is_obstacle(next):
                return None

            match self.__getitem__(next):
                case "O":
                    points_queue.append(next)
                case "[":
                    points_queue.append(next)
                    if dir == Grid.DIRS[0] or dir == Grid.DIRS[2]:
                        points_queue.append(next + Point((0, 1)))
                case "]":
                    points_queue.append(next)
                    if dir == Grid.DIRS[0] or dir == Grid.DIRS[2]:
                        points_queue.append(next - Point((0, 1)))

        return pushed_points

def read(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().split("\n\n")

def parse(input: list[str]) -> tuple[Grid, list[Point]]:
    grid = Grid(input[0])
    
    moves = []
    for row in input[1]:
        for c in row:
            match c:
                case "^": 
                    moves.append(Grid.DIRS[0])
                case ">":
                    moves.append(Grid.DIRS[1])
                case "v":
                    moves.append(Grid.DIRS[2])
                case "<":
                    moves.append(Grid.DIRS[3])

    return grid, moves

def solve(input: list[str], score_symbol: str, doubled_width = False):
    grid, moves = parse(input)

    if doubled_width:
        grid.double_width()

    for move in moves:
        grid.try_move(move)

    return grid.score(score_symbol)

def solve_part_1(input: list[str]):
    return solve(input, "O")

def solve_part_2(input: list[str]):
    return solve(input, "[", doubled_width = True)

def check():
    input_small_1 = read("assets/day15/in_small_1.txt")

    part_1_answer = solve_part_1(input_small_1)
    assert part_1_answer == 2_028
    part_2_answer = solve_part_2(input_small_1)
    assert part_2_answer == 1_751

    input_small_2 = read("assets/day15/in_small_2.txt")

    part_1_answer = solve_part_1(input_small_2)
    assert part_1_answer == 10_092
    part_2_answer = solve_part_2(input_small_2)
    assert part_2_answer == 9_021

def main():
    input = read("assets/day15/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 1_495_147
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 1_524_905

if __name__ == "__main__":
    check()
    main()