#!/usr/bin/env python3

import functools
from enum import Enum
from typing import Iterable
from collections import deque, defaultdict

class Operation(Enum):
    AND = 1
    XOR = 2
    OR = 3

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().split("\n\n")

def get_num(start: str, wires: dict[str, int]) -> int:
    interested = [wire for wire in wires.items() if wire[0].startswith(start)]
    interested.sort()

    number = functools.reduce(
        lambda state, wire: (state[0] + wire[1] * state[1], state[1] << 1), 
        interested, (0, 1)
    )
    
    return number[0]

def solve(input: list[str]) -> tuple[
    dict[str, int], 
    dict[tuple[str, str], list[tuple[Operation, str]]]
]:
    wires = dict()

    for initial in input[0].splitlines():
        wire, value = initial.split(": ")
        wires[wire] = int(value)

    rules = []
    rules_ = defaultdict(list)
    for rule in input[1].splitlines():
        input, output = rule.split(" -> ")
        if output not in wires:
            wires[output] = None

        first, op, second = input.split(" ")
        if first not in wires:
            wires[first] = None
        if second not in wires:
            wires[second] = None
        match op:
            case "AND":
                rules.append((Operation.AND, first, second, output))
                rules_[(first, second)].append((Operation.AND, output))
                rules_[(second, first)].append((Operation.AND, output))
            case "XOR":
                rules.append((Operation.XOR, first, second, output))
                rules_[(first, second)].append((Operation.XOR, output))
                rules_[(second, first)].append((Operation.XOR, output))
            case "OR":
                rules.append((Operation.OR, first, second, output))
                rules_[(first, second)].append((Operation.OR, output))
                rules_[(second, first)].append((Operation.OR, output))

    q = deque(wire for wire in wires.items() if wire[1] is not None)
    while q:
        wire_1, value = q.popleft()
        assert value is not None
        for wire_2 in wires.keys():
            if (wires[wire_2] is not None) and ((wire_1, wire_2) in rules_):
                for op, wire_3 in rules_[(wire_1, wire_2)]:
                    if wires[wire_3] is None:
                        value_3 = 0
                        match op:
                            case Operation.AND:
                                value_3 = value & wires[wire_2]
                            case Operation.XOR:
                                value_3 = value ^ wires[wire_2]
                            case Operation.OR:
                                value_3 = value | wires[wire_2]
                        wires[wire_3] = value_3
                        q.append((wire_3, value_3))
        
    return wires, rules_

def SHITTTY_part_2_solve(rules: dict[tuple[str, str], list[tuple[Operation, str]]]) -> Iterable[str]:
    current = None
    bit = 0

    rules_unrolled = defaultdict(lambda: None)
    for rule, items in rules.items():
        for item in items:
            rules_unrolled[(*rule, item[0])] = item[1]

    while bit < 45:
        x_wire = f'x{bit:02d}'
        y_wire = f'y{bit:02d}'
        z_wire = f'z{bit:02d}'

        if bit == 0:
            current = rules_unrolled[(x_wire, y_wire, Operation.AND)]
        else:
            x_xor_y = rules_unrolled[(x_wire, y_wire, Operation.XOR)]
            x_and_y = rules_unrolled[(x_wire, y_wire, Operation.AND)]

            cin_x_xor_y = rules_unrolled[(x_xor_y, current, Operation.XOR)]
            if cin_x_xor_y is None:
                yield x_xor_y
                yield x_and_y

                z_wire = rules_unrolled[(x_wire, y_wire, Operation.XOR)]
                rules_unrolled[(y_wire, x_wire, Operation.XOR)] = rules_unrolled[(x_wire, y_wire, Operation.XOR)] = rules_unrolled[(x_wire, y_wire, Operation.AND)]
                rules_unrolled[(y_wire, x_wire, Operation.AND)] = rules_unrolled[(x_wire, y_wire, Operation.AND)] = z_wire
                
                bit = 0
                continue
            
            if cin_x_xor_y != z_wire:
                yield cin_x_xor_y
                yield z_wire

                z_wire = (z_wire_rule1, z_wire_rule2) = [rule for (rule, z) in rules_unrolled.items() if z == z_wire]
                z_wire = rules_unrolled[(x_xor_y, current, Operation.XOR)]
                rules_unrolled[(current, x_xor_y, Operation.XOR)]= rules_unrolled[(x_xor_y, current, Operation.XOR)] = rules_unrolled[z_wire_rule1]
                rules_unrolled[z_wire_rule1] = z_wire
                rules_unrolled[z_wire_rule2] = z_wire
                
                bit = 0
                continue

            cin_x_and_y = rules_unrolled[(x_xor_y, current, Operation.AND)]
            carry_wire = rules_unrolled[(x_and_y, cin_x_and_y, Operation.OR)]
            current = carry_wire
        
        bit += 1

def solve_part_1(input: list[str]):
    (wires, _) = solve(input)

    return get_num("z", wires)

def solve_part_2(input: list[str]):
    (_, rules) = solve(input)

    return ",".join(sorted(SHITTTY_part_2_solve(rules)))

def check():
    input_small_1 = read_and_parse("assets/day24/in_small_1.txt")
    input_small_2 = read_and_parse("assets/day24/in_small_2.txt")

    part_1_answer = solve_part_1(input_small_1)
    assert part_1_answer == 4
    part_1_answer = solve_part_1(input_small_2)
    assert part_1_answer == 2024

def main():
    input = read_and_parse("assets/day24/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 55_114_892_239_566
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == "cdj,dhm,gfm,mrb,qjd,z08,z16,z32"

if __name__ == "__main__":
    check()
    main()