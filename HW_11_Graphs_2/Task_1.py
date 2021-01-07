from collections import deque
import sys
from typing import List, Tuple, Union


def get_min_way(way: List[List[Union[int, None]]],
                end_cell: Tuple[int, int],
                start_cell_mark: int = -1) -> List[str]:
    min_way = []
    temp_cell = way[end_cell[0]][end_cell[1]]
    while temp_cell != start_cell_mark:
        min_way.append(" ".join(map(lambda x: str(x + 1), temp_cell)))
        temp_cell = way[temp_cell[0]][temp_cell[1]]

    min_way = min_way[::-1] + [" ".join(map(lambda x: str(x + 1), end_cell))]

    return min_way


def bfs(field: List[List[Union[int, None]]],
        start_cell: Tuple[int, int],
        end_cell: Tuple[int, int]) -> Tuple[int, List[str]]:
    way = [[None for _ in range(len(field))] for _ in range(len(field))]
    way[start_cell[0]][start_cell[1]] = -1
    peak_queue = deque()
    peak_queue.append(start_cell)
    while len(peak_queue):
        x_temp_peak, y_temp_peak = peak_queue.popleft()
        for x_next_step, y_next_step in knights_move((x_temp_peak, y_temp_peak), len(field)):
            if field[x_next_step][y_next_step] is None:
                peak_queue.append((x_next_step, y_next_step))
                field[x_next_step][y_next_step] = field[x_temp_peak][y_temp_peak] + 1
                way[x_next_step][y_next_step] = (x_temp_peak, y_temp_peak)

    min_way = get_min_way(way, end_cell)

    return field[end_cell[0]][end_cell[1]], min_way


def knights_move(current_cell: Tuple[int, int], len_field: int) -> List[Tuple[int, int]]:
    _POSSIBLE_STEPS = [(2, 1), (2, -1), (-2, 1), (-2, -1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
    x, y = current_cell
    positions_after_move = []
    for x_step, y_step in _POSSIBLE_STEPS:
        pos_x, pos_y = x + x_step, y + y_step
        if 0 <= pos_x < len_field and 0 <= pos_y < len_field:
            positions_after_move.append((pos_x, pos_y))

    return positions_after_move


def main():
    n = int(sys.stdin.readline())
    x1, y1 = map(lambda x: int(x) - 1, sys.stdin.readline().split())
    x2, y2 = map(lambda x: int(x) - 1, sys.stdin.readline().split())

    distance_matrix = [[None for _ in range(n)] for _ in range(n)]
    distance_matrix[x1][y1] = 0

    num_steps, min_way = bfs(distance_matrix, (x1, y1), (x2, y2))

    print(num_steps + 1)
    print("\n".join(min_way))


if __name__ == "__main__":
    main()
