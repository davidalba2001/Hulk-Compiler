from cmp.hulk_ast import *
from semantic.semantic import *
import cmp.visitor as visitor
from typing import List


class TypeCollectorVisitor():
    def __init__(self,context:Context, scope: Scope, errors) -> None:
        self.context: Context = context
        self.scope: Scope = scope
        self.errors: List[SemanticError] = errors
        self.currentType: Type = None

    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for typex in node.statements_type:
            self.visit(typex)
        for func in node.statements_func:
            self.visit(func)
        for protocol in node.statements_protocol:
            self.visit(protocol)
            
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):
        try:
            self.context.create_type(node.identifier)
        except SemanticError as e:
            self.context.types[node.identifier] = ErrorType()
            error_with_line = SemanticError(f"Error at line {node.line}: {str(e)}")
            self.errors.append(error_with_line)
        
    @visitor.when(FuncNode)
    def visit(self, node: FuncNode):
        try:
            self.context.register_function_name(node.identifier,len(node.params))
        except SemanticError as e:
            self.context.functions[node.identifier,len(node.params)] = ErrorType()
            error_with_line = SemanticError(f"Error at line {node.line}: {str(e)}")
            self.errors.append(error_with_line)
            
    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode):
        try:
            self.context.create_protocol(node.identifier)
        except SemanticError as e:
            self.context.protocols[node.identifier] = ErrorType()
            error_with_line = SemanticError(f"Error at line {node.line}: {str(e)}")
            self.errors.append(error_with_line)
