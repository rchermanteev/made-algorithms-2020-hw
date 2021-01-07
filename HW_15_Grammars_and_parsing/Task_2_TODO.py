import sys


class Symbol:
    LIST_INT = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    MORE = ">"
    LESS = "<"
    EQUALLY = "="
    MORE_OR_EQUAL = ">="
    LESS_OR_EQUAL = "<="
    DOT = "."
    MULTIPLY = "*"
    ADD = "+"
    SUBTRACT = "-"
    DIVIDE = "/"
    OPEN_PARENTHESIS = "("
    CLOSE_PARENTHESIS = ")"
    OPERATIONS = [
        ADD, SUBTRACT, DIVIDE, MULTIPLY
    ]


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


class ParseTreeNode:
    def __init__(self):
        self.content = [None, None, None]

    @staticmethod
    def _result_operation(x, operation, y):
        x, y = int(x), int(y)
        if operation == Symbol.ADD:
            return x + y
        elif operation == Symbol.SUBTRACT:
            return x - y
        elif operation == Symbol.DIVIDE:
            return x / y
        elif operation == Symbol.MULTIPLY:
            return x * y

    def evaluate(self):
        if self.content[0] and self.content[1] and self.content[2]:
            return self._result_operation(*self.content)
        elif self.content[0]:
            return self.content[0]


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.next_token()

    def parse(self):
        if self.current_token == "":
            return None

        node = ParseTreeNode()
        if not self.current_token.isdigit() and self.current_token != Symbol.OPEN_PARENTHESIS:
            raise ValueError("Ожидалось другое значение токена")

        if self.current_token == Symbol.OPEN_PARENTHESIS:
            self.current_token = self.lexer.next_token()
            node.content[0] = self.parse()
            if self.current_token != Symbol.CLOSE_PARENTHESIS:
                raise ValueError("Ожидалось другое значение токена")
        else:
            node.content[0] = self.current_token

        self.current_token = self.lexer.next_token()
        if self.current_token == "" or self.current_token == Symbol.CLOSE_PARENTHESIS:
            return node.evaluate()

        if self.current_token not in Symbol.OPERATIONS:
            raise ValueError("Ожидалось другое значение токена")

        node.content[1] = self.current_token
        self.current_token = self.lexer.next_token()
        node.content[2] = self.parse()

        return node


def main():
    base_string = sys.stdin.readline().rstrip()
    lex = Lexer(base_string)
    parser = Parser(lex)
    try:
        res = parser.parse()
        print(res.content)
    except ValueError:
        print("WRONG")


if __name__ == "__main__":
    main()


# tests
# (1+1)+(1+1).
# ((1+1)+1)+(1+1).
