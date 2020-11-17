import sys
from typing import Union, List, Tuple


class Node:
    def __init__(self, key: int):
        self.key = key
        self.left_leaf = None
        self.right_leaf = None


class BinarySearchTree:
    def __init__(self):
        self._root = None
        self._size = 0

    def get_size(self) -> int:
        return self._size

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

            return _node

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
                    _node.key = self._find_max(_node.left_leaf).key
                    _node.left_leaf = _delete(_node.left_leaf, _node.key)

            return _node

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
bst = BinarySearchTree()
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
