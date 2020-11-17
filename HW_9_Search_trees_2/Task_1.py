import sys
from random import randint
from typing import List, Tuple, Union


class Node:
    def __init__(self, key: int, priority: int = None):
        self.key = key
        self.priority = priority
        self.left_leaf = None
        self.right_leaf = None
        self.height = 1


class CartesianTree:
    def __init__(self):
        self._root = None
        self._size = 0
        self._START_RANDOM_NUMBER = 0
        self._END_RANDOM_NUMBER = 10 ** 5

    def get_size(self) -> int:
        return self._size

    @staticmethod
    def merge(left_cart_tree, right_cart_tree):
        if left_cart_tree is None:
            return right_cart_tree

        if right_cart_tree is None:
            return left_cart_tree

        if left_cart_tree.priority > right_cart_tree.priority:
            left_cart_tree.right_leaf = CartesianTree.merge(
                left_cart_tree.right_leaf,
                right_cart_tree
            )
            return left_cart_tree
        else:
            right_cart_tree.left_leaf = CartesianTree.merge(
                left_cart_tree,
                right_cart_tree.left_leaf
            )
            return right_cart_tree

    @staticmethod
    def split(cart_tree, key):
        if cart_tree is None:
            return None, None

        if cart_tree.key > key:
            t1, t2 = CartesianTree.split(cart_tree.left_leaf, key)
            cart_tree.left_leaf = t2

            return t1, cart_tree
        else:
            t1, t2 = CartesianTree.split(cart_tree.right_leaf, key)
            cart_tree.right_leaf = t1

            return cart_tree, t2

    def print_tree(self):
        def _print_tree(_node, shift=""):
            if _node is not None:
                _print_tree(_node.left_leaf, shift=shift + "  ")
                print(f"{shift}{_node.key}")
                _print_tree(_node.right_leaf, shift=shift + "  ")

        _print_tree(self._root)

    def search(self, key: int):
        def _search(_node, _key: int):
            if _node is None:
                return None

            if _node.key == _key:
                return _node
            elif _node.key > _key:
                return _search(_node.left_leaf, _key)
            else:
                return _search(_node.right_leaf, _key)

        return _search(self._root, key)

    def insert(self, key: int):
        if self.search(key):
            return None

        new_node = Node(
            key,
            randint(self._START_RANDOM_NUMBER, self._END_RANDOM_NUMBER)
        )
        t1, t2 = self.split(self._root, key)
        self._size += 1
        self._root = CartesianTree.merge(CartesianTree.merge(t1, new_node), t2)

    def delete(self, key: int):
        if self.search(key) is None:
            return None

        t1, t2 = CartesianTree.split(self._root, key - 1)
        del_node, t2 = CartesianTree.split(t2, key)
        self._size -= 1
        self._root = CartesianTree.merge(t1, t2)

    def exists(self, key: int) -> str:
        return 'true' if self.search(key) else 'false'

    def next(self, key: int) -> Union[int, str]:
        v, res = self._root, None
        while v is not None:
            if v.key > key:
                res = v
                v = v.left_leaf
            else:
                v = v.right_leaf

        return res.key if res else 'none'

    def prev(self, key: int) -> Union[int, str]:
        v, res = self._root, None
        while v is not None:
            if v.key < key:
                res = v
                v = v.right_leaf
            else:
                v = v.left_leaf

        return res.key if res else 'none'


def transform(req: List[str]) -> Tuple[str, int]:
    return req[0], int(req[1])


requests = [transform(dirty_request.strip().split()) for dirty_request in sys.stdin.readlines()]
ct = CartesianTree()
for command, value in requests:
    if command == "insert":
        ct.insert(value)
    elif command == "exists":
        print(ct.exists(value))
    elif command == "prev":
        print(ct.prev(value))
    elif command == "next":
        print(ct.next(value))
    elif command == "delete":
        ct.delete(value)
