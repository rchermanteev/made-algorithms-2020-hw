from collections import namedtuple
from math import sqrt
from heapq import heapify, heappush, heappop
import sys
from typing import List, Tuple


class FullGraph:
    def __init__(self, num_peaks: int, oriented: bool):
        self.num_peaks = num_peaks
        self.oriented = oriented
        self._graph = []
        self.DEFAULT_COLOR = 0

    def add_peak(self, peak: Tuple[int, int]):
        self._graph.append(peak)

    @staticmethod
    def _get_weight(first_peak: Tuple[int, int], second_peak: Tuple[int, int]):
        return sqrt((first_peak[0] - second_peak[0]) ** 2 + (first_peak[1] - second_peak[1]) ** 2)

    def get_minimum_spanning_tree_weight(self, start_peak_idx: int) -> float:
        priority_queue = []
        heapify(priority_queue)
        heappush(priority_queue, (0, start_peak_idx))
        distance = [float("inf")] * self.num_peaks
        used = [False] * self.num_peaks
        distance[start_peak_idx] = 0
        for _ in range(self.num_peaks):
            if len(priority_queue) == 0:
                break

            next_dist, next_peak_idx = heappop(priority_queue)
            while used[next_peak_idx]:
                if len(priority_queue) == 0:
                    break

                next_dist, next_peak_idx = heappop(priority_queue)

            for adj_peak_idx in range(self.num_peaks):
                if adj_peak_idx != next_peak_idx:
                    if not used[adj_peak_idx]:
                        weight = self._get_weight(self._graph[next_peak_idx], self._graph[adj_peak_idx])
                        if distance[adj_peak_idx] > weight:
                            distance[adj_peak_idx] = min(distance[adj_peak_idx], weight)
                            heappush(priority_queue, (distance[adj_peak_idx], adj_peak_idx))

            used[next_peak_idx] = True

        return distance


def main():
    number_peaks = int(sys.stdin.readline())
    graph = FullGraph(number_peaks, oriented=False)
    for _ in range(number_peaks):
        point = tuple(map(int, sys.stdin.readline().split()))
        graph.add_peak(point)

    print(sum(graph.get_minimum_spanning_tree_weight(0)))


if __name__ == "__main__":
    main()
