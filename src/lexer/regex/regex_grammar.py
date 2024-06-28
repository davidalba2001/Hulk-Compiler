import sys
import os

# Obtener la ruta del directorio actual (por ejemplo, ll1_parser.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Subir tres niveles para llegar a la raíz del proyecto
project_root = os.path.abspath(os.path.join(current_dir, '../../..'))

# Agregar 'src/parsers/parser_utils' a sys.path para que Python pueda encontrar el módulo 'parser_utils'
parser_utils_path = os.path.join(project_root, 'src/lexer/regex')
sys.path.append(parser_utils_path)

try:
    
    from ast_regex import UnionNode,ConcatNode,ClosureNode,SymbolNode,EpsilonNode
    from cmp.pycompiler import Grammar
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")

G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')

#########################################################################################
#                                   PRODUCTIONS                                         #
#########################################################################################
##################################### E -> TX ###########################################
E %= T + X, lambda h, s: s[2], None, lambda h, s: s[1]                                  #
################################ X -> | TX || epsilon ###################################
X %= pipe + T + X, lambda h, s: s[3], None, None, lambda h, s: UnionNode(h[0], s[2])    #
X %= G.Epsilon, lambda h, s: h[0]                                                       #
##################################### T -> FY ###########################################
T %= F + Y, lambda h, s: s[2], None, lambda h, s: s[1]                                  #
################################## Y -> FY || epsilon ###################################
Y %= F + Y, lambda h, s: s[2], None, lambda h, s: ConcatNode(h[0], s[1])                #
Y %= G.Epsilon, lambda h, s: h[0]                                                       #
###################################### F -> AZ ##########################################
F %= A + Z, lambda h, s: s[2], None, lambda h, s: s[1]                                  #
################################# Z -> * || epsilon #####################################
Z %= star,lambda h, s: ClosureNode(h[0]),None                                           #
Z %= G.Epsilon, lambda h, s: h[0]                                                       #
############################ A -> symbol || (T) || epsilon ##############################
A %= opar + E + cpar, lambda h, s: s[2], None, None, None                               #
A %= symbol, lambda h, s: SymbolNode(s[1]), None                                        #
A %= epsilon, lambda h, s: EpsilonNode(s[1]), None                                      #
#########################################################################################