from collections import namedtuple
import sys
from typing import List, Tuple


class DisjointSetUnion:
    def __init__(self, num_elements: int):
        self.forest = [i for i in range(num_elements)]
        self.rang = [0 for _ in range(num_elements)]

    def get(self, x: int) -> int:
        if self.forest[x] != x:
            self.forest[x] = self.get(self.forest[x])

        return self.forest[x]

    def join(self, x: int, y: int):
        x = self.get(x)
        y = self.get(y)
        if x == y:
            return

        if self.rang[x] > self.rang[y]:
            x, y = y, x

        if self.rang[x] == self.rang[y]:
            self.rang[y] += 1

        self.forest[x] = y


class WeightedGraph:
    def __init__(self, num_peaks: int, num_edges: int, oriented: bool):
        self.num_edges = num_edges
        self.num_peaks = num_peaks
        self.oriented = oriented
        self.dsu = DisjointSetUnion(num_peaks)
        self._graph = []
        self.weight_edge = namedtuple("weight_edge", ["first_peak", "second_peak", "weight"])

    def add_edge(self, edge_out: int, edge_in: int, weight: int):
        weight_edge_in = self.weight_edge(edge_in, edge_out, weight)
        self._graph.append(weight_edge_in)

    def get_minimum_spanning_tree_weight(self) -> float:
        weight = 0
        sorted_by_weight_graph = sorted(self._graph, key=lambda x: x[2])
        for fir_peak, sec_peak, edge_weight in sorted_by_weight_graph:
            if self.dsu.get(fir_peak) != self.dsu.get(sec_peak):
                weight += edge_weight
                self.dsu.join(fir_peak, sec_peak)

        return weight


def transform_input(inp: List[str]) -> Tuple[int, int, int]:
    return int(inp[0]) - 1, int(inp[1]) - 1, int(inp[2])


def main():
    number_peaks, number_edges = map(int, sys.stdin.readline().split())
    graph = WeightedGraph(number_peaks, number_edges, oriented=False)
    for _ in range(number_edges):
        b, e, weight = transform_input(sys.stdin.readline().split())
        graph.add_edge(b, e, weight)

    print(graph.get_minimum_spanning_tree_weight())


if __name__ == "__main__":
    main()
