from cmp.pycompiler import EOF
from cmp.parsing import ShiftReduceParser
from cmp.utils import Token

class TokenList(list):
    def __getitem__(self,index):
        
        if isinstance(index,slice):
            return TokenList(super().__getitem__(index))
        else:
            item = super().__getitem__(index)
            if isinstance(item, Token):
                return item
            return item

    def __add__(self, other):
        if isinstance(other, list):
            return TokenList(super().__add__(other))
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, list):
            return TokenList(other + list(self))
        return NotImplemented

    def __repr__(self):
        return f"TokenList({super().__repr__()})"


def evaluate_reverse_parse(right_parse, operations, tokens):
    if not right_parse or not operations or not tokens:
        return

    right_parse = iter(right_parse)
    tokens = iter(tokens)
    stack = []
    for operation in operations:
        if operation == ShiftReduceParser.SHIFT:
            token = next(tokens)
            stack.append(token)
        elif operation == ShiftReduceParser.REDUCE:
            production = next(right_parse)
            head, body = production
            attributes = production.attributes
            assert all(
                rule is None for rule in attributes[1:]
            ), "There must be only synteticed attributes."
            rule = attributes[0]

            if len(body):
                synteticed = TokenList([None]) + stack[-len(body) :]
                value = rule(None, synteticed)
                stack[-len(body) :] = [value]
            else:
                stack.append(rule(None, None))
        else:
            raise Exception("Invalid action!!!")

    assert len(stack) == 1
    toke = next(tokens)
    token_type = toke.ttype
    assert token_type == "eof"
    return stack[0]

def evaluate_parse(left_parse, tokens):
    if not left_parse or not tokens:
        return

    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = _evaluate(next(left_parse), left_parse, tokens)

    assert isinstance(next(tokens).token_type, EOF)
    return result

def _evaluate(production, left_parse, tokens, inherited_value=None):
    head, body = production
    attributes = production.attributes

    synteticed = [None] * len(attributes)
    inherited = [None] * len(attributes)

    inherited[0] = inherited_value

    for i, symbol in enumerate(body, 1):
        if symbol.IsTerminal:
            assert inherited[i] is None
            synteticed[i] = next(tokens).lex

        else:
            next_production = next(left_parse)
            assert symbol == next_production.Left
            if not attributes[i] == None:
                synteticed[i] = _evaluate(
                    next_production,
                    left_parse,
                    tokens,
                    attributes[i](inherited, synteticed),
                )
            else:
                synteticed[i] = _evaluate(next_production, left_parse, tokens)

    return attributes[0](inherited, synteticed)
