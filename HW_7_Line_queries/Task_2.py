import sys

from math import log2, ceil
from io import IOBase, BytesIO
from os import read, write, fstat

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = read(self._fd, max(fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self, size: int = ...):
        while self.newlines == 0:
            b = read(self._fd, max(fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


def get_array(len_arr, a0):
    _MOD = 16714589
    _SHIFT = 21563
    _COEFFICIENT = 23

    arr = [a0]
    for i in range(1, len_arr):
        arr.append((_COEFFICIENT * arr[i - 1] + _SHIFT) % _MOD)

    return arr


def get_separate_table(len_arr, arr):
    sep_table = [arr.copy()]
    for j in range(1, ceil(2 ** log2(len_arr))):
        temp_arr = []
        for i in range(0, len_arr - 2 ** j + 1):
            temp_arr.append(min(sep_table[j - 1][i], sep_table[j - 1][i + 2 ** (j - 1)]))

        sep_table.append(temp_arr)

    return sep_table


def get_rmq(sep_table, left, right):
    j = int(log2(right - left + 1))
    return min(sep_table[j][left], sep_table[j][right - 2 ** j + 1])


stdin, stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)

n, m, a1 = map(int, stdin.readline().split())
u1, v1 = map(int, stdin.readline().split())

array = get_array(n, a1)
separate_table = get_separate_table(n, array)

_SHIFT_U, _SHIFT_V = 751, 593
_COEFFICIENT_U, _COEFFICIENT_V = 17, 13
_MULT_U, _MULT_V = 2, 5


r_prev = get_rmq(separate_table, min(u1 - 1, v1 - 1), max(u1 - 1, v1 - 1))
u_prev = u1
v_prev = v1
for i in range(2, m + 1):
    u_prev = ((_COEFFICIENT_U * u_prev + _SHIFT_U + r_prev + _MULT_U * (i - 1)) % n) + 1
    v_prev = ((_COEFFICIENT_V * v_prev + _SHIFT_V + r_prev + _MULT_V * (i - 1)) % n) + 1
    r_prev = get_rmq(separate_table, min(u_prev - 1, v_prev - 1), max(u_prev - 1, v_prev - 1))

print(u_prev, v_prev, r_prev)
