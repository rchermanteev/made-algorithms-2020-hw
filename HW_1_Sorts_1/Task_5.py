"""
E. Простая сортировка
ограничение по времени на тест2 секунды
ограничение по памяти на тест64 мегабайта
вводстандартный ввод
выводстандартный вывод
Дан массив целых чисел. Ваша задача — отсортировать его в порядке неубывания.

Входные данные
В первой строке входного файла содержится число N (1≤N≤100000) — количество элементов в массиве. Во второй строке
находятся N целых чисел, по модулю не превосходящих 109.

Выходные данные
В выходной файл надо вывести этот же массив в порядке неубывания, между любыми двумя числами должен стоять ровно один
пробел.
"""

import random

from typing import List


def partition(arr: List[int], idx_left_bound: int, idx_right_bound: int) -> int:
    separating_element = arr[random.randint(idx_left_bound, idx_right_bound)]
    idx_left_bound -= 1
    idx_right_bound += 1
    while True:
        idx_left_bound += 1
        while arr[idx_left_bound] < separating_element:
            idx_left_bound += 1

        idx_right_bound -= 1
        while arr[idx_right_bound] > separating_element:
            idx_right_bound -= 1

        if idx_left_bound < idx_right_bound:
            arr[idx_left_bound], arr[idx_right_bound] = arr[idx_right_bound], arr[idx_left_bound]
        else:
            return idx_right_bound


def qsort(arr: List[int]) -> List[int]:
    def _qsort(arr, idx_left_bound, idx_right_bound):
        if idx_left_bound < idx_right_bound:
            idx_section = partition(arr, idx_left_bound, idx_right_bound)
            _qsort(arr, idx_left_bound, idx_section)
            _qsort(arr, idx_section + 1, idx_right_bound)

    _qsort(arr, 0, len(arr) - 1)
    return arr


number_of_elements = int(input())
data = list(map(int, input().split()))

print(" ".join(map(str, qsort(data))))
