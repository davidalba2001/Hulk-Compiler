from lexer.lexer import Lexer
from parsers.clr1_parser import LR1Parser
from cmp.languages import Hulk
from cmp.hulk_grammar_copy import Hulk_G
from cmp.evaluation import evaluate_reverse_parse

lexer = Lexer(Hulk.lexer_table(),'eof')

with open('src/test/test1.hulk','r') as file:
    text = file.read()

tokens = lexer(text)
print(tokens)
parser = LR1Parser(Hulk_G, 'Hulk_G', True)
parser._build_parsing_table()
parse, operations = parser(tokens)
ast = evaluate_reverse_parse(parse, operations, tokens)
    
print(ast)
