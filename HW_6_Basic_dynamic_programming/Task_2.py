from typing import List, Tuple


def get_way(arr: List[List[Tuple[Tuple[int, int], str]]]) -> List[str]:
    way = []
    tmp_step = arr[-1][-1]
    for _ in range(len(arr) + len(arr[0]) - 1):
        way.append(tmp_step[1])
        tmp_step = arr[tmp_step[0][0]][tmp_step[0][1]]

    return way[::-1]


def det_solution_for_turtle(
    n_rows: int, n_cols: int, mat: List[List[int]]
) -> Tuple[int, List[str]]:
    dp = [[0] * n_cols for _ in range(n_rows)]
    dp[0][0] = mat[0][0]

    way = [[((0, 0), "")] * n_cols for _ in range(n_rows)]
    way[0][0] = ((0, 0), "")

    for i in range(0, n_rows):
        for j in range(0, n_cols):
            if i == 0 and j > 0:
                dp[i][j] = dp[i][j - 1] + mat[i][j]
                way[i][j] = ((i, j - 1), "R")

            elif j == 0 and i > 0:
                dp[i][j] = dp[i - 1][j] + mat[i][j]
                way[i][j] = ((i - 1, j), "D")

            elif i and j:
                if dp[i][j - 1] > dp[i - 1][j]:
                    dp[i][j] = dp[i][j - 1] + mat[i][j]
                    way[i][j] = ((i, j - 1), "R")
                else:
                    dp[i][j] = dp[i - 1][j] + mat[i][j]
                    way[i][j] = ((i - 1, j), "D")

    return dp[-1][-1], get_way(way)


num_rows, num_cols = map(int, input().split())
matrix = []
for _ in range(num_rows):
    matrix.append(list(map(int, input().split())))

coins, steps = det_solution_for_turtle(num_rows, num_cols, matrix)

print(coins)
print("".join(steps))
