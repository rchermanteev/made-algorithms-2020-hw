import sys
from typing import List, Tuple, Union


class Node:
    def __init__(self, key: int):
        self.key = key
        self.left_leaf = None
        self.right_leaf = None
        self.height = 1


class BalancedBinarySearchTree:
    def __init__(self):
        self._root = None
        self._size = 0

    def get_size(self) -> int:
        return self._size

    @staticmethod
    def get_height(node):
        return node.height if node else 0

    def fix(self, node):
        hl = self.get_height(node.left_leaf)
        hr = self.get_height(node.right_leaf)

        node.height = (hl if hl > hr else hr) + 1

    def get_balancing_factor(self, node) -> int:
        return self.get_height(node.right_leaf) - self.get_height(node.left_leaf)

    def do_small_right_rotate(self, p):
        q = p.left_leaf
        p.left_leaf = q.right_leaf
        q.right_leaf = p
        self.fix(p)
        self.fix(q)
        return q

    def do_small_left_rotate(self, q):
        p = q.right_leaf
        q.right_leaf = p.left_leaf
        p.left_leaf = q
        self.fix(q)
        self.fix(p)
        return p

    def balance(self, node):
        self.fix(node)
        balancing_factor = self.get_balancing_factor(node)
        if balancing_factor == 2:
            if self.get_balancing_factor(node.right_leaf) < 0:
                node.right_leaf = self.do_small_right_rotate(node.right_leaf)

            return self.do_small_left_rotate(node)

        elif balancing_factor == -2:
            if self.get_balancing_factor(node.left_leaf) > 0:
                node.left_leaf = self.do_small_left_rotate(node.left_leaf)

            return self.do_small_right_rotate(node)

        return node

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
        def _insert(_node, _key: int):
            if _node is None:
                self._size += 1
                return Node(_key)

            if _node.key > _key:
                _node.left_leaf = _insert(_node.left_leaf, _key)
            elif _node.key < _key:
                _node.right_leaf = _insert(_node.right_leaf, _key)

            return self.balance(_node)

        self._root = _insert(self._root, key)

    @staticmethod
    def _find_max(_node):
        while _node.right_leaf is not None:
            _node = _node.right_leaf

        return _node

    def delete(self, key: int):
        def _delete(_node, _key: int):
            if _node is None:
                return None

            if _node.key < _key:
                _node.right_leaf = _delete(_node.right_leaf, _key)
            elif _node.key > _key:
                _node.left_leaf = _delete(_node.left_leaf, _key)
            else:
                if _node.left_leaf is None and _node.right_leaf is None:
                    self._size -= 1
                    _node = None
                elif _node.left_leaf is None:
                    self._size -= 1
                    _node = _node.right_leaf
                elif _node.right_leaf is None:
                    self._size -= 1
                    _node = _node.left_leaf
                else:
                    max_ = self._find_max(_node.left_leaf)
                    _node.key = max_.key
                    _node.left_leaf = _delete(_node.left_leaf, _node.key)

            return self.balance(_node) if _node else _node

        self._root = _delete(self._root, key)

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
bst = BalancedBinarySearchTree()
for command, value in requests:
    if command == "insert":
        bst.insert(value)
    elif command == "exists":
        print(bst.exists(value))
    elif command == "prev":
        print(bst.prev(value))
    elif command == "next":
        print(bst.next(value))
    elif command == "delete":
        bst.delete(value)
