import random
import sys

from io import IOBase, BytesIO
from os import read, write, fstat
from typing import Union

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


class HashTable:
    PULL_PRIME_NUMBERS = [1336337, 4477457, 5308417, 8503057, 9834497]

    def __init__(self):
        self.size = 10 ** 6
        self.arr = [None] * self.size
        self.contain = 0
        self.HASH_PARAM_A = random.randint(100000, 500000)
        self.HASH_PARAM_P = HashTable.PULL_PRIME_NUMBERS[random.randint(0, len(HashTable.PULL_PRIME_NUMBERS) - 1)]
        self.count_rip_elements = 0
        self.PLUG = "r"

    def _get_hash(self, key: int) -> int:
        return ((self.HASH_PARAM_A * key) % self.HASH_PARAM_P) % self.size

    def get(self, key: int) -> Union[None, int]:
        hash_key = self._get_hash(key)
        while self.arr[hash_key] is not None:
            if self.arr[hash_key][0] == key:
                return self.arr[hash_key][1]

            hash_key = (hash_key + 1) % self.size

    def put(self, key: int, value: int):
        hash_key = self._get_hash(key)
        while self.arr[hash_key] is not None and self.arr[hash_key] != self.PLUG:
            hash_key = (hash_key + 1) % self.size

        self.arr[hash_key] = (key, value)

    def delete(self, key: int):
        hash_key = self._get_hash(key)
        while self.arr[hash_key] is not None:
            if self.arr[hash_key][0] == key:
                self.arr[hash_key] = self.PLUG
                break

            hash_key = (hash_key + 1) % self.size


class CustomSet(HashTable):
    def __init__(self):
        super(CustomSet, self).__init__()

    def insert(self, x: int):
        if self.get(x) is None:
            self.put(x, 1)

    def exists(self, x: int) -> str:
        if self.get(x):
            return 'true'

        return 'false'


stdin, stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
c_set = CustomSet()
input_command = stdin.readlines()
res = []
for el in input_command:
    command, value = el.split()
    if command == "insert":
        c_set.insert(int(value))
    elif command == "exists":
        res.append(c_set.exists(int(value)))
    elif command == "delete":
        c_set.delete(int(value))

stdout.write('\n'.join(res))
