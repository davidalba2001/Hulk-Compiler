from lexer.lexer import Lexer
from parsers.lr1_parser import LR1Parser
from cmp.languages import HulkLang
from cmp.hulk_grammar import Hulk_G
from cmp.evaluation import evaluate_reverse_parse


def main():
    lexer = Lexer(HulkLang.lexer_table(), "eof")
    parser = LR1Parser(Hulk_G, debug=True)

    with open("src/tests/test.hulk", "r") as file:
        text = file.read()

    try:
        tokens = lexer(text)
        parse, operations = parser(tokens)
        ast = evaluate_reverse_parse(parse, operations, tokens)
    except SyntaxError as error:
        print(error)


if __name__ == "__main__":
    main()
