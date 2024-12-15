from cmp.parsing import compute_firsts, compute_follows, build_parsing_table


def build_non_recursive_predictive_parser(G, M=None, firsts=None, follows=None):

    if M is None:
        if firsts is None:
            firsts = compute_firsts(G)
        if follows is None:
            follows = compute_follows(G, firsts)
        M = build_parsing_table(G, firsts, follows)

    def parser(w):

        stack = [G.EOF, G.startSymbol]
        index = 0
        left_parse = []

        while True:
            top = stack.pop()
            term = w[index]

            if top == G.EOF:
                if term == G.EOF:
                    break
                else:
                    raise ValueError("Parsing error: input not fully consumed at EOF")

            elif top in G.terminals:
                if top == term:
                    index += 1
                else:
                    raise ValueError(f"Parsing error: expected {top} but found {term}")

            elif top in G.nonTerminals:
                if (top, term) in M:
                    production = M[(top, term)][0]
                    left_parse.append(production)
                    for symbol in reversed(production.Right):
                        if not symbol.IsEpsilon:
                            stack.append(symbol)
                else:
                    raise ValueError(
                        f"Parsing error: no production for ({top}, {term}) in parsing table"
                    )
            else:
                raise ValueError(f"Parsing error: unrecognized symbol {top} on stack")

        if index != len(w) - 1:  # Ensure the input is fully consumed
            raise ValueError("Parsing error: input not fully consumed")

        # left parse is ready!!!
        return left_parse

    # parser is ready!!!
    return parser
