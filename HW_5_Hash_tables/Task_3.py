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
    class Entry:
        def __init__(self, key: str, value: str):
            self.key = key
            self.value = value
            self._prev = None
            self._next = None

    def __init__(self, _buckets_num: int = 10 ** 6 * 2):
        self._buckets_num = _buckets_num
        self._table = [[] for _ in range(self._buckets_num)]
        self._entries_num = 0
        self._buckets_usd = 0
        self._last_added = None
        self._HASH_PARAM_A = 3
        self._HASH_PARAM_P = 1336337

    def get(self, key: str, default_value: str = 'none', flag: Union[None, str] = None) -> Union[None, str]:
        index = self._get_index(self._get_hash(key))
        if self.__contains__(key):
            for element in self._table[index]:
                if element.key == key:
                    if flag == 'prev':
                        if element._prev:
                            return element._prev.value

                        return default_value

                    elif flag == 'next':
                        if element._next:
                            return element._next.value

                        return default_value

                    return element.value
        else:
            return default_value

    def put(self, key: str, value: str):
        item = self.Entry(key, value)
        index = self._get_index(self._get_hash(key))
        if self._entries_num == 0:
            self._last_added = item

        if not self.__contains__(key):
            if self._entries_num != 0:
                self._last_added._next = item
                item._prev = self._last_added
                self._last_added = item

            self._entries_num += 1
            if len(self._table[index]) == 0:
                self._buckets_usd += 1

            self._table[index].append(item)
        else:
            for i, element in enumerate(self._table[index]):
                if element.key == item.key:
                    self._table[index][i].value = item.value

    def delete(self, key: str):
        index = self._get_index(self._get_hash(key))
        if self.__contains__(key):
            for i, element in enumerate(self._table[index]):
                if element.key == key:
                    if element._next and element._prev:
                        element._prev._next = element._next
                        element._next._prev = element._prev

                    elif element._prev and element._next is None:
                        element._prev._next = None
                        self._last_added = element._prev

                    elif element._prev is None and element._next:
                        element._next._prev = None

                    self._table[index].pop(i)
                    self._entries_num -= 1
                    if len(self._table[index]) == 0:
                        self._buckets_usd -= 1

                    break

    def _get_hash(self, key: str) -> int:
        _hash = 0
        for i in range(len(key)):
            _hash = (_hash * self._HASH_PARAM_A + ord(key[i]) - ord('a')) % self._HASH_PARAM_P

        return _hash

    def _get_index(self, hash_value: int) -> int:
        return hash_value % self._buckets_num

    def __contains__(self, item) -> bool:
        index = self._get_index(self._get_hash(item))
        for i, element in enumerate(self._table[index]):
            if element.key == item:
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
    elif command[0] == "prev":
        res.append(c_map.get(*command[1:], flag='prev'))
    elif command[0] == "next":
        res.append(c_map.get(*command[1:], flag='next'))

stdout.write('\n'.join(res))
