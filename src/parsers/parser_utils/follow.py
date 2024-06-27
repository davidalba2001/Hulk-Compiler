from typing import Dict, Any
import sys
import os

# Obtener la ruta del directorio actual (follow.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}")

# Subir tres niveles para llegar a 'project_root'
project_root = os.path.abspath(os.path.join(current_dir, '../../..'))
print(f"Project root: {project_root}")

# Agregar 'project_root/src/parsers/parser_utils' a sys.path para importar 'first.py'
parser_utils_path = os.path.join(project_root, 'src/parsers/parser_utils')
sys.path.append(parser_utils_path)
print(f"sys.path: {sys.path}")

# Ahora puedes importar 'first' como un módulo
try:
    from parser_utils.first import compute_local_first,compute_firsts
    from cmp.utils import ContainerSet
    from cmp.pycompiler import Grammar
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")


def compute_follows(G, firsts):
    follows: Dict[Any, ContainerSet] = {}
    change = True

    local_firsts = {}
    
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)

    while change:
        change = False

        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            follow_X = follows[X]

            for (i,symbol) in enumerate(alpha):
                if symbol.IsNonTerminal:
                    local_firsts = compute_local_first(firsts, alpha[i+1:])
                    if not local_firsts.contains_epsilon:
                        change |= follows[symbol].update(local_firsts)
                    else:
                        change |= follows[symbol].update(local_firsts)
                        change |= follows[symbol].update(follow_X)
            
            # Handle the case when the last symbol is a non-terminal
            if alpha and alpha[-1].IsNonTerminal:
                change |= follows[alpha[-1]].update(follow_X)
    return follows
