#!/usr/bin/env python3

import math
import re

re_button_a = r"Button A: X([\+|\-]\d+), Y([\+|\-]\d+)"
re_button_b = r"Button B: X([\+|\-]\d+), Y([\+|\-]\d+)"
re_price = r"Prize: X=(\d+), Y=(\d+)"

price_a = 3
price_b = 1

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().split("\n\n")

def lcm(a: int, b: int) -> int:
    return abs(a * b) // math.gcd(a, b)

def solve(input: list[str], price_boost = 0) -> int:
    ans = 0
    for game in input:
        lines = game.splitlines()

        button_a = re.findall(re_button_a, lines[0])[0]
        button_a = list(map(int, button_a))

        button_b = re.findall(re_button_b, lines[1])[0]
        button_b = list(map(int, button_b))

        prize = re.findall(re_price, lines[2])[0]
        prize = list(map(lambda p: int(p) + price_boost, prize))

        b_lcm = lcm(button_b[0], button_b[1])
        cx = b_lcm // button_b[0]
        cy = b_lcm // button_b[1]

        if button_a[1] * cy - button_a[0] * cx == 0:
            ''' Invertible matrix 

                For such case we need to solve simple linear programming problem:
                    dx_a * pressed_a + dx_b * pressed_b == y
                    price_a * pressed_a + price_b * pressed_b -> min
                Without loss of generality, assume that `a` button is better than `b`:
                    dx_a / price_a > dx_b / price_b
                For this case can be proven that pressed_b is limited to [0..max(dx_a, dx_b)]
                With task constraints we can easily brute force pressed_b value

                Tests don't have this case so skipping it
            '''
            assert False
        else:
            button_a[1] = button_a[1] * cy - button_a[0] * cx
            button_b[1] = button_b[1] * cy - button_b[0] * cx
            assert button_b[1] == 0
            prize[1] = prize[1] * cy - prize[0] * cx

            if prize[1] % button_a[1] == 0:
                pressed_a = prize[1] // button_a[1]
                
                prize[0] = prize[0] - button_a[0] * pressed_a
                if prize[0] % button_b[0] == 0:
                    pressed_b = prize[0] // button_b[0]

                    if pressed_a >= 0 and pressed_b >= 0:
                        ans += price_a * pressed_a + price_b * pressed_b

    return ans

def solve_part_1(input: list[str]):
    return solve(input)

def solve_part_2(input: list[str]):
    return solve(input, 10000000000000)

def check():
    input_small = read_and_parse("assets/day13/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 480
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 875_318_608_908

def main():
    input = read_and_parse("assets/day13/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 31_589
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 98_080_815_200_063

if __name__ == "__main__":
    check()
    main()