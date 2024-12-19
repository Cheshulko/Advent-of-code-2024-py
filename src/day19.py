#!/usr/bin/env python3

import functools

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().split("\n\n")

def count_ways(towel: str, patterns: list[str]) -> int:
    @functools.cache
    def dp(towel: str) -> int:
        if not towel:
            return 1

        return sum(
            dp(towel[len(pattern):]) 
            for pattern in patterns 
            if towel.startswith(pattern)
        )
    
    return dp(towel)

def solve_part_1(input: list[str]):
    patterns = input[0].split(", ")
    towels = input[1].splitlines()

    return sum(map(
        lambda towel: count_ways(towel, patterns) > 0, 
        towels
    ))

def solve_part_2(input: list[str]):
    patterns = input[0].split(", ")
    towels = input[1].splitlines()

    return sum(map(
        lambda towel: count_ways(towel, patterns), 
        towels
    ))

def check():
    input_small = read_and_parse("assets/day19/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 6
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 16

def main():
    input = read_and_parse("assets/day19/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 302
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 771_745_460_576_799

if __name__ == "__main__":
    check()
    main()