from cmp.pycompiler import Sentence, Production
from cmp.utils import ContainerSet, Token, UnknownToken
from cmp.parsing import build_parsing_table


class HulkLang:
    @staticmethod
    def lexer_table():
        return {
            "NUMBER_LITERAL": "[0-9]+(\\.[0-9]+)?",
            "FUNCTION_KEYWORD": "function",
            "LET_KEYWORD": "let",
            "IN_KEYWORD": "in",
            "IF_KEYWORD": "if",
            "ELIF_KEYWORD": "elif",
            "ELSE_KEYWORD": "else",
            "TRUE_KEYWORD": "true",
            "FALSE_KEYWORD": "false",
            "WHILE_KEYWORD": "while",
            "FOR_KEYWORD": "for",
            "TYPE_KEYWORD": "type",
            "NEW_KEYWORD": "new",
            "INHERITS_KEYWORD": "inherits",
            "IS_KEYWORD": "is",
            "AS_KEYWORD": "as",
            "PROTOCOL_KEYWORD": "protocol",
            "EXTENDS_KEYWORD": "extends",
            "IDENTIFIER": "[a-zA-Z_][a-zA-Z0-9_]*",
            "BOOLEAN_LITERAL": "true|false",
            "STRING_LITERAL": '"([^"\\\\]|\\\\.ε)*" | \'([^\'\\\\]|\\\\.ε)*\'',
            "PLUS": "\\+",
            "MINUS": "\\-",
            "MULTIPLY": "\\*",
            "PERCENT": "%",
            "DIVIDE": "/",
            "POWER": "\\^",
            "LESS_THAN": "<",
            "GREATER_THAN": ">",
            "LESS_EQUAL": "<=",
            "GREATER_EQUAL": ">=",
            "EQUAL": "==",
            "NOT_EQUAL": "!=",
            "AND_OP": "&",
            "PIPE": "\\|",
            "NOT_OP": "!",
            "PAREN_OPEN": "\\(",
            "PAREN_CLOSE": "\\)",
            "BRACE_OPEN": "\\{",
            "BRACE_CLOSE": "\\}",
            "SQUARE_BRACKET_OPEN": "\\[",
            "SQUARE_BRACKET_CLOSE": "\\]",
            "COMMA": ",",
            "SEMICOLON": ";",
            "AT_SYMBOL": "@",
            "AT_AT_SYMBOL": "@@",
            "ARROW": "=>",
            "ASSIGN": "=",
            "DASSIGN": ":=",
            "COLON": ":",
            "DOT": "\\.",
            "DOUBLE_PIPE": "\\|\\|",
        }


class RegexLang:
    @staticmethod
    def lexer_table():
        return {'QUESTION': '?',
                'DOT': '.',
                'PLUS': '+',
                'PIPE': '|',
                'STAR': '*',
                'MINUS': '-',
                'CARET': '^',
                'OPAR': '(',
                'CPAR': ')',
                'OBRCKT': '[',
                'CBRCKT': ']',
                'EPSILON': 'ε',
                'DOLLAR': '$',
                'OBRACE': '{',
                'CBRACE': '}'
                }


# ================================
# DEPRECATED CODE BELOW
# ================================
# This code has been replaced and should no longer be used.
# It is kept here for reference, in case any ideas need to be revisited
# or useful parts need to be reused in the future.
# ================================

# class BasicHulk:
#     def __init__(self, G):
#         self.G = G
#         self.fixed_tokens = {lex: Token(lex, G[lex]) for lex in '+ - * / ( )'.split()}

#     @property
#     def firsts(self):
#         G = self.G
#         return {
#             G['+']: ContainerSet(G['+'], contains_epsilon=False),
#             G['-']: ContainerSet(G['-'], contains_epsilon=False),
#             G['*']: ContainerSet(G['*'], contains_epsilon=False),
#             G['/']: ContainerSet(G['/'], contains_epsilon=False),
#             G['(']: ContainerSet(G['('], contains_epsilon=False),
#             G[')']: ContainerSet(G[')'], contains_epsilon=False),
#             G['num']: ContainerSet(G['num'], contains_epsilon=False),
#             G['E']: ContainerSet(G['num'], G['('], contains_epsilon=False),
#             G['T']: ContainerSet(G['num'], G['('], contains_epsilon=False),
#             G['F']: ContainerSet(G['num'], G['('], contains_epsilon=False),
#             G['X']: ContainerSet(G['-'], G['+'], contains_epsilon=True),
#             G['Y']: ContainerSet(G['/'], G['*'], contains_epsilon=True),
#             Sentence(G['T'], G['X']): ContainerSet(G['num'], G['('], contains_epsilon=False),
#             Sentence(G['+'], G['T'], G['X']): ContainerSet(G['+'], contains_epsilon=False),
#             Sentence(G['-'], G['T'], G['X']): ContainerSet(G['-'], contains_epsilon=False),
#             G.Epsilon: ContainerSet(contains_epsilon=True),
#             Sentence(G['F'], G['Y']): ContainerSet(G['num'], G['('], contains_epsilon=False),
#             Sentence(G['*'], G['F'], G['Y']): ContainerSet(G['*'], contains_epsilon=False),
#             Sentence(G['/'], G['F'], G['Y']): ContainerSet(G['/'], contains_epsilon=False),
#             Sentence(G['num']): ContainerSet(G['num'], contains_epsilon=False),
#             Sentence(G['('], G['E'], G[')']): ContainerSet(G['('], contains_epsilon=False)
#         }

#     @property
#     def follows(self):
#         G = self.G
#         return {
#             G['E']: ContainerSet(G[')'], G.EOF, contains_epsilon=False),
#             G['T']: ContainerSet(G[')'], G['-'], G.EOF, G['+'], contains_epsilon=False),
#             G['F']: ContainerSet(G['-'], G.EOF, G['*'], G['/'], G[')'], G['+'], contains_epsilon=False),
#             G['X']: ContainerSet(G[')'], G.EOF, contains_epsilon=False),
#             G['Y']: ContainerSet(G[')'], G['-'], G.EOF, G['+'], contains_epsilon=False)
#         }

#     @property
#     def table(self):
#         G = self.G
#         return {
#             (G['E'], G['num'], ): [Production(G['E'], Sentence(G['T'], G['X'])), ],
#             (G['E'], G['('], ): [Production(G['E'], Sentence(G['T'], G['X'])), ],
#             (G['X'], G['+'], ): [Production(G['X'], Sentence(G['+'], G['T'], G['X'])), ],
#             (G['X'], G['-'], ): [Production(G['X'], Sentence(G['-'], G['T'], G['X'])), ],
#             (G['X'], G[')'], ): [Production(G['X'], G.Epsilon), ],
#             (G['X'], G.EOF, ): [Production(G['X'], G.Epsilon), ],
#             (G['T'], G['num'], ): [Production(G['T'], Sentence(G['F'], G['Y'])), ],
#             (G['T'], G['('], ): [Production(G['T'], Sentence(G['F'], G['Y'])), ],
#             (G['Y'], G['*'], ): [Production(G['Y'], Sentence(G['*'], G['F'], G['Y'])), ],
#             (G['Y'], G['/'], ): [Production(G['Y'], Sentence(G['/'], G['F'], G['Y'])), ],
#             (G['Y'], G[')'], ): [Production(G['Y'], G.Epsilon), ],
#             (G['Y'], G['-'], ): [Production(G['Y'], G.Epsilon), ],
#             (G['Y'], G.EOF, ): [Production(G['Y'], G.Epsilon), ],
#             (G['Y'], G['+'], ): [Production(G['Y'], G.Epsilon), ],
#             (G['F'], G['num'], ): [Production(G['F'], Sentence(G['num'])), ],
#             (G['F'], G['('], ): [Production(G['F'], Sentence(G['('], G['E'], G[')'])), ]
#         }

#     @property
#     def tokenizer(self):
#         G = self.G
#         fixed_tokens = self.fixed_tokens

#         def tokenize_text(text):
#             tokens = []
#             for item in text.split():
#                 try:
#                     float(item)
#                     token = Token(item, G['num'])
#                 except ValueError:
#                     try:
#                         token = fixed_tokens[item]
#                     except BaseException:
#                         token = UnknownToken(item)
#                 tokens.append(token)
#             eof = Token('$', G.EOF)
#             tokens.append(eof)
#             return tokens

#         return tokenize_text


# class Regex:
#     def __init__(self, G):
#         self.G = G

#     @property
#     def firsts(self):
#         G = self.G
#         return {
#             G['|']: ContainerSet(G['|'], contains_epsilon=False),
#             G['*']: ContainerSet(G['*'], contains_epsilon=False),
#             G['(']: ContainerSet(G['('], contains_epsilon=False),
#             G[')']: ContainerSet(G[')'], contains_epsilon=False),
#             G['symbol']: ContainerSet(G['symbol'], contains_epsilon=False),
#             G['ε']: ContainerSet(G['ε'], contains_epsilon=False),
#             G['E']: ContainerSet(G['symbol'], G['ε'], G['('], contains_epsilon=False),
#             G['T']: ContainerSet(G['symbol'], G['ε'], G['('], contains_epsilon=False),
#             G['F']: ContainerSet(G['symbol'], G['ε'], G['('], contains_epsilon=False),
#             G['A']: ContainerSet(G['ε'], G['symbol'], G['('], contains_epsilon=False),
#             G['X']: ContainerSet(G['|'], contains_epsilon=True),
#             G['Y']: ContainerSet(G['symbol'], G['ε'], G['('], contains_epsilon=True),
#             G['Z']: ContainerSet(G['*'], contains_epsilon=True),
#             Sentence(G['T'], G['X']): ContainerSet(G['symbol'], G['ε'], G['('], contains_epsilon=False),
#             Sentence(G['|'], G['E']): ContainerSet(G['|'], contains_epsilon=False),
#             G.Epsilon: ContainerSet(contains_epsilon=True),
#             Sentence(G['F'], G['Y']): ContainerSet(G['symbol'], G['ε'], G['('], contains_epsilon=False),
#             Sentence(G['T']): ContainerSet(G['symbol'], G['ε'], G['('], contains_epsilon=False),
#             Sentence(G['A'], G['Z']): ContainerSet(G['symbol'], G['ε'], G['('], contains_epsilon=False),
#             Sentence(G['*']): ContainerSet(G['*'], contains_epsilon=False),
#             Sentence(G['symbol']): ContainerSet(G['symbol'], contains_epsilon=False),
#             Sentence(G['ε']): ContainerSet(G['ε'], contains_epsilon=False),
#             Sentence(G['('], G['E'], G[')']): ContainerSet(G['('], contains_epsilon=False)
#         }

#     @property
#     def follows(self):
#         G = self.G
#         return {
#             G['E']: ContainerSet(G[')'], G.EOF, contains_epsilon=False),
#             G['T']: ContainerSet(G[')'], G.EOF, G['|'], contains_epsilon=False),
#             G['F']: ContainerSet(G[')'], G.EOF, G['symbol'], G['|'], G['ε'], G['('], contains_epsilon=False),
#             G['A']: ContainerSet(G.EOF, G['|'], G['*'], G['('], G[')'], G['symbol'], G['ε'], contains_epsilon=False),
#             G['X']: ContainerSet(G[')'], G.EOF, contains_epsilon=False),
#             G['Y']: ContainerSet(G[')'], G.EOF, G['|'], contains_epsilon=False),
#             G['Z']: ContainerSet(G.EOF, G['|'], G['('], G[')'], G['symbol'], G['ε'], contains_epsilon=False)
#         }

#     @property
#     def table(self):
#         G = self.G
#         return {
#             (G['E'], G['symbol'], ): [Production(G['E'], Sentence(G['T'], G['X'])), ],
#             (G['E'], G['ε'], ): [Production(G['E'], Sentence(G['T'], G['X'])), ],
#             (G['E'], G['('], ): [Production(G['E'], Sentence(G['T'], G['X'])), ],
#             (G['X'], G['|'], ): [Production(G['X'], Sentence(G['|'], G['E'])), ],
#             (G['X'], G[')'], ): [Production(G['X'], G.Epsilon), ],
#             (G['X'], G.EOF, ): [Production(G['X'], G.Epsilon), ],
#             (G['T'], G['symbol'], ): [Production(G['T'], Sentence(G['F'], G['Y'])), ],
#             (G['T'], G['ε'], ): [Production(G['T'], Sentence(G['F'], G['Y'])), ],
#             (G['T'], G['('], ): [Production(G['T'], Sentence(G['F'], G['Y'])), ],
#             (G['Y'], G['symbol'], ): [Production(G['Y'], Sentence(G['T'])), ],
#             (G['Y'], G['ε'], ): [Production(G['Y'], Sentence(G['T'])), ],
#             (G['Y'], G['('], ): [Production(G['Y'], Sentence(G['T'])), ],
#             (G['Y'], G[')'], ): [Production(G['Y'], G.Epsilon), ],
#             (G['Y'], G.EOF, ): [Production(G['Y'], G.Epsilon), ],
#             (G['Y'], G['|'], ): [Production(G['Y'], G.Epsilon), ],
#             (G['F'], G['symbol'], ): [Production(G['F'], Sentence(G['A'], G['Z'])), ],
#             (G['F'], G['ε'], ): [Production(G['F'], Sentence(G['A'], G['Z'])), ],
#             (G['F'], G['('], ): [Production(G['F'], Sentence(G['A'], G['Z'])), ],
#             (G['Z'], G['*'], ): [Production(G['Z'], Sentence(G['*'])), ],
#             (G['Z'], G.EOF, ): [Production(G['Z'], G.Epsilon), ],
#             (G['Z'], G['|'], ): [Production(G['Z'], G.Epsilon), ],
#             (G['Z'], G['('], ): [Production(G['Z'], G.Epsilon), ],
#             (G['Z'], G[')'], ): [Production(G['Z'], G.Epsilon), ],
#             (G['Z'], G['symbol'], ): [Production(G['Z'], G.Epsilon), ],
#             (G['Z'], G['ε'], ): [Production(G['Z'], G.Epsilon), ],
#             (G['A'], G['symbol'], ): [Production(G['A'], Sentence(G['symbol'])), ],
#             (G['A'], G['ε'], ): [Production(G['A'], Sentence(G['ε'])), ],
#             (G['A'], G['('], ): [Production(G['A'], Sentence(G['('], G['E'], G[')'])), ]
#         }

#     @property
#     def parser(self):
#         firsts = self.firsts
#         follows = self.follows
#         M = build_parsing_table(self.G, firsts, follows)
#         # Todo:parser = metodo_predictivo_no_recursivo(self.G, M)
#         return None  # parser
