"""
A. Минимум на стеке
ограничение по времени на тест2 секунды
ограничение по памяти на тест256 мегабайт
вводстандартный ввод
выводстандартный вывод
Вам требуется реализовать структуру данных, выполняющую следующие операции:

Добавить элемент x в конец структуры.
Удалить последний элемент из структуры.
Выдать минимальный элемент в структуре.
"""

import sys

from typing import Union


class Node:
    def __init__(self, value: int, next_node):
        self.value = value
        self.next_node = next_node


class LinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def get_size(self) -> int:
        return self._size

    def insert(self, value: int):
        if self._size == 0:
            new_node = Node(value, None)
            self._head, self._tail = new_node, new_node
        else:
            new_node = Node(value, self._tail)
            self._tail = new_node

        self._size += 1

    def erase(self):
        if self._size:
            if self._size == 1:
                self._tail = None
                self._head = None
            else:
                self._tail = self._tail.next_node

            self._size -= 1

    def back(self) -> Union[None, int]:
        if self._tail:
            return self._tail.value

        return None


class StackList(LinkedList):
    def __init__(self):
        super(StackList, self).__init__()
        self.min_list = LinkedList()

    def erase(self):
        er_el = self.back()
        super(StackList, self).erase()
        if er_el == self.min_list.back():
            self.min_list.erase()

    def insert(self, value: int):
        super(StackList, self).insert(value)
        if self.min_list.back() is None or value <= self.min_list.back():
            self.min_list.insert(value)

    def get_min_element(self) -> int:
        return self.min_list.back()


number_of_operations = int(sys.stdin.readline())
stack = StackList()
for _ in range(number_of_operations):
    operation = sys.stdin.readline().split()
    if operation[0] == '1':
        stack.insert(int(operation[1]))
    elif operation[0] == '2':
        stack.erase()
    elif operation[0] == '3':
        print(stack.get_min_element())
