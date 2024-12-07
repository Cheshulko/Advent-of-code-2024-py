#!/usr/bin/env python3

import math
import itertools
from enum import Enum

class Operation(Enum):
    Mul = 1
    Add = 2
    Concat = 3

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()
    
def parse_equation(line: str) -> tuple[int, list[int]]:
    target, numbers = tuple(map(str.strip, line.split(":")))
    target = int(target)
    numbers = list(map(int, numbers.split(" ")))

    return target, numbers

def solve_equation(target: int, numbers: list[int], operations: list[Operation]) -> int:
    numbers_len = len(numbers)
    results = [[] for _ in range(numbers_len)]
    results[0].append(numbers[0])

    for ind, number in enumerate(numbers[1:]):
        for result in results[ind]:
            for operation in operations:
                match operation:
                    case Operation.Mul:
                        results[ind + 1].append(result * number)
                    case Operation.Add:
                        results[ind + 1].append(result + number)
                    case Operation.Concat:
                        digit_count = math.floor(math.log10(number)) + 1
                        results[ind + 1].append(result * math.pow(10, digit_count) + number)

    if target in results[numbers_len - 1]:
        return target
    else:
        return 0

def solve_part_1(input: list[str]) -> int:
    ans = sum(itertools.starmap(
        lambda target, numbers: solve_equation(target, numbers, [
            Operation.Add, 
            Operation.Mul
        ]), 
        map(parse_equation, input)
    ))

    return ans

def solve_part_2(input: list[str]):
    ans = sum(itertools.starmap(
        lambda target, numbers: solve_equation(target, numbers, [
            Operation.Add, 
            Operation.Mul, 
            Operation.Concat
        ]), 
        map(parse_equation, input)
    ))

    return ans

def check():
    input_small = read_and_parse("assets/day07/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 3_749
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 11_387

def main():
    input = read_and_parse("assets/day07/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 1_298_300_076_754
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 248_427_118_972_289

if __name__ == "__main__":
    check()
    main()