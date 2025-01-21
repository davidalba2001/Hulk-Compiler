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
        self.calls = []
    
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
        current.type_scope.define_variable('self', node.identifier.lex, Instance(self.context.get_type(node.identifier.lex)))
        c_type_scope = current.type_scope.create_child()
        methods_scope = current.type_scope.create_child()
        for param, type in node.params:
            c_type_scope.define_variable(param.lex, type.lex,Instance(self.context.get_type(type.lex)))
        for att in node.attributes:
            self.visit(att,c_type_scope)
        for meth in node.methods:
            self.visit(meth, methods_scope)
    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        vars: list[tuple[str, Instance]] = []
        assign: AssignmentNode
        for assign in node.bindings:
            assignment: AssignmentNode | DassignmentNode = assign
            vars.append((assignment.identifier.lex, self.visit(assign, scope)))
        let_scope = scope.create_child()
        for (var, typ) in vars:
            let_scope.define_variable(var, typ.insta_type.name, Instance(self.context.get_type(typ.insta_type.name)))
        return self.visit(node.body, let_scope)

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        expression = None
        for exp in node.expressions:
            expression: Instance = self.visit(exp, scope)
        return expression
    
    ### --------------- Expresiones aritmeticas con Numbers -----------------------###
    ##################################################################################
    
    @visitor.when(PlusNode)
    def visit(self, node: PlusNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        num_t = self.context.get_type('Number')
        if left.insta_type.conforms_to(num_t) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Number'), Scope)
        else:
            self.errors.append(SemanticError("No se puede sumar tipos distintos a \'Number\'"))
            return Instance(ErrorType(), Scope(), Scope())
    
    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Number'), Scope)
        else:
            self.errors.append(SemanticError("No se puede restar tipos distintos a \'Number\'"))
            return Instance(ErrorType(), Scope(), Scope())
    
    @visitor.when(MultiplyNode)
    def visit(self, node: MultiplyNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Number'), Scope)
        else:
            self.errors.append(SemanticError("No se puede multiplicar tipos distintos a \'Number\'"))
            return Instance(ErrorType(), Scope(), Scope())   
            
    @visitor.when(DivideNode)
    def visit(self, node: DivideNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Number'), Scope)
        else:
            self.errors.append(SemanticError("No se puede dividir tipos distintos a \'Number\'"))
            return Instance(ErrorType(), Scope(), Scope())       
    
    @visitor.when(PowerNode)
    def visit(self, node: NumberNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Number'), Scope)
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Number\' en una exponenciacion"))
            return Instance(ErrorType(), Scope(), Scope())
    @visitor.when(ModNode)
    def visit(self, node: ModNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Number'), Scope)
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Number\' en una operacion de modulo"))
            return Instance(ErrorType(), Scope(), Scope())     
        

    @visitor.when(NumberNode)
    def visit(self, node:NumberNode, scope: Scope):
        return Instance(self.context.get_type('Number'), Scope)

    ############ Con Booleanos #################################################################################

    @visitor.when(OrNode)
    def visit(self, node: OrNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Boolean')) or rigt.insta_type.conforms_to(self.context.get_type('Boolean')) :
            return Instance(self.context.get_type('Boolean'))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Boolean\' en una expresion or"))
            return Instance(ErrorType(), Scope(), Scope())    
        
    @visitor.when(AndNode)
    def visit(self, node: AndNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Boolean')) or rigt.insta_type.conforms_to(self.context.get_type('Boolean')) :
            return Instance(self.context.get_type('Boolean', Scope))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Boolean\' en una expresion and"))
            return Instance(ErrorType(), Scope(), Scope())   
    
    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope: Scope):
        return Instance(self.context.get_type('Boolean', Scope))
    
    ######################## Comparadores ##############################################################################
    ###################################################################################################################
    @visitor.when(LessEqualNode)
    def visit(self, node: LessEqualNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Boolean')) or rigt.insta_type.conforms_to(self.context.get_type('Boolean')) :
            return Instance(self.context.get_type('Boolean', Scope))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Boolean\' en una expresion and"))
            return Instance(ErrorType(), Scope(), Scope())   
        
    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Boolean')) or rigt.insta_type.conforms_to(self.context.get_type('Boolean')) :
            return Instance(self.context.get_type('Boolean'))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Boolean\' en una expresion and"))
            return Instance(ErrorType(), Scope(), Scope())   

    @visitor.when(GreaterEqualNode)
    def visit(self, node: GreaterEqualNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Boolean')) or rigt.insta_type.conforms_to(self.context.get_type('Boolean')) :
            return Instance(self.context.get_type('Boolean', Scope))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Boolean\' en una expresion and"))
            return Instance(ErrorType(), Scope(), Scope())   


    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Boolean')) or rigt.insta_type.conforms_to(self.context.get_type('Boolean')) :
            return Instance(self.context.get_type('Boolean'))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Boolean\' en una expresion and"))
            return Instance(ErrorType(), Scope(), Scope())   
    
    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Boolean')) or rigt.insta_type.conforms_to(self.context.get_type('Boolean')) :
            return Instance(self.context.get_type('Boolean'))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Boolean\' en una expresion \'equal\' "))
            return Instance(ErrorType(), Scope(), Scope())   
        
    @visitor.when(NotEqualNode)
    def visit(self, node: NotEqualNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        equatable: Protocol = self.context.get_protocol('Equatable')
        if (equatable.implemented_by(left) and rigt.insta_type.conforms_to(self.context.get_type('Number'))):
            return Instance(self.context.get_type('Boolean', Scope))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  un literal en una expresion \'not equal\' "))
            return Instance(ErrorType(), Scope(), Scope())   
    
    @visitor.when(IsNode)
    def visit(self, node:IsNode, scope: Scope):
        _:Type = self.visit(node.expression, scope)
        try: 
            _ = self.context.get_type(node.identifier.lex)
        except SemanticError as err:
            self.errors.append(SemanticError(f'{err} linia {node.identifier.line}'))
            return Instance(ErrorType(), Scope(), Scope())
        return Instance(self.context.get_type('Boolean'))

          
    

    ############ Con Strings #################################################################################
    @visitor.when(StringConcatNode)
    def visit(self, node: StringConcatNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('String')) or rigt.insta_type.conforms_to(self.context.get_type('String')) :
            return Instance(self.context.get_type('String'), Scope)
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'String\' en una expresion concatenacion"))
            return Instance(ErrorType(), Scope(), Scope())   
        
    @visitor.when(StringConcatSpaceNode)
    def visit(self, node: StringConcatSpaceNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('String')) or rigt.insta_type.conforms_to(self.context.get_type('String')) :
            return Instance(self.context.get_type('String'), Scope)
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'String\' en una expresion concatenacion"))
            return Instance(ErrorType(), Scope(), Scope())   
    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope: Scope):
        return Instance(self.context.get_type('String'), Scope)

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
                return Instance(ErrorType(), Scope(), Scope())
        
        exp_type: Instance = self.visit(node.expression, current_scope)
        if not protocol and not exp_type.insta_type.conforms_to(annotation):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} de tipo {annotation} no puede ser asignada con el tipo {exp_type.insta_type.name}'))
            return Instance(ErrorType(), Scope(), Scope())
        elif protocol and not annotation.implemented_by(exp_type):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} de tipo {annotation} no puede ser asignada con el tipo {exp_type.insta_type.name}'))
            return Instance(ErrorType(), Scope(), Scope())
        elif not protocol: return exp_type
        else: return exp_type
        
    @visitor.when(DassignmentNode)
    def visit(self, node: DassignmentNode, scope: Scope):
        current_scope = scope.create_child()
        exp_type: Instance = self.visit(node.expression, current_scope)
        if isinstance(node.identifier, MemberAccessNode):
            member = node.identifier
            member_type: Instance = self.visit(member, scope)
            if isinstance(member_type.insta_type, ErrorType): return member_type
            
            exp_type: Instance = self.visit(node.expression, current_scope)
            if not exp_type.insta_type.conforms_to(member_type.insta_type):
                self.errors.append(SemanticError(f'La variable {node.identifier.arguments[-1].lex} de tipo {member_type.insta_type.name} no puede ser asignada con el tipo {exp_type.insta_type.name}'))
                return Instance(ErrorType(), Scope(), Scope())
            
            return member_type
        
        
        if not scope.is_defined(node.identifier.lex):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} no esta definida'))
            return Instance(ErrorType(), Scope(), Scope())
        var: VariableInfo = scope.find_variable(node.identifier.lex)
        if not exp_type.insta_type.conforms_to(self.context.get_type(var.type)):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} de tipo {self.context.get_type(var.type)} no puede ser asignada con el tipo {exp_type.insta_type.name}'))
            return Instance(ErrorType(), Scope(), Scope())
        
        return Instance(self.context.get_type(var.type), Scope)


    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        if node.identifier.lex == 'print': return Instance(self.context.get_type('String'), Scope)

        try:
            functs: Method = [self.context.functions[funct] for funct in self.context.functions if funct[0] == node.identifier.lex]
        except:
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no esta definida en el contexto'))
            return Instance(ErrorType(), Scope(), Scope())
        try:
            func: Method = self.context.functions[node.identifier.lex, len(node.arguments)]
        except:    
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no tiene sobrecarga definida con {len(node.arguments)} {"parametro" if len(node.arguments) == 1 else "parametros"}'))
            return Instance(ErrorType(), Scope(), Scope())
        
        definition = func.definition
        args = [self.visit(arg, scope) for arg in node.arguments]
        return self.visit(FuncInfo(args, definition), self.scope)

    @visitor.when(IdentifierNode)
    def visit(self, node: IdentifierNode, scope: Scope):
        variable: VariableInfo = None
        if scope.is_defined(node.lex):
            variable =  scope.find_variable(node.lex)
            return variable.instance
        else:
            self.errors.append(SemanticError(f"La variable {node.lex} no esta definida"))
            return Instance(ErrorType(), Scope(), Scope())

    @visitor.when(FuncInfo)
    def visit(self, node: FuncInfo, scope: Scope):

        if (node.function.identifier.lex , len(node.function.params)) in self.calls:
            func_type = self.context.get_type(node.function.type_annotation.lex)
            if isinstance(func_type, VarType):
                self.errors.append(
                    SemanticError(f'Es necesario anotar el tipo de retorno de las funciones con llamado recursivo, linia {node.identifier.line}')
                )
                return Instance(ErrorType(), Scope(), Scope())
            else: return Instance(func_type, Scope(), Scope())
        self.calls.append((node.function.identifier.lex, len(node.function.params)))
        func_scope = scope.create_child()
        func_def: FuncNode | MethodNode = node.function
        args = func_def.params
        params: List[Instance] = node.params
        for i in range(0, len(params)):
            typex: Type = self.context.get_type(args[i][1].lex)
            if params[i].insta_type.conforms_to(typex):
                func_scope.define_variable(args[i][0].lex, params[i].insta_type, params[i])
            else:
                self.errors.append(SemanticError(f'El parametro {args[i][0].lex} debe recibir un argumento de tipo {typex.name} en la funcion {func_def.identifier.lex}'))
                return Instance(ErrorType(), Scope(), Scope())
        result: Instance = self.visit(func_def.body, func_scope)
        return_type: Type = self.context.get_type(func_def.type_annotation.lex)
        self.calls.pop()
        if result.insta_type.conforms_to(return_type):
            return result
        else:
            self.errors.append(SemanticError(f'No se esta retornando el tipo {return_type} en la funcion {func_def.identifier.lex}')) 
            return Instance(ErrorType(), Scope(), Scope())

    @visitor.when(FuncNode)
    def visit(self, node: FuncNode, scope: Scope):
        self.calls.append((node.identifier.lex, len(node.params)))
        fun_scope = scope.create_child()
        for param in node.params:
            name, typex = param
            fun_scope.define_variable(name.lex, typex.lex, Instance(self.context.get_type(typex.lex)))
        result: Instance = self.visit(node.body, fun_scope)
        self.calls.pop()
        if not result.insta_type.conforms_to(self.context.get_type(node.type_annotation.lex)):
            self.errors.append(SemanticError(f'No se esta retornando el tipo {node.type_annotation.lex} en la funcion {node.identifier.lex}'))
            return Instance(ErrorType(), Scope(), Scope())
        else: 
            return node.type_annotation.lex

    @visitor.when(AsNode)
    def visit(self, node: AsNode, scope: Scope):
        try:
            down_cast = self.context.get_type(node.identifier.lex)
        except:
            self.errors.append(SemanticError(f'El tipo {node.identifier.lex} no esta definido'))
            return Instance(ErrorType(), Scope(), Scope())
        exp: Instance = self.visit(node.expression, scope)
        if exp.insta_type.conforms_to(down_cast): return Instance(down_cast)
        else: return Instance(ErrorType(), Scope(), Scope())

    @visitor.when(IfNode)
    def visit(self, node: IfNode, scope: Scope):
        cond: Instance = self.visit(node.condition, scope)
        if not cond.insta_type.conforms_to(self.context.get_type('Boolean')):
            self.errors.append(SemanticError(f'Solo typo Booleano para condiciones de if'))
            return Instance(ErrorType(), Scope(), Scope())
        if_scope = scope.create_child()
        if_type:Instance = self.visit(node.body, if_scope)
        for eli in node.elif_nodes:
            eli_t: Instance = self.visit(eli, scope)
            if not eli_t.insta_type.conforms_to(if_type.insta_type): 
                self.errors.append(SemanticError(f'El tipo de retorno de la expresion elif {eli_t.insta_type.name} no coincide con la del if ({if_type.insta_type.name})'))
                return Instance(ErrorType(), Scope(), Scope())
        else_t: Instance = self.visit(node.else_body, scope)
        if not else_t.insta_type.conforms_to(if_type.insta_type): 
            self.errors.append(SemanticError(f'El tipo de retorno de la expresion else {else_t.insta_type.name} no coincide con la del if ({if_type.insta_type.name})'))
            return Instance(ErrorType(), Scope(), Scope())
        return if_type
    
    @visitor.when(ElifNode)
    def visit(self, node: ElifNode, scope: Scope):
        cond: Type = self.visit(node.condition, scope)
        if not cond.conforms_to(self.context.get_type('Boolean')):
            self.errors.append(SemanticError(f'Solo typo Booleano para condiciones de elif'))
            return Instance(ErrorType(), Scope(), Scope())
        if_scope = scope.create_child()
        result:Type = self.visit(node.body, if_scope)
        return result

    @visitor.when(ElseNode)
    def visit(self, node:ElseNode, scope: Scope):
        if_scope = scope.create_child()
        result:Type = self.visit(node.body, if_scope)
        return result

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        cond: Instance = self.visit(node.condition, scope)
        if not cond.insta_type.conforms_to(self.context.get_type('Boolean')):
            self.errors.append(SemanticError(f'Solo typo Booleano para condiciones de while'))
            return Instance(ErrorType(), Scope(), Scope())
        while_scope = scope.create_child()
        return_t :Instance = self.visit(node.body, while_scope)
        return return_t


    @visitor.when(ForNode)
    def visit(self, node: ForNode, scope: Scope):
        iterable: Protocol = self.context.get_protocol('Iterable')
        iterand: Instance = self.visit(node.iterable, scope)
        if iterand.insta_type.name == '<error>': return iterand
        if not iterable.implemented_by(iterand.insta_type):
            self.errors.append(SemanticError(f'El iterador proporcionado no implementa iterable'))
            return Instance(ErrorType(), Scope(), Scope())
        for_scope = scope.create_child()
        for_scope.define_variable(node.identifier.lex, 'Var', Instance(VarType()))
        result: Instance = self.visit(node.body, for_scope)
        return result
    
    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode, scope: Scope):
        instance: VariableInfo = None
        members = self.verify_member_access(node.member_access[:-1], scope)
        if isinstance(members.insta_type, ErrorType): return members
        if scope.is_defined(node.type_identifier.lex): instance = scope.find_variable(node.type_identifier.lex)
        else:
            self.errors.append(SemanticError(f'La variable {node.type_identifier.lex} no esta definida en el ambito'))
        instance_type: Type =  self.context.get_type(instance.type)
        funcs: list[Method] = [instance_type.methods[method] for method in instance_type.methods if method[0] == node.identifier.lex]
        if len(funcs) == 0:
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no esta definida en el tipo {instance_type.name}'))
            return Instance(ErrorType(), Scope(), Scope())
        
        try:
            definition = instance_type.methods[node.identifier.lex, len(node.arguments)].definition
        except:
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no tiene sobrecarga definida con {len(node.arguments)} argumento/s en el tipo {instance_type.name}'))
            return Instance(ErrorType(), Scope(), Scope())
        
        args = [self.visit(arg, scope.create_child()) for arg in node.arguments]
        return self.visit(FuncInfo(args, definition), instance_type.type_scope)
    
    @visitor.when(MemberAccessNode)
    def visit(self, node: MemberAccessNode, scope: Scope):
        return self.verify_member_access(node.arguments, scope)
            

    @visitor.when(InstanceNode)
    def visit(self, node:InstanceNode, scope: Scope):
        if not self.context.get_type(node.identifier.lex):
            self.errors.append(SemanticError(f'El tipo {node.identifier.lex} no esta definido'))
            return Instance(ErrorType(), Scope(), Scope())
        var_t: Type = self.context.get_type(node.identifier.lex)
        param_dif = len(var_t.arguments) - len(node.arguments)
        if param_dif < 0:
            self.errors.append(SemanticError(f'Faltan {param_dif} argumentos al tratar de instanciar el tipo {var_t.name}'))
            return Instance(ErrorType(), Scope(), Scope())
        elif param_dif > 0:
            self.errors.append(SemanticError(f'Se estan recibiendo {abs(param_dif)} argumentos de más al tratar de instanciar el tipo {var_t.name}'))
            return Instance(ErrorType(), Scope(), Scope())
        if len(var_t.arguments) == 0: return Instance(self.context.get_type(var_t.name), Scope())
        atrib_scope = Scope()
        met_scope = Scope()
        implement: TypeNode = var_t.definition
        for i in range(0, len(var_t.arguments)):
            arg_type: Instance = self.visit(node.arguments[i], scope)
            
            param_type: Type = self.context.get_type(var_t.arguments[i].atype)
            if not arg_type.insta_type.conforms_to(param_type):
                self.errors.append(SemanticError(f'El {i} esimo argumento posicional del constructir del tipo {var_t.name} debe ser de tipo {param_type.name} y no {arg_type.insta_type.name}')) 
                return Instance(ErrorType(), Scope(), Scope())
        for atrib in implement.attributes:
            atrib_scope.define_variable(atrib.identifier.lex, self.visit(atrib, atrib_scope))
        result = Instance(var_t, atrib_scope, met_scope)
        result.att_scope.define_variable('self', result.insta_type, result)
        result.met_scope.define_variable('self', result.insta_type, result)
        return result
            
    @visitor.when(MethodNode)
    def visit(self, node: MethodNode, scope: Scope):
        
        self.calls.append((node.identifier.lex, len(node.params)))
        for param in node.params:
            name, typex = param
            scope.define_variable(name.lex, typex.lex)
        result: Instance = self.visit(node.body, scope)
        self.calls.pop()
        if not result.insta_type.conforms_to(self.context.get_type(node.type_annotation.lex)):
            self.errors.append(SemanticError(f'No se esta retornando el tipo {node.type_annotation.lex} en la funcion {node.identifier.lex}'))
            return Instance(ErrorType(), Scope(), Scope())
        else: 
            return result
        
    @visitor.when(ExplicitVectorNode)
    def visit(self, node: ExplicitVectorNode, scope: Scope):
        vect_type = self.visit(node.arguments[0])
        



    def verify_member_access(self, members: List[IdentifierNode], scope):
        if not scope.is_defined(members[0].lex):
            self.errors.append(SemanticError(f'La variable {members[0].lex} no esta definida en el ambito'))
            return Instance(ErrorType(), Scope(), Scope())
        variable: VariableInfo = scope.find_variable(members[0].lex)
        var_type: Instance = variable.instance
        current: Attribute = variable
        for i in range(0,len(members)-1):
            try:
                current: VariableInfo = var_type[members[i+1].lex]
                var_type = current.instance
            except :
                self.errors.append(f'El atributo {members[i+1].lex} no se encuentra en el tipo {var_type.insta_type.name}, inia {members[i+1].line}')
                return Instance(ErrorType(), Scope(), Scope())
        return var_type
    

