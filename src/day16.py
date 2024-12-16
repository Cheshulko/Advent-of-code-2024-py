#!/usr/bin/env python3

import collections
import functools
from typing import Iterable
import heapq
from collections import deque

@functools.total_ordering
class Point(tuple[int, int]):
    def __new__(cls, x: int, y: int):
        return super().__new__(cls, (x, y))
    
    def __add__(self, other):
        return Point(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        return Point(self[0] - other[0], self[1] - other[1])

    def __iadd__(self, other):
        self = self + other

        return self

    def __isub__(self, other):
        self = self - other

        return self
    
DirectedPoint = collections.namedtuple(
    "DirectedPoint", ["point", "ind"]
)

class Grid:
    DIRS = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]

    def __init__(self, input: list[str]):
        grid = [list(line) for line in input]
        self.grid = grid
        self.start, self.end = self._start_and_end()

    def __getitem__(self, point: Point) -> str:
        x = point[0]
        y = point[1]
    
        return self.grid[x][y]


    def find_path(self) -> tuple[int, int]:
        start = DirectedPoint(self.start, 1)
        (distance, parent) = self._dijkstra(start)

        best_distance = 10**9
        best_end_dir_point = None
        end_dir_points = [DirectedPoint(self.end, dir_ind) for dir_ind in range(len(Grid.DIRS))]
        for end_dir_point in end_dir_points:
            if end_dir_point in distance and distance[end_dir_point] < best_distance:
                best_distance = distance[end_dir_point]
                best_end_dir_point = end_dir_point

        points = self._traverse_paths(best_end_dir_point, parent)

        return (best_distance, points)

    def _get_neighbors(self, point: Point) -> Iterable[Point]:
        for dir in Grid.DIRS:
            to_point = point + dir
            if self.__getitem__(to_point) != "#":
                yield to_point

    def _dijkstra(self, source: DirectedPoint):
        distance = collections.defaultdict(lambda: 10**9)
        parent = collections.defaultdict(lambda: [])

        heap = []
        distance[source] = 0
        heapq.heappush(heap, (0, source))

        while heap:
            point_distance, current_dir_point_tuple = heapq.heappop(heap)
            current_dir_point = DirectedPoint(*current_dir_point_tuple)

            if point_distance != distance[current_dir_point]:
                continue

            for next_point in self._get_neighbors(current_dir_point.point):
                dir = next_point - current_dir_point.point
                dir_ind = Grid.DIRS.index(dir)
                next_dir_point = DirectedPoint(next_point, dir_ind)

                rotation_cost = self._calculate_rotation_cost(current_dir_point.ind, dir_ind)
                new_distance = distance[current_dir_point] + 1 + rotation_cost

                if distance[next_dir_point] >= new_distance:
                    if distance[next_dir_point] > new_distance:
                        distance[next_dir_point] = new_distance
                        parent[next_dir_point] = [current_dir_point]
                        heapq.heappush(heap, (distance[next_dir_point], next_dir_point))
                    else:
                        parent[next_dir_point].append(current_dir_point)

        return (distance, parent)

    def _traverse_paths(self, best: DirectedPoint, parent: dict[DirectedPoint, DirectedPoint]) -> int:
        unqiue_points = set()
        points_queue = deque()
        points_queue.append(best)

        while points_queue:
            current = points_queue.popleft()
            unqiue_points.add(current.point)
            for dir_point in parent[current]:
                unqiue_points.add(dir_point.point)
                points_queue.append(dir_point)

        return len(unqiue_points)

    def _calculate_rotation_cost(self, current_dir_ind: int, to_dir_ind: int) -> int:
        mi = min(current_dir_ind, to_dir_ind)
        ma = max(current_dir_ind, to_dir_ind)
        rotation_cost = min(ma - mi, len(Grid.DIRS) + mi - ma)
        rotation_cost = 1000 * rotation_cost
        
        return rotation_cost

    def _start_and_end(self) -> tuple[Point, Point]:
        start, end = None, None
        for i, row in enumerate(self.grid):
            for j, c in enumerate(row):
                if c == "S":
                    start = Point(i, j)
                elif c == "E":
                    end = Point(i, j)

        assert start and end

        return start, end

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()

def solve_part_1(input: list[str]):
    grid = Grid(input)

    return grid.find_path()[0]

def solve_part_2(input: list[str]):
    grid = Grid(input)

    return grid.find_path()[1]

def check():
    input_small_1 = read_and_parse("assets/day16/in_small_1.txt")

    part_1_answer = solve_part_1(input_small_1)
    assert part_1_answer == 7_036
    part_2_answer = solve_part_2(input_small_1)
    assert part_2_answer == 45

    input_small_2 = read_and_parse("assets/day16/in_small_2.txt")

    part_1_answer = solve_part_1(input_small_2)
    assert part_1_answer == 11_048
    part_2_answer = solve_part_2(input_small_2)
    assert part_2_answer == 64

def main():
    input = read_and_parse("assets/day16/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 88_416
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 442

if __name__ == "__main__":
    check()
    main()