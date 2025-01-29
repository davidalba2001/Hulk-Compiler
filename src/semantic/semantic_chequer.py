from semantic.semantic import*
from semantic.type_builder import TypeBuilderVisitor
from semantic.type_checker import TypeCheckerVisitor
from semantic.type_collector import TypeCollectorVisitor
from interpreter.interpreter_visitor import InterpreterVisitor
class Semantic_Check:
    def __init__(self):
        self.scope = Scope()
        self.context = Context()
        self.default_types = ['Number', 'String', 'Boolean']
        self.default_functions = ['sin', 'cos', 'sqrt', 'exp', 'rand', 'log', 'print']
        self.errors = []
        for type in self.default_types:
            self.context.create_type(type)
        self.scope.define_variable('PI', "Number", Instance(self.context.get_type('Number')))
        self.context.types[VarType().name] = VarType()
        self.context.types[ErrorType().name] = ErrorType()
        self.context.types[VectorType().name] = VectorType()
        self.context.types[ObjectType().name] = ObjectType()
        for func in self.default_functions:
            self.context.functions[func] = None
        self.context.create_protocol('Base')
        self.context.create_protocol('Iterable').define_method('next', [], [], VarType())
        
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
        
    def interpreter(self, ast):
        interpreter = InterpreterVisitor(self.context, self.scope)
        interpreter.visit(ast, interpreter.scope)