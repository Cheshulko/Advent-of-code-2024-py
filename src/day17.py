#!/usr/bin/env python3

from typing import Iterable, Optional

class Program:
    def __init__(self, registers: list[int], source: list[int]):
        self.registers = registers
        self.source = source
        self.ip = 0
        self.is_halt = False

    def run(self) -> Iterable[Optional[str]]:
        while not self.is_halt:            
            if self.ip >= len(self.source):
                self.is_halt = True

                return None
        
            match self.source[self.ip]:
                case 0: # adv
                    self.registers[0] = self.registers[0] >> self._get_combo()
                    self.ip += 2
                case 1: # bxl
                    self.registers[1] = self.registers[1] ^ self._get_literal()
                    self.ip += 2
                case 2: # bst
                    combo = self._get_combo()
                    self.registers[1] = combo - (combo >> 3 << 3)
                    self.ip += 2
                case 3: # jnz
                    if self.registers[0]:
                        self.ip = self._get_literal()
                    else:
                        self.ip += 2
                case 4: # bxc
                    self.registers[1] = self.registers[1] ^ self.registers[2]
                    self.ip += 2
                case 5: # out
                    combo = self._get_combo()
                    out = combo - (combo >> 3 << 3)
                    self.ip += 2

                    yield out
                case 6: # bdv
                    self.registers[1] = self.registers[0] >> self._get_combo()
                    self.ip += 2
                case 7: # cdv
                    self.registers[2] = self.registers[0] >> self._get_combo()
                    self.ip += 2

    def _get_literal(self) -> int:
        return self.source[self.ip + 1]

    def _get_combo(self) -> int:
        match self.source[self.ip + 1]:
            case 0 | 1 | 2 | 3:
                return self.source[self.ip + 1]
            case 4:
                return self.registers[0]
            case 5: 
                return self.registers[1]
            case 6: 
                return self.registers[2]

def read(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().split("\n\n")

def solve_part_1(input: list[str]):
    registers = list(
        int(line.split(": ")[1]) 
        for line in input[0].splitlines()
    )
    source = list(map(int, input[1].split(": ")[1].split(",")))
    result = list(Program(registers, source).run())

    return ",".join(map(str, result))

def solve_part_2(input: list[str]):
    registers = list(
        int(line.split(": ")[1]) 
        for line in input[0].splitlines()
    )
    source = list(map(int, input[1].split(": ")[1].split(",")))

    results = [0]
    for length in range(1, len(source) + 1):
        variants = []

        for result in results:
            for part in range(1 << 3):
                a = (1 << 3) * result + part
                registers[0] = a

                if list(Program(registers, source).run()) == source[-length:]:
                    variants.append(a)

        results = variants

    return min(results)

def check():
    input_small = read("assets/day17/in_small_1.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == "4,6,3,5,6,3,5,2,1,0"

    input_small = read("assets/day17/in_small_2.txt")
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 117_440

def main():
    input = read("assets/day17/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == "3,5,0,1,5,1,5,1,0"
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 107_413_700_225_434

if __name__ == "__main__":
    check()
    main()