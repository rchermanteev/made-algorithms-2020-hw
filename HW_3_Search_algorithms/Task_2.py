"""
B. Быстрый поиск в массиве
ограничение по времени на тест1 секунда
ограничение по памяти на тест512 мегабайт
вводстандартный ввод
выводстандартный вывод
Дан массив из n целых чисел. Все числа от −109 до 109.

Нужно уметь отвечать на запросы вида «Cколько чисел имеют значения от l до r»?
"""

import sys

from typing import List


def get_idx_lower_bound(arr: List[int], x: int) -> int:
    left_board = -1
    right_board = len(arr)
    while left_board < right_board - 1:
        middle = (left_board + right_board) // 2
        if x <= arr[middle]:
            right_board = middle
        else:
            left_board = middle

    return right_board


def get_idx_upper_bound(arr: List[int], x: int) -> int:
    return get_idx_lower_bound(arr, x + 1)


def get_number_of_elements_between_numbers(arr: List[int], left_num: int, right_num: int) -> int:
    return get_idx_upper_bound(arr, right_num) - get_idx_lower_bound(arr, left_num)


len_array = int(sys.stdin.readline())
array = sorted(list(map(int, sys.stdin.readline().split())))
num_requests = int(sys.stdin.readline())
requests = []
for _ in range(num_requests):
    requests.append(list(map(int, sys.stdin.readline().split())))

for request in requests:
    print(get_number_of_elements_between_numbers(array, *request))
