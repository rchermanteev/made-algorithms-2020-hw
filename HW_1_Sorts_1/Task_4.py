"""
D. Количество инверсий
ограничение по времени на тест5 секунд
ограничение по памяти на тест256 мегабайт
вводстандартный ввод
выводстандартный вывод
Напишите программу, которая для заданного массива  находит количество пар (i,j) таких, что i<j и
ai>aj.

Входные данные
Первая строка входного файла содержит натуральное число n (1≤n≤500000) — количество элементов
массива. Вторая строка содержит n попарно различных элементов массива A (0≤ai≤10**6).

Выходные данные
В выходной файл выведите одно число — ответ на задачу.
"""

from typing import Tuple, List


def merge(a: List[int], b: List[int]) -> Tuple[List[int], int]:
    i, j = 0, 0
    c = []
    count_inversion = 0
    len_a, len_b = len(a), len(b)

    while i < len_a and j < len_b:
        if j == len_b or (i < len_a and a[i] < b[j]):
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
            count_inversion += len_a - i

    while i < len_a:
        c.append(a[i])
        i += 1

    while j < len_b:
        c.append(b[j])
        j += 1

    return c, count_inversion


def merge_sort_with_inversion_count(arr: List[int]) -> Tuple[List[int], int]:
    n = len(arr)
    if n == 1:
        return arr, 0

    l, count_inv_l = merge_sort_with_inversion_count(arr[:n // 2])
    r, count_inv_r = merge_sort_with_inversion_count(arr[n // 2:])

    merge_list, count_inv_merge = merge(l, r)

    return merge_list, count_inv_l + count_inv_r + count_inv_merge


number_of_elements = int(input())
data = list(map(int, input().split()))

_, count_inv = merge_sort_with_inversion_count(data)

print(count_inv)
