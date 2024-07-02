from cmp.pycompiler import Grammar

G = Grammar()

program = G.NonTerminal('PROGRAM', True)  
expression, expression_block, statements = G.NonTerminals('EXPRESSION EXPRESSION_BLOCK STATEMENTS') 
arithmetic_expr, term, exponential_term, factor = G.NonTerminals('ARITHMETIC_EXPR TERM EXPONENTIAL_TERM FACTOR')
function_def, function_inline, function_full = G.NonTerminals('FUNCTION_DEF FUNCTION_INLINE FUNCTION_FULL')  
function_call, builtin_function_call = G.NonTerminals('FUNCTION_CALL BUILTIN_FUNCTION_CALL')  
param_list, param = G.NonTerminals('PARAM_LIST PARAM')  
argument_list, argument = G.NonTerminals('ARGUMENT_LIST ARGUMENT')
let_expr, let_body = G.NonTerminals('LET_EXPR LET_BODY')
binding_list,binding= G.NonTerminals('BINDING_LIST BINDING')
assignment, dassignment = G.NonTerminals('ASSIGNMENT DASSIGNMENT')
constant = G.NonTerminals('CONSTANT')
string_expr , concat_string = G.NonTerminal('STRING_EXPR CONCAT_STRING')  
conditional_expr,if_clause,elif_clauses,elif_clause,else_clause = G.NonTerminal('CONDITIONAL_EXPR IF_CLAUSE ELIF_CLAUSES ELIF_CLAUSE ELSE_CLAUSE')
boolean_expr,boolean_term,boolean_factor = G.NonTerminal('BOOLEAN_EXPR BOOLEAN_TERM BOOLEAN_FACTOR')  
relational_expr , relatable_term,relational_op= G.NonTerminal('RELATIONAL_EXPR RELATABLE_TERM RELATIONAL_OP')  
while_loop , for_loop = G.NonTerminal('WHILE_LOOP FOR_LOOP')

# TERMINALS (TERMINALES)

sqrt, sin, cos, exp, log, rand, print_keyword = G.Terminals('SQRT SIN COS EXP LOG RAND PRINT') 
pi, e = G.Terminals('PI E')
number_literal, boolean_literal, string_literal = G.Terminals('NUMBER_LITERAL BOOLEAN_LITERAL STRING_LITERAL')  
plus, minus, multiply, divide, power = G.Terminals('+ - * / ^')  
less_than, greater_than, less_equal, greater_equal, equal, not_equal = G.Terminals('< > <= >= == !=')
and_op, or_op, not_op = G.Terminals('& | !')
paren_open, paren_close, brace_open, brace_close = G.Terminals('( ) { }')
comma, semicolon, at_symbol, arrow, assign, dassign = G.Terminals(', ; @ => = :=')
identifier = G.Terminal('IDENTIFIER') 
function_keyword, let_keyword, in_keyword= G.Terminals('FUNCTION LET IN')
if_keyword,elif_keyword,else_keyword = G.Terminal('IF ELIF ELSE')
true_keyword , false_keyword = G.Terminal('TRUE FALSE')
while_keyword, for_keyword = G.Terminals('WHILE FOR ')

############################################################

program %= statements

statements %= expression + semicolon + statements
statements %= expression + statements 
statements %= function_def + statements
statements %= function_def
statements %= expression


expression %= expression_block
expression %= arithmetic_expr
expression %= let_expr
expression %= function_call
expression %= boolean_expr
expression %= conditional_expr
expression %= while_loop
expression %= for_loop
expression %= string_expr

expression_block %= brace_open + statements + brace_close


arithmetic_expr %= arithmetic_expr + plus + term 
arithmetic_expr %= arithmetic_expr + minus + term 
arithmetic_expr %= term
term %= term + multiply + exponential_term 
term %= term + divide + exponential_term
term %= exponential_term
exponential_term %=  factor + power + exponential_term
exponential_term %=  factor
factor %= paren_open + expression + paren_close
factor %= number_literal

let_expr %= let_keyword + binding_list + in_keyword + let_body

binding_list %= binding_list + comma + binding
binding_list %= binding

binding %= assignment
binding %= dassignment

assignment %= identifier + assign + expression
dassignment %= identifier + dassign + expression

let_body %= expression  
let_body %= expression_block 

function_def %= function_inline
function_def %= function_full
function_inline %= function_keyword + identifier + paren_open + param_list + paren_close + arrow + expression 
function_full %= function_keyword + identifier + paren_open + param_list + paren_close + expression_block
param_list %= param_list  + comma + param 
param_list %= param
param %=  identifier

function_call %= identifier + paren_open + argument_list + paren_close
function_call %= builtin_function_call
argument_list %= argument_list + comma + argument  
argument_list %= argument 
argument %= expression  


builtin_function_call %= sqrt + paren_open + arithmetic_expr + paren_close
builtin_function_call %= sin + paren_open + arithmetic_expr + paren_close
builtin_function_call %= cos + paren_open + arithmetic_expr + paren_close
builtin_function_call %= exp + paren_open + arithmetic_expr + paren_close
builtin_function_call %= rand + paren_open + paren_close
builtin_function_call %= log + paren_open + arithmetic_expr + comma + arithmetic_expr + paren_close
builtin_function_call %= print_keyword + paren_open + expression + paren_close

boolean_expr %= boolean_expr + or_op + boolean_term
boolean_expr %= boolean_term

boolean_term %= boolean_term + and_op + boolean_factor
boolean_term %= boolean_factor

boolean_factor %= not_op + boolean_factor
boolean_factor %= paren_open + boolean_expr + paren_close
boolean_factor %= relational_expr
boolean_factor %= true_keyword
boolean_factor %= false_keyword

relational_expr %= relatable_term + relational_op + relatable_term
relational_op %= less_than | greater_than | less_equal | greater_equal | equal | not_equal
relatable_term %= arithmetic_expr

conditional_expr %= if_clause
conditional_expr %= if_clause + else_clause
conditional_expr %= if_clause + elif_clauses
conditional_expr %= if_clause + elif_clauses + else_clause

if_clause %= if_keyword + paren_open + boolean_expr + paren_close + expression
elif_clauses %= elif_clauses + elif_clause
elif_clauses %= elif_clause
elif_clause %= elif_keyword + paren_open + boolean_expr + paren_close + expression
else_clause %= else_keyword + expression

string_expr %= concat_string
string_expr %= string_literal

concat_string %= string_literal + at_symbol + expression 

while_loop %= while_keyword + paren_open + boolean_expr + paren_close + expression
for_loop %= for_keyword + paren_open + identifier + in_keyword + expression + paren_close + expression_block