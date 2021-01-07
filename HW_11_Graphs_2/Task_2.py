from collections import namedtuple
from heapq import heapify, heappush, heappop
import sys
from typing import List, Tuple


class WeightedGraph:
    def __init__(self, num_peaks: int, num_edges: int, oriented: bool):
        self.num_edges = num_edges
        self.num_peaks = num_peaks
        self.oriented = oriented
        self._graph = [[] for _ in range(num_peaks)]
        self.DEFAULT_COLOR = 0
        self.weight_edge = namedtuple("weight_edge", ["adj_peak", "weight"])

    def add_edge(self, edge_out: int, edge_in: int, weight: int):
        weight_edge_in = self.weight_edge(edge_in, weight)
        self._graph[edge_out].append(weight_edge_in)
        if not self.oriented:
            weight_edge_out = self.weight_edge(edge_out, weight)
            self._graph[edge_in].append(weight_edge_out)

    def dijkstra(self, start_peak: int) -> List[int]:
        priority_queue = []
        heapify(priority_queue)
        heappush(priority_queue, (0, start_peak))
        distance = [float("inf")] * self.num_peaks
        used = [False] * self.num_peaks
        distance[start_peak] = 0
        for _ in range(self.num_peaks):
            if len(priority_queue) == 0:
                break

            next_dist, next_peak = heappop(priority_queue)
            while used[next_peak]:
                if len(priority_queue) == 0:
                    break

                next_dist, next_peak = heappop(priority_queue)

            for adj_peak, adj_peak_weight in self._graph[next_peak]:
                if not used[adj_peak]:
                    if distance[adj_peak] > distance[next_peak] + adj_peak_weight:
                        distance[adj_peak] = min(distance[adj_peak], distance[next_peak] + adj_peak_weight)
                        heappush(priority_queue, (distance[adj_peak], adj_peak))

            used[next_peak] = True

        return distance


def transform_input(inp: List[str]) -> Tuple[int, int, int]:
    return int(inp[0]) - 1, int(inp[1]) - 1, int(inp[2])


def main():
    number_peaks, number_edges = map(int, sys.stdin.readline().split())
    graph = WeightedGraph(number_peaks, number_edges, oriented=False)
    for _ in range(number_edges):
        b, e, weight = transform_input(sys.stdin.readline().split())
        graph.add_edge(b, e, weight)

    print(" ".join(map(str, graph.dijkstra(0))))


if __name__ == "__main__":
    main()
