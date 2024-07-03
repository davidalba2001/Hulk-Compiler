from cmp.hulk_ast import *
from semantic.semantic import *
import cmp.visitor as visitor
from typing import List


class TypeCollectorVisitor():
    def __init__(self,context:Context, scope: Scope, errors) -> None:
        self.context: Context = context
        self.scope: Scope = scope
        self.errors: List[str] = errors
        self.currentType: Type = None

    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        statements: StatementsNode = node.statements
        for typex in statements.statements_type:
            self.visit(typex)
        for func in statements.statements_func:
            self.visit(func)
        for protocol in statements.statements_protocol:
            self.visit(protocol)
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):
        if node.identifier not in self.context.functions:
            try:
                self.context.create_type(node.identifier)
            except:
                self.errors.append(SemanticError(f'El nombre de tipo {node.identifier} ya ha sido tomado'))
        else: self.errors.append(f"El nombre {node.identifier} ya esta en uso")
    @visitor.when(FuncNode)
    def visit(self, node: FuncNode):
        if not(node.identifier in self.context.functions or node.identifier in self.context.types or node.identifier in self.context.protocols):
            self.context.functions[node.identifier] = []
            
    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode):
        try:
            self.context.create_protocol(node.identifier)
        except:
            self.errors.append(SemanticError(f'El nombre de protocolo {node.identifier} ya ha sido tomado'))




