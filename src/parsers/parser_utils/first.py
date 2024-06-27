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

# Ahora puedes importar el módulo cmp
try:
    from cmp.utils import ContainerSet
    from cmp.pycompiler import Grammar
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")

def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon()

    else:      
        for symbol in alpha:
            if not firsts[symbol].contains_epsilon:
                first_alpha.set_epsilon(False)   
                first_alpha.update(firsts[symbol])
                break
            else:
                first_alpha.hard_update(firsts[symbol])

    return first_alpha

def compute_firsts(G:Grammar):
    firsts = {}
    change = True

    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            first_X = firsts[X]
                
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            
            local_first = compute_local_first(firsts, alpha)
            
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    return firsts

