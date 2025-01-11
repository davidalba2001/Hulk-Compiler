from cmp.automata import *
from cmp.ast import *


class EpsilonNode(AtomicNode):
    def evaluate(self):
        e = self.lex
        return DFA(states=1, finals=[0], transitions={})


class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return NFA(states=2, finals=[1], transitions={(0, s): [1]})


class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)


class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)


class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)


class PlusNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_plus(value)


class QuestNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_question(value)


class QuantifierNode(Node):
    def __init__(self, node, min, max):
        self.node = node
        self.min = min
        self.max = max

    def evaluate(self):
        vnode = self.node.evaluate()
        vmin = self.min.evaluate()
        vmax = self.max.evaluate()
        return self.operate(vnode, vmin, vmax)

    @staticmethod
    def operate(value, min, max):
        return automata_quantifier(value, min, max)


class NumberNode(AtomicNode):
    def evaluate(self):
        lex = self.lex
        try:
            value = int(lex)
            return value
        except:
            raise "Not integer"


class DotNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_dot(lvalue, rvalue)


class StarAnchorNode(UnaryNode):
    def __init__(self, node):
        super().__init__(node)

    @staticmethod
    def operate(value):
        return automata_start_anchor(value)


class EndAnchorNode(UnaryNode):
    def __init__(self, node):
        super().__init__(node)

    @staticmethod
    def operate(value):
        return automata_end_anchor(value)


class RangeNode(Node):
    def __init__(self, characters, ranges):
        self.characters = [character.lex for character in characters]
        self.ranges = [(symbol[0].lex,symbol[1].lex) for symbol in ranges]

    def evaluate(self):
        return automata_range(self.characters, self.ranges)


class NotRangeNode(Node):
    def __init__(self, characters, ranges):
        self.characters = [character.lex for character in characters] 
        self.ranges = [(symbol[0].lex,symbol[1].lex) for symbol in ranges]

    def evaluate(self):
        return automata_range(self.characters, self.ranges, True)
