import sys

POWER_ALPHABET = 26
FIRST_SYMBOL_IN_ALPHABET = "a"


class Node:
    def __init__(self, is_terminal: bool, position_in_input: int):
        self.is_terminal = is_terminal
        self.position_in_input = position_in_input
        self.next = [None] * POWER_ALPHABET


class Trie:
    def __init__(self):
        self._trie = Node(False, -1)

    @staticmethod
    def _cust_ord(symbol: str) -> int:
        return ord(symbol) - ord(FIRST_SYMBOL_IN_ALPHABET)

    def insert(self, string: str, position_in_input: int):
        peak = self._trie
        for idx, symbol in enumerate(string):
            idx_symbol = self._cust_ord(symbol)
            if peak.next[idx_symbol] is None:
                peak.next[idx_symbol] = Node(False, -1)

            if idx == len(string) - 1:
                peak.next[idx_symbol].is_terminal = True
                peak.next[idx_symbol].position_in_input = position_in_input

            peak = peak.next[idx_symbol]

    def contains(self, string: str, start_peak=None):
        peak = start_peak or self._trie
        for symbol in string:
            idx_symbol = self._cust_ord(symbol)
            if peak.next[idx_symbol] is None:
                return -1, None, -1

            peak = peak.next[idx_symbol]

        if peak.is_terminal:
            return 1, peak, peak.position_in_input

        return 0, peak, peak.position_in_input


def main():
    text = sys.stdin.readline().rstrip()
    num_words = int(sys.stdin.readline())
    trie = Trie()
    for i in range(num_words):
        word = sys.stdin.readline().rstrip()
        trie.insert(word, i)

    result = ["No"] * num_words
    for i in range(len(text)):
        j = i
        cur_peak = None
        while j < len(text):
            answer, cur_peak, pos_on_input = trie.contains(text[j], cur_peak)
            if answer == -1:
                break
            elif answer == 1:
                result[pos_on_input] = "Yes"

            j += 1

    for check in result:
        print(check)


if __name__ == "__main__":
    main()
