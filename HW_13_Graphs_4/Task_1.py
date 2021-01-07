import sys
import threading
from typing import List, Tuple

sys.setrecursionlimit(10 ** 9)
threading.stack_size(2 ** 26)


class WeightedGraph:
    def __init__(self, num_peaks: int, num_edges: int, oriented: bool):
        self.num_edges = num_edges
        self.num_peaks = num_peaks
        self.oriented = oriented
        self._graph = [[] for _ in range(num_peaks)]
        self.DEFAULT_COLOR = 0

    def add_edge(self, edge_out: int, edge_in: int, max_flow: int):
        weight_edge_in = [edge_in, max_flow, 0, len(self._graph[edge_in])]
        self._graph[edge_out].append(weight_edge_in)
        inv_edge_out = [edge_out, 0, 0, len(self._graph[edge_out]) - 1]
        self._graph[edge_in].append(inv_edge_out)
        if not self.oriented:
            weight_edge_out = [edge_out, max_flow, 0, len(self._graph[edge_out])]
            self._graph[edge_in].append(weight_edge_out)
            inv_edge_out = [edge_in, 0, 0, len(self._graph[edge_in]) - 1]
            self._graph[edge_out].append(inv_edge_out)

    def push_flow(self, peak: int, drain: int, current_flow: int, used: List[int]) -> int:
        if peak == drain:
            return current_flow

        used[peak] = 1
        for adj_peak, edge_max_flow, edge_cur_flow, idx_adj_peak in self._graph[peak]:
            if not used[adj_peak] and edge_cur_flow < edge_max_flow:
                next_flow = min(current_flow, edge_max_flow - edge_cur_flow)
                delta = self.push_flow(adj_peak, drain, next_flow, used)
                idx_peak = self._graph[adj_peak][idx_adj_peak][3]
                if delta > 0:
                    self._graph[adj_peak][idx_adj_peak][2] -= delta
                    self._graph[peak][idx_peak][2] += delta
                    return delta

        return 0

    def get_max_flow(self, source: int, drain: int) -> int:
        answer = 0
        while True:
            used = [self.DEFAULT_COLOR for _ in range(self.num_peaks)]
            delta = self.push_flow(source, drain, float('inf'), used)
            if delta > 0:
                answer += delta
            else:
                break

        return answer


def transform_input(inp: List[str]) -> Tuple[int, int, int]:
    return int(inp[0]) - 1, int(inp[1]) - 1, int(inp[2])


def main():
    number_peaks = int(sys.stdin.readline())
    number_edges = int(sys.stdin.readline())
    graph = WeightedGraph(number_peaks, number_edges, oriented=False)
    for _ in range(number_edges):
        b, e, weight = transform_input(sys.stdin.readline().split())
        graph.add_edge(b, e, weight)

    print(graph.get_max_flow(0, number_peaks - 1))


if __name__ == "__main__":
    threading.Thread(target=main).start()
