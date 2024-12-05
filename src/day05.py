#!/usr/bin/env python3

Rules = dict[int, list[int]]
Update = list[int]
Updates = list[Update]

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().split("\n\n")
    
def parse_rules(input: str) -> Rules:
    lines = input.splitlines()

    rules = {}
    for line in lines:
        u, v = map(int, line.split("|"))
        rules.setdefault(u, []).append(v)

    return rules

def parse_updates(input: str) -> Updates:
    lines = input.splitlines()

    return [list(map(int, line.split(","))) for line in lines]

def dfs(ind: int, rules: Rules, update: Update, used: list[bool], ans: list[int]):
    used[ind] = True

    for to in rules.get(update[ind], []):
        if to in update:
            to_ind = update.index(to)
            if not used[to_ind]:
                dfs(to_ind, rules, update, used, ans)

    ans.append(update[ind])

def topological_sort(update: Update, rules: Rules) -> list[int]:
    ans = []
    n = len(update)
    used = [False] * n

    for ind in range(n):
        if not used[ind]:
            dfs(ind, rules, update, used, ans)

    ans.reverse()

    return ans


def solve_part_1(input: list[str]):
    rules = parse_rules(input[0])
    updates = parse_updates(input[1])

    ans = 0
    for update in updates:
        fixed_update = topological_sort(update, rules)
        if fixed_update == update:
            ans += fixed_update[len(fixed_update) // 2]

    return ans

def solve_part_2(input: list[str]):
    rules = parse_rules(input[0])
    updates = parse_updates(input[1])

    ans = 0
    for update in updates:
        fixed_update = topological_sort(update, rules)
        if fixed_update != update:
            ans += fixed_update[len(fixed_update) // 2]

    return ans

def check():
    input_small = read_and_parse("assets/day05/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 143
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == 123

def main():
    input = read_and_parse("assets/day05/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 5_268
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == 5_799

if __name__ == "__main__":
    check()
    main()