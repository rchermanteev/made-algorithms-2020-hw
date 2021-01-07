from collections import deque
from math import log2, ceil
import sys
from typing import List, Tuple


class WeightedGraph:
    def __init__(self, num_peaks: int, num_edges: int, oriented: bool):
        self.num_edges = num_edges
        self.num_peaks = num_peaks
        self.oriented = oriented
        self._biggest_flow = -1
        self._graph = [[] for _ in range(num_peaks)]
        self.DEFAULT_COLOR = 0

    def add_edge(self, edge_out: int, edge_in: int, max_flow: int):
        self._biggest_flow = max(self._biggest_flow, max_flow)
        weight_edge_in = [edge_in, max_flow, 0, len(self._graph[edge_in]), 1]
        self._graph[edge_out].append(weight_edge_in)
        inv_edge_out = [edge_out, 0, 0, len(self._graph[edge_out]) - 1, 0]
        self._graph[edge_in].append(inv_edge_out)
        if not self.oriented:
            weight_edge_out = [edge_out, max_flow, 0, len(self._graph[edge_out]), 2]
            self._graph[edge_in].append(weight_edge_out)
            inv_edge_out = [edge_in, 0, 0, len(self._graph[edge_in]) - 1, 0]
            self._graph[edge_out].append(inv_edge_out)

    def push_flow_bfs(self, source: int, drain: int, current_flow: int, used: List[int], scale: int) -> int:
        peak_queue = deque()
        peak_queue.append(source)
        way = [[None, None, None] for _ in range(self.num_peaks)]
        way[source] = [-1, -1, -1]
        used[source] = 1
        while len(peak_queue):
            peak = peak_queue.popleft()
            for adj_peak, edge_max_flow, edge_cur_flow, idx_adj_peak, _ in self._graph[peak]:
                if not used[adj_peak] and edge_cur_flow + scale < edge_max_flow:
                    current_flow = min(current_flow, edge_max_flow - edge_cur_flow)
                    used[adj_peak] = 1
                    peak_queue.append(adj_peak)
                    way[adj_peak] = [peak, adj_peak, idx_adj_peak]

        if way[drain][0] is None:
            return 0

        if current_flow > 0:
            cur_peak = way[-1]

            while cur_peak[0] != -1:
                in_peak, out_peak, idx_out_peak = cur_peak
                idx_in_peak = self._graph[out_peak][idx_out_peak][3]
                self._graph[in_peak][idx_in_peak][2] += current_flow
                self._graph[out_peak][idx_out_peak][2] -= current_flow
                cur_peak = way[in_peak]

        return current_flow

    def get_max_flow(self, source: int, drain: int) -> int:
        answer = 0
        scale = 10 ** ceil(log2(self._biggest_flow))
        while scale > 0:
            while True:
                used = [self.DEFAULT_COLOR for _ in range(self.num_peaks)]
                delta = self.push_flow_bfs(source, drain, float('inf'), used, scale)

                if delta > 0:
                    answer += delta
                else:
                    break

            scale /= 100

        return answer


def transform_input(inp: List[str]) -> Tuple[int, int, int]:
    return int(inp[0]) - 1, int(inp[1]) - 1, int(inp[2])


def inverted_transform_input(inp: List[str]) -> Tuple[int, int, int]:
    return int(inp[0]) + 1, int(inp[1]) + 1, int(inp[2])


def main():
    number_peaks = int(sys.stdin.readline())
    number_edges = int(sys.stdin.readline())
    graph = WeightedGraph(number_peaks, number_edges, oriented=False)
    base_state = []
    for _ in range(number_edges):
        b, e, weight = transform_input(sys.stdin.readline().split())
        base_state.append([b, e, 0])
        graph.add_edge(b, e, weight)

    print(graph.get_max_flow(0, number_peaks - 1))

    for peak in range(number_peaks):
        for adj_peak, _, edge_cur_flow, _, is_original in graph._graph[peak]:
            if is_original:
                for i in range(len(base_state)):
                    if base_state[i][2]:
                        continue

                    if is_original == 1:
                        if base_state[i][0] == peak and base_state[i][1] == adj_peak:
                            base_state[i][2] = edge_cur_flow
                            break

                    if is_original == 2:
                        if base_state[i][0] == adj_peak and base_state[i][1] == peak:
                            base_state[i][2] = -edge_cur_flow
                            break

    base_state_with_flow = map(inverted_transform_input, base_state)
    for el in base_state_with_flow:
        print(el[2])


if __name__ == "__main__":
    main()
