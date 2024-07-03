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
            vars.append((assignment.identifier, self.visit(assign, scope)))
        let_scope = scope.create_child()
        for var, type in vars:
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
        if left.conforms_to(self.context.get_type('number')) or rigt.conforms_to(self.context.get_type('number')) :
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede sumar tipos distintos a \'number\'"))
            return self.context.get_type('<error>')
    
    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('number')) or rigt.conforms_to(self.context.get_type('number')) :
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede restar tipos distintos a \'number\'"))
            return self.context.get_type('<error>')
    
    @visitor.when(MultiplyNode)
    def visit(self, node: MultiplyNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('number')) or rigt.conforms_to(self.context.get_type('number')) :
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede multiplicar tipos distintos a \'number\'"))
            return self.context.get_type('<error>')   
            
    @visitor.when(DivideNode)
    def visit(self, node: DivideNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('number')) or rigt.conforms_to(self.context.get_type('number')) :
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede dividir tipos distintos a \'number\'"))
            return self.context.get_type('<error>')       
    
    @visitor.when(PowerNode)
    def visit(self, node: NumberNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('number')) or rigt.conforms_to(self.context.get_type('number')) :
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

    ############ Con booleanos #################################################################################

    @visitor.when(OrNode)
    def visit(self, node: OrNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('boolean')) or rigt.conforms_to(self.context.get_type('boolean')) :
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'boolean\' en una expresion or"))
            return self.context.get_type('<error>')    
        
    @visitor.when(AndNode)
    def visit(self, node: AndNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('boolean')) or rigt.conforms_to(self.context.get_type('boolean')) :
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'boolean\' en una expresion and"))
            return self.context.get_type('<error>')   
    
    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope: Scope):
        return self.context.get_type('boolean')
    
    ######################## Comparadores ##############################################################################
    ###################################################################################################################
    #TODO: arreglar algunas cosas
    @visitor.when(LessEqualNode)
    def visit(self, node: LessEqualNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('boolean')) or rigt.conforms_to(self.context.get_type('boolean')) :
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'boolean\' en una expresion and"))
            return self.context.get_type('<error>')   
        
    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('boolean')) or rigt.conforms_to(self.context.get_type('boolean')) :
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'boolean\' en una expresion and"))
            return self.context.get_type('<error>')   

    @visitor.when(GreaterEqualNode)
    def visit(self, node: GreaterEqualNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('boolean')) or rigt.conforms_to(self.context.get_type('boolean')) :
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'boolean\' en una expresion and"))
            return self.context.get_type('<error>')   


    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('boolean')) or rigt.conforms_to(self.context.get_type('boolean')) :
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'boolean\' en una expresion and"))
            return self.context.get_type('<error>')   
    
    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('boolean')) or rigt.conforms_to(self.context.get_type('boolean')) :
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'boolean\' en una expresion \'equal\' "))
            return self.context.get_type('<error>')   
        
    @visitor.when(NotEqualNode)
    def visit(self, node: NotEqualNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        equatable: Protocol = self.context.get_protocol('equatable')
        if (equatable.implemented_by(left) and rigt.conforms_to(self.context.get_type('number'))):
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  un literal en una expresion \'not equal\' "))
            return self.context.get_type('<error>')   
    

    ############ Con strings #################################################################################
    @visitor.when(StringConcatNode)
    def visit(self, node: StringConcatNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('string')) or rigt.conforms_to(self.context.get_type('string')) :
            return self.context.get_type('string')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'string\' en una expresion concatenacion"))
            return self.context.get_type('<error>')   
        
    @visitor.when(StringConcatSpaceNode)
    def visit(self, node: StringConcatSpaceNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('string')) or rigt.conforms_to(self.context.get_type('string')) :
            return self.context.get_type('string')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'string\' en una expresion concatenacion"))
            return self.context.get_type('<error>')   
    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope: Scope):
        return self.context.get_type('string')

    #####================================================================================================#######


#TODO: Revisar que esto pinche
    @visitor.when(AssignmentNode)
    def visit(self, node: AssignmentNode, scope: Scope):
        current_scope = scope.create_child()
        annotation = self.context.get_type('var')
        protocol = False
        try:
            annotation = self.context.get_type(node.type_annotation)
        except:
            try:
                annotation = self.context.get_protocol(node.type_annotation)
                protocol = True
            except:    
                self.errors.append(SemanticError(f'El tipo {node.type_annotation} anotado a la variable {node.identifier} no esta definido'))
                return self.context.get_type('<error>')
        
        exp_type: Type = self.visit(node.expression, current_scope)
        if not exp_type.conforms_to(annotation) and not protocol:
            self.errors.append(SemanticError(f'La variable {node.identifier} de tipo {annotation} no puede ser asignada con el tipo {exp_type}'))
            return self.context.get_type('<error>')
        elif protocol and not annotation.implemented_by(exp_type):
            self.errors.append(SemanticError(f'La variable {node.identifier} de tipo {annotation} no puede ser asignada con el tipo {exp_type}'))
            return self.context.get_type('<error>')
        elif not protocol: return exp_type
        else: return annotation
        
    @visitor.when(DassignmentNode)
    def visit(self, node: DassignmentNode, scope: Scope):
        current_scope = scope.create_child()
        var: VariableInfo = scope.find_variable(node.identifier)
        if not scope.is_defined(node.identifier):
            self.errors.append(SemanticError(f'La variable {node.identifier} no esta definida'))
            return self.context.get_type('<error>')
        
        exp_type: Type = self.visit(node.expression, current_scope)
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
        return_type: Type = self.context.get_type(func_def.type_annotation)
        if result.conforms_to(return_type):
            return return_type
        else:
            self.errors.append(SemanticError(f'No se esta retornando el tipo {return_type} en la funcion {func_def.identifier}')) 
            return self.context.get_type('<error>')

    @visitor.when(FuncNode)
    def visit(self, node: FuncNode, scope: Scope):
        fun_scope = scope.create_child()
        for param in node.params:
            name, typex = param
            scope.define_variable(name, typex)
        result: Type = self.visit(node.body, fun_scope)
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
        if exp.conforms_to(down_cast): return down_cast
        else: return self.context.get_type('<error>')

    @visitor.when(IfNode)
    def visit(self, node: IfNode, scope: Scope):
        cond: Type = self.visit(node.condition, scope)
        if not cond.conforms_to(self.context.get_type('boolean')):
            self.errors.append(SemanticError(f'Solo typo booleano para condiciones de if'))
            return self.context.get_type('<error>')
        if_scope = scope.create_child()
        _:Type = self.visit(node.branch, if_scope)
        for eli in node.elif_nodes:
            _: Type = self.visit(eli, scope)
        _: Type = self.visit(node.false_branch, scope)
        return self.context.get_type('var')
    
    @visitor.when(ElifNode)
    def visit(self, node: ElifNode, scope: Scope):
        cond: Type = self.visit(node.condition, scope)
        if not cond.conforms_to(self.context.get_type('boolean')):
            self.errors.append(SemanticError(f'Solo typo booleano para condiciones de elif'))
            return self.context.get_type('<error>')
        if_scope = scope.create_child()
        result:Type = self.visit(node.branch, if_scope)
        return result

    @visitor.when(ElseNode)
    def visit(self, node:ElseNode, scope: Scope):
        cond: Type = self.visit(node.condition, scope)
        if not cond.conforms_to(self.context.get_type('boolean')):
            self.errors.append(SemanticError(f'Solo typo booleano para condiciones de else'))
            return self.context.get_type('<error>')
        if_scope = scope.create_child()
        result:Type = self.visit(node.branch, if_scope)
        return result

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        cond: Type = self.visit(node.condition, scope)
        if not cond.conforms_to(self.context.get_type('boolean')):
            self.errors.append(SemanticError(f'Solo typo booleano para condiciones de while'))
            return self.context.get_type('<error>')
        while_scope = scope.create_child()
        _:Type = self.visit(node.branch, while_scope)
        return self.context.get_type('var')


    @visitor.when(ForNode)
    def visit(self, node: ForNode, scope: Scope):
        iterable: Protocol = self.context.create_protocol('iterable')
        iterand: Type = self.visit(node.iterable, scope)
        if iterand.name == '<error>': return iterand
        if not iterable.implemented_by(iterand):
            self.errors.append(SemanticError(f'El iterador proporcionado no implementa iterable'))
            return self.context.get_type('<error>')
        for_scope = scope.create_child()
        for_scope.define_variable(node.identifier, 'var')
        result: Type = self.visit(node.body, for_scope)
        return result
    
    @visitor.when(MethodCallNode)
    def visist(self, node: MethodCallNode, scope: Scope):
        instance: VariableInfo = None
        if scope.is_defined(node.type_identifier): instance = scope.find_variable(node.type_identifier)
        else:
            self.errors.append(SemanticError(f'La variable {node.type_identifier} no esta definida en el ambito'))
        instance_type: Type =  self.context.get_type(instance.type)
        funcs: list[Method] = [method for method in instance_type.methods if method.name == node.identifier]
        if len(funcs) == 0:
            self.errors.append(SemanticError(f'La funcion {node.identifier} no esta definida en el tipo {instance_type.name}'))
            return self.context.get_type('<error>')
        definition = None
        for func in funcs:
            if len(func.param_names) == node.arguments:
                definition = func.definition
        if not definition:
            self.errors.append(SemanticError(f'La funcion {node.identifier} no tiene sobrecarga definida con {len(node.arguments)} en el tipo {instance_type.name}'))
            return self.context.get_type('<error>')
        args = [self.visit(arg) for arg in node.arguments]
        return self.visit(FuncInfo(args, definition), scope)
    ########### Built-in Functions ####################################################################################
    ###################################################################################################################
    @visitor.when(SqrtNode)
    def visit(self, node: SqrtNode, scope: Scope):
        argument:Type = self.visit(node.arguments, scope)
        if not argument.conforms_to(self.context.get_type('number')):
            self.errors.append(SemanticError(f'En la llamada a la funcion {node.identifier} no se esta usando un argumento numerico'))
            return self.context.get_type('<error>')
        else: return self.context.get_type('number')

    @visitor.when(SinNode)
    def visit(self, node: SinNode, scope: Scope):
        argument:Type = self.visit(node.arguments, scope)
        if not argument.conforms_to(self.context.get_type('number')):
            self.errors.append(SemanticError(f'En la llamada a la funcion {node.identifier} no se esta usando un argumento numerico'))
            return self.context.get_type('<error>')
        else: return self.context.get_type('number')

    @visitor.when(CosNode)
    def visit(self, node: CosNode, scope: Scope):
        argument:Type = self.visit(node.arguments, scope)
        if not argument.conforms_to(self.context.get_type('number')):
            self.errors.append(SemanticError(f'En la llamada a la funcion {node.identifier} no se esta usando un argumento numerico'))
            return self.context.get_type('<error>')
        else: return self.context.get_type('number')

    @visitor.when(ExpNode)
    def visit(self, node: ExpNode, scope: Scope):
        argument:Type = self.visit(node.arguments, scope)
        if not argument.conforms_to(self.context.get_type('number')):
            self.errors.append(SemanticError(f'En la llamada a la funcion {node.identifier} no se esta usando un argumento numerico'))
            return self.context.get_type('<error>')
        else: return self.context.get_type('number')

    @visitor.when(RandNode)
    def visit(self, node: RandNode, scope: Scope):
        return self.context.get_type('number')

    @visitor.when(LogNode)
    def visit(self, node: LogNode, scope: Scope):
        left:Type = self.visit(node.arguments[0], scope)
        rigt:Type = self.visit(node.arguments[1], scope)
        if left.conforms_to(self.context.get_type('number')) and rigt.conforms_to(self.context.get_type('number')) :
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a \'number\' al evaluar la funcion log"))
            return self.context.get_type('<error>')

    @visitor.when(PrintNode)
    def visit(self, node: PrintNode, scope: Scope):
        argument:Type = self.visit(node.arguments, scope)
        if not argument.conforms_to(self.context.get_type('number')):
            self.errors.append(SemanticError(f'En la llamada a la funcion {node.identifier} no puede usar argumentos de tipo {argument.name}'))
            return self.context.get_type('<error>')
        else: return argument
    #####################################################################################################################################
    ###################################################################################################################################
