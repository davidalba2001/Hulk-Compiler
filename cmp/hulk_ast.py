# Clase base para todos los nodos
class Node:
    def __init__(self, node_type):
        self.node_type = node_type

# Nodo principal del programa
class Program(Node):
    def __init__(self, statements, main_expression):
        super().__init__('PROGRAM')
        self.statements = statements
        self.main_expression = main_expression

# Nodo para declaraciones de diferentes tipos
class StatementsNode(Node):
    def __init__(self, statements_type, statements_func, statements_protocol):
        super().__init__('STATEMENTS')
        self.statements_type = statements_type
        self.statements_func = statements_func
        self.statements_protocol = statements_protocol

# Nodo para declaraciones
class StatementNode(Node):
    def __init__(self, node_type='STATEMENT'):
        super().__init__(node_type)

# Nodo base para expresiones
class ExpressionNode(Node):
    def __init__(self, node_type='EXPRESSION'):
        super().__init__(node_type)

# Nodo para operaciones aritméticas
class ArithmeticNode(ExpressionNode):
    def __init__(self, left, right):
        super().__init__('ARITHMETIC')
        self.left = left
        self.right = right

# Nodo para átomos (constantes, literales)
class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        super().__init__('ATOMIC')
        self.lex = lex

# Nodo para operaciones binarias
class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        super().__init__('BINARY')
        self.left = left
        self.right = right

# Nodo para la definición de tipos
class TypeNode(StatementNode):
    def __init__(self, identifier, inherits_clause, type_body):
        super().__init__('TYPE')
        self.identifier = identifier
        self.inherits_clause = inherits_clause
        self.type_body = type_body

# Nodo para la definición de funciones
class FuncNode(StatementNode):
    def __init__(self, identifier, params, type_annotation, expression):
        super().__init__('FUNCTION')
        self.identifier = identifier
        self.params = params
        self.type_annotation = type_annotation
        self.expression = expression

# Nodo para la definición de protocolos
class ProtocolNode(StatementNode):
    def __init__(self, identifier, extends_clause, protocol_body):
        super().__init__('PROTOCOL')
        self.identifier = identifier
        self.extends_clause = extends_clause
        self.protocol_body = protocol_body

# Nodo para bloques de código
class BlockNode(ExpressionNode):
    def __init__(self, expressions):
        super().__init__('BLOCK')
        self.expressions = expressions

# Nodos para operaciones aritméticas específicas
class PlusNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'PLUS'

class MinusNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'MINUS'

class MultiplyNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'MULTIPLY'

class DivideNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'DIVIDE'

class PowerNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'POWER'

# Nodo para la declaración de variables con let
class LetNode(ExpressionNode):
    def __init__(self, bindings, body):
        super().__init__('LET')
        self.bindings = bindings
        self.body = body

# Nodo para una asignación
class AssignmentNode(StatementNode):
    def __init__(self, identifier, type_annotation, expression):
        super().__init__('ASSIGNMENT')
        self.identifier = identifier
        self.type_annotation = type_annotation
        self.expression = expression

# Nodo para la declaración destructiva
class DassignmentNode(StatementNode):
    def __init__(self, identifier, expression, type_annotation=None):
        super().__init__('DASSIGNMENT')
        self.identifier = identifier
        self.type_annotation = type_annotation
        self.expression = expression

# Nodos para operadores lógicos y relacionales
class OrNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'OR'

class AndNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'AND'

class IsNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'IS'

class NotNode(ExpressionNode):
    def __init__(self, expression):
        super().__init__('NOT')
        self.expression = expression

class LessThanNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'LESS_THAN'

class GreaterThanNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'GREATER_THAN'

class LessEqualNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'LESS_EQUAL'

class GreaterEqualNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'GREATER_EQUAL'

class EqualNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'EQUAL'

class NotEqualNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'NOT_EQUAL'

# Nodo para valores booleanos
class BooleanNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)
        self.node_type = 'BOOLEAN'

# Nodo para estructuras condicionales
class IfNode(ExpressionNode):
    def __init__(self, condition, true_block, elif_nodes=None, else_node=None):
        super().__init__('IF')
        self.condition = condition
        self.true_block = true_block
        self.elif_nodes = elif_nodes or []
        self.else_node = else_node

class ElifNode(ExpressionNode):
    def __init__(self, condition, block):
        super().__init__('ELIF')
        self.condition = condition
        self.block = block

class ElseNode(ExpressionNode):
    def __init__(self, block):
        super().__init__('ELSE')
        self.block = block

# Nodo para estructuras de bucles
class WhileNode(ExpressionNode):
    def __init__(self, condition, body):
        super().__init__('WHILE')
        self.condition = condition
        self.body = body

class ForNode(ExpressionNode):
    def __init__(self, identifier, iterable, body):
        super().__init__('FOR')
        self.identifier = identifier
        self.iterable = iterable
        self.body = body

# Nodo para concatenación de cadenas
class StringConcatNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'STRING_CONCAT'

# Nodo para llamadas a métodos y funciones
class MethodCallNode(ExpressionNode):
    def __init__(self, identifier, params):
        super().__init__('METHOD_CALL')
        self.identifier = identifier
        self.params = params

class FunctionCallNode(ExpressionNode):
    def __init__(self, identifier, params):
        super().__init__('FUNCTION_CALL')
        self.identifier = identifier
        self.params = params

# Nodo para instanciación de objetos
class InstanceNode(ExpressionNode):
    def __init__(self, identifier, params):
        super().__init__('INSTANCE')
        self.identifier = identifier
        self.params = params

# Nodo para acceso a índices de vectores
class VectorIndexNode(ExpressionNode):
    def __init__(self, identifier, index):
        super().__init__('VECTOR_INDEX')
        self.identifier = identifier
        self.index = index

# Nodo para expresiones de tipo "as"
class AsNode(ExpressionNode):
    def __init__(self, expression, identifier):
        super().__init__('AS')
        self.expression = expression
        self.identifier = identifier

# Nodo para la instrucción de impresión
class PrintNode(StatementNode):
    def __init__(self, expr):
        super().__init__('PRINT')
        self.expr = expr
