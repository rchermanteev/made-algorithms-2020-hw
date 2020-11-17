def get_levenshtein_distance(str_1: str, str_2: str) -> int:
    def _get_difference(a: str, b: str) -> int:
        return 0 if a == b else 1

    len_str_1, len_str_2 = len(str_1), len(str_2)
    dp = [[0 for _ in range(len_str_2 + 1)] for _ in range(len_str_1 + 1)]
    dp[0][0] = 0
    for i in range(1, len_str_1 + 1):
        dp[i][0] = i

    for j in range(1, len_str_2 + 1):
        dp[0][j] = j

    for i in range(1, len_str_1 + 1):
        for j in range(1, len_str_2 + 1):
            delete, insert = dp[i][j - 1] + 1, dp[i - 1][j] + 1
            change = dp[i - 1][j - 1] + _get_difference(str_1[i - 1], str_2[j - 1])
            dp[i][j] = min(delete, insert, change)

    return dp[-1][-1]


first_string = input()
second_string = input()

print(get_levenshtein_distance(first_string, second_string))
