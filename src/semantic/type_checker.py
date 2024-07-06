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
        if (left.name == rigt.name == 'number') or (left.name == 'number' and rigt.name == 'var') or (left.name == 'var' and rigt.name == 'number') or (left.name == 'var' and rigt.name == 'var'):
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede sumar tipos distintos a \'number\'"))
            return self.context.get_type('<error>')
    
    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if (left.name == rigt.name == 'number') or (left.name == 'number' and rigt.name == 'var') or (left.name == 'var' and rigt.name == 'number') or (left.name == 'var' and rigt.name == 'var'):
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede restar tipos distintos a \'number\'"))
            return self.context.get_type('<error>')
    
    @visitor.when(MultiplyNode)
    def visit(self, node: MultiplyNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if (left.name == rigt.name == 'number') or (left.name == 'number' and rigt.name == 'var') or (left.name == 'var' and rigt.name == 'number') or (left.name == 'var' and rigt.name == 'var'):
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede multiplicar tipos distintos a \'number\'"))
            return self.context.get_type('<error>')   
            
    @visitor.when(DivideNode)
    def visit(self, node: DivideNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if (left.name == rigt.name == 'number') or (left.name == 'number' and rigt.name == 'var') or (left.name == 'var' and rigt.name == 'number') or (left.name == 'var' and rigt.name == 'var'):
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede dividir tipos distintos a \'number\'"))
            return self.context.get_type('<error>')       
    
    @visitor.when(PowerNode)
    def visit(self, node: NumberNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if (left.name == rigt.name == 'number') or (left.name == 'number' and rigt.name == 'var') or (left.name == 'var' and rigt.name == 'number') or (left.name == 'var' and rigt.name == 'var'):
            return self.context.get_type('number')
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


#TODO: Falta implementar protocolo
    @visitor.when(AssignmentNode)
    def visit(self, node: AssignmentNode, scope: Scope):
        current_scope = scope.create_child()
        annotation: Type = self.context.get_type('var')
        try:
            annotation = self.context.get_type(node.type_annotation)
        except:
            self.errors.append(SemanticError(f'El tipo {node.type_annotation} anotado a la variable {node.identifier} no esta definido'))
            return self.context.get_type('<error>')
        
        exp_type: Type = self.context.get_type('object')
        if node.type_annotation == 'var':
            return self.visit(node.expression, current_scope)
        else:
            exp_type = self.visit(node.expression, current_scope)
        if exp_type.name == 'var': return annotation
        if not exp_type.conforms_to(annotation):
            self.errors.append(SemanticError(f'La variable {node.identifier} de tipo {annotation} no puede ser asignada con el tipo {exp_type}'))
            return self.context.get_type('<error>')
        else: return annotation
        
    @visitor.when(DassignmentNode)
    def visit(self, node: DassignmentNode, scope: Scope):
        current_scope = scope.create_child()
        var: VariableInfo = scope.find_variable(node.identifier)
        if not scope.is_defined(node.identifier):
            self.errors.append(SemanticError(f'La variable {node.identifier} no esta definida'))
            return self.context.get_type('<error>')
        
        exp_type: Type = self.context.get_type('object')
        if var.type == 'var':
            return self.visit(node.expression, current_scope)
        else:
            exp_type = self.visit(node.expression, current_scope)
        if exp_type.name == 'var': return self.context.get_type(var.type)
        if not exp_type.conforms_to(self.context.get_type(var.type)):
            self.errors.append(SemanticError(f'La variable {node.identifier} de tipo {self.context.get_type(var.type)} no puede ser asignada con el tipo {exp_type}'))
            return self.context.get_type('<error>')
        else: return self.context.get_type(var.type)


    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        try:
            funcs: list[Method] = self.context.functions[node.identifier]
        except:
            self.errors.append(SemanticError(f'La funcion {node.identifier} no esta definida en el contexto'))
            return self.context.get_type('<error>')
        definition = None
        for func in funcs:
            if len(func.param_names) == node.arguments:
                definition = func.definition
        if not definition:
            self.errors.append(SemanticError(f'La funcion {node.identifier} no tiene sobrecarga definida con {len(node.arguments)}'))
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

    @visitor.when(FuncInfo)
    def visit(self, node: FuncInfo, scope: Scope):
        func_scope = self.scope.create_child()
        func_def: FuncNode = node.function
        params = func_def.params
        args = node.params
        for i in range(0, len(params)):
            typex: Type = self.context.get_type(params[i][1])
            if typex.conforms_to(args[i]):
                func_scope.define_variable(params[i][0], typex.name)
            else:
                self.errors.append(SemanticError(f'El parametro {params[i][0]} debe recibir un argumento de {typex.name} en la funcion {func_def.identifier}'))
                return self.context.get_type('<error>')
        result: Type = self.visit(func_def.body, func_def)
        if result.name == '<error>': return result
        return_type = self.context.get_type(func_def.type_annotation)
        if result.conforms_to(return_type) and return_type.name != 'var':
            return return_type
        elif return_type.name == 'var':
            return result
        else:
            self.errors.append(SemanticError(f'No se esta retornando el tipo {return_type} en la funcion {func_def.identifier}'))    

    @visitor.when(FuncNode)
    def visit(self, node: FuncNode, scope: Scope):
        fun_scope = scope.create_child()
        for param in node.params:
            name, typex = param
            scope.define_variable(name, typex)
        result: Type = self.visit(node.body, fun_scope)
        if result.name == '<error>': return result
        if result.name == 'var': return node.type_annotation
        if not result.conforms_to(node.type_annotation):
            self.errors.append(SemanticError(f'No se esta retornando el tipo {node.type_annotation} en la funcion {node.identifier}'))
            return self.context.get_type('<error>')
        else: 
            return node.type_annotation

    @visitor.when(AsNode)
    def visit(self, node: AsNode, scope: Scope):
        try:
            down_cast = self.context.get_type(node.identifier)
        except:
            self.errors.append(SemanticError(f'El tipo {node.identifier} no esta definido'))
            return self.context.get_type('<error>')
        exp: Type = self.visit(node.expression)
        if exp.name is '<error>': return exp
        if exp.name is 'var' or exp.conforms_to(down_cast): return down_cast
        