from lexer.lexer import Lexer
from parsers.lr1_parser import LR1Parser
from cmp.languages import Hulk
from cmp.hulk_grammar_copy import Hulk_G
from cmp.evaluation import evaluate_reverse_parse


def main():
    lexer = Lexer(Hulk.lexer_table(), "eof")
    parser = LR1Parser(Hulk_G)
    parser._build_parsing_table()

    with open("src/test/test1.hulk", "r") as file:
        text = file.read()

    try:
        tokens = lexer(text)
        parse, operations = parser(tokens)
        ast = evaluate_reverse_parse(parse, operations, tokens)
    except SyntaxError as error:
        print(error)


# Solo se ejecuta cuando este archivo se ejecuta directamente
if __name__ == "__main__":
    main()
