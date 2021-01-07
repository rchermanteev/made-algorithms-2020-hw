import sys

from typing import List


def z_function(string: str) -> List[int]:
    len_string = len(string)
    z = [0] * len_string
    left, right = 0, 0
    for i in range(1, len_string):
        z[i] = max(0, min(right - i, z[i - left]))
        while i + z[i] < len_string and string[z[i]] == string[z[i] + i]:
            z[i] += 1

        if i + z[i] > right:
            left = i
            right = i + z[i]

    return z


def main():
    base_string = sys.stdin.readline().rstrip()
    print(" ".join(map(str, z_function(base_string)[1:])))


if __name__ == '__main__':
    main()
