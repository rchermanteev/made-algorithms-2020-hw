"""
C. Цифровая сортировка
ограничение по времени на тест3 секунды
ограничение по памяти на тест256 мегабайт
вводстандартный ввод
выводстандартный вывод
Дано n строк, выведите их порядок после k фаз цифровой сортировки.

В этой задаче требуется реализовать цифровую сортировку.
"""
from typing import List


def counting_sort(arr: List[str], step_: int) -> List[str]:
    _MIN_EL, _MAX_EL = ord('a'), ord('z')
    len_cl = _MAX_EL - _MIN_EL + 1
    counting_list = [0] * len_cl
    for el in arr:
        counting_list[ord(el[step_]) - _MIN_EL] += 1

    points_list = [0]
    for i in range(1, len(counting_list)):
        points_list.append(points_list[i - 1] + counting_list[i - 1])

    res_arr = [""] * len(arr)
    for el in arr:
        res_arr[points_list[ord(el[step_]) - _MIN_EL]] = el
        points_list[ord(el[step_]) - _MIN_EL] += 1

    return res_arr


def digital_sorting(arr: List[str], num_steps: int = None) -> List[str]:
    len_str = len(arr[0])
    if num_steps is None:
        num_steps = len_str

    for step in range(num_steps):
        arr = counting_sort(arr, len_str - 1 - step)

    return arr


number_of_string, string_length, number_of_steps = map(int, input().split())
strings = []
for _ in range(number_of_string):
    strings.append(input())

for str_ in digital_sorting(strings, number_of_steps):
    print(str_)
