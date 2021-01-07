import sys


class PolynomialHash:
    def __init__(self, string):
        self._string = string
        self._hash = [0] * len(string)
        self._pow = [0] * len(string)
        self._HASH_PARAM_A = 83
        self._HASH_PARAM_P = 1000001501
        self._setup_polynomial_hash()

    def _setup_polynomial_hash(self):
        self._hash[0] = ord(self._string[0])
        self._pow[0] = 1
        for i in range(1, len(self._string)):
            self._hash[i] = (
                    (self._hash[i - 1] * self._HASH_PARAM_A + ord(self._string[i])) % self._HASH_PARAM_P
            )
            self._pow[i] = (self._pow[i - 1] * self._HASH_PARAM_A) % self._HASH_PARAM_P

    def _get_hash(self, start_substr: int, end_substr: int,):
        if start_substr == 0:
            return self._hash[end_substr]

        _hash = (
                (self._hash[end_substr] - (self._hash[start_substr - 1] * self._pow[end_substr - start_substr + 1]) %
                 self._HASH_PARAM_P + self._HASH_PARAM_P) % self._HASH_PARAM_P
        )

        return _hash

    def get_base_string(self) -> str:
        return self._string

    def compare_substring(
            self,
            start_first_substr: int,
            end_first_substr: int,
            start_second_substr: int,
            end_second_substr: int
    ) -> bool:
        _hash_first_substr = self._get_hash(start_first_substr, end_first_substr)
        _hash_second_substr = self._get_hash(start_second_substr, end_second_substr)

        return _hash_first_substr == _hash_second_substr


def main():
    base_string = sys.stdin.readline().strip()
    num_requests = int(sys.stdin.readline())
    requests = []
    for _ in range(num_requests):
        requests.append(list(map(lambda x: int(x) - 1, sys.stdin.readline().split())))

    ph_str = PolynomialHash(base_string)
    for request in requests:
        if ph_str.compare_substring(*request):
            print("Yes")
        else:
            print("No")


if __name__ == "__main__":
    main()
