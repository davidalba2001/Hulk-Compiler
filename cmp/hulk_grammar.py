from cmp.pycompiler import Grammar
from cmp.hulk_ast import *

Hulk_G = Grammar()

program = Hulk_G.NonTerminal('PROGRAM', startSymbol = True)  
expression, expression_block, statements, main_expression ,function_decls= Hulk_G.NonTerminals('EXPRESSION EXPRESSION_BLOCK STATEMENTS MAIN_EXPRESSION FUNCTION_DECLS') 
arithmetic_expr, term, exponential_term, factor = Hulk_G.NonTerminals('ARITHMETIC_EXPR TERM EXPONENTIAL_TERM FACTOR')
function_decl, function_inline, function_full = Hulk_G.NonTerminals('FUNCTION_DECL FUNCTION_INLINE FUNCTION_FULL')  
function_call, builtin_function_call = Hulk_G.NonTerminals('FUNCTION_CALL BUILTIN_FUNCTION_CALL')  
param_list, param = Hulk_G.NonTerminals('PARAM_LIST PARAM')  
argument_list, argument = Hulk_G.NonTerminals('ARGUMENT_LIST ARGUMENT')
let_expr, let_body,statement = Hulk_G.NonTerminals('LET_EXPR LET_BODY STATEMENT')
binding_list,binding= Hulk_G.NonTerminals('BINDING_LIST BINDING')
assignment, dassignment = Hulk_G.NonTerminals('ASSIGNMENT DASSIGNMENT')
constant = Hulk_G.NonTerminal('CONSTANT')
string_expr , concat_string,concat_space_string = Hulk_G.NonTerminals('STRING_EXPR CONCAT_STRING CONCAT_SPACE_STRING')  
conditional_expr,if_clause,elif_clauses,elif_clause,else_clause = Hulk_G.NonTerminals('CONDITIONAL_EXPR IF_CLAUSE ELIF_CLAUSES ELIF_CLAUSE ELSE_CLAUSE')
boolean_expr,boolean_term,boolean_factor = Hulk_G.NonTerminals('BOOLEAN_EXPR BOOLEAN_TERM BOOLEAN_FACTOR')  
relational_expr , relatable_term,relational_op= Hulk_G.NonTerminals('RELATIONAL_EXPR RELATABLE_TERM RELATIONAL_OP')  
while_loop , for_loop = Hulk_G.NonTerminals('WHILE_LOOP FOR_LOOP')
type_decl, type_body, type_inst = Hulk_G.NonTerminals('TYPE_DECL TYPE_BODY TYPE_INST')
optional_parentized_param_list, parentized_param_list = Hulk_G.NonTerminals('OPTIONAL_PARENIZED_PARAM_LIST PARENIZED_PARAM_LIST')
optional_parentized_argument_list,parentized_argument_list = Hulk_G.NonTerminals('OPTIONAL_PARENIZED_ARGUMENT_LIST PARENIZED_ARGUMENT_LIST')
inherits_clause, attributes_or_methods, attribute_or_method = Hulk_G.NonTerminals('INHERITS_CLAUSE ATTRIBUTES_OR_METHODS ATTRIBUTE_OR_METHOD')
signatures = Hulk_G.NonTerminal('SIGNATURES') 
method_decl, method_inline, method_full, method_call, method_signature = Hulk_G.NonTerminals('METHOD_DECL METHOD_INLINE METHOD_FULL METHOD_CALL METHOD_SIGNATURE')
type_annotation,optional_type_annotation = Hulk_G.NonTerminals('TYPE_ANNOTATION OPTIONAL_TYPE_ANNOTATION')
annotation_params,annotation_param = Hulk_G.NonTerminals('ANNOTATION_PARAMS ANNOTATION_PARAM')
protocol_decl,protocol_body,extends_clause  = Hulk_G.NonTerminals('PROTOCOL_DECL PROTOCOL_BODY EXTENDS_CLAUSE')
is_expression,as_expression = Hulk_G.NonTerminals('IS_EXPRESSION','AS_EXPRESSION')
statement_block,expression_statement = Hulk_G.NonTerminals('STATEMENT_BLOCK EXPRESSION_STATEMENT')
vector_inst, vector_explicit, vector_implicit, vector_indexing = Hulk_G.NonTerminals('VECTOR_INST VECTOR_EXPLICIT VECTOR_IMPLICIT VECTOR_INDEXING')

# TERMINALS (TERMINALES)
#############################################################################################################################
sqrt_keyword, sin_keyword, cos_keyword, exp_keyword, log_keyword, rand_keyword, print_keyword = Hulk_G.Terminals('SQRT_KEYWORD SIN_KEYWORD COS_KEYWORD EXP_KEYWORD LOG_KEYWORD RAND_KEYWORD PRINT_KEYWORD')
pi, e = Hulk_G.Terminals('PI E')
identifier, number_literal, boolean_literal, string_literal = Hulk_G.Terminals('IDENTIFIER NUMBER_LITERAL BOOLEAN_LITERAL STRING_LITERAL')
plus, minus, multiply, divide, power, percent = Hulk_G.Terminals('PLUS MINUS MULTIPLY DIVIDE POWER PERCENT')
less_than, greater_than, less_equal, greater_equal, equal, not_equal = Hulk_G.Terminals('LESS_THAN GREATER_THAN LESS_EQUAL GREATER_EQUAL EQUAL NOT_EQUAL')
and_op, or_op, not_op = Hulk_G.Terminals('AND_OP OR_OP NOT_OP')
paren_open, paren_close, brace_open, brace_close, square_bracket_open, square_bracket_close = Hulk_G.Terminals('PAREN_OPEN PAREN_CLOSE BRACE_OPEN BRACE_CLOSE SQUARE_BRACKET_OPEN SQUARE_BRACKET_CLOSE')
comma, semicolon, at_symbol, at_at_symbol, arrow, assign, dassign, colon, dot, double_pipe = Hulk_G.Terminals('COMMA SEMICOLON AT_SYMBOL AT_AT_SYMBOL ARROW ASSIGN DASSIGN COLON DOT DOUBLE_PIPE')
function_keyword, let_keyword, in_keyword = Hulk_G.Terminals('FUNCTION_KEYWORD LET_KEYWORD IN_KEYWORD')
if_keyword, elif_keyword, else_keyword = Hulk_G.Terminals('IF_KEYWORD ELIF_KEYWORD ELSE_KEYWORD')
true_keyword, false_keyword = Hulk_G.Terminals('TRUE_KEYWORD FALSE_KEYWORD')
while_keyword, for_keyword = Hulk_G.Terminals('WHILE_KEYWORD FOR_KEYWORD')
type_keyword = Hulk_G.Terminal('TYPE_KEYWORD')
new_keyword, inherits_keyword = Hulk_G.Terminals('NEW_KEYWORD INHERITS_KEYWORD')
is_keyword, as_keyword = Hulk_G.Terminals('IS_KEYWORD AS_KEYWORD')
protocol_keyword, extends_keyword = Hulk_G.Terminals('PROTOCOL_KEYWORD EXTENDS_KEYWORD')
 
###############################################################################################################################
line = 'line'
###############################################################################################################################
program %= statements + main_expression ,lambda h,s: ProgramNode(s[1],s[2])
program %= statements ,lambda h,s: ProgramNode(s[1],None)
program %= main_expression,lambda h,s: ProgramNode(None,s[1])


statements %= statements  + statement ,lambda h,s : list(map(lambda t: t[0] + t[1], zip(s[1],s[2])))
statements %= statement, lambda h, s: s[1]
 
statement  %= type_decl, lambda h, s : ([s[1]],[],[]) 
statement  %= function_decl, lambda h, s:([],[s[1]],[])
statement  %= protocol_decl, lambda h, s: ([],[],[s[1]])

main_expression %= expression + semicolon ,lambda h,s: s[1]
main_expression %= expression_block ,lambda h,s: s[1]

# Expressions
expression %= arithmetic_expr ,lambda h,s: s[1]
expression %=  boolean_expr ,lambda h,s: s[1]
expression %= expression_block ,lambda h,s: s[1]
expression %= let_expr ,lambda h,s: s[1]
expression %= function_call ,lambda h,s: s[1]
expression %= dassignment ,lambda h,s: s[1]
expression %= conditional_expr ,lambda h,s: s[1]
expression %= while_loop ,lambda h,s: s[1]
expression %= for_loop ,lambda h,s: s[1]
expression %= string_expr ,lambda h,s: s[1]
expression %= method_call ,lambda h,s: s[1]
expression %= type_inst ,lambda h,s: s[1]
expression %= vector_indexing ,lambda h,s: s[1]
expression %= as_expression ,lambda h,s: s[1]
expression %= identifier , lambda h, s: IdNode(s[1],s[1,line])

as_expression %= expression + as_keyword + identifier ,lambda h,s: AsNode(s[1],s[3],s[2,line])
# Expression Block
expression_block %= brace_open + statement_block + brace_close ,lambda h,s: BlockNode(s[2])

#TODO: No se permite que un bloque de expresiones no contenga niguna expresion o se no se permite {}
statement_block %= statement_block + expression_statement ,lambda h,s: [s[1]] + s[2]
statement_block %= expression_statement ,lambda h,s: s[1]

expression_statement %= expression + semicolon ,lambda h,s: s[2]
#expression_statement %= expression ,lambda h,s: s[2]
# Arithmetic Expression
arithmetic_expr %= arithmetic_expr + plus + term ,lambda h,s: PlusNode(s[1],s[3],s[2,line])
arithmetic_expr %= arithmetic_expr + minus + term ,lambda h,s: MinusNode(s[1],s[3],s[2,line])
arithmetic_expr %= term, lambda h,s: s[1]  
term %= term + multiply + exponential_term ,lambda h,s: MultiplyNode(s[1],s[3],s[2,line])
term %= term + divide + exponential_term, lambda h,s: DivideNode(s[1],s[3],s[2,line])
term %= term + percent + exponential_term, lambda h,s: ModNode(s[1],s[3],s[2,line])
term %= exponential_term ,lambda h,s: s[1] 
exponential_term %=  factor + power + exponential_term ,lambda h,s: PowerNode(s[1],s[3],s[2,line])
exponential_term %=  factor ,lambda h,s: s[1]

factor %= paren_open + arithmetic_expr + paren_close, lambda h,s: s[2]
factor %= number_literal ,lambda h,s:NumberNode(s[1],s[1,line])
factor %= constant,lambda h,s: s[1]
constant %= e  ,lambda h,s: ConstantNode(s[1],s[1,line])
constant %= pi ,lambda h,s: ConstantNode(s[1],s[1,line])


factor %=  boolean_expr ,lambda h,s: s[1]
factor %= expression_block ,lambda h,s: s[1]
factor %= let_expr ,lambda h,s: s[1]
factor %= function_call ,lambda h,s: s[1]
factor %= dassignment ,lambda h,s: s[1]
factor %= conditional_expr ,lambda h,s: s[1]
factor %= while_loop ,lambda h,s: s[1]
factor %= for_loop ,lambda h,s: s[1]
factor %= string_expr ,lambda h,s: s[1]
factor %= method_call ,lambda h,s: s[1]
factor %= type_inst ,lambda h,s: s[1]
factor %= vector_indexing ,lambda h,s: s[1]
factor %= as_expression ,lambda h,s: s[1]
factor %= identifier , lambda h, s: IdNode(s[1],s[1,line])





# Let Expression
let_expr %= let_keyword + binding_list + in_keyword + let_body ,lambda h,s: LetNode(s[2],s[4],s[1,line])

binding_list %= binding_list + comma + binding ,lambda h,s: [s[1]] + s[3]
binding_list %= binding ,lambda h,s: s[1]
binding %= assignment ,lambda h,s: s[1]
binding %= dassignment ,lambda h,s: s[1]

assignment %= identifier + optional_type_annotation + assign + expression ,lambda h,s: AssignmentNode(s[1],s[2],s[4],s[3,line])
# ? Todo: Se pudiera hacer una dassign y declarar nuevo type_annotation?
dassignment %= identifier + dassign + expression , lambda h,s: DassignmentNode(s[1],s[3],s[2,line])

type_annotation %= colon + identifier ,lambda h,s: s[2]

optional_type_annotation %= type_annotation ,lambda h,s: s[1]
optional_type_annotation %= Hulk_G.Epsilon ,lambda h,s: "Var" #Todo : Duda de si esto devuelve None pudiera modelars

let_body %=  expression ,lambda h,s: s[1] 
# Functions Statmenets

function_decl %= function_inline ,lambda h,s: s[1]
function_decl %= function_full ,lambda h,s: s[1]

function_inline %= function_keyword + identifier + parentized_param_list + optional_type_annotation + arrow + expression ,lambda h,s: FuncNode(s[2],s[3],s[4],s[6],s[1,line])
function_full %= function_keyword + identifier + parentized_param_list + optional_type_annotation + expression_block,lambda h,s: FuncNode(s[2],s[3],s[4],s[5],s[1,line])

param_list %= param_list  + comma + param ,lambda h,s: [s[1]] + s[3]
param_list %= Hulk_G.Epsilon , lambda h,s: h[0]
param %=  identifier + optional_type_annotation ,lambda h,s: (s[1],s[2])

parentized_param_list %= paren_open + param_list + paren_close ,lambda h,s: s[2]

optional_parentized_param_list %= parentized_param_list  ,lambda h,s: s[1]
optional_parentized_param_list %= Hulk_G.Epsilon  ,lambda h,s: h[0]

# Functions Calls
function_call %= identifier + parentized_argument_list, lambda h,s: FunctionCallNode(s[1],s[2],s[1,line])
function_call %= builtin_function_call ,lambda h,s: s[1]
 
argument_list %= argument_list + comma + argument ,lambda h,s: [s[1]] + s[2]
argument_list %= Hulk_G.Epsilon ,lambda h,s: h[0]
argument %= expression ,lambda h,s: s[1]

optional_parentized_argument_list %= parentized_argument_list ,lambda h,s: s[1]
optional_parentized_argument_list %= Hulk_G.Epsilon ,lambda h,s: h[0]

parentized_argument_list %= paren_open + argument_list + paren_close ,lambda h,s: s[1]


builtin_function_call %= sqrt_keyword + paren_open + expression + paren_close,lambda h,s: SqrtNode(s[3],s[1,line])
builtin_function_call %= sin_keyword + paren_open + expression + paren_close,lambda h,s: SinNode(s[3],s[1,line])
builtin_function_call %= cos_keyword + paren_open + expression + paren_close,lambda h,s: CosNode(s[3],s[1,line])
builtin_function_call %= exp_keyword + paren_open + expression + paren_close,lambda h,s: ExpNode(s[3],s[1,line])
builtin_function_call %= rand_keyword + paren_open + paren_close,lambda h,s: RandNode(s[1,line])
builtin_function_call %= log_keyword + paren_open + expression + comma + expression + paren_close,lambda h,s: LogNode([s[3]] + s[5],s[1,line])
builtin_function_call %= print_keyword + paren_open + expression + paren_close,lambda h,s: PrintNode(s[3],s[1,line])

# Boolean Expression
boolean_expr %= boolean_expr + or_op + boolean_term ,lambda h,s: OrNode(s[1],s[3],s[2,line])
boolean_expr %= boolean_term ,lambda h,s: s[1]

boolean_term %= boolean_term + and_op + boolean_factor ,lambda h,s: AndNode(s[1],s[3],s[2,line])
boolean_term %= boolean_factor,lambda h,s: s[1]

boolean_factor %= is_expression ,lambda h,s: s[1]
boolean_factor %= not_op + boolean_factor ,lambda h,s: NotNode(s[2],s[1,line])
boolean_factor %= paren_open + boolean_expr + paren_close,lambda h,s: s[2]
boolean_factor %= relational_expr ,lambda h,s: s[1]
boolean_factor %= true_keyword   ,lambda h,s: BooleanNode(s[1],s[1,line])
boolean_factor %= false_keyword ,lambda h,s: BooleanNode(s[1],s[1,line])

is_expression %= expression + is_keyword + identifier ,lambda h,s: IsNode(s[1],s[3],s[2,line])

relational_expr %= relational_expr + less_than + relatable_term ,lambda h,s: LessThanNode(s[1],s[3],s[2,line])
relational_expr %= relational_expr + greater_than + relatable_term ,lambda h,s: GreaterThanNode(s[1],s[3],s[2,line])
relational_expr %= relational_expr + less_equal + relatable_term ,lambda h,s: LessEqualNode(s[1],s[3],s[2,line])
relational_expr %= relational_expr + greater_equal  + relatable_term ,lambda h,s: GreaterEqualNode(s[1],s[3],s[2,line])
relational_expr %= relational_expr + equal + relatable_term ,lambda h,s: EqualNode(s[1],s[3],s[2,line])
relational_expr %= relational_expr + not_equal + relatable_term ,lambda h,s: NotEqualNode(s[1],s[3],s[2,line])
relational_expr %= relatable_term ,lambda h,s: s[1]


relatable_term %= arithmetic_expr ,lambda h,s: s[1]
relatable_term %= expression_block ,lambda h,s: s[1]
relatable_term %= let_expr ,lambda h,s: s[1]
relatable_term %= function_call ,lambda h,s: s[1]
relatable_term %= dassignment ,lambda h,s: s[1]
relatable_term %= conditional_expr ,lambda h,s: s[1]
relatable_term %= while_loop ,lambda h,s: s[1]
relatable_term %= for_loop ,lambda h,s: s[1]
relatable_term %= string_expr ,lambda h,s: s[1]
relatable_term %= method_call ,lambda h,s: s[1]
relatable_term %= type_inst ,lambda h,s: s[1]
relatable_term %= vector_indexing ,lambda h,s: s[1]
relatable_term %= as_expression ,lambda h,s: s[1]
relatable_term %= identifier , lambda h, s: IdNode(s[1],s[1,line])






# Conditional Expression
conditional_expr %= if_clause + elif_clauses + else_clause ,lambda h,s: IfNode(s[1][0],s[1][1],s[2],s[3],s[1][2])
    
if_clause %= if_keyword + paren_open + expression + paren_close + expression,lambda h,s:(s[3],s[5],s[1,line])

elif_clauses %= elif_clauses + elif_clause,lambda h,s: [s[1]] + s[2]
elif_clauses %= Hulk_G.Epsilon ,lambda h,s: h[0]

elif_clause %= elif_keyword + paren_open + expression + paren_close + expression ,lambda h,s: ElifNode(s[3],s[5],s[1,line])

else_clause %= else_keyword + expression , lambda h,s: ElseNode(s[2],s[1,line])
else_clause %= Hulk_G.Epsilon ,lambda h,s: h[0]

# Loop Expression
while_loop %= while_keyword + paren_open + expression + paren_close + expression ,lambda h,s: WhileNode(s[3],s[5],s[1,line])
for_loop %= for_keyword + paren_open + identifier + in_keyword + expression + paren_close + expression ,lambda h,s: ForNode(s[3],s[5],s[7],s[1,line])

# String Expression
string_expr %= concat_string,lambda h,s : s[1]
string_expr %= concat_space_string,lambda h,s : s[1]
string_expr %= string_literal,lambda h,s : StringNode(s[1],s[1,line])
 

concat_string %= concat_string + at_symbol + expression ,lambda h,s : StringConcatNode(s[1],s[3],s[2,line])
concat_string % string_expr,lambda h,s : s[1]
 
concat_space_string %= concat_space_string + at_at_symbol + expression ,lambda h,s : StringConcatSpaceNode(s[1],s[3],s[2,line])
concat_space_string %= string_expr, lambda h,s : s[1]
# Type Statement
type_decl %= type_keyword + identifier + optional_parentized_param_list + inherits_clause + brace_open + type_body + brace_close, lambda h,s: TypeNode(s[2],s[3],s[4],s[6],s[1,line])

inherits_clause %= inherits_keyword  + identifier + optional_parentized_argument_list ,lambda h,s : (s[1],s[2])
inherits_clause %= Hulk_G.Epsilon ,lambda h,s : ("Object",None) #TODO Creo que deberia ser ('object','object')


type_body %= attributes_or_methods ,lambda h,s : s[1]

attributes_or_methods %= attributes_or_methods + attribute_or_method ,lambda h,s : list(map(lambda t: t[0] + t[1], zip(s[1],s[2])))
attributes_or_methods %= Hulk_G.Epsilon ,lambda h,s : h[0]
    
attribute_or_method %= assignment + semicolon ,lambda h,s : ([s[1]],[])
attribute_or_method %= method_decl,lambda h,s :lambda h,s : ([],[s[1]])

method_decl %= method_inline ,lambda h,s : s[1]
method_decl %= method_full ,lambda h,s : s[1]

method_inline %= identifier + parentized_param_list + optional_type_annotation + arrow + expression, lambda h,s: MethodNode(s[1],s[2],s[3],s[5],s[1,line])
method_full %= identifier + parentized_param_list + optional_type_annotation + expression_block, lambda h,s: MethodNode(s[1],s[2],s[3],s[4],s[1,line])
# Type Instnace Expression
type_inst %= new_keyword +  identifier + parentized_argument_list ,lambda h,s : InstanceNode(s[2],s[3],s[1,line])
type_inst %= vector_inst ,lambda h,s: s[1]

# Method Call Expression
method_call %= identifier + dot + identifier + paren_open + argument_list + paren_close,lambda h,s :MethodCallNode(s[1],s[3],s[5],s[1,line])

# Protocol Statement
protocol_decl %= protocol_keyword + identifier + extends_clause + brace_open + protocol_body + brace_close,lambda h,s :ProtocolNode(s[2],s[3],s[5],s[1,line])
protocol_body %= signatures,lambda h,s :s[1]

annotation_params %= annotation_params  + comma + annotation_param ,lambda h,s : [s[1]] + s[2]
annotation_params %= Hulk_G.Epsilon,lambda h,s : h[0]
annotation_param %=  identifier + type_annotation,lambda h,s : (s[1],s[2])

signatures %= signatures + method_signature,lambda h,s : [s[1]]+s[2]
# Todo: Un protocolo puede estar vacio? : Modelado como que no
signatures %= method_signature,lambda h,s : s[1]

method_signature %= identifier + paren_open + annotation_params + paren_close + type_annotation + semicolon,lambda h,s : (s[1],s[3],s[5])

extends_clause %= extends_keyword + identifier,lambda h,s : s[2]
extends_clause %= Hulk_G.Epsilon,lambda h,s : lambda h,s: h[0]

# Vector Instance
vector_inst %= vector_explicit ,lambda h,s :s[1]
vector_inst %= vector_implicit,lambda h,s :s[1]

vector_explicit %= square_bracket_open + argument_list + square_bracket_close,lambda h,s : ExplicitVectorNode(s[2],s[1,line])
vector_implicit %= square_bracket_open + expression + double_pipe + identifier + in_keyword + expression + square_bracket_close,lambda h,s :ImplicitVectorNode(s[2],s[4],s[6],s[1,line])

# Vector Indexing Expression
vector_indexing %= identifier + square_bracket_open + expression + square_bracket_close,lambda h,s : VectorIndexNode(s[1],s[3],s[1,line])
