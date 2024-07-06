from cmp.hulk_ast import *
from semantic.semantic import *
import cmp.visitor as visitor
from typing import List


class TypeCheckerVisitor():
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
        self.visit(node.main_expression)

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope: Scope):
        type_scope = scope.create_child()
        methods_scope = scope.create_child()
        methods_scope.define_variable('self', node.identifier.lex)
        for param, type in node.params:
            type_scope.define_variable(param, type)
        for att in node.attributes:
            self.visit(att, type_scope)
        for meth in node.methods:
            self.visit(meth, methods_scope)
    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        vars = []
        assign: AssignmentNode
        for assign in node.bindings:
            assignment: AssignmentNode = assign
            vars.append((assignment.identifier.lex, self.visit(assign, scope)))
        let_scope = scope.create_child()
        for var, type in vars:
            if type.name == '<error>':
                return type
            let_scope.define_variable(var, type.name)
        return self.visit(node.body, let_scope)

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        expression = None
        for exp in node.expressions:
            expression: Type = self.visit(exp, scope)
        return expression
    


    ### --------------- Expresiones aritmeticas con numbers -----------------------###
    ##################################################################################
    
    @visitor.when(PlusNode)
    def visit(self, node: PlusNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.name == rigt.name == 'number':
            return left
        else:
            self.errors.append(SemanticError("No se puede sumar tipos distintos a \'number\'"))
            return self.context.get_type('<error>')
    
    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.name == rigt.name == 'number':
            return left
        else:
            self.errors.append(SemanticError("No se puede restar tipos distintos a \'number\'"))
            return self.context.get_type('<error>')
    
    @visitor.when(MultiplyNode)
    def visit(self, node: MultiplyNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.name == rigt.name == 'number':
            return left
        else:
            self.errors.append(SemanticError("No se puede multiplicar tipos distintos a \'number\'"))
            return self.context.get_type('<error>')   
            
    @visitor.when(DivideNode)
    def visit(self, node: DivideNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.name == rigt.name == 'number':
            return left
        else:
            self.errors.append(SemanticError("No se puede dividir tipos distintos a \'number\'"))
            return self.context.get_type('<error>')       
    
    @visitor.when(PowerNode)
    def visit(self, node: NumberNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.name == rigt.name == 'number':
            return left
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'number\' en una exponenciacion"))
            return self.context.get_type('<error>')     
        
    @visitor.when(ConstantNode)
    def visit(self, node: ConstantNode, scope: Scope):
        return self.context.get_type('number')       

    @visitor.when(NumberNode)
    def visit(self, node:NumberNode, scope: Scope):
        return self.context.get_type('number')


    #####================================================================================================#######


#TODO: Revisar que la asignacion este en orden
    @visitor.when(AssignmentNode)
    def visit(self, node: AssignmentNode, scope: Scope):
        current_scope = scope.create_child()
        annotation: Type = self.context.get_type('var')
        try:
            annotation = self.context.get_type(node.type_annotation)
        except:
            self.errors.append(SemanticError(f'El tipo {node.type_annotation} anotado a la variable {node.identifier.lex} no esta definido'))
            return self.context.get_type('<error>')
        
        exp_type: Type = self.context.get_type('object')
        if node.type_annotation == 'var':
            current_scope.find_variable()
            return self.visit(node.expression, current_scope)
        else:
            exp_type = self.visit(node.expression, current_scope)
        if not exp_type.conforms_to(annotation):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} de tipo {annotation} no puede ser asignada con el tipo {exp_type}'))
            return self.context.get_type('<error>')
        else: return exp_type
        

    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        try:
            definition = self.context.functions[node.identifier.lex]
        except:
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no esta definida en el contexto'))
            return self.context.get_type('<error>')
        args = [self.visit(arg) for arg in node.arguments]
        if self.context.get_type('<error>') in args:
            return self.context.get_type('<error>')
        return self.visit(FuncInfo(args, definition), scope)
    
    @visitor.when(IdNode)
    def visit(self, node: IdNode, scope: Scope):
        variable: VariableInfo = None
        if scope.is_defined(node.lex):
            variable =  scope.find_variable()
            return self.context.get_type(variable.type)
        else:
            self.errors.append(SemanticError(f"La variable {node.lex} no esta definida"))
            return self.context.get_type('<error>')


