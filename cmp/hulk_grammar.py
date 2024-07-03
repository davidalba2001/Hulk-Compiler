from cmp.pycompiler import Grammar

G = Grammar()

program = G.NonTerminal('PROGRAM', startSymbol = True)  
expression, expression_block, statements, main_expression ,function_decls= G.NonTerminals('EXPRESSION EXPRESSION_BLOCK STATEMENTS MAIN_EXPRESSION FUNCTION_DECLS') 
arithmetic_expr, term, exponential_term, factor = G.NonTerminals('ARITHMETIC_EXPR TERM EXPONENTIAL_TERM FACTOR')
function_decl, function_inline, function_full = G.NonTerminals('FUNCTION_DECL FUNCTION_INLINE FUNCTION_FULL')  
function_call, builtin_function_call = G.NonTerminals('FUNCTION_CALL BUILTIN_FUNCTION_CALL')  
param_list, param = G.NonTerminals('PARAM_LIST PARAM')  
argument_list, argument = G.NonTerminals('ARGUMENT_LIST ARGUMENT')
let_expr, let_body,statement = G.NonTerminals('LET_EXPR LET_BODY STATEMENT')
binding_list,binding= G.NonTerminals('BINDING_LIST BINDING')
assignment, dassignment = G.NonTerminals('ASSIGNMENT DASSIGNMENT')
constant = G.NonTerminal('CONSTANT')
string_expr , concat_string = G.NonTerminals('STRING_EXPR CONCAT_STRING')  
conditional_expr,if_clause,elif_clauses,elif_clause,else_clause = G.NonTerminals('CONDITIONAL_EXPR IF_CLAUSE ELIF_CLAUSES ELIF_CLAUSE ELSE_CLAUSE')
boolean_expr,boolean_term,boolean_factor = G.NonTerminals('BOOLEAN_EXPR BOOLEAN_TERM BOOLEAN_FACTOR')  
relational_expr , relatable_term,relational_op= G.NonTerminals('RELATIONAL_EXPR RELATABLE_TERM RELATIONAL_OP')  
while_loop , for_loop = G.NonTerminals('WHILE_LOOP FOR_LOOP')
type_decl, type_body, type_inst = G.NonTerminals('TYPE_DECL TYPE_BODY TYPE_INST')
optional_parentized_param_list, parentized_param_list = G.NonTerminals('OPTIONAL_PARENIZED_PARAM_LIST PARENIZED_PARAM_LIST')
optional_parentized_argument_list,parentized_argument_list = G.NonTerminals('OPTIONAL_PARENIZED_ARGUMENT_LIST PARENIZED_ARGUMENT_LIST')
inherits_clause, attributes_or_methods, attribute_or_method = G.NonTerminals('INHERITS_CLAUSE ATTRIBUTES_OR_METHODS ATTRIBUTE_OR_METHOD')
signatures = G.NonTerminal('SIGNATURES') 
method_decl, method_inline, method_full, method_call, method_signature = G.NonTerminals('METHOD_DECL METHOD_INLINE METHOD_FULL METHOD_CALL METHOD_SIGNATURE')
type_annotation,optional_type_annotation = G.NonTerminals('TYPE_ANNOTATION OPTIONAL_TYPE_ANNOTATION')
annotation_params,annotation_param = G.NonTerminals('ANNOTATION_PARAMS ANNOTATION_PARAM')
protocol_decl,protocol_body,extends_clause  = G.NonTerminals('PROTOCOL_DECL PROTOCOL_BODY EXTENDS_CLAUSE')

is_expr, as_expr = G.NonTerminals('IS_EXPR AS_EXPR')
statement_block,expression_statement = G.NonTerminals('STATEMENT_BLOCK EXPRESSION_STATEMENT')
vector_inst, vector_explicit, vector_implicit, vector_indexing = G.NonTerminals('VECTOR_INST VECTOR_EXPLICIT VECTOR_IMPLICIT VECTOR_INDEXING')
# TERMINALS (TERMINALES)
#############################################################################################################################
sqrt_keyword, sin_keyword, cos_keyword, exp_keyword, log_keyword, rand_keyword, print_keyword = G.Terminals('SQRT SIN COS EXP LOG RAND PRINT') 
pi, e = G.Terminals('PI E')
identifier,number_literal, boolean_literal, string_literal = G.Terminals('IDENTIFIER NUMBER_LITERAL BOOLEAN_LITERAL STRING_LITERAL')  
plus, minus, multiply, divide, power = G.Terminals('+ - * / ^')  
less_than, greater_than, less_equal, greater_equal, equal, not_equal = G.Terminals('< > <= >= == !=')
and_op, or_op, not_op = G.Terminals('& | !')
paren_open, paren_close, brace_open, brace_close,square_bracket_open, square_bracket_close = G.Terminals('( ) { } [ ]')
comma, semicolon, at_symbol, arrow, assign, dassign,colon,dot,double_pipe = G.Terminals(', ; @ => = := : . ||')
function_keyword, let_keyword, in_keyword= G.Terminals('FUNCTION LET IN')
if_keyword,elif_keyword,else_keyword = G.Terminals('IF ELIF ELSE')
true_keyword , false_keyword = G.Terminals('TRUE FALSE')
while_keyword, for_keyword = G.Terminals('WHILE FOR ')
type_keyword = G.Terminal('TYPE')
new_keyword, inherits_keyword = G.Terminals('NEW INHERITS')
is_keyword , as_keyword = G.Terminals('IS AS')
protocol_keyword,extends_keyword = G.Terminals('PROTOCOL EXTENDS')
###############################################################################################################################
program %= statements + main_expression ,lambda h,s: ProgramNode(s[1],s[2])
statements %= statements  + statement ,lambda h,s : list(map(lambda t: t[0] + t[1], zip(s[1],s[2])))
statements %= G.Epsilon, lambda h, s: h[0] 
statement  %= type_decl, lambda h, s : ([s[1]],[],[]) 
statement  %= function_decl, lambda h, s:([],[s[1]],[])
statement  %= protocol_decl, lambda h, s: ([],[],[s[1]])

main_expression %= expression + semicolon ,lambda h,s: s[1]
main_expression %= expression_block ,lambda h,s: s[1]

# Expressions
expression %= expression_block ,lambda h,s: s[1]
expression %= arithmetic_expr ,lambda h,s: s[1]
expression %= let_expr ,lambda h,s: s[1]
expression %= function_call ,lambda h,s: s[1]
expression %= dassignment ,lambda h,s: s[1]
expression %= boolean_expr ,lambda h,s: s[1]
expression %= conditional_expr ,lambda h,s: s[1]
expression %= while_loop ,lambda h,s: s[1]
expression %= for_loop ,lambda h,s: s[1]
expression %= string_expr ,lambda h,s: s[1]
expression %= method_call ,lambda h,s: s[1]
expression %= type_inst ,lambda h,s: s[1]
expression %= vector_indexing ,lambda h,s: s[1]
expression %= expression + as_keyword + identifier ,lambda h,s: AsNode(s[1],s[3])

# Expression Block
expression_block %= brace_open + statement_block + brace_close ,lambda h,s: BlockNode(s[2])

#TODO: No se permite que un bloque de expresiones no contenga niguna expresion o se no se permite {}
statement_block %= statement_block + expression_statement ,lambda h,s: [s[1]] + s[2]
statement_block %= expression_statement ,lambda h,s: s[1]

expression_statement %= expression + semicolon ,lambda h,s: s[2]
expression_statement %= expression ,lambda h,s: s[2]

# Arithmetic Expression
arithmetic_expr %= arithmetic_expr + plus + term ,lambda h,s: PlusNode(s[1],s[2])
arithmetic_expr %= arithmetic_expr + minus + term ,lambda h,s: MinusNode(s[1],s[2])
arithmetic_expr %= lambda h,s: s[1] 
term %= term + multiply + exponential_term ,lambda h,s: MultiplyNode(s[1],s[2])
term %= term + divide + exponential_term, lambda h,s: DivideNode(s[1],s[2])
term %= exponential_term ,lambda h,s: s[1] 
exponential_term %=  factor + power + exponential_term ,lambda h,s: PowerNode(s[1],s[2])
exponential_term %=  factor ,lambda h,s: s[1]
factor %= paren_open + arithmetic_expr + paren_close, lambda h,s: s[2]
factor %= number_literal ,lambda h,s:NumberNode(s[1])
factor %= expression ,lambda h,s: s[1]
factor %= constant,lambda h,s: s[1]
constant %= e 
constant %= pi

# Let Expression
let_expr %= let_keyword + binding_list + in_keyword + let_body ,lambda h,s: LetNode(s[2],s[3])

binding_list %= binding_list + comma + binding ,lambda h,s: [s[1]] + s[3]
binding_list %= G.Epsilon,lambda h,s: h[0]
binding %= assignment ,lambda h,s: s[1]
binding %= dassignment ,lambda h,s: s[1]

assignment %= identifier + optional_type_annotation + assign + expression ,lambda h,s: AssignmentNode(s[1],s[2],s[4])
# ? Todo: Se pudiera hacer una dassign y declarar nuevo type_annotation?
dassignment %= identifier + dassign + expression , lambda h,s: DassignmentNode(s[1],s[3])

type_annotation %= colon + identifier ,lambda h,s: s[2]

optional_type_annotation %= type_annotation ,lambda h,s: s[1]
optional_type_annotation %= G.Epsilon ,lambda h,s: "var" #Todo : Duda de si esto devuelve None pudiera modelars

let_body %=  expression ,lambda h,s: s[1] 
# Functions Statmenets

function_decl %= function_inline ,lambda h,s: s[1]
function_decl %= function_full ,lambda h,s: s[1]

function_inline %= function_keyword + identifier + parentized_param_list + optional_type_annotation + arrow + expression ,lambda h,s: FuncNode(s[2],s[3],s[4],s[6])
function_full %= function_keyword + identifier + parentized_param_list + optional_type_annotation + expression_block,lambda h,s: FuncNode(s[2],s[3],s[4],s[5])

param_list %= param_list  + comma + param ,lambda h,s: [s[1]] + s[3]
param_list %= G.Epsilon , lambda h,s: h[0]
param %=  identifier + optional_type_annotation ,lambda h,s: (s[1],s[2])

parentized_param_list %= paren_open + param_list + paren_close ,lambda h,s: s[2]

optional_parentized_param_list %= parentized_param_list  ,lambda h,s: s[1]
optional_parentized_param_list %= G.Epsilon  ,lambda h,s: h[0]

# Functions Calls
function_call %= identifier + parentized_argument_list, lambda h,s: FunctionCallNode(s[1],s[2])
function_call %= builtin_function_call ,lambda h,s: s[1]
 
argument_list %= argument_list + comma + argument ,lambda h,s: [s[1]] + s[2]
argument_list %= G.Epsilon ,lambda h,s: h[0]
argument %= expression + optional_type_annotation ,lambda h,s: (s[1],s[2])

optional_parentized_argument_list %= parentized_argument_list ,lambda h,s: s[1]
optional_parentized_argument_list %= G.Epsilon ,lambda h,s: h[0]

parentized_argument_list %= paren_open + argument_list + paren_close ,lambda h,s: s[1]



builtin_function_call %= sqrt_keyword + paren_open + expression + paren_close,lambda h,s: SqrtNode(s[3])
builtin_function_call %= sin_keyword + paren_open + expression + paren_close,lambda h,s: SinNode(s[3])
builtin_function_call %= cos_keyword + paren_open + expression + paren_close,lambda h,s: CosNode(s[3])
builtin_function_call %= exp_keyword + paren_open + expression + paren_close,lambda h,s: ExpNode(s[3])
builtin_function_call %= rand_keyword + paren_open + paren_close,lambda h,s: RandNode()
builtin_function_call %= log_keyword + paren_open + expression + comma + expression + paren_close,lambda h,s: LogNode(s[3],s[5])
builtin_function_call %= print_keyword + paren_open + expression + paren_close,lambda h,s: PrintNode(s[3])

# Boolean Expression
boolean_expr %= boolean_expr + or_op + boolean_term ,lambda h,s: OrNode(s[1],s[2])
boolean_expr %= boolean_term ,lambda h,s: s[1]

boolean_term %= boolean_term + and_op + boolean_factor ,lambda h,s: AndNode(s[1],s[2])
boolean_term %= boolean_factor,lambda h,s: s[1]

boolean_factor %= expression + is_keyword + identifier ,lambda h,s: IsNode(s[1],s[2])
boolean_factor %= not_op + boolean_factor ,lambda h,s: NotNode(s[2])
boolean_factor %= paren_open + boolean_expr + paren_close,lambda h,s: s[2]
boolean_factor %= relational_expr ,lambda h,s: s[1]
boolean_factor %= true_keyword   ,lambda h,s: BooleanNode(s[1])
boolean_factor %= false_keyword ,lambda h,s: BooleanNode(s[1])

relational_expr %= relational_expr + less_than + relatable_term ,lambda h,s: LessThanNode(s[1],s[3])
relational_expr %= relational_expr + greater_than + relatable_term ,lambda h,s: GreaterThanNode(s[1],s[3])
relational_expr %= relational_expr + less_equal + relatable_term ,lambda h,s: LessEqualNode(s[1],s[3])
relational_expr %= relational_expr + greater_equal  + relatable_term ,lambda h,s: GreaterEqualNode(s[1],s[3])
relational_expr %= relational_expr + equal + relatable_term ,lambda h,s: EqualNode(s[1],s[3])
relational_expr %= relational_expr + not_equal + relatable_term ,lambda h,s: NotEqualNode(s[1],s[3])
relational_expr %= relatable_term ,lambda h,s: s[1]

relatable_term %= expression ,lambda h,s: s[1]

# Conditional Expression
conditional_expr %= if_clause + elif_clauses + else_clause ,lambda h,s: ConditionalNode(s[1][0],s[1][1],s[2],s[3])
    
if_clause %= if_keyword + paren_open + boolean_expr + paren_close + expression,lambda h,s:(s[3],s[5])

elif_clauses %= elif_clauses + elif_clause,lambda h,s: [s[1]] + s[2]
elif_clauses %= G.Epsilon ,lambda h,s: h[0]

elif_clause %= elif_keyword + paren_open + boolean_expr + paren_close + expression ,lambda h,s: ElifNode(s[3],s[5])

else_clause %= else_keyword + expression , lambda h,s: ElseNode(s[2])
else_clause %= G.Epsilon ,lambda h,s: h[0]

# Loop Expression
while_loop %= while_keyword + paren_open + boolean_expr + paren_close + expression ,lambda h,s: WhileNode(s[3],s[5])
for_loop %= for_keyword + paren_open + identifier + in_keyword + expression + paren_close + expression ,lambda h,s: ForNode(s[3],s[5],s[7])

# String Expression
string_expr %= concat_string,lambda h,s :
string_expr %= string_literal,lambda h,s :
concat_string %= string_literal + at_symbol + expression ,lambda h,s :

# Type Statement
type_decl %= type_keyword + identifier + optional_parentized_param_list + inherits_clause + brace_open + type_body + brace_close, lambda h,s: TypeNode(s[2],s[3],s[4],s[6])

inherits_clause %= inherits_keyword  + identifier + optional_parentized_argument_list ,lambda h,s : (s[1],s[2])
inherits_clause %= G.Epsilon ,lambda h,s : ("object",None)


type_body %= attributes_or_methods ,lambda h,s : s[1]

attributes_or_methods %= attributes_or_methods + attribute_or_method ,lambda h,s :
attributes_or_methods %= G.Epsilon ,lambda h,s :
    
attribute_or_method %= assignment + semicolon ,lambda h,s : ([s[1]],[])
attribute_or_method %= method_decl,lambda h,s :lambda h,s : ([],[s[1]])

method_decl %= method_inline ,lambda h,s : s[1]
method_decl %= method_full ,lambda h,s : s[1]
method_inline %= identifier + paren_open + param_list + paren_close + arrow + expression, lambda h,s: MethodNode(s[1],s[3],s[6])
method_full %=  identifier + paren_open + param_list + paren_close + expression_block, lambda h,s: MethodNode(s[1],s[3],s[5])
# Type Instnace Expression
type_inst %= new_keyword +  identifier + parentized_argument_list ,lambda h,s : InstanceNode(s[2],s[3])
type_inst %= vector_inst ,lambda h,s: s[1]

# Method Call Expression
method_call %= identifier + dot + identifier + paren_open + argument_list + paren_close,lambda h,s :MethodCallNode(s[1],s[3],s[5])

# Protocol Statement
protocol_decl %= protocol_keyword + identifier + extends_clause + brace_open + protocol_body + brace_close,lambda h,s :ProtocolNode(s[2],s[3],s[5])
protocol_body %= signatures,lambda h,s :s[1]

annotation_params %= annotation_params  + comma + annotation_param ,lambda h,s : s
annotation_params %= G.Epsilon,lambda h,s :
annotation_param %=  identifier + type_annotation,lambda h,s :

signatures %= signatures + method_signature,lambda h,s :
# Todo: Un protocolo puede estar vacio? : Modelado como que no
signatures %= method_signature,lambda h,s :

method_signature %= identifier + paren_open + annotation_params + paren_close + type_annotation + semicolon,lambda h,s :

extends_clause %= extends_keyword + identifier,lambda h,s :
extends_clause %= G.Epsilon,lambda h,s :

# Vector Instance
vector_inst %= vector_explicit ,lambda h,s :
vector_inst %= vector_implicit,lambda h,s :

vector_explicit %= square_bracket_open + argument_list + square_bracket_close,lambda h,s :
vector_implicit %= square_bracket_open + expression + double_pipe + identifier + in_keyword + expression + square_bracket_close,lambda h,s :

# Vector Indexing Expression
vector_indexing %= identifier + square_bracket_open + expression + square_bracket_close,lambda h,s :