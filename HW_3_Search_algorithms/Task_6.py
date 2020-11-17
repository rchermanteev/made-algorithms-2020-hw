from math import sqrt, log, ceil


def get_minimum_travel_time(field_spd: int, forest_spd: int, cord_y: float) -> float:
    def _get_time_travel(
        _x: float, _fld_s: int = field_spd, _fst_s: int = forest_spd, _y: float = cord_y
    ) -> float:
        return (
            sqrt((1 - _y) ** 2 + _x ** 2) / _fld_s
            + sqrt(_y ** 2 + (1 - _x) ** 2) / _fst_s
        )

    left_board = 0.0
    right_board = 1
    _EPSILON = 10 ** -4
    _ITERATION_NUMBER = ceil(log((right_board - left_board) / _EPSILON, 1.5))
    for _ in range(_ITERATION_NUMBER):
        fir_third = left_board + (right_board - left_board) / 3
        sec_third = left_board + 2 * (right_board - left_board) / 3
        if _get_time_travel(fir_third) < _get_time_travel(sec_third):
            right_board = sec_third
        else:
            left_board = fir_third

    return right_board


field_speed, forest_speed = map(int, input().split())
coordinate_y = float(input())

print(get_minimum_travel_time(field_speed, forest_speed, coordinate_y))
