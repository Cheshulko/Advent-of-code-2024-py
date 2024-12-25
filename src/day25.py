#!/usr/bin/env python3

from itertools import product

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().split("\n\n")

def solve_part_1(input: list[str]):
    locks = []
    keys = []

    for scheme in input:
        rows = scheme.splitlines()
        kit = [-1] * len(rows[0])
        for row in rows:
            for j, c in enumerate(row):
                kit[j] += c == "#"

        if all(map(lambda c: c == "#", rows[0])):
            locks.append((len(rows), kit))
        else:
            keys.append((len(rows), kit))

    ans = 0
    for (lock, key) in product(locks, keys):
        assert lock[0] == key[0]

        ans += all(map(
            lambda p: p[0] + p[1] + 2 <= lock[0], 
            zip(lock[1], key[1])
        ))

    return ans

def check():
    input_small = read_and_parse("assets/day25/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 3

def main():
    input = read_and_parse("assets/day25/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 3_439

if __name__ == "__main__":
    check()
    main()