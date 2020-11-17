"""
A. Приближенный двоичный поиск
ограничение по времени на тест2 секунды
ограничение по памяти на тест256 мегабайт
вводстандартный ввод
выводстандартный вывод
Даны два массива. Первый массив отсортирован по неубыванию, второй массив содержит запросы — целые числа. Для каждого
запроса выведите число из первого массива наиболее близкое к числу в этом запросе. Если таких несколько, выведите
меньшее из них.
"""

from typing import List


def get_most_suitable(pair: List[int], x: int) -> int:
    if abs(pair[0] - x) < abs(pair[1] - x):
        return pair[0]
    elif abs(pair[0] - x) > abs(pair[1] - x):
        return pair[1]
    else:
        return min(pair)


def bin_search(arr: List[int], x: int) -> int:
    def _bin_search(_arr: List[int], _left: int, _right: int, _x: int) -> int:
        if _left == _right - 1:
            tmp_arr = _arr[_left: _right + 1]
            return get_most_suitable(tmp_arr, _x) if len(tmp_arr) == 2 else _arr[_left]

        _middle = (_left + _right) // 2
        if _x == _arr[_middle]:
            return _arr[_middle]

        if _x < _arr[_middle]:
            return _bin_search(_arr, _left, _middle, _x)
        else:
            return _bin_search(_arr, _middle, _right, _x)

    return _bin_search(arr, 0, len(arr), x)


len_array, len_requests = map(int, input().split())
array = list(map(int, input().split()))
requests = map(int, input().split())

for request in requests:
    print(bin_search(array, request))
