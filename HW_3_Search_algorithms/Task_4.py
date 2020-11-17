import sys

from math import log2, ceil
from typing import List


def get_num_scraps(len_scrap: int, rps: List[int]) -> int:
    num_scraps = 0
    for rp in rps:
        num_scraps += rp // len_scrap

    return num_scraps


def get_max_piece_of_rope(_ropes: List[int], _num_houses: int) -> int:
    left_board = 0
    right_board = max(_ropes) if _ropes else 1
    _ITERATION_NUMBER = int(log2((right_board - left_board))) + 1
    for _ in range(_ITERATION_NUMBER):
        middle = ceil((left_board + right_board) / 2)
        if middle:
            num_scraps = get_num_scraps(middle, _ropes)
            if num_scraps < _num_houses:
                right_board = middle - 1
            else:
                left_board = middle

    if left_board and get_num_scraps(left_board, _ropes) < _num_houses:
        return 0

    return left_board


number_ropes, number_houses = map(int, sys.stdin.readline().split())
ropes = []
for _ in range(number_ropes):
    ropes.append(int(sys.stdin.readline()))

print(get_max_piece_of_rope(ropes, number_houses))
