try:
    import pydot
    import string
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
        self.transitions = {start+state: {} for state in range(states) }
        
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
        if ((state,'') in automaton.map):
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
    final = a2.states + d2 + 1
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin + d1 ,symbol)] = [dest + d1 for dest in destinations]

    for (origin, symbol), destinations in a2.map.items():
        transitions[(origin + d2 ,symbol)] = [dest + d2 for dest in destinations]
    
    for state in a1.finals:
        transitions[(state + d1 ,'')] = [a2.start + d2]
    
    for state in a2.finals:
        if (state, '') in a2.map:
            finals = [final + d2 for final in a2.map[state, '']]
            transitions[(state + d2, '')] = finals + [final]
        else:
            transitions[(state + d2, '')] = [final]
               
    states = a1.states + a2.states + 1
    finals = { final }
    nfa  = NFA(states, finals, transitions, start)
    dfa = nfa_to_dfa(nfa)
    return dfa

def automata_closure(a1:NFA):
    transitions = {}
    
    start = 0
    s1 = 1
    final = a1.states + 1
    # renombrando los states
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin+1,symbol)] = [dest+1 for dest in destinations]
    # andiendo start 
    transitions[(start,'')] = [s1,final]
    
    for state in a1.finals:
        transitions[(state + 1,'')] = [s1,final]
            
    state = a1.states +  2
    finals = {final}
    
    return NFA(state, finals, transitions, start)

def automata_plus(a1):
    # Implementación del operador + (uno o más)
    transitions = {}
    start = 0
    s1 = 1
    final = a1.states + 1
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin+1,symbol)] = [dest+1 for dest in destinations]
    
    transitions[(start,'')] = [s1]
    
    for state in a1.finals:
        transitions[(state + 1,'')] = [s1,final]
            
    states = a1.states + 2
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_question(a1):
    # Implementación del operador ? (cero o uno)
    transitions = {}
    
    start = 0
    s1 = 1
    final = a1.states + 1
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin+ 1,symbol)] = [dest+ 1 for dest in destinations]
    
    transitions[(start,'')] = [s1,final]
    
    for state in a1.finals:
        transitions[(state + 1,'')] = [final]
            
    states = a1.states + 2
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_symbol(symbol):
    return NFA(states = 2,finals = [1],transitions={(0,symbol):[1]})

def automata_quantifier(a1, min_val, max_val):
    if not isinstance(min_val,int) or not isinstance(max_val,int):
        raise ValueError(f"min_val and max_val must be integers, but got {type(min_val).__name__} and {type(max_val).__name__}")
    
    if min_val < 0:
        raise ValueError("min_val must be greater than or equal to 0")
    
    if min_val > max_val:
        raise ValueError("min_val must be less than or equal to max_val")

    automaton = _quantifier_builder(a1, min_val, max_val)
    
    return automaton

def shift_automata(a1:NFA,shift):
    transitions = {}
    start = a1.start + shift
    states = a1.states
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin + shift,symbol)] = [dest + shift for dest in destinations]
    
    finals = {final + shift for final in a1.finals}
    return NFA(states,finals,transitions, start)

def _transform_transitions(transitions):

    new_transitions = {}

    for state, symbols in transitions.items():
        for symbol, states in symbols.items():
            new_transitions[(state, symbol)] = states
    
    return new_transitions

def _update_transitions(trans0,trans1):
    trans_update = trans0
    trans_dict = trans1
    key = value = None
    try:
        key,value = list(trans0.items())[0]
        if isinstance(key, int) and isinstance(value, dict):
            trans_update = _transform_transitions(trans_update)
    except:   
        pass

    try: 
        key,value = list(trans1.items())[0]
        if isinstance(key, int) and isinstance(value, dict):
            trans_dict =  _transform_transitions(trans_dict)
    except:  
        pass
            
    for (key,states) in trans_dict.items():
            if(key in trans_update.keys()):
                update = trans_update[key]
                trans_update[key] = list(set(update).union(states))
            else:
                 trans_update[key] = states
    
    return trans_update

def _quantifier_builder(a1:NFA,min,max):
    states = a1.states * max + max
    start = a1.start
    transitions = {}
    shift = a1.states + 1
    
    automaton:list[NFA] = [a1]
    for i in range(max-1):
        current_aut = automaton[i]
        automaton.append(shift_automata(current_aut,shift))
        
    inner = [state.start - 1 for state in automaton[1:]]
    inner.append(inner[-1:][0] + a1.states+1)
    index = 0
    
    for autom in automaton:
        for final in autom.finals:
            transitions[(final,'')] = [inner[index]]
        index += 1
    index = 0
        
    for autom in automaton[1:]:
        transitions[(inner[index],'')] = [autom.start]
        index += 1
        
    update_transitions = {} 
    for automt in automaton:
        update_transitions = _update_transitions(automt.transitions,update_transitions)
    
    transitions = _update_transitions(transitions,update_transitions)
    
    if(min > 0):
        finals = {final for final in inner[min-1:]}
    else:
        min = 1
        finals = {final for final in inner[min-1:]}
        finals.add(start)
        
    return NFA(states,finals,transitions, start)
         
def automata_range(characters,ranges,flag = False):
    all_chars = []
    for start,end in ranges:
        all_chars += _get_chars_in_range(start, end)

    all_chars = set(all_chars)
    all_chars = all_chars.union(characters)
    
    if(flag):
        all_chars =  set(string.printable).difference(all_chars)
    
    transitions = {}
    start_state = 0
    final_state = 1

    for symbol in all_chars:
        transitions[(start_state,symbol)] = [final_state]

    states = 2
    finals = {final_state}

    return NFA(states, finals, transitions, start_state)
        
def _get_chars_in_range(start, end):
    
    if isinstance(start, str) and isinstance(end, str):
        if len(start) != 1 or len(end) != 1:
            raise ValueError("start and end must be single characters")
        if ord(start) > ord(end):
            raise ValueError("start must be less than or equal to end")
        start_ord = ord(start)
        end_ord = ord(end)
        is_char = True
    elif isinstance(start, int) and isinstance(end, int):
        if start > end:
            raise ValueError("start must be less than or equal to end")
        start_ord = start
        end_ord = end
        is_char = False
    else:
        raise ValueError("start and end must be both single characters or both integers")
    
    return  [chr(symbol) if is_char else str(symbol) for symbol in range(start_ord, end_ord + 1)]

def combined_automaton():
    printable_chars = set(string.printable).difference('\n')

    char_automata = [automata_symbol(char) for char in printable_chars]

    combined_automaton = char_automata[0]
    for automaton in char_automata[1:]:
        combined_automaton = automata_union(combined_automaton, automaton)
    return combined_automaton

def automata_dot(start_automaton, end_automaton):
    
    combined = combined_automaton()
    intermediate_automaton = automata_concatenation(start_automaton, combined)
    final_automaton = automata_concatenation(intermediate_automaton, end_automaton)
    return final_automaton
   
def automata_start_anchor(a1):
    clousre = automata_closure(combined_automaton())
    automaton = automata_concatenation(a1,clousre)
    return automaton

def automata_end_anchor(a1):
    transitions = {}
    
    start = 0
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin, symbol)] = [dest  for dest in destinations]
    
    for state in a1.finals:
        transitions[(state,'')] = [start]
    
    states = a1.states
    finals = a1.finals
    
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