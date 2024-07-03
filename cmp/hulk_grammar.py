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
sqrt, sin, cos, exp, log, rand, print_keyword = G.Terminals('SQRT SIN COS EXP LOG RAND PRINT') 
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
program %= statements + main_expression
statements %= statements  + statement
statements %= G.Epsilon
statement  %= type_decl
statement  %= function_decl
statement  %= protocol_decl

main_expression %= expression + semicolon
main_expression %= expression_block

# Expressions
expression %= expression_block
expression %= arithmetic_expr
expression %= let_expr
expression %= function_call
expression %= dassignment
expression %= boolean_expr
expression %= conditional_expr
expression %= while_loop
expression %= for_loop
expression %= string_expr
expression %= method_call
expression %= type_inst
expression %= vector_indexing
expression %= expression + as_keyword + identifier 

# Expression Block
expression_block %= brace_open + statement_block + brace_close

#TODO: No se permite que un bloque de expresiones no contenga niguna expresion o se no se permite {}
statement_block %= statement_block + expression_statement
statement_block %= expression_statement

expression_statement %= expression + semicolon
expression_statement %= expression

# Arithmetic Expression
arithmetic_expr %= arithmetic_expr + plus + term 
arithmetic_expr %= arithmetic_expr + minus + term 
arithmetic_expr %= term
term %= term + multiply + exponential_term 
term %= term + divide + exponential_term
term %= exponential_term
exponential_term %=  factor + power + exponential_term
exponential_term %=  factor
factor %= paren_open + arithmetic_expr + paren_close
factor %= number_literal
factor %= expression
factor %= constant
constant %= e
constant %= pi

# Let Expression
let_expr %= let_keyword + binding_list + in_keyword + let_body

binding_list %= binding_list + comma + binding
binding_list %= G.Epsilon
binding %= assignment 
binding %= dassignment 

assignment %= identifier + optional_type_annotation + assign + expression 
# ? Todo: Se pudiera hacer una dassign y declarar nuevo type_annotation?
dassignment %= identifier + dassign + expression

type_annotation %= colon + identifier

optional_type_annotation %= type_annotation
optional_type_annotation %= G.Epsilon

let_body %=  expression 
# Functions Statmenets

function_decl %= function_inline
function_decl %= function_full

function_inline %= function_keyword + identifier + parentized_param_list + optional_type_annotation + arrow + expression
function_full %= function_keyword + identifier + parentized_param_list + optional_type_annotation + expression_block

param_list %= param_list  + comma + param 
param_list %= G.Epsilon
param %=  identifier + optional_type_annotation

parentized_param_list %= paren_open + param_list + paren_close

optional_parentized_param_list %= parentized_param_list 
optional_parentized_param_list %= G.Epsilon


# Functions Calls
function_call %= identifier + parentized_argument_list
function_call %= builtin_function_call
 
argument_list %= argument_list + comma + argument  
argument_list %= G.Epsilon 
argument %= expression + optional_type_annotation 

optional_parentized_argument_list %= parentized_argument_list
optional_parentized_argument_list %= G.Epsilon

parentized_argument_list %= paren_open + argument_list + paren_close

builtin_function_call %= sqrt + paren_open + arithmetic_expr + paren_close
builtin_function_call %= sin + paren_open + arithmetic_expr + paren_close
builtin_function_call %= cos + paren_open + arithmetic_expr + paren_close
builtin_function_call %= exp + paren_open + arithmetic_expr + paren_close
builtin_function_call %= rand + paren_open + paren_close
builtin_function_call %= log + paren_open + arithmetic_expr + comma + arithmetic_expr + paren_close
builtin_function_call %= print_keyword + paren_open + expression + paren_close

# Boolean Expression
boolean_expr %= boolean_expr + or_op + boolean_term
boolean_expr %= boolean_term

boolean_term %= boolean_term + and_op + boolean_factor
boolean_term %= boolean_factor

boolean_factor %= expression + is_keyword + identifier
boolean_factor %= not_op + boolean_factor
boolean_factor %= paren_open + boolean_expr + paren_close
boolean_factor %= relational_expr
boolean_factor %= true_keyword
boolean_factor %= false_keyword

relational_expr %= relational_expr + relational_op + relatable_term
relational_expr %= relatable_term

relational_op %= less_than 
relational_op %= greater_than
relational_op %= less_equal
relational_op %= greater_equal
relational_op %= equal 
relational_op %= not_equal
#Todo: Existan otro tipo de expresione relacionables ?
relatable_term %= arithmetic_expr 

# Conditional Expression
conditional_expr %= if_clause + elif_clauses + else_clause

if_clause %= if_keyword + paren_open + boolean_expr + paren_close + expression

elif_clauses %= elif_clauses + elif_clause
elif_clauses %= G.Epsilon

elif_clause %= elif_keyword + paren_open + boolean_expr + paren_close + expression

else_clause %= else_keyword + expression
else_clause %= G.Epsilon

# Loop Expression
while_loop %= while_keyword + paren_open + boolean_expr + paren_close + expression
for_loop %= for_keyword + paren_open + identifier + in_keyword + expression + paren_close + expression

# String Expression
string_expr %= concat_string
string_expr %= string_literal

concat_string %= string_literal + at_symbol + expression 

# Type Statement
type_decl %= type_keyword + identifier + optional_parentized_param_list + inherits_clause + brace_open + type_body + brace_close

inherits_clause %= inherits_keyword  + identifier + optional_parentized_argument_list
inherits_clause %= G.Epsilon

# Type Instnace Expression
type_inst %= new_keyword +  identifier + parentized_argument_list
type_inst %= vector_inst
type_body %= attributes_or_methods

attributes_or_methods %= attributes_or_methods + attribute_or_method
attributes_or_methods %= G.Epsilon

attribute_or_method %= assignment + semicolon
attribute_or_method %= method_decl

method_decl %= method_inline
method_decl %= method_full
method_inline %= identifier + paren_open + param_list + paren_close + arrow + expression 
method_full %=  identifier + paren_open + param_list + paren_close + expression_block

# Method Call Expression
method_call %= identifier + dot + identifier + paren_open + argument_list + paren_close

# Protocol Statement
protocol_decl %= protocol_keyword + identifier + extends_clause + brace_open + protocol_body + brace_close
protocol_body %= signatures

annotation_params %= annotation_params  + comma + annotation_param 
annotation_params %= G.Epsilon
annotation_param %=  identifier + type_annotation

signatures %= signatures + method_signature
# Todo: Un protocolo puede estar vacio? : Modelado como que no
signatures %= method_signature

method_signature %= identifier + paren_open + annotation_params + paren_close + type_annotation + semicolon

extends_clause %= extends_keyword + identifier
extends_clause %= G.Epsilon

# Vector Instance
vector_inst %= vector_explicit 
vector_inst %= vector_implicit

vector_explicit %= square_bracket_open + argument_list + square_bracket_close
vector_implicit %= square_bracket_open + expression + double_pipe + identifier + in_keyword + expression + square_bracket_close

# Vector Indexing Expression
vector_indexing %= identifier + square_bracket_open + expression + square_bracket_close