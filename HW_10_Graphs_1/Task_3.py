import sys
import threading
from typing import List, Union

sys.setrecursionlimit(10 ** 9)
threading.stack_size(2 ** 26)


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

    def _dfs_fir_loop_search(self, peak: int, list_of_marks: List[int]) -> Union[bool, None]:
        list_of_marks[peak] = 1
        for adj_peak in self._graph[peak]:
            if list_of_marks[adj_peak] == self.DEFAULT_COLOR:
                self._dfs_fir_loop_search(adj_peak, list_of_marks)
            if list_of_marks[adj_peak] == 1:
                return True

        list_of_marks[peak] = 2

    def check_for_loop_content(self):
        colors = [self.DEFAULT_COLOR for _ in range(self.num_peaks)]
        for peak_idx in range(len(self._graph)):
            if colors[peak_idx] == self.DEFAULT_COLOR:
                is_loop = self._dfs_fir_loop_search(peak_idx, colors)
                if is_loop is True:
                    return True

        return False

    def _dfs_for_topological_sort(self, peak: int, list_of_marks: List[int], answer: List[int]):
        list_of_marks[peak] = 1
        for adj_peak in self._graph[peak]:
            if list_of_marks[adj_peak] == self.DEFAULT_COLOR:
                self._dfs_for_topological_sort(adj_peak, list_of_marks, answer)

        answer.append(peak)

    def topological_sort(self) -> List[int]:
        if self.check_for_loop_content():
            return [-1]

        used = [self.DEFAULT_COLOR for _ in range(self.num_peaks)]
        answer = []
        for peak_idx in range(len(self._graph)):
            if used[peak_idx] == self.DEFAULT_COLOR:
                self._dfs_for_topological_sort(peak_idx, used, answer)

        return answer[::-1]


def transform_answer(ans: List[int]) -> List[int]:
    return ans if ans == [-1] else list(map(lambda x: x + 1, ans))


def main():
    number_peaks, number_edges = map(int, sys.stdin.readline().split())
    graph = Graph(number_peaks, number_edges, oriented=True)
    for _ in range(number_edges):
        b, e = map(lambda x: int(x) - 1, sys.stdin.readline().split())
        graph.add_edge(b, e)

    print(" ".join(map(lambda x: str(x), transform_answer(graph.topological_sort()))))


if __name__ == "__main__":
    threading.Thread(target=main).start()
