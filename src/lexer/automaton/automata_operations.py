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
    from dfa import DFA
    from nfa import NFA
    from cmp.utils import ContainerSet
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")


def move(automaton:NFA, states, symbol):
    moves = set()
    for state in states:
        if(state in automaton.transitions and symbol in automaton.transitions[state]):
            for item in automaton.transitions[state][symbol]:
                moves.add(item)
    return moves

def epsilon_closure(automaton, states):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p
    
    while pending:
        state = pending.pop()
        if ('' in automaton.transitions[state]):
            for x in automaton.transitions[state]['']:
                closure.add(x)
                pending.append(x)
                
    return ContainerSet(*closure)

def nfa_to_dfa(automaton):
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [start]
    pending = [start]
    
    while pending:
        state = pending.pop()
        
        for symbol in automaton.vocabulary:
            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                
                new_state = epsilon_closure(automaton,move(automaton,state,symbol))
                
                if(len(new_state)>0):
                    if(new_state not in states):
                        new_state.id = len(states)
                        new_state.is_final = any(s in automaton.finals for s in new_state)
                        states.append(new_state)
                        pending = [new_state] + pending
                    else:
                        state_index = states.index(new_state)
                        new_state = states[state_index]
                
                    transitions[state.id, symbol] = new_state.id
                
    
    finals = [state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa

def automata_union(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin + d1 ,symbol)] = [dest + d1 for dest in destinations]

    for (origin, symbol), destinations in a2.map.items():
        transitions[(origin + d2,symbol)] = [dest + d2 for dest in destinations]
    
    transitions[(start, '')] = [d1,d2]
    
    for state in a1.finals:
        transitions[(state + d1, '')] = [final]
    for state in a2.finals:
        transitions[(state + d2, '')] = [final]
            
    states = a1.states + a2.states + 2
    finals = {final}
    
    return NFA(states, finals, transitions, start)

def automata_concatenation(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin + d1 ,symbol)] = [dest + d1 for dest in destinations]

    for (origin, symbol), destinations in a2.map.items():
        transitions[(origin + d2 ,symbol)] = [dest + d2 for dest in destinations]
    
    for state in a1.finals:
        transitions[(state + d1 ,'')] = [a2.start + d2]
    
    for state in a2.finals:
        transitions[(state + d2 , '')] = [final]
               
    states = a1.states + a2.states + 1
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_closure(a1):
    transitions = {}
    
    start = 0
    d1 = 1
    final = a1.states + d1
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin+d1,symbol)] = [dest+d1 for dest in destinations]
    
    transitions[(start,'')] = [d1,final]
    
    for state in a1.finals:
        transitions[(state + d1,'')] = [d1,final]
            
    states = a1.states +  2
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def distinguish_states(group, automaton, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)
    
    for member in group:
        key = set()
        for symbol in vocabulary:
            try:
                dest_state = automaton.transitions[member.value][symbol][0]
                key.add(partition.find(dest_state))
            except KeyError:
               pass
            
        tp_key = tuple(key)
        if tp_key not in split:
            split[tp_key] = []
            
        split[tp_key].append(member.value)
    
    return [g for g in split.values()]
        
def state_minimization(automaton):
            
    partition = DisjointSet(*range(automaton.states))
    finals = list(automaton.finals)
    non_finals = [s for s in range(automaton.states) if s not in automaton.finals]
    
    partition.merge(finals)
    partition.merge(non_finals)
    
    while True:
        new_partition = DisjointSet(*range(automaton.states))
        for group in partition.groups:
            
            subgroups = distinguish_states(group, automaton, partition)
        
            for subgroup in subgroups:   
    
                if(len(subgroup) > 1):
                    new_partition.merge(subgroup)
        
        if len(new_partition) == len(partition):
            break

        partition = new_partition
        
    return partition

def automata_minimization(automaton):
    
    partition = state_minimization(automaton)
    states = [s.value for s in partition.representatives]
    
    transitions = {}
    for i, state in enumerate(states):
    
        for symbol, destinations in automaton.transitions[state].items():
            dest_repres = partition.find(destinations)
            dest_state = states.index(dest_repres)
            
            try:
                transitions[i,symbol]
                assert False
            except KeyError:
                transitions[i,symbol] = dest_state
                pass
    
    finals = [states.index(partition.find(final)) for final in automaton.finals]
    start  = partition.find(automaton.start)
    
    return DFA(len(states), finals, transitions, start)