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


class HashMap:
    class Iterator:
        def __init__(self, table, name=None):
            self._table = table
            self._name = name
            self._cur1 = 0
            self._cur2 = 0

        def __iter__(self):
            return self

        def __next__(self):
            while self._cur1 < len(self._table):
                if self._cur2 < len(self._table[self._cur1]):
                    element = self._table[self._cur1][self._cur2]
                    if self._name == "keys":
                        element = element.get_key()
                    elif self._name == "values":
                        element = element.get_value()
                    else:
                        element = (element.get_key(), element.get_value())

                    self._cur2 += 1

                    return element

                self._cur1 += 1
                self._cur2 = 0

            raise StopIteration

    class Entry:
        def __init__(self, key: str, value: str):
            self.key = key
            self.value = value

        def get_key(self) -> str:
            return self.key

        def get_value(self) -> str:
            return self.value

        def __eq__(self, other) -> bool:
            return self.key == other.get_key()

    def __init__(self, _buckets_num: int = 16):
        self._buckets_num = _buckets_num
        self._table = [[] for _ in range(self._buckets_num)]
        self._entries_num = 0
        self._buckets_usd = 0
        self._HASH_PARAM_A = 3
        self._HASH_PARAM_P = 1336337

    def get(self, key: str, default_value: str = 'none') -> Union[None, str]:
        index = self._get_index(self._get_hash(key))
        for element in self._table[index]:
            if element.get_key() == key:
                return element.get_value()
        else:
            return default_value

    def put(self, key: str, value: str):
        item = self.Entry(key, value)
        index = self._get_index(self._get_hash(key))
        if not self.__contains__(key):
            self._entries_num += 1
            if len(self._table[index]) == 0:
                self._buckets_usd += 1
            self._table[index].append(item)
        else:
            for i, element in enumerate(self._table[index]):
                if element.get_key() == item.get_key():
                    self._table[index][i] = item

        if self._buckets_usd / self.__len__() < 2:
            self._resize()

    def delete(self, key: str):
        index = self._get_index(self._get_hash(key))
        if self.__contains__(key):
            for i, element in enumerate(self._table[index]):
                if element.get_key() == key:
                    self._table[index].pop(i)
                    self._entries_num -= 1
                    if len(self._table[index]) == 0:
                        self._buckets_usd -= 1

                    break

    def __len__(self) -> int:
        return self._entries_num

    def _get_hash(self, key: str) -> int:
        _hash = 0
        for i in range(len(key)):
            _hash = (_hash * self._HASH_PARAM_A + ord(key[i]) - ord('a')) % self._HASH_PARAM_P

        return _hash

    def _get_index(self, hash_value: int) -> int:
        return hash_value % self._buckets_num

    def values(self):
        return self.Iterator(self._table, "values")

    def keys(self):
        return self.Iterator(self._table, "keys")

    def items(self):
        return self.Iterator(self._table)

    def _resize(self):
        self._entries_num = 0
        array = []
        self._buckets_num *= 2
        for item in self.items():
            array.append(item)
        self._table = []
        for i in range(self._buckets_num):
            self._table.append([])
        for i, element in enumerate(array):
            item = self.Entry(element[0], element[1])
            self.put(item.get_key(), item.get_value())

    def __contains__(self, item: int) -> bool:
        index = self._get_index(self._get_hash(item))
        for i, element in enumerate(self._table[index]):
            if element.get_key() == item:
                return True

        return False


stdin, stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
c_map = HashMap()
input_command = stdin.readlines()
res = []
for el in input_command:
    command = el.split()
    if command[0] == "put":
        c_map.put(*command[1:])
    elif command[0] == "get":
        res.append(c_map.get(*command[1:]))
    elif command[0] == "delete":
        c_map.delete(*command[1:])

stdout.write('\n'.join(res))
