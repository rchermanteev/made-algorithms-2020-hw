import sys


class Symbol:
    LIST_INT = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    DOT = "."
    MULTIPLY = "*"
    ADD = "+"
    SUBTRACT = "-"
    DIVIDE = "/"
    OPEN_PARENTHESIS = "("
    CLOSE_PARENTHESIS = ")"


class Lexer:
    def __init__(self, string: str):
        self.string = string
        self.current_position = 0

    def next_token(self) -> str:
        token = []
        if self.string[self.current_position] != Symbol.DOT:
            token.append(self.string[self.current_position])
            self.current_position += 1
            while (
                    self.string[self.current_position - 1] in Symbol.LIST_INT and
                    self.string[self.current_position] in Symbol.LIST_INT
            ):
                token.append(self.string[self.current_position])
                self.current_position += 1

        return "".join(token)


def main():
    base_string = sys.stdin.readline().rstrip()
    lex = Lexer(base_string)
    token = lex.next_token()
    while token:
        print(token)
        token = lex.next_token()


if __name__ == "__main__":
    main()
