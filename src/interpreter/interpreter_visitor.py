from cmp.hulk_ast import *
from semantic.semantic import *
import cmp.visitor as visitor

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
            print(self.visit(node.main_expression, self.scope.create_child()).value)


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
            member_type: Instance = self.visit(member, scope)
            if isinstance(member_type.insta_type, ErrorType): return member_type
            
            exp_type: Instance = self.visit(node.expression, current_scope)
            if not exp_type.insta_type.conforms_to(member_type.insta_type):
                self.errors.append(SemanticError(f'La variable {node.identifier.arguments[-1].lex} de tipo {member_type.insta_type.name} no puede ser asignada con el tipo {exp_type.insta_type.name}'))
                return Instance(ErrorType(), self.scope, self.scope)
            
            return member_type
            
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
        return LiteralInstance(self.context.get_type('Number'), left*right  ) 
            
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
        return LiteralInstance(self.context.get_type('Number'),  left**right) 
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
            result =  int(node.lex)
        except: result = float(node.lex)
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
        if name == 'range': return self.context.get_type("Range").basic_instance
        
        return Instance(self.context.get_type('Number'))