#!/usr/bin/env python3

from typing import Optional
from collections import defaultdict

Sequence = tuple[int, int, int, int]

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()

def window_iterate(list, window_size):
    for i in range(len(list) - window_size + 1):
        yield tuple(list[i:i + window_size])

def simulate(seed: int, unique_sequences: Optional[dict[Sequence, int]] = None) -> int:
    secret = seed

    changes = [None]
    prices = [seed % 10]
    for _ in range(2000):
        secret ^= secret * 64
        secret %= 16777216

        secret ^= secret // 32
        secret %= 16777216

        secret ^= secret * 2048
        secret %= 16777216

        changes.append(secret % 10 - seed % 10)
        prices.append(secret % 10)

        seed = secret

    if unique_sequences is not None:
        sequences = set()
        for ind, sequence in enumerate(window_iterate(changes[1:], 4)):
            if sequence not in sequences:
                unique_sequences[sequence] += prices[ind + 4]
                sequences.add(sequence)

    return secret

def solve_part_1(input: list[str]):
    return sum(simulate(int(seed)) for seed in input)

def solve_part_2(input: list[str]):
    unique_sequences = defaultdict(int)

    for seed in input:
        _ = simulate(int(seed), unique_sequences)

    return max(unique_sequences.values())

def check():
    input_small = read_and_parse("assets/day22/in_small_1.txt")
    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 37_327_623

    input_small = read_and_parse("assets/day22/in_small_2.txt")
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 23

def main():
    input = read_and_parse("assets/day22/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 16_999_668_565
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 1_898

if __name__ == "__main__":
    check()
    main()