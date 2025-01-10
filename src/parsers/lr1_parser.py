
import os
from cmp.utils import ContainerSet, pprint
from cmp.parsing import compute_firsts, compute_local_first
from cmp.pycompiler import Item
from cmp.parsing import ShiftReduceParser
from cmp.automata import State, multiline_formatter
from utils.serialize import (
    serialize_object,
    deserialize_object,
    get_cache_path,
    load_cache,
)
from cmp.pycompiler import Grammar


def expand(item, firsts):
    """
    Si el siguiente item es un Terminal entoces determina con que items de debe expandir el conjunto
    Si el item es de la forma X → α B γ, {lookaheads} ,  entonces se expande con todos los items B → .σ  { first(γ +λ) | λ is in lookaheads}
    """

    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    lookaheads = ContainerSet()
    # Actualiza el lookahead
    for preview in item.Preview():
        lookaheads.update(compute_local_first(firsts, preview))

    assert not lookaheads.contains_epsilon
    productions = next_symbol.productions

    return [Item(production, 0, lookaheads) for production in productions]


def compress(items):
    """Unifica los items LR(1) con un mismo item LR(0) """
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()

        lookaheads.update(item.lookaheads)

    return {
        Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items()
    }


def closure_lr1(items, firsts):
    """Aplica expand hasta que no se pueda expandir mas el conjunto y luego hace un compres para unifiar las producciones con el mismo centro"""
    closure = ContainerSet(*items)

    changed = True
    while changed:
        changed = False

        new_items = ContainerSet()
        for item in closure:
            new_items.update(ContainerSet(*expand(item, firsts)))

        changed = closure.update(new_items)

    return compress(closure)


def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    """
    Retorna el conjunto de items al que se puede llegar consumiendo el simbolo,
    si just_kernel es falso devuelve el conjunto de items clausurados,si no
    devuelve un item kernel
    """
    assert (
        just_kernel or firsts is not None
    ), "`firsts` must be provided if `just_kernel=False`"
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)


class LR1Parser(ShiftReduceParser):

    def __init__(self, G: Grammar, verbose=False, debug=False):
        super().__init__(G, verbose)
        self.debug = debug
        self.automaton = self.build_LR1_automaton(self.G.AugmentedGrammar(True))
        self.cache_or_load_tables(G.name)

    def cache_or_load_tables(self, filename):

        goto_file = f"{filename}_goto"
        action_file = f"{filename}_action"

        if os.path.exists(get_cache_path(goto_file)) and os.path.exists(
            get_cache_path(action_file)
        ):
            self.action = deserialize_object(action_file)
            self.goto = deserialize_object(goto_file)
        else:
            self._build_parsing_table()
            serialize_object(self.action, action_file)
            serialize_object(self.goto, goto_file)

    def build_LR1_automaton(self, G):
        # Aquí podemos usar `self.grammar_name` directamente para obtener el nombre
        @load_cache(f"{G.name}_lr1_automaton")  # Definir el cache con el valor de self.grammar_name
        def internal_build_LR1_automaton(self, G):

            assert len(G.startSymbol.productions) == 1, "Grammar must be augmented"

            firsts = compute_firsts(G)
            firsts[G.EOF] = ContainerSet(G.EOF)

            start_production = G.startSymbol.productions[0]
            start_item = Item(start_production, 0, lookaheads=(G.EOF,))
            start = frozenset([start_item])

            closure = closure_lr1(start, firsts)
            automaton = State(frozenset(closure), True)

            pending = [start]
            visited = {start: automaton}

            while pending:
                current_kernel = pending.pop()
                current_state = visited[current_kernel]

                for symbol in G.terminals + G.nonTerminals:

                    kernel = goto_lr1(current_state.state, symbol, just_kernel=True)

                    if not kernel:
                        continue
                    try:
                        next_state = visited[kernel] # Si ya se visito el kernel entonces se obtiene el estado
                    except KeyError:
                        visited[kernel] = next_state = State(frozenset(goto_lr1(current_state.state, symbol, firsts)), True)
                        pending.append(kernel)

                    current_state.add_transition(symbol.Name, next_state)

            automaton.set_formatter(multiline_formatter)
            return automaton

        return internal_build_LR1_automaton(self, G)

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        automaton = self.automaton
        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, "\t", "\n\t ".join(str(x) for x in node.state), "\n")
            node.idx = i

        for node in automaton:

            idx = node.idx

            for item in node.state:
                X = item.production.Left
                symbol = item.NextSymbol
                if X == G.startSymbol and item.IsReduceItem:
                    self._register(self.action, (idx, G.EOF), (self.OK, 0), node.state, self.debug)
                elif item.IsReduceItem:  # Que el puntico este al final
                    k = self.G.Productions.index(item.production)
                    for s in item.lookaheads:  # Si esta al final entonces escribe reduce en en todos los simbolos del lookaheads
                        self._register(self.action, (idx, s), (self.REDUCE, k), node.state, self.debug)
                elif symbol.IsTerminal:  # Si detras del punto viene un terminal entonces se hace shift
                    self._register(self.action, (idx, symbol), (self.SHIFT, node.transitions[symbol.Name][0].idx), node.state, self.debug)
                else:  # Si detras del punto es un no terminal se hace un Goto
                    self._register(
                        self.goto, (idx, symbol), node.transitions[symbol.Name][0].idx, node.state, self.debug
                    )

    @staticmethod
    def _register(table, key, value, state=None, debug=False):
        if key not in table or table[key] == value:
            table[key] = value
        elif state is None:  
           raise AssertionError("Shift-Reduce or Reduce-Reduce conflict!!!")
        else:
            raise AssertionError(LR1Parser.identify_conflicts(state,key[1], debug))
        

    @staticmethod
    def identify_conflicts(state: State, symbol, debug=False):
        conflicts_items = [item for item in state if item.IsReduceItem or item.NextSymbol == symbol]

        reduce_items = [item for item in conflicts_items if item.IsReduceItem]
        shift_items = [item for item in conflicts_items if item.NextSymbol == symbol]

        if len(reduce_items) > 1:
            if debug:
                print("Conflict Details:")
                print("Reduce Items:")
                for item in reduce_items:
                    print(f"  - {item}")  # Asumiendo que `item` tiene un método __str__ o similar
            return "Reduce-Reduce conflict!!!"

        if len(shift_items) > 0 and len(reduce_items) > 0:
            if debug:
                print("Conflict Details:")
                print("Shift Items:")
                for item in shift_items:
                    print(f" ▶️ {item}")  # Asumiendo que `item` tiene un método __str__ o similar
                print("Reduce Items:")
                for item in reduce_items:
                    print(f" ▶️ {item}")
            return "Shift-Reduce conflict!!!"

        return "No conflict detected."
