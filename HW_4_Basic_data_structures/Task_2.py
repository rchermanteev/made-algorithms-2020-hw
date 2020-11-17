from typing import Union


class ArrayList:
    def __init__(self):
        self.size = 0
        self.capacity = 4
        self.elements = [None] * 4

    def get(self, idx: int) -> Union[None, int]:
        if 0 <= idx < self.size:
            return self.elements[idx]

    def add(self, value: int):
        if self.size + 1 > self.capacity:
            self.ensure_capacity()

        self.elements[self.size] = value
        self.size += 1

    def pop(self) -> Union[None, int]:
        del_el = None
        if self.size > 0:
            del_el = self.get(self.size - 1)
            self.size -= 1
            self.elements[self.size] = None

        if self.size <= self.capacity / 4 and self.capacity > 4:
            self.decrease_capacity()

        return del_el

    def ensure_capacity(self):
        self.capacity *= 2
        new_elements = [None] * self.capacity
        for i in range(self.size):
            new_elements[i] = self.elements[i]

        self.elements = new_elements

    def decrease_capacity(self):
        self.capacity //= 2
        new_elements = [None] * self.capacity
        for i in range(self.size):
            new_elements[i] = self.elements[i]

        self.elements = new_elements


class ArrayStack(ArrayList):
    def __init__(self):
        super(ArrayStack, self).__init__()

    def add(self, value: int):
        if type(value) != int:
            el_2 = self.pop()
            el_1 = self.pop()
            if el_1 is not None and el_2 is not None:
                if value == "+":
                    self.add(el_1 + el_2)
                elif value == "-":
                    self.add(el_1 - el_2)
                elif value == "*":
                    self.add(el_1 * el_2)
            else:
                raise ValueError
        else:
            super(ArrayStack, self).add(value)


input_data = map(lambda x: int(x) if x.isdigit() else x, input().split())
arr_stack = ArrayStack()
for el in input_data:
    arr_stack.add(el)

print(arr_stack.get(0))
