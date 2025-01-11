from semantic.semantic import*
from semantic.type_builder import TypeBuilderVisitor
from semantic.type_checker import TypeCheckerVisitor
from semantic.type_collector import TypeCollectorVisitor
class Semantic_Check:
    def __init__(self):
        self.scope = Scope()
        self.context = Context()
        self.default_types = ['Object', 'Number', 'tring', 'Boolean', 'Var']
        self.default_functions = ['sen', 'cos', 'sqrt', 'exp', 'rand', 'log', 'print']
        self.errors = []
        for type in self.default_types:
            self.context.create_type(type)
        for func in self.default_functions:
            self.context.functions[func] = None
        self.context.types['ERROR'] = ErrorType() 
    def semantic_checking(self, ast):
        type_collector = TypeCollectorVisitor(self.context, self.scope, self.errors)
        type_collector.visit(ast)
        if len(type_collector.errors) > 0:
            return type_collector.errors

        type_builder = TypeBuilderVisitor(self.context, self.scope, self.errors)
        type_builder.visit(ast)
        if len(type_builder.errors) > 0:
            return type_builder.errors

        type_checker = TypeCheckerVisitor(self.context, self.scope, self.errors)
        type_checker.visit(ast)
        if len(type_checker.errors) > 0:
            return type_checker.errors
