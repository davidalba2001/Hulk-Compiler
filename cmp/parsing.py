try:
    from cmp.pycompiler import Grammar
    from cmp.utils import ContainerSet,Token
    from cmp.exceptions import LL1GrammarException
    import dill as pickle 
    import os
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")


class ShiftReduceParser:
    SHIFT = "SHIFT"
    REDUCE = "REDUCE"
    OK = "OK"
    
    def __init__(self,G,name_Grammar,verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {} 
        self.goto = {}

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self,w,get_shift_reduce= True):
        stack = [0]
        cursor = 0
        output = []
        operations = []
        isTokenList = isinstance(w, list) and all(isinstance(token, Token) for token in w)
        while True:
            
            state = stack[-1]
            if isTokenList:
                lookahead_token:Token = w[cursor]
                lookahead = lookahead_token.token_type
            else:    
                lookahead = w[cursor]
            if self.verbose:
                print(stack, "<---||--->", w[cursor:])

            
            if isTokenList:
                if (state,lookahead) not in self.action:
                    raise SyntaxError(
                        f"Unexpected symbol: {lookahead} at (line {lookahead_token.line}, column {lookahead_token.column})"
                    )
            else:
                if (state, lookahead) not in self.action:
                    raise SyntaxError(f"Unexpected symbol: {lookahead}")
                
                
            action, tag = self.action[state, lookahead]
            # Your code here!!! (Shift case)
            if action == self.SHIFT:
                stack.append(tag)
                operations.append(action)
                cursor += 1
            # Your code here!!! (Reduce case)
            elif action == self.REDUCE:
                production = head, body = self.G.Productions[tag]
                for _ in range(len(body)):
                    stack.pop()
                state = stack[-1]
                stack.append(self.goto[state, head])
                operations.append(action)
                output.append(production)

            # Your code here!!! (OK case)
            elif action == self.OK:
                if get_shift_reduce:
                    return output,operations
                else:
                    return output

            # Your code here!!! (Invalid case)
            else:
                raise SyntaxError(f"Invalid action: {action}")

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

def compute_firsts(G: Grammar):
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

def compute_follows(G, firsts):
    follows = {}
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

            for i, symbol in enumerate(alpha):
                if symbol.IsNonTerminal:
                    local_firsts = compute_local_first(firsts, alpha[i + 1 :])
                    if not local_firsts.contains_epsilon:
                        change |= follows[symbol].update(local_firsts)
                    else:
                        change |= follows[symbol].update(local_firsts)
                        change |= follows[symbol].update(follow_X)

            # Handle the case when the last symbol is a non-terminal
            if alpha and alpha[-1].IsNonTerminal:
                change |= follows[alpha[-1]].update(follow_X)
    return follows

def build_parsing_table(G, firsts, follows):
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
                    raise LL1GrammarException(
                        f"Grammar is not LL(1): Conflict at non-terminal {X} with terminal {term}"
                    )
                M[X, term] = [production]
        else:
            for term in follows[X]:
                if (X, term) in M:
                    raise LL1GrammarException(
                        f"Grammar is not LL(1): Conflict at non-terminal {X} with terminal {term}"
                    )
                M[X, term] = [production]

    return M
