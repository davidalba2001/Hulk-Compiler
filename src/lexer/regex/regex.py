from parsers.lr1_parser import LR1Parser
from cmp.automata import nfa_to_dfa, automata_minimization , DFA
from cmp.evaluation import evaluate_reverse_parse
from cmp.utils import Token
from cmp.regex_grammar import G_Regex


tag_symbol = {'QUESTION': '?','DOT': '.','PLUS': '+','PIPE': '|','STAR': '*','MINUS': '-','CARET': '^',
        'OPAR': '(','CPAR': ')','OBRCKT': '[','CBRCKT': ']','EPSILON': 'ε','DOLLAR': '$','OBRACE': '{','CBRACE': '}'
                  }

parser_Regex = LR1Parser(G_Regex)

class Regex:
    def __init__(self, pattern,skip_whitespaces= True):
        tokens:list[Token] = regex_tokenizer(pattern,G_Regex,skip_whitespaces)
        self.automaton:DFA = build_automaton(tokens)

def build_automaton(tokens:list[Token]):
    
    parse, operations = parser_Regex(tokens)
    ast = evaluate_reverse_parse(parse, operations, tokens)
    nfa = ast.evaluate()
    dfa = nfa_to_dfa(nfa)
    #mini = automata_minimization(dfa)
    return dfa

def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []
    fixed_tokens = {tag_symbol[str(terminal)]: Token(tag_symbol[str(terminal)], terminal) for terminal in G.terminals if str(terminal) != 'SYMBOL'}
    special_char = False
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        elif special_char:
            token = Token(char, G['SYMBOL'])
            special_char = False            
        elif char == '\\':
            special_char = True
            continue 
        else:
            try:
                token = fixed_tokens[char]
            except:
                token = Token(char, G['SYMBOL'])
        tokens.append(token)
    tokens.append(Token('$', G.EOF))
    return tokens






