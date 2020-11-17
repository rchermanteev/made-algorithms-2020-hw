"""
C. Квадратный корень и квадратный квадрат
ограничение по времени на тест2 секунды
ограничение по памяти на тест256 мегабайт
вводстандартный ввод
выводстандартный вывод
Найдите такое число x, что x^2 + sqrt(x) = C , с точностью не менее 6 знаков после точки.
"""

from math import log2, ceil


def get_value_func(x: float) -> float:
    return x ** 2 + x ** (1/2)


def real_binary_search(target: float) -> float:
    left_bound = 0
    right_bound = 2 ** 20
    _EPSILON = 10 ** -6
    _ITERATION_NUMBER = ceil(log2((right_bound - left_bound) / _EPSILON))
    for _ in range(_ITERATION_NUMBER):
        middle = (left_bound + right_bound) / 2
        if get_value_func(middle) < target:
            left_bound = middle
        else:
            right_bound = middle

    return right_bound


parameter = float(input())

print(real_binary_search(parameter))
