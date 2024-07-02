import sys
import os

# Obtener la ruta del directorio actual (por ejemplo, donde se encuentra este script)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Subir tres niveles para llegar a la raíz del proyecto
project_root = os.path.abspath(os.path.join(current_dir, '../../..'))

# Agregar 'src/parsers' a sys.path para que Python pueda encontrar el módulo 'll1_parser'
parsers_path = os.path.join(project_root, 'src/parsers')
sys.path.append(parsers_path)

print(f"sys.path: {sys.path}")

try:
    from ll1_parser import build_non_recursive_predictive_parser
    from cmp.automata import nfa_to_dfa, automata_minimization
    from cmp.evaluation import evaluate_parse
    from cmp.utils import Token
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")


class Regex:
    def __init__(self, pattern : str):
        tokens = regex_tokenizer(pattern)
        self.automaton = build_automaton(tokens)

def build_automaton(tokens):
    parser = build_non_recursive_predictive_parser(G)
    left_parse = parser(tokens)
    ast = evaluate_parse(left_parse, tokens)
    nfa = ast.evaluate()
    dfa = nfa_to_dfa(nfa)
    mini = automata_minimization(dfa)

def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []
    fixed_tokens = {lex: Token(lex, G[lex]) for lex in '| * ( ) ε'.split() }
    special_char = False
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        elif special_char:
            token = Token(char, G['symbol'])
            special_char = False            
        elif char == '\\':
            special_char = True
            continue 
        else:
            try:
                token = fixed_tokens[char]
            except:
                token = Token(char, G['symbol'])
        tokens.append(token)
        
    tokens.append(Token('$', G.EOF))
    return tokens







