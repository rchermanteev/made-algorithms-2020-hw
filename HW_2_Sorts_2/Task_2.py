"""
B. Сортировка подсчетом
ограничение по времени на тест1 секунда
ограничение по памяти на тест64 мегабайта
вводстандартный ввод
выводстандартный вывод
Дан список из N элементов, которые принимают целые значения от 0 до 100. Отсортируйте этот список в порядке неубывания
элементов. Выведите полученный список.
"""

from typing import List, Tuple


def get_min_and_max_elements(arr_: List[int]) -> Tuple[int, int]:
    min_el_, max_el_ = arr_[0], arr_[0]
    for i in range(1, len(arr_)):
        if arr_[i] > max_el_:
            max_el_ = arr_[i]
        elif arr_[i] < min_el_:
            min_el_ = arr_[i]

    return min_el_, max_el_


def counting_sort(arr: List[int]) -> List[int]:
    min_el, max_el = get_min_and_max_elements(arr)
    len_cl = max_el - min_el + 1
    counting_list = [0] * len_cl
    for el in arr:
        counting_list[el - min_el] += 1

    arr = []
    for i in range(len_cl):
        while counting_list[i] > 0:
            arr.append(i + min_el)
            counting_list[i] -= 1

    return arr


data = list(map(int, input().split()))

print(" ".join(map(str, counting_sort(data))))
