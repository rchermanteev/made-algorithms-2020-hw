from math import sqrt
import sys
from typing import Tuple


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
        distance = [float("inf")] * self.num_peaks
        used = [False] * self.num_peaks
        distance[start_peak_idx] = 0
        for _ in range(self.num_peaks):
            next_peak_idx = -1
            for peak_idx in range(self.num_peaks):
                if not used[peak_idx] and (next_peak_idx == -1 or distance[peak_idx] < distance[next_peak_idx]):
                    next_peak_idx = peak_idx

            if distance[next_peak_idx] == float("inf"):
                break

            for adj_peak_idx in range(self.num_peaks):
                if adj_peak_idx != next_peak_idx:
                    if not used[adj_peak_idx]:
                        weight = self._get_weight(self._graph[next_peak_idx], self._graph[adj_peak_idx])
                        if distance[adj_peak_idx] > weight:
                            distance[adj_peak_idx] = min(distance[adj_peak_idx], weight)

            used[next_peak_idx] = True

        return sum(distance)


def main():
    number_peaks = int(sys.stdin.readline())
    graph = FullGraph(number_peaks, oriented=False)
    for _ in range(number_peaks):
        point = tuple(map(int, sys.stdin.readline().split()))
        graph.add_peak(point)

    print(graph.get_minimum_spanning_tree_weight(0))


if __name__ == "__main__":
    main()
