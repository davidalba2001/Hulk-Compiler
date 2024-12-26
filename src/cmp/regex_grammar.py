from cmp.ast import *
from cmp.ast_regex import *
from cmp.pycompiler import Grammar


G_Regex = Grammar("Regex")

# No Terminales
expression = G_Regex.NonTerminal('EXPRESSION', True)  # No terminal inicial, marcado como inicial
alternative, start_anchor, end_anchor, pattern, subpattern, in_range, symbol_or_range, number, more_symbols = G_Regex.NonTerminals(
    'ALTERNATIVE STARTANCHOR ENDANCHOR PATTERN SUBPATTERN INRANGE SYMBOLORRANGE NUMBER MORESYMBOLS')


# Terminales con etiquetas específicas
question, dot, plus, pipe, star, minus, caret, opar, cpar, obrckt, cbrckt, epsilon, dollar, obrace, cbrace, symbol = G_Regex.Terminals(
    'QUESTION DOT PLUS PIPE STAR MINUS CARET OPAR CPAR OBRCKT CBRCKT EPSILON DOLLAR OBRACE CBRACE SYMBOL')


expression %= expression + pipe + alternative, lambda h, s: UnionNode(s[1], s[3])
expression %= alternative, lambda h, s: s[1]

alternative %= caret + end_anchor, lambda h, s: StarAnchorNode(s[2])
end_anchor %= pattern + dollar, lambda h, s: EndAnchorNode(s[1])
end_anchor %= pattern, lambda h, s: s[1]
alternative %= end_anchor, lambda h, s: s[1]


pattern %= pattern + subpattern, lambda h, s: ConcatNode(s[1], s[2])
pattern %= pattern + dot + subpattern, lambda h, s: DotNode(s[1], s[3])
pattern %= subpattern, lambda h, s: s[1]

subpattern %= subpattern + star, lambda h, s: ClosureNode(s[1])
subpattern %= subpattern + plus, lambda h, s: PlusNode(s[1])
subpattern %= subpattern + question, lambda h, s: QuestNode(s[1])
subpattern %= subpattern + obrace + number + cbrace, lambda h, s: QuantifierNode(s[2], s[2])
subpattern %= subpattern + obrace + number + minus + number + cbrace, lambda h, s: QuantifierNode(s[1], s[3], s[5])
number %= more_symbols, lambda h, s: NumberNode(s[1])
more_symbols %= more_symbols + symbol, lambda h, s: s[1] + s[2]
more_symbols %= symbol, lambda h, s: s[1]
subpattern %= obrckt + in_range + cbrckt, lambda h, s: RangeNode(s[2][0], s[2][1])
subpattern %= obrckt + caret + in_range + cbrckt, lambda h, s: NotRangeNode(s[3][0], s[3][1])
subpattern %= opar + expression + cpar, lambda h, s: s[2]
subpattern %= symbol, lambda h, s: SymbolNode(s[1])
subpattern %= epsilon, lambda h, s: EpsilonNode(s[1])

in_range %= in_range + symbol_or_range, lambda h, s: list(map(lambda t: t[0] + t[1], zip(s[1], s[2])))
in_range %= symbol_or_range, lambda h, s: s[1]

symbol_or_range %= symbol + minus + symbol, lambda h, s: ([], [(s[1], s[3])])
symbol_or_range %= symbol, lambda h, s: ([s[1]], [])
