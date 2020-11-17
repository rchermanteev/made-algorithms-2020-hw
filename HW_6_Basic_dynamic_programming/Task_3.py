from typing import List, Tuple, Union


def custom_max(
    dp: List[float], temp_seq: List[int], target_idx: int, target_val: int
) -> Tuple[int, Union[int, float]]:
    temp_arr = []
    for i in range(target_idx):
        if temp_seq[i] < target_val:
            temp_arr.append((i, dp[i]))

    if temp_arr:
        return max(temp_arr, key=lambda x: x[1])

    return target_idx, 0


def get_way(dirt_way: List[int], dp: List[float], seq: List[int]) -> List[int]:
    state = max(enumerate(dp), key=lambda x: x[1])[0]
    way = []
    flag = True
    while flag:
        if state == dirt_way[state]:
            flag = False

        way.append(seq[state])
        state = dirt_way[state]

    return way[::-1]


def get_longest_ascending_subsequence(seq: List[int], len_seq: int) -> List[int]:
    dp = [float("-Inf")] * len_seq
    dp[0] = 1
    dirty_way = [0]
    for i in range(1, len_seq):
        idx_prev_el, transition = custom_max(dp, seq[:i], i, seq[i])
        dp[i] = transition + 1
        dirty_way.append(idx_prev_el)

    return get_way(dirty_way, dp, seq)


sequence_length = int(input())
sequence = list(map(int, input().split()))

sub_seq = get_longest_ascending_subsequence(sequence, sequence_length)

print(len(sub_seq))
print(" ".join(map(str, sub_seq)))
