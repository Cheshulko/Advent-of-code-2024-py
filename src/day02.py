#!/usr/bin/env python3

import operator
from typing import Iterable

Level = list[int]

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()

def read_levels(input: list[str]) -> list[Level]:
    return [list(map(int, line.split(" "))) for line in input]

def is_monotonic(level: Level, min_difference, max_difference) -> bool:
    neighbors = zip(level[:-1], level[1:])
    differences = [operator.sub(*pair) for pair in neighbors]

    return all(map(
        lambda difference: min_difference <= difference <= max_difference, 
        differences
    ))

def is_increasing(level: Level, min_difference=1, max_difference=3) -> bool:
    return is_monotonic(level, min_difference, max_difference)

def is_decreasing(level: Level, min_difference=-3, max_difference=-1) -> bool:
    return is_monotonic(level, min_difference, max_difference)

def is_level_monotonic(level: Level) -> bool:
    return is_increasing(level) or is_decreasing(level)

def tolerate_level(level: Level) -> Iterable[list[Level]]:
    for tolerate_index in range(len(level)):
        yield level[:tolerate_index] + level[tolerate_index + 1:]

def solve_part_1(input: list[str]) -> int:
    levels = read_levels(input)
    monotonic_levels = list(filter(is_level_monotonic, levels))

    return len(monotonic_levels)

def solve_part_2(input: list[str]) -> int:
    levels = read_levels(input)

    monotonic_levels = list(filter(
        lambda level: 
            any(map(is_level_monotonic, tolerate_level(level))), 
            levels
    ))

    return len(monotonic_levels)

def check():
    input_small = read_and_parse("assets/day02/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 2
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 4

def main():
    input = read_and_parse("assets/day02/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 390
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 439

if __name__ == "__main__":
    check()
    main()