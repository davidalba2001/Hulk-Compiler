import sys
import os

# Obtener la ruta del directorio actual (first.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}")

# Subir cuatro niveles para llegar a 'project_root'
project_root = os.path.abspath(os.path.join(current_dir, '../../..'))
print(f"Project root: {project_root}")

# Agregar 'project_root' a sys.path
sys.path.append(project_root)
print(f"sys.path: {sys.path}")

# Ahora puedes importar 'first' como un módulo
try:
    from cmp.pycompiler import Grammar
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")

class LL1GrammarException(Exception):
    pass

def build_parsing_table(G: Grammar, firsts, follows):
    # init parsing table
    M = {}
    
    # P: X -> alpha
    for production in G.Productions:
        X = production.Left
        alpha = production.Right

        try:
            alpha_is_epsilon = alpha.IsEpsilon
        except AttributeError:
            alpha_is_epsilon = False

        if not alpha_is_epsilon:
            for term in firsts[alpha]:
                if (X, term) in M:
                    raise LL1GrammarException(f"Grammar is not LL(1): Conflict at non-terminal {X} with terminal {term}")
                M[X, term] = [production]
        else:
            for term in follows[X]:
                if (X, term) in M:
                    raise LL1GrammarException(f"Grammar is not LL(1): Conflict at non-terminal {X} with terminal {term}")
                M[X, term] = [production]
        
    return M