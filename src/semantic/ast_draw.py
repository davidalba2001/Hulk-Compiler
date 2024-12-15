# from cmp.hulk_ast import *
# from semantic.semantic import *
# import cmp.visitor as visitor
# from typing import List

# import matplotlib.pyplot as plt
# import networkx as nx



# class ASTDrawer:
#     def __init__(self, context: Context, scope: Scope, errors) -> None:
#         self.context: Context = context
#         self.scope: Scope = scope
#         self.errors: List[str] = errors
#         self.currentType: Type = None

#     @visitor.on("node")
#     def visit(self, node, tabs):
#         pass
        
#     @visitor.when(ProgramNode)
#     def visit(self, node: ProgramNode):
#         pass