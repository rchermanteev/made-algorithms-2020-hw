import sys

from typing import Union


class ArrayQueue:
    def __init__(self):
        self.begin = 0
        self.end = 0
        self.capacity = 4
        self.elements = [None] * 4

    def size(self) -> int:
        return (self.end - self.begin) % self.capacity

    def add(self, value: int):
        if (self.end + 1) % self.capacity == self.begin:
            self.ensure_capacity()
            self.elements[self.size()] = value
        else:
            self.elements[self.end] = value

        self.end = (self.end + 1) % self.capacity

    def ensure_capacity(self):
        new_elements = [None] * self.capacity * 2
        for i in range(self.capacity):
            new_elements[i] = self.elements[(self.begin + i) % self.capacity]

        self.begin = 0
        self.end = self.capacity - 1
        self.capacity *= 2
        self.elements = new_elements.copy()

    def front(self) -> Union[None, int]:
        return self.elements[self.begin % self.capacity]

    def pop(self) -> Union[None, int]:
        del_el = self.front()
        if self.size() > 0:
            self.elements[self.begin] = None
            self.begin = (self.begin + 1) % self.capacity

        if self.end == self.begin:
            self.begin, self.end = 0, 0

        if self.size() <= self.capacity // 4 and self.capacity > 4:
            self.decrease_capacity()

        return del_el

    def decrease_capacity(self):
        prev_capacity = self.capacity
        _size = self.size()
        self.capacity //= 2
        new_elements = [None] * self.capacity
        for i in range(_size):
            new_elements[i] = self.elements[(self.begin + i) % prev_capacity]

        self.end = _size
        self.begin = 0
        self.elements = new_elements.copy()


queue = ArrayQueue()
number_of_operations = int(sys.stdin.readline())
result = []
for _ in range(number_of_operations):
    input_data = sys.stdin.readline().split()
    if input_data[0] == "+":
        queue.add(int(input_data[1]))
    if input_data[0] == "-":
        result.append(queue.pop())

for el in result:
    print(el)
