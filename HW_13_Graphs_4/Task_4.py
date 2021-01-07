from collections import deque
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

    def push_flow_dfs(self, peak: int, drain: int, current_flow: int, used: List[int]) -> int:
        if peak == drain:
            return current_flow

        used[peak] = 1
        for adj_peak, edge_max_flow, edge_cur_flow, idx_adj_peak, _ in self._graph[peak]:
            if not used[adj_peak] and edge_cur_flow < edge_max_flow:
                next_flow = min(current_flow, edge_max_flow - edge_cur_flow)
                delta = self.push_flow_dfs(adj_peak, drain, next_flow, used)
                idx_peak = self._graph[adj_peak][idx_adj_peak][3]
                if delta > 0:
                    self._graph[adj_peak][idx_adj_peak][2] -= delta
                    self._graph[peak][idx_peak][2] += delta
                    return delta

        return 0

    def build_ways(self, source: int, drain: int) -> int:
        num_ways = 0
        while True:
            used = [self.DEFAULT_COLOR for _ in range(self.num_peaks)]
            delta = self.push_flow_dfs(source, drain, float('inf'), used)
            if delta > 0:
                num_ways += delta
            else:
                break

        return num_ways

    def _bfs(self, source: int) -> Tuple[List[int]]:
        used = [self.DEFAULT_COLOR for _ in range(self.num_peaks)]
        peak_queue = deque()
        peak_queue.append(source)
        way = [[None, None, None] for _ in range(self.num_peaks)]
        way[source] = [-1, -1, -1]
        used[source] = 1
        while len(peak_queue):
            peak = peak_queue.popleft()
            for adj_peak, edge_max_flow, edge_cur_flow, idx_adj_peak, _ in self._graph[peak]:
                if not used[adj_peak] and edge_cur_flow == 1:
                    used[adj_peak] = 1
                    peak_queue.append(adj_peak)
                    way[adj_peak] = [peak, adj_peak, idx_adj_peak]

        return way

    def get_way(self, source: int, drain: int) -> List[int]:
        way = self._bfs(source)
        peak_way = [drain]
        cur_peak = way[drain]
        if cur_peak[0] is None:
            return []

        while cur_peak[0] != -1:
            in_peak, out_peak, idx_out_peak = cur_peak
            idx_in_peak = self._graph[out_peak][idx_out_peak][3]
            self._graph[in_peak][idx_in_peak][2] -= 1
            cur_peak = way[in_peak]
            peak_way.append(in_peak)

        return peak_way[::-1]


def transform_input(inp: List[str]) -> Tuple[int, int]:
    return int(inp[0]) - 1, int(inp[1]) - 1


def main():
    number_peaks, number_edges, source, drain = map(int, sys.stdin.readline().split())
    source, drain = transform_input([source, drain])
    graph = WeightedGraph(number_peaks, number_edges, oriented=True)
    for _ in range(number_edges):
        b, e = transform_input(sys.stdin.readline().split())
        graph.add_edge(b, e, 1)

    graph.build_ways(source, drain)
    masha_way = graph.get_way(source, drain)
    petr_way = graph.get_way(source, drain)
    if masha_way and petr_way:
        print("YES")
        print(" ".join(map(lambda x: str(x + 1), masha_way)))
        print(" ".join(map(lambda x: str(x + 1), petr_way)))
    else:
        print("NO")


if __name__ == "__main__":
    threading.Thread(target=main).start()
