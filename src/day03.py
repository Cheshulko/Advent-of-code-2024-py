#!/usr/bin/env python3

import collections
import operator
import re

State = collections.namedtuple(
    "State", ["reg", "accumulate"]
)

Operation = collections.namedtuple(
    "Operation", ["mul", "do", "do_not"]
)

re_mul = r"mul\((\d{1,3}),(\d{1,3})\)"

re_operations = r"(mul\(\d{1,3},\d{1,3}\))|(do\(\))|(don't\(\))"

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()

def calculate_sum(line: str) -> int:
    pairs = re.findall(re_mul, line)
    result = sum(map(lambda pair: operator.mul(*map(int, pair)), pairs))

    return result

def apply_operation(state: State, operation: Operation) -> State:
    if operation.mul:
        return State(
            reg = state.reg,
            accumulate = state.accumulate + state.reg * calculate_sum(operation.mul)
        )
    elif operation.do:
        return State(
            reg = 1,
            accumulate = state.accumulate
        )
    else:
        return State(
            reg = 0,
            accumulate = state.accumulate
        )

def solve_part_1(input: list[str]):
    result = sum(map(calculate_sum, input))

    return result

def solve_part_2(input: list[str]):
    state = State(reg = 1, accumulate = 0)

    for line in input:
        matches = re.findall(re_operations, line)

        for match in matches:
            state = apply_operation(state, Operation(*match))

    return state.accumulate

def check():
    input_small = read_and_parse("assets/day03/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 161
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 48

def main():
    input = read_and_parse("assets/day03/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 156_388_521
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 75_920_122

if __name__ == "__main__":
    check()
    main()