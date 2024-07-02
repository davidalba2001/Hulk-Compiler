import sys
import os

# Obtener la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Moverse a la raíz del proyecto
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))

# Agregar la carpeta raíz del proyecto al sys.path
sys.path.append(project_root)

try:
    from cmp.pycompiler import Grammar,Item
    from cmp.parsing import compute_firsts, compute_follows, ShiftReduceParser
    from cmp.automata import State
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")

def build_LR0_automaton(G:Grammar):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [ start_item ]
    visited = { start_item: automaton }

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue
        
        next_item =  current_item.NextItem()
        if(next_item not in visited):
            visited[next_item] = State(next_item,True)
            pending.append(next_item)
            
        epsilon_transition_states = []
        next_symbol = current_item.NextSymbol
        if next_symbol.IsNonTerminal:
            for production in G.Productions:
                if production.Left == next_symbol:
                    new_item = Item(production,0)
                    if(new_item not in visited):
                        visited[new_item] = State(new_item,True)
                        pending.append(new_item)
                    epsilon_transition_states.append(visited[new_item])                  
            
        current_state = visited[current_item]
        next_state = visited[next_item]
        current_state.add_transition(next_symbol.Name,next_state)
        for next_state in epsilon_transition_states:
            current_state.add_epsilon_transition(next_state)
        
    return automaton



class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        G:Grammar = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        
        automaton = build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item:Item = state.state
                head,body = item.production
                symbol = item.NextSymbol
                if head == G.startSymbol and item.IsReduceItem:
                    self._register(self.action,(idx,G.EOF),(self.OK,0))
                elif item.IsReduceItem:
                    k = self.G.Productions.index(item.production)
                    for c in follows[head]:                        
                        self._register(self.action,(idx,c),(self.REDUCE,k))
                elif symbol.IsTerminal:
                    self._register(self.action,(idx,symbol),(self.SHIFT,node.transitions[symbol.Name][0].idx))
                else:
                    self._register(self.goto,(idx,symbol),node.transitions[symbol.Name][0].idx)
                    
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value