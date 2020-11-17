import sys
from random import randint
from typing import List, Tuple


class Node:
    def __init__(self, value: int, priority: int = None):
        self.value = value
        self.priority = priority
        self.left_leaf = None
        self.right_leaf = None
        self.height = 1
        self.size = 1

    @staticmethod
    def get_leaf_size(leaf):
        return leaf.size if leaf else 0

    def fix_size(self):
        self.size = (
                self.get_leaf_size(self.left_leaf) +
                self.get_leaf_size(self.right_leaf) + 1
        )


class CartesianTreeWithImplicitKey:
    def __init__(self):
        self._root = None
        self._size = 0
        self._START_RANDOM_NUMBER = 0
        self._END_RANDOM_NUMBER = 10 ** 5

    def get_size(self) -> int:
        return self._size

    @staticmethod
    def merge(left_cart_tree_node, right_cart_tree_node):
        if left_cart_tree_node is None:
            return right_cart_tree_node

        if right_cart_tree_node is None:
            return left_cart_tree_node

        if left_cart_tree_node.priority > right_cart_tree_node.priority:
            left_cart_tree_node.right_leaf = CartesianTreeWithImplicitKey.merge(
                left_cart_tree_node.right_leaf,
                right_cart_tree_node
            )
            left_cart_tree_node.fix_size()

            return left_cart_tree_node
        else:
            right_cart_tree_node.left_leaf = CartesianTreeWithImplicitKey.merge(
                left_cart_tree_node,
                right_cart_tree_node.left_leaf
            )
            right_cart_tree_node.fix_size()

            return right_cart_tree_node

    @staticmethod
    def split(cart_tree_node, key: int):
        if cart_tree_node is None:
            return None, None

        if cart_tree_node.get_leaf_size(cart_tree_node.left_leaf) > key:
            t1, t2 = CartesianTreeWithImplicitKey.split(
                cart_tree_node.left_leaf,
                key
            )
            cart_tree_node.left_leaf = t2
            cart_tree_node.fix_size()

            return t1, cart_tree_node
        else:
            t1, t2 = CartesianTreeWithImplicitKey.split(
                cart_tree_node.right_leaf,
                key - cart_tree_node.get_leaf_size(cart_tree_node.left_leaf) - 1
            )
            cart_tree_node.right_leaf = t1
            cart_tree_node.fix_size()

            return cart_tree_node, t2

    def print_tree(self):
        def _print_tree(_node, shift=""):
            if _node is not None:
                _print_tree(_node.left_leaf, shift=shift + "  ")
                print(f"{shift}{_node.value}")
                _print_tree(_node.right_leaf, shift=shift + "  ")

        _print_tree(self._root)

    def get_array(self) -> List[int]:
        def _get_array(_node, _arr):
            if _node is not None:
                _get_array(_node.left_leaf, _arr)
                _arr.append(_node.value)
                _get_array(_node.right_leaf, _arr)

        arr = []
        _get_array(self._root, arr)

        return arr

    def search(self, key: int):
        def _search(_node, _key: int):
            if _node is None:
                return None

            if _node.get_leaf_size(_node.left_leaf) == _key:
                return _node
            elif _node.get_leaf_size(_node.left_leaf) > _key:
                return _search(_node.left_leaf, _key)
            else:
                return _search(_node.right_leaf, _key)

        return _search(self._root, key)

    def insert(self, key: int, value: int):
        new_node = Node(
            value,
            randint(self._START_RANDOM_NUMBER, self._END_RANDOM_NUMBER)
        )
        t1, t2 = self.split(self._root, key)
        self._size += 1
        self._root = CartesianTreeWithImplicitKey.merge(
            CartesianTreeWithImplicitKey.merge(t1, new_node),
            t2
        )

    def delete(self, key: int):
        t1, t2 = CartesianTreeWithImplicitKey.split(self._root, key)
        t11, del_node = CartesianTreeWithImplicitKey.split(t1, key - 1)
        self._size -= 1
        self._root = CartesianTreeWithImplicitKey.merge(t11, t2)

    def move_segment_to_begin(self, left_idx: int, right_idx: int):
        left_idx, right_idx = left_idx - 1, right_idx - 1
        t1, t2 = CartesianTreeWithImplicitKey.split(self._root, left_idx - 1)
        t21, t22 = CartesianTreeWithImplicitKey.split(t2, right_idx - left_idx)
        self._root = CartesianTreeWithImplicitKey.merge(
            CartesianTreeWithImplicitKey.merge(t21, t1),
            t22
        )


def transform(req: List[str]) -> Tuple[int, int]:
    return int(req[0]), int(req[1])


len_array, count_requests = map(int, sys.stdin.readline().split())
array = [i for i in range(1, len_array + 1)]
requests = [transform(sys.stdin.readline().strip().split()) for _ in range(count_requests)]
ct = CartesianTreeWithImplicitKey()
for _key, _value in enumerate(array):
    ct.insert(_key, _value)

for left, right in requests:
    ct.move_segment_to_begin(left, right)

print(" ".join(map(str, ct.get_array())))
