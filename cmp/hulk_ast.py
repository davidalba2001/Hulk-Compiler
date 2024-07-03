
class Node:
    def __init__(self, node_type):
        self.node_type = node_type


class ProgramNode(Node):
    def __init__(self, statements, main_expression):
        super().__init__('PROGRAM')
        self.statements = statements
        self.main_expression = main_expression

class StatementsNode(Node):
    def __init__(self, statements_type, statements_func, statements_protocol):
        super().__init__('STATEMENTS')
        self.statements_type = statements_type
        self.statements_func = statements_func
        self.statements_protocol = statements_protocol
              
class ExpressionNode(Node):
    def __init__(self, ntype='EXPRESSION'):
        super().__init__(ntype)
        
class StatementNode(Node):
    def __init__(self, ntype='STATEMENT'):
        super().__init__(ntype)

class CallableNode(Node):
    def __init__(self, identifier, params, type_annotation, body, node_type='CALLABLE'):
        super().__init__(node_type)
        self.identifier = identifier
        self.params = params
        self.type_annotation = type_annotation
        self.body = body

#############################################################

class TypeNode(StatementNode):
    def __init__(self, identifier,params,superType,body):
        super().__init__('TYPE')
        self.identifier = identifier
        self.params = params
        self.superType = superType
        self.body = body
        
class ProtocolNode(StatementNode):
    def __init__(self, identifier,superProtocol,body):
        super().__init__('PROTOCOL')
        self.identifier = identifier
        self.superProtocol = superProtocol
        self.body = body

class AtomicNode(ExpressionNode):
    def __init__(self, lex,ntype = 'ATOMIC' ):
        super().__init__(ntype)
        self.lex = lex

class BinaryNode(ExpressionNode):
    def __init__(self, left, right,ntype='BINARY'):
        super().__init__(ntype)
        self.left = left
        self.right = right
        
class UnaryNode(ExpressionNode):
    def __init__(self,expressions,ntype = 'UNARY'):
        super().__init__(ntype)
        self.expressions = expressions
        
class ConditionalNode(ExpressionNode):
        def __init__(self,branch,ntype = 'CONDITIONAL'):
            super().__init__(branch,ntype)
            self.branch = branch
                  

class BindingNode(ExpressionNode):
        def __init__(self, identifier, expression,ntype = 'BINDING'):
            super().__init__('BINDING')
            self.identifier = identifier
            self.expression = expression
            
class LoopNode(ExpressionNode):
    def __init__(self,body,ntype = 'LOOP'):    
        self.body = body
        
class BlockNode(ExpressionNode):
    def __init__(self,expressions):
        super().__init__(expressions,'BLOCK')
        
class TypeInstanceNode(ExpressionNode):
    def __init__(self, ntype='TYPE_INSTANCE'):
        super().__init__(ntype)

class AsNode(ExpressionNode):
    def __init__(self, expression, identifier):
        super().__init__('AS')
        self.expression = expression
        self.identifier = identifier
        
class CallNode(ExpressionNode):
    def __init__(self, identifier, arguments, node_type):
        super().__init__(node_type)
        self.identifier = identifier
        self.arguments = arguments
        

class LetNode(ExpressionNode):
    def __init__(self, bindings, body):
        super().__init__('LET')
        self.bindings = bindings
        self.body = body
                

class VectorIndexNode(ExpressionNode):
    def __init__(self, identifier, index):
        super().__init__('VECTOR_INDEX')
        self.identifier = identifier
        self.index = index


class IsNode(ExpressionNode):
    def __init__(self, expression, identifier):
        super().__init__('IS')
        self.expression = expression
        self.identifier = identifier
        
 #########################################################################       
        
class FuncNode(CallableNode, StatementNode):
    def __init__(self, identifier, params, type_annotation, body):
        CallableNode.__init__(self, identifier, params, type_annotation, body, 'FUNCTION')
        StatementNode.__init__(self, 'FUNCTION')

class MethodNode(CallableNode):
    def __init__(self, identifier, params, type_annotation, body):
        CallableNode.__init__(self, identifier, params, type_annotation, body, 'METHOD')
                
class FunctionCallNode(CallNode):
    def __init__(self, identifier, arguments):
        super().__init__(identifier, arguments, 'FUNCTION_CALL')

class MethodCallNode(CallNode):
    def __init__(self, type_identifier, identifier, arguments):
        super().__init__(identifier, arguments, 'METHOD_CALL')
        self.type_identifier = type_identifier

class InstanceNode(TypeInstanceNode):
    def __init__(self, identifier, arguments):
        super().__init__('INSTANCE')
        self.identifier = identifier
        self.params = arguments

class ExplicitVectorNode(TypeInstanceNode):
    def __init__(self, arguments):
        super().__init__('EXPLICIT_VECTOR')
        self.arguments = arguments

class ImplicitVectorNode(TypeInstanceNode):
    def __init__(self, expression, identifier, iterable):
        super().__init__('IMPLICIT_VECTOR')
        self.expression = expression
        self.identifier = identifier
        self.iterable = iterable
        

class StringNode(AtomicNode):
    def __init__(self,lex):
        super().__init__(lex)
        self.node_type = 'STRING'
        
class StringConcatSpaceNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'STRING_CONCAT_SPACE'

class StringConcatNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.node_type = 'STRING_CONCAT' 

class WhileNode(LoopNode):
    def __init__(self, condition,body):
        super().__init__(body,'WHILE')
        self.condition = condition
       

class ForNode(LoopNode):
    def __init__(self, identifier, iterable, body):
        super().__init__(body,'FOR')
        self.identifier = identifier
        self.iterable = iterable

class AssignmentNode(BindingNode):
    def __init__(self, identifier, type_annotation, expression):
        super().__init__(identifier,expression,'ASSIGNMENT')
        self.type_annotation = type_annotation

class DassignmentNode(BindingNode):
    def __init__(self, identifier, expression):
        super().__init__(identifier,expression,'DASSIGNMENT')
        
  
class SqrtNode(FunctionCallNode):
    def __init__(self, arguments):
        super().__init__("sqrt",arguments,'SQRT')
        
class SinNode(FunctionCallNode):
    def __init__(self, arguments):
        super().__init__("sin",arguments,'SIN')
class CosNode(FunctionCallNode):
    def __init__(self, arguments):
        super().__init__("cos",arguments,'COS')
    
class ExpNode(FunctionCallNode):
    def __init__(self, arguments):
        super().__init__("exp",arguments,'EXP')
    
class RandNode(FunctionCallNode):
    def __init__(self, arguments):
        super().__init__("rand",arguments,'RAND')
         
class LogNode(FunctionCallNode):
        def __init__(self, arguments):
            super().__init__("log",arguments,'LOG')

class PrintNode(FunctionCallNode):
    def __init__(self, arguments):
            super().__init__("print",arguments,'PRINT')
            

class IfNode(ConditionalNode):
    def __init__(self, condition,branch, elif_nodes, false_branch):
        super().__init__(branch,'If')
        self.condition = condition
        self.elif_nodes = elif_nodes if elif_nodes else []
        self.false_branch = false_branch
    
class ElifNode(ConditionalNode):
    def __init__(self, condition, branch):
        super().__init__(branch,'ELIF')
        self.condition = condition

class ElseNode(ConditionalNode):
    def __init__(self, branch):
        super().__init__(branch,'ELSE')


class PlusNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'PLUS')

class MinusNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'MINUS')

class MultiplyNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'MULTIPLY')

class DivideNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'DIVIDE')

class PowerNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'POWER')

class OrNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'OR')
     

class AndNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'AND')

class NotNode(UnaryNode):
    def __init__(self,expression):
        super().__init__(expression,'NOT')
        

class LessThanNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'LESS_THAN')

class GreaterThanNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'GREATER_THAN')
     

class LessEqualNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'LESS_EQUAL')

class GreaterEqualNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'GREATER_EQUAL')
    

class EqualNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'EQUAL')

class NotEqualNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(left, right,'NOT_EQUAL')

class BooleanNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex,'BOOLEAN')
    
class NumberNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex,'NUMBER')

class ConstantNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex,"CONSTANT")