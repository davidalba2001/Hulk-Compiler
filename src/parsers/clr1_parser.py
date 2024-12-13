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
    import dill as pickle
    from functools import wraps

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

    return [Item(production, 0, lookaheads) for production in productions]


def compress(items):
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
    assert (
        just_kernel or firsts is not None
    ), "`firsts` must be provided if `just_kernel=False`"
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)


path_serialized = "src/parsers/serialized/"


def load_or_build1(path_serialized):
    def decorator(build_method):
        @wraps(build_method)
        def wrapper(self, *args, **kwargs):
            path = path_serialized + self.name_Grammar + "_lr1.pkl"
            if os.path.exists(path):
                obj = deserialize_object(path)
            else:
                obj = build_method(self, *args, **kwargs)
                serialize_object(obj, path)
            return obj

        return wrapper

    return decorator


def serialize_object(obj, filename):
    original_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(10000)
        with open(filename, "wb") as file:
            pickle.dump(obj, file)
    finally:
        sys.setrecursionlimit(original_limit)


def deserialize_object(filename):
    original_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(10000)
        with open(filename, "rb") as file:
            return pickle.load(file)
    finally:
        sys.setrecursionlimit(original_limit)


class LR1Parser(ShiftReduceParser):

    def __init__(self, G, name_Grammar, verbose=False):
        super().__init__(G, name_Grammar, verbose)
        self.name_Grammar = name_Grammar
        self.automaton = self.build_LR1_automaton(self.G.AugmentedGrammar(True))
        path_action = path_serialized + name_Grammar + "_action.pkl"
        path_goto = path_serialized + name_Grammar + "_goto.pkl"
        self.build_or_load(path_action, path_goto)

    def build_or_load(self, path_action, path_goto):
        if os.path.exists(path_action) and os.path.exists(path_goto):
            self.action = deserialize_object(path_action)
            self.goto = deserialize_object(path_goto)
        else:
            self._build_parsing_table()
            serialize_object(self.action, path_action)
            serialize_object(self.action, path_goto)

    @load_or_build1(path_serialized)
    def build_LR1_automaton(self, G):
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
            current = pending.pop()
            current_state = visited[current]

            for symbol in G.terminals + G.nonTerminals:

                next_items = frozenset(goto_lr1(current_state.state, symbol, firsts))

                if not next_items:
                    continue
                try:
                    next_state = visited[next_items]
                except KeyError:
                    visited[next_items] = State(next_items, True)
                    pending.append(next_items)
                    next_state = visited[next_items]

                current_state.add_transition(symbol.Name, next_state)

        automaton.set_formatter(multiline_formatter)
        return automaton

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        automaton = self.automaton
        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, "\t", "\n\t ".join(str(x) for x in node.state), "\n")
            node.idx = i

        for node in automaton:
            idx = node.idx
            if(idx == 450 or idx == 449): print(idx, node)
            for item in node.state:
                X = item.production.Left
                symbol = item.NextSymbol
                if X == G.startSymbol and item.IsReduceItem:
                    self._register(self.action, (idx, G.EOF), (self.OK, 0))
                elif item.IsReduceItem:
                    k = self.G.Productions.index(item.production)
                    for s in item.lookaheads:
                        self._register(self.action, (idx, s), (self.REDUCE, k))
                elif symbol.IsTerminal:
                    self._register(
                        self.action,
                        (idx, symbol),
                        (self.SHIFT, node.transitions[symbol.Name][0].idx),
                    )
                else:
                    self._register(
                        self.goto, (idx, symbol), node.transitions[symbol.Name][0].idx
                    )
                pass

    @staticmethod
    def _register(table, key, value):
        assert (
            key not in table or table[key] == value
        ), "Shift-Reduce or Reduce-Reduce conflict!!!"
        table[key] = value
