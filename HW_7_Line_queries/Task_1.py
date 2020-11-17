import sys

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


def get_arr(len_arr, x, y, a0):
    arr = [a0]
    _MOD = 2 ** 16
    for _ in range(len_arr - 1):
        arr.append((x * arr[-1] + y) % _MOD)

    return arr


def get_requests(num_req, z, t, b0, len_arr):
    _MOD = 2 ** 30
    arr_b = [b0]
    for _ in range(2 * num_req - 1):
        arr_b.append((z * arr_b[-1] + t) % _MOD)

    arr_c = [arr_b[i] % len_arr for i in range(len(arr_b))]
    requests = []
    for i in range(0, len(arr_c), 2):
        requests.append((min(arr_c[i], arr_c[i + 1]), max(arr_c[i], arr_c[i + 1])))

    return requests


def get_array_of_sum(arr):
    arr_of_sum = [arr[0]]
    for i in range(1, len(arr)):
        arr_of_sum.append(arr_of_sum[-1] + arr[i])

    return arr_of_sum


def get_prefix_amount(arr_of_sum, req):
    left_idx, right_idx = req
    if left_idx == 0:
        return arr_of_sum[right_idx]

    return arr_of_sum[right_idx] - arr_of_sum[left_idx - 1]


stdin, stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)

len_arr, x, y, a0 = map(int, stdin.readline().split())
num_req, z, t, b0 = map(int, stdin.readline().split())

array = get_arr(len_arr, x, y, a0)
requests = get_requests(num_req, z, t, b0, len_arr)

array_of_sum = get_array_of_sum(array)
result = 0
for request in requests:
    result += get_prefix_amount(array_of_sum, request)

print(result)
