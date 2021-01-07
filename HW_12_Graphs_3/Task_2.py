import sys
from typing import Tuple, Union, List


class DisjointSetUnion:
    def __init__(self, num_elements: int):
        self.forest = [[i, [i]] for i in range(num_elements)]
        self.experience = [0 for _ in range(num_elements)]
        self.rang = [0 for _ in range(num_elements)]

    def _get(self, x: int) -> List[Union[int, List[int]]]:
        cur_peak = self.forest[x][0]
        while self.forest[cur_peak][0] != cur_peak:
            cur_peak = self.forest[cur_peak][0]

        return self.forest[cur_peak]

    def get_exp_player(self, plr_id: int) -> int:
        return self.experience[plr_id]

    def join(self, x: int, y: int):
        x = self._get(x)
        y = self._get(y)
        if x[0] == y[0]:
            return

        if self.rang[x[0]] > self.rang[y[0]]:
            x, y = y, x

        if self.rang[x[0]] == self.rang[y[0]]:
            self.rang[y[0]] += 1

        self.forest[x[0]] = [y[0], None]
        self.forest[y[0]][1] += x[1]

    def add_exp(self, plr_id: int, exp: int):
        main_peak, group = self._get(plr_id)
        for plr in group:
            self.experience[plr] += exp


def transform(req: str) -> Union[Tuple[str, int], Tuple[str, int, int]]:
    req = req.split()
    if req[0] == "get":
        return req[0], int(req[1]) - 1
    elif req[0] == "add":
        return req[0], int(req[1]) - 1, int(req[2])
    elif req[0] == "join":
        return req[0], int(req[1]) - 1, int(req[2]) - 1


def main():
    number_players, number_requests = map(int, sys.stdin.readline().split())
    requests = [transform(dirty_request.strip()) for dirty_request in sys.stdin.readlines()]

    dsu = DisjointSetUnion(number_players)
    for request in requests:
        if request[0] == "join":
            dsu.join(request[1], request[2])
        elif request[0] == "get":
            player_exp = dsu.get_exp_player(request[1])
            print(player_exp)
        elif request[0] == "add":
            dsu.add_exp(request[1], request[2])


if __name__ == "__main__":
    main()
