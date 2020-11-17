import sys
import threading
from typing import List, Union, Tuple

sys.setrecursionlimit(10 ** 9)
threading.stack_size(10 ** 8)


class Graph:
    def __init__(self, num_peaks, num_edges, oriented):
        self.num_edges = num_edges
        self.num_peaks = num_peaks
        self.oriented = oriented
        self._graph = [[] for _ in range(num_peaks)]
        self.DEFAULT_COLOR = 0

    def add_edge(self, edge_out, edge_in):
        self._graph[edge_out].append(edge_in)
        if not self.oriented:
            self._graph[edge_in].append(edge_out)

    def _dfs(self, peak: int, list_of_marks: List[int], color: int):
        list_of_marks[peak] = color
        for adj_peak in self._graph[peak]:
            if list_of_marks[adj_peak] == self.DEFAULT_COLOR:
                self._dfs(adj_peak, list_of_marks, color)

    def dfs(self):
        used = [self.DEFAULT_COLOR for _ in range(self.num_peaks)]
        for peak_idx in range(len(self._graph)):
            if used[peak_idx] == self.DEFAULT_COLOR:
                self._dfs(peak_idx, used, 1)

        return used

    def get_mask_of_connectivity_component(self,
                                           return_num_colors: bool = False
                                           ) -> Union[List[int], Tuple[List[int], int]]:
        colors = [self.DEFAULT_COLOR for _ in range(self.num_peaks)]
        color = 0
        for peak_idx in range(len(self._graph)):
            if colors[peak_idx] == self.DEFAULT_COLOR:
                color += 1
                self._dfs(peak_idx, colors, color)

        return colors, color if return_num_colors else colors


def main():
    number_peaks, number_edges = map(int, sys.stdin.readline().split())
    graph = Graph(number_peaks, number_edges, oriented=False)
    for _ in range(number_edges):
        b, e = map(lambda x: int(x) - 1, sys.stdin.readline().split())
        graph.add_edge(b, e)

    colors_mask, num_colors = graph.get_mask_of_connectivity_component(return_num_colors=True)

    print(num_colors)
    print(" ".join(map(str, colors_mask)))


if __name__ == "__main__":
    threading.Thread(target=main).start()
