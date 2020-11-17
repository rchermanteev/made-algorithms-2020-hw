"""
C. Простая сортировка
ограничение по времени на тест2 секунды
ограничение по памяти на тест64 мегабайта
вводстандартный ввод
выводстандартный вывод
Дан массив целых чисел. Ваша задача — отсортировать его в порядке неубывания.

Входные данные
В первой строке входного файла содержится число N (1≤N≤100000) — количество элементов в массиве. Во второй строке находятся N целых чисел, по модулю не превосходящих 109.

Выходные данные
В выходной файл надо вывести этот же массив в порядке неубывания, между любыми двумя числами должен стоять ровно один пробел.
"""


def merge(a: list, b: list) -> list:
    i = 0
    j = 0
    n = len(a)
    m = len(b)
    c = []
    while i < n and j < m:
        if j == m or (i < n and a[i] < b[j]):
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
    while i < n:
        c.append(a[i])
        i += 1
    while j < m:
        c.append(b[j])
        j += 1

    return c


def merge_sort(arr: list) -> list:
    n = len(arr)
    if n == 1:
        return arr

    return merge(merge_sort(arr[:n // 2]), merge_sort(arr[n // 2:]))


number_of_elements = int(input())
data = list(map(int, input().split()))

print(" ".join(map(str, merge_sort(data))))
