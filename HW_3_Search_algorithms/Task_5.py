"""
E. Очень Легкая Задача
ограничение по времени на тест2 секунды
ограничение по памяти на тест256 мегабайт
вводстандартный ввод
выводстандартный вывод
Сегодня утром жюри решило добавить в вариант олимпиады еще одну, Очень Легкую Задачу. Ответственный секретарь
Оргкомитета напечатал ее условие в одном экземпляре, и теперь ему нужно до начала олимпиады успеть сделать еще n копий.
В его распоряжении имеются два ксерокса, один из которых копирует лист за x секунд, а другой – за y.
(Разрешается использовать как один ксерокс, так и оба одновременно. Можно копировать не только с оригинала,
но и с копии.) Помогите ему выяснить, какое минимальное время для этого потребуется.
"""

from math import log2, ceil


def get_min_time_on_copying(f_spd: int, s_spd: int, copies_needed: int) -> int:
    def _get_num_copies(_t: int, _s1: int = f_spd , _s2: int = s_spd) -> int:
        return _t // _s1 + _t // _s2

    left_board = 0
    _MIN_SPEED = min(f_spd, s_spd)
    right_board = _MIN_SPEED * copies_needed
    copies_needed -= 1
    _ITERATION_NUMBER = ceil(log2((right_board - left_board)))
    for _ in range(_ITERATION_NUMBER):
        middle = int((left_board + right_board) / 2)
        num_copies = _get_num_copies(middle)
        if num_copies < copies_needed:
            left_board = middle + 1
        else:
            right_board = middle

    return _MIN_SPEED + right_board


number_copies, first_copy_speed, second_copy_speed = map(int, input().split())

print(get_min_time_on_copying(first_copy_speed, second_copy_speed, number_copies))
