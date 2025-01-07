from cmp.hulk_ast import *
import cmp.visitor as visitor


class Formatter(object):
    
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, tabs=0):
        pass

    @visitor.when(StatementNode)
    def visit(self, node:StatementNode, tabs=0):
        pass

    @visitor.when(CallableNode)
    def visit(self, node:StatementNode, tabs=0):
        pass
    
    @visitor.when(ExtendableNode)
    def visit(self, node:ExtendableNode, tabs=0):
        pass
    
    @visitor.when(ExpressionNode)
    def visit(self, node:ExpressionNode, tabs=0):
        pass
    @visitor.when(TypeNode)
    def visit(self, node:TypeNode, tabs=0):
        pass
    @visitor.when(ProtocolNode)
    def visit(self, node:ProtocolNode, tabs=0):
        pass
    @visitor.when(FuncNode)
    def visit(self, node:FuncNode, tabs=0):
        pass
    @visitor.when(AtomicNode)
    def visit(self, node:AtomicNode, tabs=0):
        pass
    @visitor.when(BinaryNode)
    def visit(self, node:BinaryNode, tabs=0):
        pass
    @visitor.when(UnaryNode)
    def visit(self, node:UnaryNode, tabs=0):
        pass
    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode, tabs=0):
        pass
    @visitor.when(LoopNode)
    def visit(self, node:LoopNode, tabs=0):
        pass
    @visitor.when(BlockNode)
    def visit(self, node:BlockNode, tabs=0):
        pass
    @visitor.when(TypeInstanceNode)
    def visit(self, node:TypeInstanceNode, tabs=0):
        pass
    @visitor.when(AsNode)
    def visit(self, node:AsNode, tabs=0):
        pass
    @visitor.when(CallNode)
    def visit(self, node:CallNode, tabs=0):
        pass
    @visitor.when(LetNode)
    def visit(self, node:LetNode, tabs=0):
        pass
    @visitor.when(VectorIndexNode)
    def visit(self, node:VectorIndexNode, tabs=0):
        pass
    @visitor.when(IsNode)
    def visit(self, node:IsNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass