from cmp.hulk_ast import *
from semantic.semantic import *
import cmp.visitor as visitor
import math
import random as rnd
class InterpreterVisitor:
    def __init__(self,context:Context, scope: Scope):
        self.context = context
        self.scope = scope

    @visitor.on('node')
    def visit(self, node, scope, tabs):
        pass


    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope:Scope):
        if node.main_expression:
            self.visit(node.main_expression, self.scope.create_child())


    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        result = None
        for exp in node.expressions:
            result = self.visit(exp, scope)
        return result
    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        assign: AssignmentNode
        let_scope = scope.create_child()
        for assign in node.bindings:
            assignment: AssignmentNode | DassignmentNode = assign
            var, value = (assignment.identifier.lex, self.visit(assign, let_scope.create_child()))
            let_scope.define_variable(var, value.insta_type, instance= value)
        return self.visit(node.body, let_scope)

    @visitor.when(IdentifierNode)
    def visit(self, node: IdentifierNode, scope: Scope):
        variable: VariableInfo =  scope.find_variable(node.lex)
        return variable.instance
    
    @visitor.when(AssignmentNode)
    def visit(self, node: AssignmentNode, scope: Scope):
        return self.visit(node.expression, scope)
    
    @visitor.when(DassignmentNode)
    def visit(self, node: DassignmentNode, scope: Scope):
        current_scope = scope.create_child()
        value = self.visit(node.expression, current_scope)
        if isinstance(node.identifier, MemberAccessNode):
            member = node.identifier
            member_type: Instance = self.visit(MemberAccessNode(member.arguments[:-1]), scope)
            exp_type: Instance = self.visit(node.expression, current_scope)  
            member_type.attr[member.arguments[-1].lex].instance = exp_type
            return exp_type
            
        var: VariableInfo = scope.find_variable(node.identifier.lex)
        var.instance = value
        return value


########### Operaciones con Numbers #################################################################################
    @visitor.when(PlusNode)
    def visit(self, node: PlusNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('Number'),right + left) 
    
    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('Number'), right - left) 
    
    @visitor.when(MultiplyNode)
    def visit(self, node: MultiplyNode, scope: Scope):
        left = self.visit(node.left, scope)
        right= self.visit(node.right, scope)
        return LiteralInstance(self.context.get_type('Number'), left.value*right.value  ) 
            
    @visitor.when(DivideNode)
    def visit(self, node: DivideNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('Number'), left / right )    
    
    @visitor.when(PowerNode)
    def visit(self, node: NumberNode, scope: Scope):
        left = self.visit(node.left, scope)
        right= self.visit(node.right, scope)
        return LiteralInstance(self.context.get_type('Number'),  left.value **right.value) 
    @visitor.when(ModNode)
    def visit(self, node: ModNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('Number'), left%right) 
        

    @visitor.when(NumberNode)
    def visit(self, node:NumberNode, scope: Scope):
        try:
            result = int(node.lex)
        except:
            result = float(node.lex)
        return LiteralInstance(self.context.get_type('Number'), result)

    ############ Con Booleanos #################################################################################

    @visitor.when(OrNode)
    def visit(self, node: OrNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('Boolean'), left or right) 
        
    @visitor.when(AndNode)
    def visit(self, node: AndNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('Boolean'), left and right) 
    
    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope: Scope):
        return LiteralInstance(self.context.get_type('Boolean'),True if node.lex == "True" else False) 
    
    ######################## Comparadores ##############################################################################
    ###################################################################################################################
    @visitor.when(LessEqualNode)
    def visit(self, node: LessEqualNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('Boolean'),left <= right) 
        
    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('Boolean'),left < right)   

    @visitor.when(GreaterEqualNode)
    def visit(self, node: GreaterEqualNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('Boolean'),left >= right)   


    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('Boolean'),left > right)   
    
    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('Boolean'),left == right)   
        
    @visitor.when(NotEqualNode)
    def visit(self, node: NotEqualNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('Boolean'),left != right) 

    @visitor.when(IsNode)
    def visit(self, node:IsNode, scope: Scope):
        left: Instance = self.visit(node.left, scope)
        right: Type = self.context.get_type(node.identifier.lex)
        return LiteralInstance(self.context.get_type('Boolean'), left.insta_type.conforms_to(right)) 


    ############ Con Strings #################################################################################
    @visitor.when(StringConcatNode)
    def visit(self, node: StringConcatNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('String'), left + right) 
    
    @visitor.when(StringConcatSpaceNode)
    def visit(self, node: StringConcatSpaceNode, scope: Scope):
        left: LiteralInstance = self.visit(node.left, scope)
        right: LiteralInstance = self.visit(node.right, scope)
        left = left.value
        right = right.value
        return LiteralInstance(self.context.get_type('String'), left + " " + right)  
    
    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope: Scope):
        return LiteralInstance(self.context.get_type('String'), node.lex)


    
    @visitor.when(InstanceNode)
    def visit(self, node:InstanceNode, scope: Scope):
        var_t: Type = self.context.get_type(node.identifier.lex)
        instanc_scope = scope.create_child()
        for i in range(0 , len(node.arguments if node.arguments else [])) :
            arg_instace = self.visit(node.arguments[i], scope)
            instanc_scope.define_variable(var_t.arguments[i].name, var_t.arguments[i].atype, arg_instace )
        result = self.build_instance(var_t.definition, instanc_scope)
        return result

    @visitor.when(MemberAccessNode)
    def visit(self, node: MemberAccessNode, scope: Scope):
        return self.verify_member_access(node.arguments, scope)
    

    @visitor.when(FuncInfo)
    def visit(self, node: FuncInfo, scope: Scope):
        func_scope = scope.create_child()
        func_def: FuncNode | MethodNode = node.function
        args = func_def.params
        params: List[Instance] = node.params
        for i in range(0, len(params)):
            func_scope.define_variable(args[i][0].lex, params[i].insta_type, params[i])
        result: Instance = self.visit(func_def.body, func_scope)
        return result

    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode, scope: Scope):
        if node.identifier.lex in ['sin', 'cos', 'sqrt', 'exp', 'rand', 'log', 'print', 'range']:
            return self.check_built_in_f(node, node.arguments, scope)
        
        func: Method = self.context.functions[node.identifier.lex, len(node.arguments)]
        
        definition = func.definition
        args = [self.visit(arg, scope) for arg in node.arguments]
        return self.visit(FuncInfo(args, definition), self.scope.create_child())
    
    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode, scope: Scope):
        members: Instance = self.verify_member_access(node.member_access[:-1], scope)
        if isinstance(members.insta_type, ErrorType): return members

        instance_type: Type =  self.context.get_type(members.insta_type)
        
        definition = instance_type.methods[node.identifier.lex, len(node.arguments)].definition
        
        args = [self.visit(arg, scope.create_child()) for arg in node.arguments]
        return self.visit(FuncInfo(args, definition), members.met_scope)
    




    #TODO: esto esta fula
    @visitor.when(AsNode)
    def visit(self, node: AsNode, scope: Scope):
        down_cast = self.context.get_type(node.identifier.lex)
        exp: Instance = self.visit(node.expression, scope)
        return exp
    



    @visitor.when(IfNode)
    def visit(self, node: IfNode, scope: Scope):
        cond: LiteralInstance = self.visit(node.condition, scope)
        if_scope = scope.create_child()
        if_type:Instance = self.visit(node.body, if_scope)
        if cond.value: return if_type
        for eli in node.elif_nodes:
            cond = self.visit(eli.condition, scope.create_child())
            if cond.value: 
                return self.visit(eli, scope)
        else_t: Instance = self.visit(node.else_body, scope.create_child())
        return else_t
    
    @visitor.when(ElifNode)
    def visit(self, node: ElifNode, scope: Scope):
        result:Type = self.visit(node.body, scope)
        return result

    @visitor.when(ElseNode)
    def visit(self, node:ElseNode, scope: Scope):
        result:Type = self.visit(node.body, scope)
        return result



    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        cond: LiteralInstance = self.visit(node.condition, scope)
        
        while_scope = scope.create_child()
        while(cond.value): 
            return_t :Instance = self.visit(node.body, while_scope)
            cond = self.visit(node.condition, scope)
        return return_t


    @visitor.when(ForNode)
    def visit(self, node: ForNode, scope: Scope):
        for_scope = scope.create_child()
        iterand: Instance = self.visit(node.iterable, scope)
        result = None
        if isinstance(iterand, VectorInstance):
            vector = iterand.vector
            if len(vector) == 0: return None
            for_scope.define_variable(node.identifier.lex, iterand.insta_type)
            for elemnt in vector:
                var = for_scope.find_variable(node.identifier.lex)
                var.instance = elemnt
                result = self.visit(node.body, for_scope)
            return result


        ident_type: Instance = self.visit(iterand.methods[('current', 0)].definition, iterand.met_scope)
        for_scope.define_variable(node.identifier.lex, ident_type.insta_type.name, ident_type)
        condition: LiteralInstance = self.visit(iterand.methods[('next', 0)].definition, iterand.met_scope)
        while(condition):
            result: Instance = self.visit(node.body, for_scope)
            var: VariableInfo = for_scope.find_variable(node.identifier.lex)
            var.instance = self.visit(iterand.methods[('current', 0)].definition, iterand.met_scope)
            condition: LiteralInstance = self.visit(iterand.methods[('next', 0)].definition, iterand.met_scope)

        
        return result
    

    @visitor.when(ExplicitVectorNode)
    def visit(self, node: ExplicitVectorNode, scope: Scope):
        content = []
        vect_type = None
        if len(node.arguments) > 0:
            vect_type = self.visit(node.arguments[0], scope).insta_type
            for exp in node.arguments:
                element = self.visit(exp, scope)
                content.append(element)
                vect_type = lowest_common_ancestor(vect_type, element.insta_type)
        return VectorInstance(self.context.get_type(vect_type), content)

    @visitor.when(ImplicitVectorNode)
    def visit(self, node: ImplicitVectorNode, scope: Scope):
        elements = []
        elemnt_scope = scope.create_child()
        iterable_inst: Instance = self.visit(node.iterable, scope)
        next_func: MethodNode = iterable_inst.methods[('next', 0)].definition
        next_func = MethodCallNode([node.iterable, next_func.identifier])
        current: MethodNode = iterable_inst.methods[('current', 0)].definition
        current_i:Instance = self.visit(current, iterable_inst.met_scope)
        var = elemnt_scope.define_variable(node.identifier.lex, current, current_i)
        while(condition):
            elements.append(self.visit(node.expression, elemnt_scope))
            var: VariableInfo = elemnt_scope.find_variable(node.identifier.lex)
            var.instance = self.visit(current, iterable_inst.met_scope)
            condition: LiteralInstance = self.visit(next_func, iterable_inst.met_scope)
        

        return VectorInstance(vect_type.insta_type)
    
    @visitor.when(VectorIndexNode)
    def visit(self, node: VectorIndexNode, scope: Scope):
        variable: VariableInfo = scope.find_variable(node.identifier.lex)
        index_type: LiteralInstance = self.visit(node.index, scope)
        try:
            result = variable.instance.vector[int(index_type.value)]
        except Exception as exc:
            print(exc)
            return None
        return result



    ## Metodos auxiliares ##################################################################
   
    def verify_member_access(self, members: List[IdentifierNode], scope):
        variable: VariableInfo = scope.find_variable(members[0].lex)
        var_type: Instance = variable.instance
        current: Attribute = variable
        for i in range(0,len(members)-1):
            current: VariableInfo = var_type.attr[members[i+1].lex]
            var_type = current.instance
        return var_type



    def build_instance(self, node: TypeNode, scope: Scope):
        curren_type = node
        att_scope = scope.create_child()
        meth_scope = self.scope.create_child()
        attrubutes = {}
        parent_instance_node = InstanceNode(curren_type.super_type, curren_type.super_type_args)
        parent_instance: Instance = self.visit(parent_instance_node, scope) if node.super_type.lex != 'Object' else Instance(ObjectType())
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
        params_f = []
       
        
        if name == 'print': 
            return self.print_func(self.visit(params[0], scope))
            
        for param in params:
            params_f.append(self.visit(param, scope))
        return self.built_in(name, params_f)
    
    def print_func(self, param):
        print(param.value)
        return LiteralInstance(self.context.get_type("String"), f'{param.value}' if not isinstance(param.value, str) else param.value)
    def built_in(self, op, x):
        match op:
            case 'sin':
                return LiteralInstance(self.context.get_type('Number'),  math.sin(x[0].value))
            case 'cos':
                return LiteralInstance(self.context.get_type('Number'),  math.cos(x[0].value))
            case 'sqrt':
                return LiteralInstance(self.context.get_type('Number'),  math.sqrt(x[0].value))
            case 'exp':
                return LiteralInstance(self.context.get_type('Number'),  math.e**x[0].value)
            case 'rand':
                return LiteralInstance(self.context.get_type('Number'),  rnd.randint(0, 1))
            case "log":
                return LiteralInstance(self.context.get_type('Number'),  math.log(x[1].value, x[0].value))
            case "range":
                return VectorInstance(self.context.get_type('Number'), [LiteralInstance(self.context.get_type('Number') ,x) for x in range(int(x[0].value),int(x[1].value))])
            
