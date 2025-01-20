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
        for typex in node.statements_type:
            self.visit(typex, self.scope.create_child())
        for func in node.statements_func:
            self.visit(func, self.scope.create_child())
        for protocol in node.statements_protocol:
            self.visit(protocol, self.scope.create_child())
        if node.main_expression:
            self.visit(node.main_expression, self.scope.create_child())

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope: Scope):
        current = self.context.get_type(node.identifier.lex)
        current.type_scope.define_variable('self', node.identifier.lex)
        type_scope = current.type_scope.create_child()
        methods_scope = current.type_scope.create_child()
        for param, type in node.params:
            type_scope.define_variable(param.lex, type.lex)
        for att in node.attributes:
            self.visit(att, type_scope)
        for meth in node.methods:
            self.visit(meth, methods_scope)
    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        vars = []
        assign: AssignmentNode
        for assign in node.bindings:
            assignment: AssignmentNode | DassignmentNode = assign
            vars.append((assignment.identifier.lex, self.visit(assign, scope)))
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
        num_t = self.context.get_type('number')
        if left.conforms_to(num_t) or rigt.conforms_to(self.context.get_type('number')) :
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede sumar tipos distintos a \'number\'"))
            return ErrorType()
    
    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('number')) or rigt.conforms_to(self.context.get_type('number')) :
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede restar tipos distintos a \'number\'"))
            return ErrorType()
    
    @visitor.when(MultiplyNode)
    def visit(self, node: MultiplyNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('number')) or rigt.conforms_to(self.context.get_type('number')) :
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede multiplicar tipos distintos a \'number\'"))
            return ErrorType()   
            
    @visitor.when(DivideNode)
    def visit(self, node: DivideNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('number')) or rigt.conforms_to(self.context.get_type('number')) :
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede dividir tipos distintos a \'number\'"))
            return ErrorType()       
    
    @visitor.when(PowerNode)
    def visit(self, node: NumberNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('number')) or rigt.conforms_to(self.context.get_type('number')) :
            return self.context.get_type('number')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'number\' en una exponenciacion"))
            return ErrorType()
        

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
            return ErrorType()    
        
    @visitor.when(AndNode)
    def visit(self, node: AndNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('boolean')) or rigt.conforms_to(self.context.get_type('boolean')) :
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'boolean\' en una expresion and"))
            return ErrorType()   
    
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
            return ErrorType()   
        
    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('boolean')) or rigt.conforms_to(self.context.get_type('boolean')) :
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'boolean\' en una expresion and"))
            return ErrorType()   

    @visitor.when(GreaterEqualNode)
    def visit(self, node: GreaterEqualNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('boolean')) or rigt.conforms_to(self.context.get_type('boolean')) :
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'boolean\' en una expresion and"))
            return ErrorType()   


    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('boolean')) or rigt.conforms_to(self.context.get_type('boolean')) :
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'boolean\' en una expresion and"))
            return ErrorType()   
    
    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('boolean')) or rigt.conforms_to(self.context.get_type('boolean')) :
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'boolean\' en una expresion \'equal\' "))
            return ErrorType()   
        
    @visitor.when(NotEqualNode)
    def visit(self, node: NotEqualNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        equatable: Protocol = self.context.get_protocol('equatable')
        if (equatable.implemented_by(left) and rigt.conforms_to(self.context.get_type('number'))):
            return self.context.get_type('boolean')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  un literal en una expresion \'not equal\' "))
            return ErrorType()   
    

    ############ Con strings #################################################################################
    @visitor.when(StringConcatNode)
    def visit(self, node: StringConcatNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('string')) or rigt.conforms_to(self.context.get_type('string')) :
            return self.context.get_type('string')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'string\' en una expresion concatenacion"))
            return ErrorType()   
        
    @visitor.when(StringConcatSpaceNode)
    def visit(self, node: StringConcatSpaceNode, scope: Scope):
        left:Type = self.visit(node.left, scope)
        rigt:Type = self.visit(node.right, scope)
        if left.conforms_to(self.context.get_type('string')) or rigt.conforms_to(self.context.get_type('string')) :
            return self.context.get_type('string')
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'string\' en una expresion concatenacion"))
            return ErrorType()   
    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope: Scope):
        return self.context.get_type('string')

    #####================================================================================================#######

    @visitor.when(AssignmentNode)
    def visit(self, node: AssignmentNode, scope: Scope):
        current_scope = scope.create_child()
        annotation = self.context.get_type('Var')
        protocol = False
        try:
            annotation = self.context.get_type(node.type_annotation.lex)
        except:
            try:
                annotation = self.context.get_protocol(node.type_annotation.lex)
                protocol = True
            except:    
                self.errors.append(SemanticError(f'El tipo {node.type_annotation.lex} anotado a la variable {node.identifier.lex} no esta definido'))
                return ErrorType()
        
        exp_type: Type = self.visit(node.expression, current_scope)
        if not exp_type.conforms_to(annotation) and not protocol:
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} de tipo {annotation} no puede ser asignada con el tipo {exp_type}'))
            return ErrorType()
        elif protocol and not annotation.implemented_by(exp_type):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} de tipo {annotation} no puede ser asignada con el tipo {exp_type}'))
            return ErrorType()
        elif not protocol: return exp_type
        else: return annotation
        
    @visitor.when(DassignmentNode)
    def visit(self, node: DassignmentNode, scope: Scope):
        current_scope = scope.create_child()
        exp_type: Type = self.visit(node.expression, current_scope)
        if isinstance(node.identifier, MemberAccessNode):
            member = node.identifier
            member_type = self.visit(member)
            if isinstance(member_type, ErrorType): return ErrorType()
            
            exp_type: Type = self.visit(node.expression, current_scope)
            if not exp_type.conforms_to(self.context.get_type(var.type)):
                self.errors.append(SemanticError(f'La variable {node.identifier.lex} de tipo {self.context.get_type(var.type)} no puede ser asignada con el tipo {exp_type}'))
                return ErrorType()
            return member_type
        
        
        if not scope.is_defined(node.identifier.lex):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} no esta definida'))
            return ErrorType()
        var: VariableInfo = scope.find_variable(node.identifier.lex)
        if not exp_type.conforms_to(self.context.get_type(var.type)):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} de tipo {self.context.get_type(var.type)} no puede ser asignada con el tipo {exp_type}'))
            return ErrorType()
        
        return self.context.get_type(var.type)


    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        if node.identifier.lex == 'print': return self.context.get_type('string')

        try:
            functs: Method = [self.context.functions[funct] for funct in self.context.functions if funct[0] == node.identifier.lex]
        except:
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no esta definida en el contexto'))
            return ErrorType()
        try:
            func: Method = self.context.functions[node.identifier.lex, len(node.arguments)]
        except:    
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no tiene sobrecarga definida con {len(node.arguments)} {"parametro" if len(node.arguments) == 1 else "parametros"}'))
            return ErrorType()
        
        definition = func.definition
        args = [self.visit(arg, scope) for arg in node.arguments]
        return self.visit(FuncInfo(args, definition), self.scope)

    @visitor.when(IdentifierNode)
    def visit(self, node: IdentifierNode, scope: Scope):
        variable: VariableInfo = None
        if scope.is_defined(node.lex):
            variable =  scope.find_variable(node.lex)
            return self.context.get_type(variable.type)
        else:
            self.errors.append(SemanticError(f"La variable {node.lex} no esta definida"))
            return ErrorType()

    @visitor.when(FuncInfo)
    def visit(self, node: FuncInfo, scope: Scope):
        func_scope = scope.create_child()
        func_def: FuncNode | MethodNode = node.function
        args = func_def.params
        params: List[Type] = node.params
        for i in range(0, len(params)):
            typex: Type = self.context.get_type(args[i][1].lex)
            if params[i].conforms_to(typex):
                func_scope.define_variable(args[i][0].lex, params[i])
            else:
                self.errors.append(SemanticError(f'El parametro {args[i][0].lex} debe recibir un argumento de tipo {typex.name} en la funcion {func_def.identifier.lex}'))
                return ErrorType()
        result: Type = self.visit(func_def.body, func_scope)
        return_type: Type = self.context.get_type(func_def.type_annotation.lex)
        if result.conforms_to(return_type):
            return return_type
        else:
            self.errors.append(SemanticError(f'No se esta retornando el tipo {return_type} en la funcion {func_def.identifier.lex}')) 
            return ErrorType()

    @visitor.when(FuncNode)
    def visit(self, node: FuncNode, scope: Scope):
        fun_scope = scope.create_child()
        for param in node.params:
            name, typex = param
            fun_scope.define_variable(name.lex, typex.lex)
        result: Type = self.visit(node.body, fun_scope)
        if not result.conforms_to(self.context.get_type(node.type_annotation.lex)):
            self.errors.append(SemanticError(f'No se esta retornando el tipo {node.type_annotation.lex} en la funcion {node.identifier.lex}'))
            return ErrorType()
        else: 
            return node.type_annotation.lex

    @visitor.when(AsNode)
    def visit(self, node: AsNode, scope: Scope):
        try:
            down_cast = self.context.get_type(node.identifier.lex)
        except:
            self.errors.append(SemanticError(f'El tipo {node.identifier.lex} no esta definido'))
            return ErrorType()
        exp: Type = self.visit(node.expression)
        if exp.conforms_to(down_cast): return down_cast
        else: return ErrorType()

    @visitor.when(IfNode)
    def visit(self, node: IfNode, scope: Scope):
        cond: Type = self.visit(node.condition, scope)
        if not cond.conforms_to(self.context.get_type('boolean')):
            self.errors.append(SemanticError(f'Solo typo booleano para condiciones de if'))
            return ErrorType()
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
            return ErrorType()
        if_scope = scope.create_child()
        result:Type = self.visit(node.branch, if_scope)
        return result

    @visitor.when(ElseNode)
    def visit(self, node:ElseNode, scope: Scope):
        cond: Type = self.visit(node.condition, scope)
        if not cond.conforms_to(self.context.get_type('boolean')):
            self.errors.append(SemanticError(f'Solo typo booleano para condiciones de else'))
            return ErrorType()
        if_scope = scope.create_child()
        result:Type = self.visit(node.branch, if_scope)
        return result

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        cond: Type = self.visit(node.condition, scope)
        if not cond.conforms_to(self.context.get_type('boolean')):
            self.errors.append(SemanticError(f'Solo typo booleano para condiciones de while'))
            return ErrorType()
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
            return ErrorType()
        for_scope = scope.create_child()
        for_scope.define_variable(node.identifier.lex, 'var')
        result: Type = self.visit(node.body, for_scope)
        return result
    
    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode, scope: Scope):
        instance: VariableInfo = None
        members = self.verify_member_access(node.member_access[:-1], scope)
        if isinstance(members, ErrorType): return members
        if scope.is_defined(node.type_identifier.lex): instance = scope.find_variable(node.type_identifier.lex)
        else:
            self.errors.append(SemanticError(f'La variable {node.type_identifier.lex} no esta definida en el ambito'))
        instance_type: Type =  self.context.get_type(instance.type)
        funcs: list[Method] = [instance_type.methods[method] for method in instance_type.methods if method[0] == node.identifier.lex]
        if len(funcs) == 0:
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no esta definida en el tipo {instance_type.name}'))
            return ErrorType()
        
        try:
            definition = instance_type.methods[node.identifier.lex, len(node.arguments)].definition
        except:
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no tiene sobrecarga definida con {len(node.arguments)} argumento/s en el tipo {instance_type.name}'))
            return ErrorType()
        
        args = [self.visit(arg, scope.create_child()) for arg in node.arguments]
        return self.visit(FuncInfo(args, definition), instance_type.type_scope)
    
    @visitor.when(MemberAccessNode)
    def visit(self, node: MemberAccessNode, scope: Scope):
        return self.verify_member_access(node.arguments, scope)
            
    @visitor.when(InstanceNode)
    def visit(self, node:InstanceNode, scope: Scope):
        if not self.context.get_type(node.identifier.lex):
            self.errors.append(SemanticError(f'El tipo {node.identifier.lex} no esta definido'))
            return ErrorType()
        var_t: Type = self.context.get_type(node.identifier.lex)
        param_dif = len(var_t.arguments) - len(node.arguments)
        if param_dif < 0:
            self.errors.append(SemanticError(f'Faltan {param_dif} argumentos al tratar de instanciar el tipo {var_t.name}'))
        elif param_dif < 0:
            self.errors.append(SemanticError(f'Se estan recibiendo {abs(param_dif)} argumentos de más al tratar de instanciar el tipo {var_t.name}'))
        if len(var_t.arguments) == 0: return self.context.get_type(var_t.name)
        for i in range(len(var_t.arguments)):
            arg_type: Type = self.visit(node.arguments[i])
            param_type: Type = self.context.get_type(var_t.arguments[i].atype)
            if not arg_type.conforms_to(param_type):
                self.errors.append(SemanticError(f'El {i} esimo argumento posicional del constructir del tipo {var_t.name} debe ser de tipo {param_type.name} y no {arg_type.name}')) 
                return ErrorType()
            
    @visitor.when(MethodNode)
    def visit(self, node: MethodNode, scope: Scope):
        for param in node.params:
            name, typex = param
            scope.define_variable(name.lex, typex.lex)
        result: Type = self.visit(node.body, scope)
        if not result.conforms_to(self.context.get_type(node.type_annotation.lex)):
            self.errors.append(SemanticError(f'No se esta retornando el tipo {node.type_annotation.lex} en la funcion {node.identifier.lex}'))
            return ErrorType()
        else: 
            return node.type_annotation.lex

    def verify_member_access(self, members: List[IdentifierNode], scope):
        if not scope.is_defined(members[0].lex):
            self.errors.append(SemanticError(f'La variable {members[0].lex} no esta definida en el ambito'))
            return ErrorType()
        variable: VariableInfo = scope.find_variable(members[0].lex)
        var_type: Type = self.context.get_type(variable.type)
        current: Attribute = variable
        for i in range(0,len(members)-1):
            try:
                current = var_type.get_attribute(members[i+1].lex)
                var_type = self.context.get_type(current.type)
            except SemanticError as error:
                self.errors.append(error)
                return ErrorType()
        return var_type

