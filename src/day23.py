#!/usr/bin/env python3

from collections import defaultdict

class Graph:
    def __init__(self, input: list[str]):
        adj = defaultdict(list)
        unique = set()
        connected = set()

        for pair in input:
            v, u, = pair.split("-")
            adj[v].append(u)
            adj[u].append(v)
            connected.add((u, v))
            connected.add((v, u))

            unique.add(u)
            unique.add(v) 

        self.adj = adj
        self.unique = unique
        self.connected = connected

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()
    
def solve_part_1(input: list[str]):
    graph = Graph(input)

    cliques_2 = graph.connected
    cliques_3 = set()
    
    for next in graph.unique:
        if not next.startswith("t"):
            continue

        for clique in cliques_2:
            if next in clique:
                continue
            if (next, clique[0]) in graph.connected and (
                (next, clique[1]) in graph.connected
            ):
                cliques_3.add(tuple(sorted((*clique, next))))

    return len(cliques_3)

def solve_part_2(input: list[str]):
    graph = Graph(input)

    cliques = graph.connected
    while len(cliques) > 1:
        cliques_ = set()
        for clique in cliques:
            for next in graph.unique:
                if next in clique:
                    continue

                if all(
                    (vertex, next) in graph.connected 
                    for vertex in clique
                ):
                    cliques_.add(tuple(sorted([*clique, next]))) 

        cliques = cliques_

    assert len(cliques) == 1
    unique = list(cliques)[0]
    ans = ",".join(list(unique))
    
    return ans

def check():
    input_small = read_and_parse("assets/day23/in_small.txt")

    part_1_answer = solve_part_1(input_small)
    assert part_1_answer == 7
    part_2_answer = solve_part_2(input_small)
    assert part_2_answer == "co,de,ka,ta"

def main():
    input = read_and_parse("assets/day23/in.txt")
    
    part_1_answer = solve_part_1(input)
    print(f"Part 1: {part_1_answer}")
    assert part_1_answer == 1_119
    part_2_answer = solve_part_2(input)
    print(f"Part 2: {part_2_answer}")
    assert part_2_answer == "av,fr,gj,hk,ii,je,jo,lq,ny,qd,uq,wq,xc"

if __name__ == "__main__":
    check()    
    main()