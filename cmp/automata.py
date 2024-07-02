try:
    import pydot
    from cmp.utils import ContainerSet,DisjointSet
except:
    pass

class State:
    def __init__(self, state, final=False, formatter=lambda x: str(x), shape='circle'):
        self.state = state
        self.final = final
        self.transitions = {}
        self.epsilon_transitions = set()
        self.tag = None
        self.formatter = formatter
        self.shape = shape

    # The method name is set this way from compatibility issues.
    def set_formatter(self, value, attr='formatter', visited=None):
        if visited is None:
            visited = set()
        elif self in visited:
            return

        visited.add(self)
        self.__setattr__(attr, value)
        for destinations in self.transitions.values():
            for node in destinations:
                node.set_formatter(value, attr, visited)
        for node in self.epsilon_transitions:
            node.set_formatter(value, attr, visited)
        return self

    def has_transition(self, symbol):
        return symbol in self.transitions

    def add_transition(self, symbol, state):
        try:
            self.transitions[symbol].append(state)
        except:
            self.transitions[symbol] = [state]
        return self

    def add_epsilon_transition(self, state):
        self.epsilon_transitions.add(state)
        return self

    def recognize(self, string):
        states = self.epsilon_closure
        for symbol in string:
            states = self.move_by_state(symbol, *states)
            states = self.epsilon_closure_by_state(*states)
        return any(s.final for s in states)

    def to_deterministic(self, formatter=lambda x: str(x)):
        closure = self.epsilon_closure
        start = State(tuple(closure), any(s.final for s in closure), formatter)

        closures = [ closure ]
        states = [ start ]
        pending = [ start ]

        while pending:
            state = pending.pop()
            symbols = { symbol for s in state.state for symbol in s.transitions }

            for symbol in symbols:
                move = self.move_by_state(symbol, *state.state)
                closure = self.epsilon_closure_by_state(*move)

                if closure not in closures:
                    new_state = State(tuple(closure), any(s.final for s in closure), formatter)
                    closures.append(closure)
                    states.append(new_state)
                    pending.append(new_state)
                else:
                    index = closures.index(closure)
                    new_state = states[index]

                state.add_transition(symbol, new_state)

        return start

    @staticmethod
    def from_nfa(nfa, get_states=False):
        states = []
        for n in range(nfa.states):
            state = State(n, n in nfa.finals)
            states.append(state)

        for (origin, symbol), destinations in nfa.map.items():
            origin = states[origin]
            origin[symbol] = [ states[d] for d in destinations ]

        if get_states:
            return states[nfa.start], states
        return states[nfa.start]

    @staticmethod
    def move_by_state(symbol, *states):
        return { s for state in states if state.has_transition(symbol) for s in state[symbol]}

    @staticmethod
    def epsilon_closure_by_state(*states):
        closure = { state for state in states }

        l = 0
        while l != len(closure):
            l = len(closure)
            tmp = [s for s in closure]
            for s in tmp:
                for epsilon_state in s.epsilon_transitions:
                        closure.add(epsilon_state)
        return closure

    @property
    def epsilon_closure(self):
        return self.epsilon_closure_by_state(self)

    @property
    def name(self):
        return self.formatter(self.state)

    def get(self, symbol):
        target = self.transitions[symbol]
        assert len(target) == 1
        return target[0]

    def __getitem__(self, symbol):
        if symbol == '':
            return self.epsilon_transitions
        try:
            return self.transitions[symbol]
        except KeyError:
            return None

    def __setitem__(self, symbol, value):
        if symbol == '':
            self.epsilon_transitions = value
        else:
            self.transitions[symbol] = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.state)

    def __hash__(self):
        return hash(self.state)

    def __iter__(self):
        yield from self._visit()

    def _visit(self, visited=None):
        if visited is None:
            visited = set()
        elif self in visited:
            return

        visited.add(self)
        yield self

        for destinations in self.transitions.values():
            for node in destinations:
                yield from node._visit(visited)
        for node in self.epsilon_transitions:
            yield from node._visit(visited)

    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        visited = set()
        def visit(start):
            ids = id(start)
            if ids not in visited:
                visited.add(ids)
                G.add_node(pydot.Node(ids, label=start.name, shape=self.shape, style='bold' if start.final else ''))
                for tran, destinations in start.transitions.items():
                    for end in destinations:
                        visit(end)
                        G.add_edge(pydot.Edge(ids, id(end), label=tran, labeldistance=2))
                for end in start.epsilon_transitions:
                    visit(end)
                    G.add_edge(pydot.Edge(ids, id(end), label='ε', labeldistance=2))

        visit(self)
        G.add_edge(pydot.Edge('start', id(self), label='', style='dashed'))

        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

    def write_to(self, fname):
        return self.graph().write_svg(fname)

def multiline_formatter(state):
    return '\n'.join(str(item) for item in state)

def lr0_formatter(state):
    try:
        return '\n'.join(str(item)[:-4] for item in state)
    except TypeError:
        return str(state)[:-4]

class NFA:
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
            
    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'ε' if tran == '' else tran
            G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass
        
class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        if self.current in self.transitions:
            if symbol in  self.transitions[self.current]:
                return self.transitions[self.current][symbol][0]
        return None
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        self._reset()
        for symbol in string:
            self.current = self._move(symbol)
        return self.current in self.finals


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