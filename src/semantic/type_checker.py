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
        c_type_scope = current.type_scope.create_child()
        methods_scope = current.type_scope.create_child()
        self_instance =  Instance(self.context.get_type(node.identifier.lex), a_scope=c_type_scope, m_scope=methods_scope)
        for param, type in node.params:
            c_type_scope.define_variable(param.lex, type.lex, self.context.get_type(type.lex).basic_instance)
        parent_type: Type = self.context.get_type(node.super_type.lex)
        parent_scope = c_type_scope.create_child()
        parent_instance = InstanceNode(node.super_type, node.super_type_args)
        parent_instance = self.visit(parent_instance, parent_scope) if parent_instance.identifier.lex != 'Object' else Instance(ObjectType())
        for parent_att in parent_instance.attr:
            self_instance.attr[parent_att] = c_type_scope.define_variable(parent_att, parent_instance.attr[parent_att].name, parent_instance.attr[parent_att].instance)
        for parent_met in parent_instance.methods:
            self_instance.methods[parent_met] = parent_instance.methods[parent_met]
        for att in node.attributes:
            atribute_type = self.visit(att,c_type_scope)
            self_instance.attr[att.identifier.lex] =  c_type_scope.define_variable(att.identifier.lex, atribute_type.insta_type.name, atribute_type)
        
        current.basic_instance = self.build_instance(node, c_type_scope)
        methods_scope.define_variable('self', node.identifier.lex, current.basic_instance)
        for meth in node.methods:
            self.visit(meth, methods_scope)
        print('aqui')
    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        assign: AssignmentNode
        let_scope = scope.create_child()
        for assign in node.bindings:
            assignment: AssignmentNode | DassignmentNode = assign
            var, typ = (assignment.identifier.lex, self.visit(assign, let_scope.create_child()))
            let_scope.define_variable(var, typ.insta_type.name, typ)
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
            return Instance(self.context.get_type('Number'))
        else:
            self.errors.append(SemanticError("No se puede sumar tipos distintos a \'Number\'"))
            return Instance(ErrorType())
    
    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Number'), Scope)
        else:
            self.errors.append(SemanticError("No se puede restar tipos distintos a \'Number\'"))
            return Instance(ErrorType(), self.scope, self.scope)
    
    @visitor.when(MultiplyNode)
    def visit(self, node: MultiplyNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Number'), Scope)
        else:
            self.errors.append(SemanticError("No se puede multiplicar tipos distintos a \'Number\'"))
            return Instance(ErrorType(), self.scope, self.scope)   
            
    @visitor.when(DivideNode)
    def visit(self, node: DivideNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Number'), Scope)
        else:
            self.errors.append(SemanticError("No se puede dividir tipos distintos a \'Number\'"))
            return Instance(ErrorType(), self.scope, self.scope)       
    
    @visitor.when(PowerNode)
    def visit(self, node: NumberNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Number'), Scope)
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Number\' en una exponenciacion"))
            return Instance(ErrorType(), self.scope, self.scope)
    @visitor.when(ModNode)
    def visit(self, node: ModNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Number'), Scope)
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Number\' en una operacion de modulo"))
            return Instance(ErrorType(), self.scope, self.scope)     
        

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
            return Instance(ErrorType(), self.scope, self.scope)    
        
    @visitor.when(AndNode)
    def visit(self, node: AndNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Boolean')) or rigt.insta_type.conforms_to(self.context.get_type('Boolean')) :
            return Instance(self.context.get_type('Boolean', Scope))
        else:
            self.errors.append(SemanticError(f"No se puede usar tipos distintos a  \'Boolean\' en una expresion and"))
            return Instance(ErrorType(), self.scope, self.scope)   
    
    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope: Scope):
        return Instance(self.context.get_type('Boolean', Scope))
    
    ######################## Comparadores ##############################################################################
    ###################################################################################################################
    @visitor.when(LessEqualNode)
    def visit(self, node: LessEqualNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Boolean', Scope))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Number\' en una expresion <= "))
            return Instance(ErrorType(), self.scope, self.scope)   
        
    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Boolean'))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Number\' en una expresion <"))
            return Instance(ErrorType(), self.scope, self.scope)   

    @visitor.when(GreaterEqualNode)
    def visit(self, node: GreaterEqualNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Boolean'), scope)
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Number\' en una expresion >="))
            return Instance(ErrorType(), self.scope, self.scope)   


    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Boolean'))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Number\' en una expresion >"))
            return Instance(ErrorType(), self.scope, self.scope)   
    
    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('Number')) or rigt.insta_type.conforms_to(self.context.get_type('Number')) :
            return Instance(self.context.get_type('Boolean'))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'Number\' en una expresion \'equal\' "))
            return Instance(ErrorType(), self.scope, self.scope)   
        
    @visitor.when(NotEqualNode)
    def visit(self, node: NotEqualNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        equatable: Protocol = self.context.get_protocol('Equatable')
        if (equatable.implemented_by(left) and rigt.insta_type.conforms_to(self.context.get_type('Number'))):
            return Instance(self.context.get_type('Boolean', Scope))
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  un literal en una expresion \'not equal\' "))
            return Instance(ErrorType(), self.scope, self.scope)   
    
    @visitor.when(IsNode)
    def visit(self, node:IsNode, scope: Scope):
        _:Type = self.visit(node.expression, scope)
        try: 
            _ = self.context.get_type(node.identifier.lex)
        except SemanticError as err:
            self.errors.append(SemanticError(f'{err} linia {node.identifier.line}'))
            return Instance(ErrorType(), self.scope, self.scope)
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
            return Instance(ErrorType(), self.scope, self.scope)   
        
    @visitor.when(StringConcatSpaceNode)
    def visit(self, node: StringConcatSpaceNode, scope: Scope):
        left:Instance = self.visit(node.left, scope)
        rigt:Instance = self.visit(node.right, scope)
        if left.insta_type.conforms_to(self.context.get_type('String')) or rigt.insta_type.conforms_to(self.context.get_type('String')) :
            return Instance(self.context.get_type('String'), Scope)
        else:
            self.errors.append(SemanticError("No se puede usar tipos distintos a  \'String\' en una expresion concatenacion"))
            return Instance(ErrorType(), self.scope, self.scope)   
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
                return Instance(ErrorType(), self.scope, self.scope)
        
        exp_type: Instance = self.visit(node.expression, current_scope)
        if not protocol and not exp_type.insta_type.conforms_to(annotation):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} de tipo {annotation} no puede ser asignada con el tipo {exp_type.insta_type.name}'))
            return Instance(ErrorType(), self.scope, self.scope)
        elif protocol and not annotation.implemented_by(exp_type.insta_type):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} de tipo {annotation} no puede ser asignada con el tipo {exp_type.insta_type.name}'))
            return Instance(ErrorType(), self.scope, self.scope)
        elif not protocol:
            return exp_type
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
                return Instance(ErrorType(), self.scope, self.scope)
            
            return member_type
        
        
        if not scope.is_defined(node.identifier.lex):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} no esta definida, Linia: {node.identifier.line}'))
            return Instance(ErrorType(), self.scope, self.scope)
        var: VariableInfo = scope.find_variable(node.identifier.lex)
        if not exp_type.insta_type.conforms_to(self.context.get_type(var.type)):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} de tipo {self.context.get_type(var.type)} no puede ser asignada con el tipo {exp_type.insta_type.name}'))
            return Instance(ErrorType(), self.scope, self.scope)
        
        return var.instance


    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        if node.identifier.lex in ['sin', 'cos', 'sqrt', 'exp', 'rand', 'log', 'print', 'range']:
            return self.check_built_in_f(node, node.arguments, scope)

        try:
            functs: Method = [self.context.functions[funct] for funct in self.context.functions if funct[0] == node.identifier.lex]
        except:
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no esta definida en el contexto, Linia: {node.identifier.line}'))
            return Instance(ErrorType(), self.scope, self.scope)
        try:
            func: Method = self.context.functions[node.identifier.lex, len(node.arguments)]
        except:    
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no tiene sobrecarga definida con {len(node.arguments)} {"parametro" if len(node.arguments) == 1 else "parametros"}'))
            return Instance(ErrorType(), self.scope, self.scope)
        
        definition = func.definition
        args = [self.visit(arg, scope) for arg in node.arguments]
        return self.visit(FuncInfo(args, definition), self.scope.create_child())

    @visitor.when(IdentifierNode)
    def visit(self, node: IdentifierNode, scope: Scope):
        variable: VariableInfo = None
        if scope.is_defined(node.lex):
            variable =  scope.find_variable(node.lex)
            return variable.instance
        else:
            self.errors.append(SemanticError(f"La variable {node.lex} no esta definida, Linia: {node.line}"))
            return Instance(ErrorType(), self.scope, self.scope)

    @visitor.when(FuncInfo)
    def visit(self, node: FuncInfo, scope: Scope):

        if (node.function.identifier.lex , len(node.function.params)) in self.calls:
            func_type = self.context.get_type(node.function.type_annotation.lex)
            if isinstance(func_type, VarType):
                self.errors.append(
                    SemanticError(f'Es necesario anotar el tipo de retorno de las funciones con llamado recursivo, linia {node.identifier.line}')
                )
                return Instance(ErrorType(), self.scope, self.scope)
            else: return Instance(func_type, self.scope, self.scope.create_child())
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
                return Instance(ErrorType(), self.scope, self.scope)
        result: Instance = self.visit(func_def.body, func_scope)
        return_type: Type = self.context.get_type(func_def.type_annotation.lex)
        self.calls.pop()
        if result.insta_type.conforms_to(return_type):
            return result
        else:
            self.errors.append(SemanticError(f'No se esta retornando el tipo {return_type} en la funcion {func_def.identifier.lex}')) 
            return Instance(ErrorType(), self.scope, self.scope)

    @visitor.when(FuncNode)
    def visit(self, node: FuncNode, scope: Scope):
        self.calls.append((node.identifier.lex, len(node.params)))
        fun_scope = scope.create_child()
        for param in node.params:
            name, typex = param
            fun_scope.define_variable(name.lex, typex.lex, self.context.get_type(typex.lex).basic_instance)
        result: Instance = self.visit(node.body, fun_scope)
        self.calls.pop()
        if not result.insta_type.conforms_to(self.context.get_type(node.type_annotation.lex)):
            self.errors.append(SemanticError(f'No se esta retornando el tipo {node.type_annotation.lex} en la funcion {node.identifier.lex}'))
            return Instance(ErrorType(), self.scope, self.scope)
        else: 
            return node.type_annotation.lex

    @visitor.when(AsNode)
    def visit(self, node: AsNode, scope: Scope):
        try:
            down_cast = self.context.get_type(node.identifier.lex)
        except:
            self.errors.append(SemanticError(f'El tipo {node.identifier.lex} no esta definido'))
            return Instance(ErrorType(), self.scope, self.scope)
        exp: Instance = self.visit(node.expression, scope)
        if exp.insta_type.conforms_to(down_cast): return Instance(down_cast)
        else: return Instance(ErrorType(), self.scope, self.scope)

    @visitor.when(IfNode)
    def visit(self, node: IfNode, scope: Scope):
        cond: Instance = self.visit(node.condition, scope)
        if not cond.insta_type.conforms_to(self.context.get_type('Boolean')):
            self.errors.append(SemanticError(f'Solo typo Booleano para condiciones de if'))
            return Instance(ErrorType(), self.scope, self.scope)
        if_scope = scope.create_child()
        if_type:Instance = self.visit(node.body, if_scope)
        for eli in node.elif_nodes:
            eli_t: Instance = self.visit(eli, scope)
            if not eli_t.insta_type.conforms_to(if_type.insta_type): 
                self.errors.append(SemanticError(f'El tipo de retorno de la expresion elif ({eli_t.insta_type.name}) no coincide con la del if ({if_type.insta_type.name})'))
                return Instance(ErrorType(), self.scope, self.scope)
        else_t: Instance = self.visit(node.else_body, scope)
        if not else_t.insta_type.conforms_to(if_type.insta_type): 
            self.errors.append(SemanticError(f'El tipo de retorno de la expresion else {else_t.insta_type.name} no coincide con la del if ({if_type.insta_type.name})'))
            return Instance(ErrorType(), self.scope, self.scope)
        return if_type
    
    @visitor.when(ElifNode)
    def visit(self, node: ElifNode, scope: Scope):
        cond: Instance = self.visit(node.condition, scope)
        if not cond.insta_type.conforms_to(self.context.get_type('Boolean')):
            self.errors.append(SemanticError(f'Solo typo Booleano para condiciones de elif'))
            return Instance(ErrorType(), self.scope, self.scope)
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
            return Instance(ErrorType(), self.scope, self.scope)
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
            return Instance(ErrorType(), self.scope, self.scope)
        for_scope = scope.create_child()
        for_scope.define_variable(node.identifier.lex, 'Var', Instance(VarType()))
        result: Instance = self.visit(node.body, for_scope)
        return result
    
    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode, scope: Scope):
        members: Instance = self.verify_member_access(node.member_access[:-1], scope)
        if isinstance(members.insta_type, ErrorType): return members

        instance_type: Type =  self.context.get_type(members.insta_type)
        funcs: list[Method] = [instance_type.methods[method] for method in members.methods if method[0] == node.identifier.lex]
        if len(funcs) == 0:
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no esta definida en el tipo {instance_type.name}'))
            return Instance(ErrorType(), self.scope, self.scope)
        
        try:
            definition = instance_type.methods[node.identifier.lex, len(node.arguments)].definition
        except:
            self.errors.append(SemanticError(f'La funcion {node.identifier.lex} no tiene sobrecarga definida con {len(node.arguments)} argumento/s en el tipo {instance_type.name}'))
            return Instance(ErrorType(), self.scope, self.scope)
        
        args = [self.visit(arg, scope.create_child()) for arg in node.arguments]
        return self.visit(FuncInfo(args, definition), members.met_scope)
    
    @visitor.when(MemberAccessNode)
    def visit(self, node: MemberAccessNode, scope: Scope):
        return self.verify_member_access(node.arguments, scope)
            

    @visitor.when(InstanceNode)
    def visit(self, node:InstanceNode, scope: Scope):
        if not self.context.get_type(node.identifier.lex):
            self.errors.append(SemanticError(f'El tipo {node.identifier.lex} no esta definido, Linia: {node.identifier.line}'))
            return Instance(ErrorType(), self.scope, self.scope)
        var_t: Type = self.context.get_type(node.identifier.lex)
        param_dif = len(var_t.arguments) - len(node.arguments if node.arguments else [])
        if param_dif < 0:
            self.errors.append(SemanticError(f'Faltan {param_dif} argumentos al tratar de instanciar el tipo {var_t.name}, Linia: {node.identifier.line}'))
            return Instance(ErrorType(), self.scope, self.scope)
        elif param_dif > 0:
            self.errors.append(SemanticError(f'Se estan recibiendo {abs(param_dif)} argumentos de más al tratar de instanciar el tipo {var_t.name}, Linia: {node.identifier.line}'))
            return Instance(ErrorType(), self.scope, self.scope)
        instanc_scope = scope.create_child()
        for i in range(0 , len(node.arguments if node.arguments else [])) :
            arg_instace = self.visit(node.arguments[i], scope)
            if arg_instace.insta_type.conforms_to(self.context.get_type(var_t.arguments[i].atype)): 
                instanc_scope.define_variable(var_t.arguments[i].name, var_t.arguments[i].atype, arg_instace )
            else:
                self.errors.append(SemanticError(f'El argumento de la {i} esima posicion para instanciar el tipo {node.identifier.lex} debe ser de tipo {var_t.arguments[i].atype.name}, Linia : {node.identifier.line}'))

        result = self.build_instance(var_t.definition, instanc_scope)
        return result
            
    @visitor.when(MethodNode)
    def visit(self, node: MethodNode, scope: Scope):
        m_scope = scope.create_child()
        self.calls.append((node.identifier.lex, len(node.params)))
        for param in node.params:
            name, typex = param
            m_scope.define_variable(name.lex, typex.lex, Instance(self.context.get_type(typex.lex)))
        result: Instance = self.visit(node.body, m_scope)
        self.calls.pop()
        if not result.insta_type.conforms_to(self.context.get_type(node.type_annotation.lex)):
            self.errors.append(SemanticError(f'No se esta retornando el tipo {node.type_annotation.lex} en la funcion {node.identifier.lex}'))
            return Instance(ErrorType(), self.scope, self.scope)
        else: 
            return result
        
    @visitor.when(ExplicitVectorNode)
    def visit(self, node: ExplicitVectorNode, scope: Scope):
        vect_type = self.visit(node.arguments[0], scope).insta_type
        if len(node.arguments) > 1:
            for exp in node.arguments:
                vect_type = lowest_common_ancestor(vect_type, self.visit(exp, scope).insta_type)
        return VectorInstance(vect_type)

    @visitor.when(ImplicitVectorNode)
    def visit(self, node: ImplicitVectorNode, scope: Scope):
        elemnt_scope = scope.create_child()
        iterable_inst: Instance = self.visit(node.iterable, scope)
        iter_protocol = self.context.get_protocol('Iterable')
        if not (iter_protocol.implemented_by( iterable_inst.insta_type) or isinstance(iter_protocol, VectorInstance) or iterable_inst.insta_type.name == 'Range') or isinstance(iterable_inst.insta_type, ErrorType):
            self.errors.append(SemanticError(f'El tipo {iterable_inst.insta_type.name} no implementa el protocolo Iterable'))
            return Instance(ErrorType())
        next_func = iterable_inst.methods[('next', 0)].definition if not (isinstance(iter_protocol, VectorInstance) or iterable_inst.insta_type.name == 'Range') else None
        elemnts_type: Type = self.visit(next_func, iterable_inst.met_scope).insta_type if not (isinstance(iter_protocol, VectorInstance) or iterable_inst.insta_type.name == 'Range') else iterable_inst.type if isinstance(iter_protocol, VectorInstance) else self.context.get_type('Number')
        elemnt_scope.define_variable(node.identifier, elemnts_type.name, Instance(elemnts_type))
        vect_type = self.visit(node.expression, elemnt_scope)
        return VectorInstance(vect_type)
    
    @visitor.when(VectorIndexNode)
    def visit(self, node: VectorIndexNode, scope: Scope):
        if not scope.is_defined(node.identifier.lex):
            self.errors.append(SemanticError(f'El vector {node.identifier.lex} no esta definido en el ambito, linia: {node.identifier.line}'))
            return Instance(ErrorType())
        variable: VariableInfo = scope.find_variable(node.identifier.lex)
        if self.context.get_type(variable.type).conforms_to(VectorType()):
            self.errors.append(SemanticError(f'La variable {node.identifier.lex} de tipo {variable.type} no es indexable, linia: {node.identifier.line}'))
            return Instance(ErrorType())
        index_type: Instance = self.visit(node.index, scope)
        if not index_type.insta_type.conforms_to(self.context.get_type('Number')):
            self.errors.append(SemanticError(f'El indice de un vector debe ser de tipo Number, linia: {node.identifier.line}'))
            return Instance(ErrorType())
        return Instance(variable.instance.type)




    def verify_member_access(self, members: List[IdentifierNode], scope):
        if not scope.is_defined(members[0].lex):
            self.errors.append(SemanticError(f'La variable {members[0].lex} no esta definida en el ambito, Linia: {members[0].line}'))
            return Instance(ErrorType(), self.scope, self.scope)
        variable: VariableInfo = scope.find_variable(members[0].lex)
        var_type: Instance = variable.instance
        current: Attribute = variable
        for i in range(0,len(members)-1):
            try:
                current: VariableInfo = var_type.attr[members[i+1].lex]
                var_type = current.instance
            except :
                self.errors.append(f'El atributo {members[i+1].lex} no se encuentra en el tipo {var_type.insta_type.name}, Linia {members[i+1].line}')
                return Instance(ErrorType(), self.scope, self.scope)
        return var_type
    
    def build_instance(self, node: TypeNode, scope: Scope):
        curren_type = node
        att_scope = scope.create_child()
        meth_scope = self.scope.create_child()
        attrubutes = {}
        parent_instance = InstanceNode(curren_type.super_type, curren_type.super_type_args)
        parent_instance: Instance = self.visit(parent_instance, scope) if node.super_type.lex != 'Object' else Instance(ObjectType())
        for assign in node.attributes:
            var_type: Instance = self.visit(assign, att_scope)
            attrubutes[assign.identifier.lex] = att_scope.define_variable(assign.identifier.lex, var_type.insta_type.name, instance=var_type)
        for p_att in parent_instance.attr:
            current_att = parent_instance.attr[p_att]
            attrubutes[p_att] = att_scope.define_variable(current_att.name, current_att.type, current_att.instance)
        
        methods = self.context.get_type(node.identifier.lex).methods
        for met in parent_instance.methods:
            if not met in methods: methods[met] = parent_instance.methods[met]
        result =  Instance(self.context.get_type(node.identifier.lex), att_scope, meth_scope, attrubutes, methods)
        meth_scope.define_variable("self", node.identifier.lex, result)
        result.met_scope = meth_scope
        return result
    
    def check_built_in_f(self, node: FunctionCallNode, params, scope: Scope):
        name = node.identifier.lex
        built_in = {'sin': 1, 'cos': 1, 'sqrt':1, 'exp': 1, 'print': 1, 'rand': 0, 'log': 2, 'range': 2 }
        args = built_in[name]
        
       
        
        if len(params) != args:
            self.errors.append(SemanticError(f'La funcion {name} debe recibir {args} parametros, Linia: {node.identifier.line}'))
            return Instance(ErrorType())
        if name == 'print': 
            self.visit(params[0], scope)
            return Instance(self.context.get_type('String'))
        for param in params:
            if not self.visit(param, scope).insta_type.conforms_to(self.context.get_type('Number')):
                 self.errors.append(SemanticError(f'La funcion {name} debe recibir {args} parametros de tipo Number, Linia: {node.identifier.line}'))
                 return Instance(ErrorType())
        if name == 'range': return Instance(self.context.get_type("Range"))
        
        return Instance(self.context.get_type('Number'))
    

