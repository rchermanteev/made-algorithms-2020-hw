import sys
import threading
from collections import defaultdict
from typing import Dict

sys.setrecursionlimit(10 ** 9)
threading.stack_size(2 ** 26)


class Graph:
    def __init__(self, num_peaks, num_edges, oriented):
        self.num_edges = num_edges
        self.num_peaks = num_peaks
        self.oriented = oriented
        self._graph = defaultdict(list)
        self.DEFAULT_COLOR = 0

    def add_edge(self, edge_out, edge_in):
        self._graph[edge_out].append(edge_in)
        if not self.oriented:
            self._graph[edge_in].append(edge_out)

    def _dfs(self, peak: str, ways: Dict[str, int], len_way: int):
        ways[peak] = len_way
        for adj_peak in self._graph[peak]:
            if ways[adj_peak] == self.DEFAULT_COLOR:
                self._dfs(adj_peak, ways, len_way + 1)

    def get_longest_path(self, base_peak: str):
        used = dict(zip(self._graph.keys(), [self.DEFAULT_COLOR for _ in range(len(self._graph.keys()))]))
        self._dfs(base_peak, used, 1)

        return max(used.values())


_ROOT_PEAK = "polycarp"


def main():
    num_reposts = int(sys.stdin.readline())
    graph = Graph(num_reposts, num_reposts, oriented=False)
    for _ in range(num_reposts):
        customer, _, owner = map(lambda x: x.lower(), sys.stdin.readline().split())
        graph.add_edge(owner, customer)

    print(graph.get_longest_path(_ROOT_PEAK))


if __name__ == "__main__":
    threading.Thread(target=main).start()
