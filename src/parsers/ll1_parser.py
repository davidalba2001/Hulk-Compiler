import sys
import os

# Obtener la ruta del directorio actual (por ejemplo, ll1_parser.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Subir tres niveles para llegar a la raíz del proyecto
project_root = os.path.abspath(os.path.join(current_dir, '../../..'))

# Agregar 'src/parsers/parser_utils' a sys.path para que Python pueda encontrar el módulo 'parser_utils'
parser_utils_path = os.path.join(project_root, 'src/parsers')
sys.path.append(parser_utils_path)

try:
    from parser_utils.first import compute_firsts
    from parser_utils.follow import compute_follows
    from parser_utils.parsing_table import build_parsing_table
    from cmp.pycompiler import Grammar
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")


def build_non_recursive_predictive_parser(G:Grammar, M=None, firsts=None, follows=None):
    
    # checking table...
    if M is None:
        if firsts is None:
            firsts = compute_firsts(G)
        if follows is None:
            follows = compute_follows(G, firsts)
        M = build_parsing_table(G, firsts, follows)
    
    
    # parser construction...
    def parser(w):
        
        # init:
        stack = [G.EOF,G.startSymbol]
        index = 0
        left_parse = []

        while True:
            top = stack.pop()
            term = w[index]
            
            if top == G.EOF:
                if term == G.EOF:
                    break  # Successful parsing
                else:
                    raise ValueError("Parsing error: input not fully consumed at EOF")
            
            elif top in G.terminals:
                if top == term:
                    index += 1
                else:
                    raise ValueError(f"Parsing error: expected {top} but found {term}")
            
            
            elif top in G.nonTerminals:
                if (top,term) in M:
                    production = M[(top, term)][0]
                    left_parse.append(production)
                    for symbol in reversed(production.Right):
                        if not symbol.IsEpsilon:
                            stack.append(symbol)
                else:
                    raise ValueError(f"Parsing error: no production for ({top}, {term}) in parsing table")
            else:
                raise ValueError(f"Parsing error: unrecognized symbol {top} on stack")
        
        if index != len(w) - 1:  # Ensure the input is fully consumed
            raise ValueError("Parsing error: input not fully consumed")
        
        # left parse is ready!!!
        return left_parse
    
    # parser is ready!!!
    return parser
    
G = Grammar()
E = G.NonTerminal('E', True)
T,F,X,Y = G.NonTerminals('T F X Y')
plus, minus, star, div, opar, cpar, num = G.Terminals('+ - * / ( ) num')
E %= T + X
X %= plus + T + X | minus + T + X | G.Epsilon
T %= F + Y
Y %= star + F + Y | div + F + Y | G.Epsilon
F %= num | opar + E + cpar

build_non_recursive_predictive_parser(G)