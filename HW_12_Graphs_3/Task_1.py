import sys
from typing import Tuple, Union, List


class DisjointSetUnion:
    def __init__(self, num_elements: int):
        self.forest = [[i, i, i, 1] for i in range(num_elements)]
        self.rang = [0 for _ in range(num_elements)]

    def get(self, x: int) -> List[int]:
        if self.forest[x][0] != x:
            self.forest[x] = self.get(self.forest[x][0])

        return self.forest[x]

    def join(self, x: int, y: int):
        x = self.get(x)
        y = self.get(y)
        if x[0] == y[0]:
            return

        if self.rang[x[0]] > self.rang[y[0]]:
            x, y = y, x

        if self.rang[x[0]] == self.rang[y[0]]:
            self.rang[y[0]] += 1

        self.forest[x[0]][0] = y[0]
        self.forest[y[0]] = [y[0], min(y[1], x[1]), max(y[2], x[2]), y[3] + x[3]]


def transform(req: str) -> Union[Tuple[str, int], Tuple[str, int, int]]:
    req = req.split()
    if len(req) == 2:
        return req[0], int(req[1]) - 1
    elif len(req) == 3:
        return req[0], int(req[1]) - 1, int(req[2]) - 1


def main():
    number_elements = int(sys.stdin.readline())
    requests = [transform(dirty_request.strip()) for dirty_request in sys.stdin.readlines()]

    dsu = DisjointSetUnion(number_elements)
    for request in requests:
        if request[0] == "union":
            dsu.join(request[1], request[2])
        elif request[0] == "get":
            group, min_el, max_el, count_el = dsu.get(request[1])
            print(f"{str(min_el + 1)} {str(max_el + 1)} {str(count_el)}")


if __name__ == "__main__":
    main()
