
class Node:
    def __init__(self,line = None, node_type = 'NODE'):
        self.node_type = node_type
        self.line = line

class ProgramNode(Node):
    def __init__(self, statements, main_expression,line = None,ntype = 'PROGRAM'):
        super().__init__(line,ntype)
        self.statements = statements
        self.main_expression = main_expression

class StatementsNode(Node):
    def __init__(self, statements_type, statements_func, statements_protocol,line = None,ntype = 'STATEMENTS'):
        super().__init__(line,ntype)
        self.statements_type = statements_type
        self.statements_func = statements_func
        self.statements_protocol = statements_protocol
              
class ExpressionNode(Node):
    def __init__(self,line = None,ntype='EXPRESSION'):
        super().__init__(line,ntype)
        
class StatementNode(Node):
    def __init__(self,line = None,ntype='STATEMENT'):
        super().__init__(line,ntype)

class CallableNode(Node):
    def __init__(self, identifier, params, type_annotation, body,line = None,ntype='CALLABLE'):
        super().__init__(line,ntype)
        self.identifier = identifier
        self.params = params
        self.type_annotation = type_annotation
        self.body = body

#############################################################

class TypeNode(StatementNode):
    def __init__(self, identifier,params,base_type,body,line = None,ntype = 'TYPE'):
        super().__init__(line,ntype)
        self.identifier = identifier
        self.params = params
        self.base_type = base_type[0]
        self.base_type_args = base_type[1]
        self.attributes = body[0]
        self.methods = body[1]
        
class ProtocolNode(StatementNode):
    def __init__(self, identifier,superProtocol,body,line = None,ntype = 'PROTOCOL'):
        super().__init__(line,ntype)
        self.identifier = identifier
        self.superProtocol = superProtocol
        self.body = body

class AtomicNode(ExpressionNode):
    def __init__(self,lex,line = None,ntype = 'ATOMIC' ):
        super().__init__(line,ntype)
        self.lex = lex
        self.line = line
    
class BinaryNode(ExpressionNode):
    def __init__(self, left, right,line = None,ntype='BINARY'):
        super().__init__(line,ntype)
        self.left = left
        self.right = right
        
class UnaryNode(ExpressionNode):
    def __init__(self,expressions,line = None,ntype = 'UNARY'):
        super().__init__(line,ntype)
        self.expressions = expressions
        
class ConditionalNode(ExpressionNode):
        def __init__(self,branch,line = None,ntype = 'CONDITIONAL'):
            super().__init__(line,ntype)
            self.branch = branch
                  

class BindingNode(ExpressionNode):
        def __init__(self, identifier, expression,line = None,ntype = 'BINDING'):
            super().__init__(line,ntype)
            self.identifier = identifier
            self.expression = expression
            
class LoopNode(ExpressionNode):
    def __init__(self,body,line = None,ntype = 'LOOP'): 
        super().__init__(line,ntype)   
        self.body = body
        
class BlockNode(ExpressionNode):
    def __init__(self,expressions,line = None,ntype='BLOCK'):
        super().__init__(line,ntype)
        self.expressions = expressions
        
class TypeInstanceNode(ExpressionNode):
    def __init__(self,line = None,ntype='TYPE_INSTANCE'):
        super().__init__(line,ntype)

class AsNode(ExpressionNode):
    def __init__(self, expression, identifier,line = None,ntype = 'AS'):
        super().__init__(line,ntype)
        self.expression = expression
        self.identifier = identifier
        
class CallNode(ExpressionNode):
    def __init__(self, identifier, arguments,line = None,ntype = "CALL"):
        super().__init__(line,ntype)
        self.identifier = identifier
        self.arguments = arguments
        

class LetNode(ExpressionNode):
    def __init__(self, bindings, body,line = None, ntype = 'LET'):
        super().__init__(line,ntype)
        self.bindings = bindings
        self.body = body
                

class VectorIndexNode(ExpressionNode):
    def __init__(self, identifier, index,line = None,ntype = 'VECTOR_INDEX'):
        super().__init__(line,ntype)
        self.identifier = identifier
        self.index = index


class IsNode(ExpressionNode):
    def __init__(self, expression, identifier,line = None,ntype = 'IS'):
        super().__init__(line,ntype)
        self.expression = expression
        self.identifier = identifier
        
 #########################################################################      

class IdNode(AtomicNode):
    def __init__(self,lex,line = None, ntype='IDENTIFIER'):
        super().__init__(lex,line,ntype)

class FuncNode(CallableNode, StatementNode):
    def __init__(self, identifier, params, type_annotation, body,line = None,ntype = 'FUNCTION'):
        CallableNode.__init__(self, identifier, params, type_annotation,body,line,ntype )
        StatementNode.__init__(self,line,ntype)

class MethodNode(CallableNode):
    def __init__(self, identifier, params, type_annotation, body,line = None ,ntype = 'METHOD'):
        CallableNode.__init__(self, identifier, params, type_annotation, body,line)
                
class FunctionCallNode(CallNode):
    def __init__(self, identifier, arguments,line = None,ntype = 'FUNCTION_CALL'):
        super().__init__(identifier, arguments,line,ntype)

class MethodCallNode(CallNode):
    def __init__(self, type_identifier, identifier, arguments,line = None,ntype = 'METHOD_CALL'):
        super().__init__(identifier, arguments,line,ntype)
        self.type_identifier = type_identifier

class InstanceNode(TypeInstanceNode):
    def __init__(self, identifier, arguments,line = None,ntype = 'INSTANCE'):
        super().__init__(line,ntype)
        self.identifier = identifier
        self.params = arguments

class ExplicitVectorNode(TypeInstanceNode):
    def __init__(self, arguments,line = None,ntype = 'EXPLICIT_VECTOR'):
        super().__init__(line,ntype)
        self.arguments = arguments

class ImplicitVectorNode(TypeInstanceNode):
    def __init__(self, expression, identifier, iterable,line = None,ntype = 'IMPLICIT_VECTOR'):
        super().__init__(line,ntype)
        self.expression = expression
        self.identifier = identifier
        self.iterable = iterable
        
class StringNode(AtomicNode):
    def __init__(self,lex,line = None,ntype = 'STRING'):
        super().__init__(lex,line,ntype)

        
class StringConcatSpaceNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'STRING_CONCAT_SPACE'):
        super().__init__(left, right,line,ntype)
        

class StringConcatNode(BinaryNode):
    def __init__(self, left, right,line=None,ntype = 'STRING_CONCAT' ):
        super().__init__(left, right,line,ntype)

class WhileNode(LoopNode):
    def __init__(self, condition,body,line = None,ntype = 'WHILE'):
        super().__init__(body,line,ntype)
        self.condition = condition
       
class ForNode(LoopNode):
    def __init__(self, identifier, iterable,body,line = None,ntype = 'FOR'):
        super().__init__(body,line,ntype)
        self.identifier = identifier
        self.iterable = iterable

class AssignmentNode(BindingNode):
    def __init__(self, identifier, type_annotation, expression,line = None,ntype = 'ASSIGNMENT'):
        super().__init__(identifier,expression,line,ntype)
        self.type_annotation = type_annotation

class DassignmentNode(BindingNode):
    def __init__(self, identifier, expression,line = None,ntype = 'DASSIGNMENT'):
        super().__init__(identifier,expression,line,ntype)
         
class SqrtNode(FunctionCallNode):
    def __init__(self, arguments,line = None,ntype = 'SQRT'):
        super().__init__("sqrt",arguments,line,ntype)
        
class SinNode(FunctionCallNode):
    def __init__(self, arguments,line = None,ntype = 'SIN'):
        super().__init__("sin",arguments,line,ntype)
class CosNode(FunctionCallNode):
    def __init__(self, arguments,line = None,ntype = 'COS'):
        super().__init__("cos",arguments,line,ntype)
    
class ExpNode(FunctionCallNode):
    def __init__(self, arguments,line = None,ntype = 'EXP'):
        super().__init__("exp",arguments,line,ntype)
    
class RandNode(FunctionCallNode):
    def __init__(self, arguments,line = None,ntype = 'RAND'):
        super().__init__("rand",arguments,line,ntype)
         
class LogNode(FunctionCallNode):
        def __init__(self, arguments,line = None,ntype = 'LOG'):
            super().__init__("log",arguments,line,ntype)

class PrintNode(FunctionCallNode):
    def __init__(self, arguments,line = None,ntype = 'PRINT'):
            super().__init__("print",arguments,line,ntype)
            
class IfNode(ConditionalNode):
    def __init__(self, condition,branch, elif_nodes, false_branch,line = None,ntype = 'If'):
        super().__init__(branch,line,ntype)
        self.condition = condition
        self.elif_nodes = elif_nodes if elif_nodes else []
        self.false_branch = false_branch
    
class ElifNode(ConditionalNode):
    def __init__(self, condition, branch,line = None,ntype = 'ELIF'):
        super().__init__(branch,line,ntype)
        self.condition = condition

class ElseNode(ConditionalNode):
    def __init__(self, branch,line = None,ntype = 'ELSE'):
        super().__init__(branch,line,ntype)

class PlusNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'PLUS'):
        super().__init__(left, right,line,ntype)

class ModNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'MOD'):
        super().__init__(left, right,line,ntype)

class MinusNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'MINUS'):
        super().__init__(left, right,line,ntype)

class MultiplyNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'MULTIPLY'):
        super().__init__(left, right,line,ntype)

class DivideNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'DIVIDE'):
        super().__init__(left, right,line,ntype)

class PowerNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'POWER'):
        super().__init__(left, right,line,ntype)

class OrNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'OR'):
        super().__init__(left, right,line,ntype)
     
class AndNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'AND'):
        super().__init__(left, right,line,ntype)

class NotNode(UnaryNode):
    def __init__(self,expression,line = None,ntype = 'NOT'):
        super().__init__(expression,line,ntype)
        
class LessThanNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'LESS_THAN'):
        super().__init__(left, right,line,ntype)

class GreaterThanNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'GREATER_THAN'):
        super().__init__(left, right,line,ntype)
     
class LessEqualNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'LESS_EQUAL'):
        super().__init__(left, right,line,ntype)

class GreaterEqualNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'GREATER_EQUAL'):
        super().__init__(left, right,line,ntype)
    
class EqualNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'EQUAL'):
        super().__init__(left, right,line,ntype)

class NotEqualNode(BinaryNode):
    def __init__(self, left, right,line = None,ntype = 'NOT_EQUAL'):
        super().__init__(left, right,line,ntype)

class BooleanNode(AtomicNode):
    def __init__(self, lex,line = None,ntype = 'BOOLEAN'):
        super().__init__(lex,line,ntype)
    
class NumberNode(AtomicNode):
    def __init__(self,lex,line = None,ntype = 'NUMBER'):
        super().__init__(lex,line,ntype)

class ConstantNode(AtomicNode):
    def __init__(self, lex,line = None,ntype = 'CONSTANT'):
        super().__init__(lex,line,ntype)