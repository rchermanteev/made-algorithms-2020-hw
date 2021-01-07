import sys


class Trie:
    def __init__(self):
        self._trie = {}

    def insert(self, string, position_in_input):
        peak = self._trie
        for idx, symbol in enumerate(string):
            if peak.get(symbol) is None:
                peak[symbol] = [{}, False, -1]

            if idx == len(string) - 1:
                peak[symbol][1] = True
                peak[symbol][2] = position_in_input

            peak = peak[symbol][0]

    def contains(self, string, start_peak=None):
        peak = start_peak or self._trie
        is_term = False
        position_in_input = -1
        for symbol in string:
            if peak.get(symbol) is None:
                return -1, None, -1

            peak, is_term, position_in_input = peak[symbol]

        if is_term:
            return 1, peak, position_in_input

        return 0, peak, position_in_input


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
