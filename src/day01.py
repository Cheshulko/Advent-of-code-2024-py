#!/usr/bin/env python3

import collections

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()

def build_pairs(input: list[str]) -> list[tuple[int, int]]:
    values = [line.split(" ") for line in input]
    pairs = [tuple(map(int, filter(bool, value))) for value in values]

    return pairs

def solve_part_1(input: list[str]):
    pairs = build_pairs(input)
    first_list, second_list = map(sorted, map(list, zip(*pairs)))
    difference = sum(abs(x - y) for x, y in  zip(first_list, second_list))
    
    return difference

def solve_part_2(input: list[str]):
    pairs = build_pairs(input)
    frequency = collections.Counter([pair[1] for pair in pairs])
    similarity  = sum(pair[0] * frequency.get(pair[0], 0) for pair in pairs)

    return similarity

def check():
    input_small = read_and_parse("assets/day01/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 11
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 31

def main():
    input = read_and_parse("assets/day01/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 3_569_916
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 26_407_426

if __name__ == "__main__":
    check()
    main()