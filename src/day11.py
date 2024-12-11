#!/usr/bin/env python3

import math

Stone = tuple[int, int]

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()

def next_stones(stone: int) -> list[int]:
    if stone == 0:
        return [stone + 1]
    else:
        digit_count = math.floor(math.log10(stone)) + 1
        if digit_count % 2 == 0:
            pow = 10 ** (digit_count // 2)
            second, first = stone % pow, stone // pow
            
            return [first, second]
        else:
            return [stone * 2024]

def solve_for_stone(stone: Stone, dp: dict[Stone, int]) -> int:
    if stone in dp:
        return dp[stone]
    
    if stone[1] == 0:
        return 1
    
    ans = sum(
        solve_for_stone((num, stone[1] - 1), dp) 
        for num in next_stones(stone[0])
    )

    dp[stone] = ans

    return ans

def solve(input: list[str], blinks: int) -> int:
    assert len(input) == 1
    input = input[0]

    dp = {}
    stones = [(stone, blinks) for stone in map(int, input.split(" "))]
    ans = sum(
        solve_for_stone(stone, dp) 
        for stone in stones
    )

    return ans

def solve_part_1(input: list[str]):
    return solve(input, 25)

def solve_part_2(input: list[str]):
    return solve(input, 75)

def check():
    input_small = read_and_parse("assets/day11/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 5_5312
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 65_601_038_650_482

def main():
    input = read_and_parse("assets/day11/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 200_446
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 238_317_474_993_392

if __name__ == "__main__":
    check()
    main()