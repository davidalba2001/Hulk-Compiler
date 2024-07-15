import sys
import os

# Obtener la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Moverse a la raíz del proyecto
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))

# Agregar la carpeta raíz del proyecto al sys.path
sys.path.append(project_root)

try:
    from cmp.pycompiler import Grammar
    from cmp.utils import ContainerSet
    from cmp.parsing import compute_firsts, compute_local_first
    from cmp.pycompiler import Item
    from cmp.parsing import ShiftReduceParser
    from cmp.automata import State, multiline_formatter
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")


def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []
    
    lookaheads = ContainerSet()
    for preview in item.Preview():
        lookaheads.update(compute_local_first(firsts, preview))
    
    assert not lookaheads.contains_epsilon
    productions = next_symbol.productions
    
    return [Item(production,0,lookaheads) for production in productions]

def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)
    
    return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }

def closure_lr1(items, firsts):
    closure = ContainerSet(*items)
    
    changed = True
    while changed:
        changed = False
        
        new_items = ContainerSet()
        for item in closure:
            new_items.update(ContainerSet(*expand(item,firsts)))

        changed = closure.update(new_items)
        
    return compress(closure)

def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)

def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    
    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])
    
    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)
    
    pending = [ start ]
    visited = { start: automaton }
    
    while pending:
        current = pending.pop()
        current_state = visited[current]
        
        for symbol in G.terminals + G.nonTerminals:
            
            next_items = frozenset(goto_lr1(current_state.state,symbol,firsts))
            
            if not next_items:
                continue
            try:
                next_state = visited[next_items]
            except KeyError:
                visited[next_items] = State(next_items,True)
                pending.append(next_items)
                next_state = visited[next_items]
            
            current_state.add_transition(symbol.Name, next_state)
    
    automaton.set_formatter(multiline_formatter)
    return automaton

# def build_LR1_automaton(G):
#     assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'                                 # !ERROR!

#     firsts = compute_firsts(G)
#     firsts[G.EOF] = ContainerSet(G.EOF)

#     start_production = G.startSymbol.productions[0]
#     start_item = Item(start_production, 0, lookaheads=(G.EOF,))
#     start = frozenset([start_item])

#     closure = closure_lr1(start, firsts)
#     automaton = State(frozenset(closure), True)

#     pending = [start]
#     visited = {start: automaton}

#     while pending:
#         current = pending.pop()
#         current_state = visited[current]

#         for symbol in G.terminals + G.nonTerminals:
#             items = current_state.state
#             kernel = goto_lr1(items, symbol, just_kernel=True)

#             if not kernel:
#                 continue
#             try:
#                 next_state = visited[kernel]
#             except:
#                 closure = goto_lr1(items, symbol, firsts)
#                 next_state = visited[kernel] = State(frozenset(closure), True)
#                 pending.append(kernel)

#             current_state.add_transition(symbol.Name, next_state)

#     automaton.set_formatter(multiline_formatter)
#     return automaton



class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                X = item.production.Left
                symbol = item.NextSymbol
                if X == G.startSymbol and item.IsReduceItem:
                    self._register(self.action,(idx,G.EOF),(self.OK,0))
                elif item.IsReduceItem:
                    k = self.G.Productions.index(item.production)
                    for s in item.lookaheads:                        
                        self._register(self.action,(idx,s),(self.REDUCE,k))
                elif symbol.IsTerminal:
                    self._register(self.action,(idx,symbol),(self.SHIFT,node.transitions[symbol.Name][0].idx))
                else:
                    self._register(self.goto,(idx,symbol),node.transitions[symbol.Name][0].idx)
                pass
        
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value