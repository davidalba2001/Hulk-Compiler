from cmp.ast import *
from cmp.ast_regex import *
from cmp.pycompiler import Grammar
# No Terminales


G_Regex = Grammar()

Expression = G_Regex.NonTerminal('Expression', True)  # No terminal inicial, marcado como inicial
Alternative = G_Regex.NonTerminal('Alternative')
StartAnchor = G_Regex.NonTerminal('StartAnchor')
EndAnchor = G_Regex.NonTerminal('EndAnchor')
Pattern = G_Regex.NonTerminal('Pattern')
Subpattern = G_Regex.NonTerminal('Subpattern')
Range = G_Regex.NonTerminal('Range')
SymbolOrRange = G_Regex.NonTerminal('SymbolOrRange')
Number = G_Regex.NonTerminal('NUMBER')
MoreSymbols = G_Regex.NonTerminal('MoreSymbols')
# Terminales con etiquetas específicas
question = G_Regex.Terminal('QUESTION')
dot = G_Regex.Terminal('DOT')
plus = G_Regex.Terminal('PLUS')
pipe = G_Regex.Terminal('PIPE')
star = G_Regex.Terminal('STAR')
minus = G_Regex.Terminal('MINUS')
caret = G_Regex.Terminal('CARET')
opar = G_Regex.Terminal('OPAR')
cpar = G_Regex.Terminal('CPAR')
obrckt  = G_Regex.Terminal('OBRCKT')
cbrckt  = G_Regex.Terminal('CBRCKT')
symbol  = G_Regex.Terminal('SYMBOL')

epsilon = G_Regex.Terminal('EPSILON') 
dollar = G_Regex.Terminal('DOLLAR')   
obrace = G_Regex.Terminal('OBRACE')   
cbrace = G_Regex.Terminal('CBRACE')

Expression %= Expression + pipe + Alternative, lambda h,s: UnionNode(s[1],s[3])
Expression %= Alternative , lambda h,s: s[1]

Alternative %= caret + EndAnchor ,lambda h,s: StarAnchorNode(s[2])
EndAnchor %= Pattern + dollar ,lambda h,s: EndAnchorNode(s[1])
EndAnchor %= Pattern,lambda h,s: s[1]
Alternative %= EndAnchor ,lambda h,s: s[1]


Pattern  %= Pattern + Subpattern ,lambda h,s: ConcatNode(s[1],s[2])
Pattern  %= Pattern+ dot + Subpattern ,lambda h,s: DotNode(s[1],s[3])
Pattern  %= Subpattern ,lambda h,s: s[1]

Subpattern %= Subpattern + star ,lambda h,s: ClosureNode(s[1])
Subpattern %= Subpattern + plus ,lambda h,s: PlusNode(s[1])
Subpattern %= Subpattern + question ,lambda h,s: QuestNode(s[1])
Subpattern %= Subpattern + obrace + Number +cbrace ,lambda h,s: QuantifierNode(s[2],s[2])
Subpattern %= Subpattern + obrace + Number + minus + Number +cbrace ,lambda h,s:QuantifierNode(s[1],s[3],s[5])
Number %= MoreSymbols, lambda h,s: NumberNode(s[1])
MoreSymbols %= MoreSymbols + symbol, lambda h,s : s[1]+s[2]
MoreSymbols %= symbol,lambda h,s : s[1]
Subpattern %= obrckt + Range + cbrckt ,lambda h,s: RangeNode(s[2][0],s[2][1])
Subpattern %= obrckt + caret + Range + cbrckt, lambda h,s: NotRangeNode(s[3][0],s[3][1]) 
Subpattern %= opar + Expression + cpar ,lambda h,s: s[2]
Subpattern %= symbol ,lambda h,s:  SymbolNode(s[1])
Subpattern %= epsilon ,lambda h,s: EpsilonNode(s[1])

Range %= Range + SymbolOrRange ,lambda h,s: list(map(lambda t: t[0] + t[1], zip(s[1],s[2])))
Range %= SymbolOrRange ,lambda h,s: s[1]

SymbolOrRange %= symbol + minus +symbol ,lambda h,s: ([],[(s[1],s[3])])
SymbolOrRange %= symbol ,lambda h,s: ([s[1]],[])

