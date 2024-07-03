from lexer.lexer import Lexer
from parsers.clr1_parser import LR1Parser
from cmp.languages import Hulk
from cmp.hulk_grammar import Hulk_G
from cmp.evaluation import evaluate_reverse_parse

lexer = Lexer(Hulk.lexer_table(),'eof')
parser = LR1Parser(Hulk_G,'Hulk_G')

with open('..test/test.hulk','r') as file:
    text = file.read()

tokens = lexer(text)

parse, operations = parser(tokens)
ast = evaluate_reverse_parse(parse, operations, tokens)
    

