#!/usr/bin/env python3

from collections import deque

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()

def bisect_right_deque(deque, x):
    low, high = 0, len(deque)
    while low < high:
        mid = (low + high) // 2
        if deque[mid] <= x:
            low = mid + 1
        else:
            high = mid

    return low

def checksum(index: int, value: int) -> int:
    return (index + index + value - 1) * value // 2

def solve_part_1(input: list[str]):
    assert len(input) == 1
    input = list(map(int, input[0]))

    ans, index = 0, 0
    left, right = 0, len(input) - 1
    while True:
        while left < len(input) and input[left] == 0:
            left += 1

        while (right >= 0 and input[right] == 0) or right % 2:
            right -= 1

        if left > right:
            break

        if left % 2:
            value = min(input[left], input[right])
            ans += checksum(index, value) * right // 2
            index += value

            input[left] -= value
            input[right] -= value 
        else:
            value = input[left]
            ans += checksum(index, value) * left // 2
            index += value
            
            left += 1  

    return ans

def solve_part_2(input: list[str]):
    assert len(input) == 1
    input = list(map(int, input[0]))

    n = len(input)
    filled = [[] for _ in range(n)]
    moved = [False for _ in range(n)]
    free_spaces = [deque() for _ in range(10)]

    for ind, value in enumerate(input):
        if ind % 2:
            free_spaces[value].append(ind)

    for ind, value in enumerate(reversed(input)):
        ind = n - 1 - ind

        for space in range(10):
            while len(free_spaces[space]) and free_spaces[space][0] > ind:
                free_spaces[space].popleft()

        if not ind % 2:
            leftmost_free_ind = None
            leftmost_free_value = None 
            for di, free_inds in enumerate(free_spaces[value:]):
                for free_ind in free_inds:
                    if not leftmost_free_ind or free_ind < leftmost_free_ind:
                        leftmost_free_ind = free_ind
                        leftmost_free_value = di + value

            if leftmost_free_ind:
                moved[ind] = True
                free_spaces[leftmost_free_value].popleft()
                filled[leftmost_free_ind].append((value, ind // 2))
                leftmost_free_value = leftmost_free_value - value

                index = bisect_right_deque(free_spaces[leftmost_free_value], leftmost_free_ind)
                free_spaces[leftmost_free_value].insert(index, leftmost_free_ind)

    ans = 0
    index = 0
    for ind in range(n):
        if not ind % 2:
            if not moved[ind]:
                ans += checksum(index, input[ind]) * ind // 2
        elif len(filled[ind]) > 0:
            filled_index = index
            for filled_cnt, id in filled[ind]:
                ans += checksum(filled_index, filled_cnt) * id
                filled_index += filled_cnt
        
        index += input[ind]

    return ans    

def check():
    input_small = read_and_parse("assets/day09/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 1_928
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 2_858

def main():
    input = read_and_parse("assets/day09/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 6_346_871_685_398
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 6_373_055_193_464

if __name__ == "__main__":
    check()
    main()