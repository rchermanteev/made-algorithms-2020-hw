from collections import namedtuple
from typing import Tuple, List


def custom_max(arr: List[Tuple[int, int]], shift: int = 0) -> Tuple[int, int]:
    max_el_idx = -1
    max_el_val = float("-Inf")
    for i in range(len(arr)):
        if arr[i][0] > max_el_val:
            max_el_val = arr[i][0]
            max_el_idx = i

    return max_el_val, max_el_idx + shift


def get_grasshopper_way(arr: List[Tuple[int, int]]) -> List[int]:
    way = [len(arr)]
    prev_pillow = arr[-1][1]
    while prev_pillow != 0:
        way.append(prev_pillow + 1)
        prev_pillow = arr[prev_pillow][1]

    way.append(1)

    return sorted(way)


def get_solution_for_grasshopper(
    num_pillars: int, max_jump_len: int, list_coins_on_pillars: List[int]
) -> Tuple[int, int, List[int]]:
    StatePillow = namedtuple("StatePillow", ["max_coins", "prev_pillow"])
    l_coins_on_pillars = [0] + list_coins_on_pillars + [0]
    base_state = StatePillow(max_coins=0, prev_pillow=0)
    pb = [base_state]
    for i in range(1, num_pillars):
        if i <= max_jump_len:
            best_prev_coins, best_prev_pillow = custom_max(pb)
        else:
            best_prev_coins, best_prev_pillow = custom_max(
                pb[i - max_jump_len: i], i - max_jump_len
            )

        tmp_state = StatePillow(
            max_coins=best_prev_coins + l_coins_on_pillars[i],
            prev_pillow=best_prev_pillow,
        )
        pb.append(tmp_state)

    way_gr = get_grasshopper_way(pb)

    return pb[-1][0], len(way_gr) - 1, way_gr


number_pillars, max_jump_length = map(int, input().split())
list_of_coins_on_pillars = list(map(int, input().split()))

max_coins, num_jumps, grasshopper_way = get_solution_for_grasshopper(
    number_pillars, max_jump_length, list_of_coins_on_pillars
)

print(max_coins)
print(num_jumps)
print(" ".join(map(str, grasshopper_way)))
