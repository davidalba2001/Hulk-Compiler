from cmp.hulk_ast import *
from semantic.semantic import *
import cmp.visitor as visitor
from typing import List


class TypeBuilderVisitor():
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
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):
        self.currentType: Type = self.context.get_type(node.identifier) 
        try:
            inheritance = self.context.get_type(node.superType.identifier)
        except:
            self.errors.append(SemanticError(f'El tipo  {node.inheritance} del que se hereda no esta definido'))
            inheritance = self.context.get_type('object')
        
        self.currentType.inheritance = inheritance
        
        for arg in node.params:
            name = arg[0]
            type = arg[1]
            try:
                type: Type =  self.context.get_type(type)
            except: 
                self.errors.append(SemanticError(f'El tipo anotado como \"{type.name}\" no esta definido'))
                type = self.context.get_type('object')
            try:
                self.currentType.define_arguments(name, type)      
            except:
                self.errors.append(f'Existenten mas argumentos con el nombre {name.id}')

        for attrDef in node.attributes:
            self.visit(attrDef)
            
        for methodDef in node.methods:
            self.visit(methodDef)
            
        # Se actualiza el tipo para cuando vea luego algun metodo
        self.currentType = None

    @visitor.when(AssignmentNode)
    def visit(self, node: AssignmentNode):
        try:
            attribution = self.context.get_type(node.type_annotation)
        except:
            self.errors.append(SemanticError(f'El tipo {node.type_annotation} anotado a el campo {node.identifier} no esta definido'))
            attribution = self.context.get_type('var')
        if self.currentType:
            self.currentType.define_arguments(node.identifier, attribution)
    @visitor.when(MethodNode)
    def visit(self, node: MethodNode):
        type_annotation: TypeNode = self.context.get_type('object')
        try: 
            type_annotation = self.context.get_type(node.type_annotation)
        except:
            self.errors.append(f'El tipo de retorno {node.type_annotation} no esta definido')
        
        args: List = node.params
        args_names = []
        args_types = []
        for param in args:
            name, type = param
            if name in args_names:
                self.errors.append(SemanticError(f'Ya el nombre de variable {name} ya esta en uso'))
            args_names.append(name)
            try:
                self.context.get_type(type)
                args_types.append(type)
            except:
                self.errors.append(f'El tipo del parametro {type} que se le pasa a la funcion {node.identifier} no esta definido')
                args_types.append('object')
            
        if self.currentType:
            try:
                self.currentType.define_method(node.identifier, args_names, args_types, type_annotation)
            except:
                self.errors.append(SemanticError(f'La funcion {node.identifier} ya existe en el contexto de {self.currentType.name}.'))
            
    @visitor.when(FuncNode)
    def visit(self, node: FuncNode):
        type_annotation: TypeNode = self.context.get_type('object')
        try: 
            type_annotation = self.context.get_type(node.type_annotation)
        except:
            self.errors.append(f'El tipo de retorno {node.type_annotation} no esta definido')
        
        args: List = node.params
        args_names = []
        args_types = []
        for param in args:
            name, type = param
            if name in args_names:
                self.errors.append(SemanticError(f'Ya el nombre de variable {name} ya esta en uso'))
            args_names.append(name)
            try:
                self.context.get_type(type)
                args_types.append(type)
            except:
                self.errors.append(f'El tipo del parametro {type} que se le pasa a la funcion {node.identifier} no esta definido')
                args_types.append('object')
            
            functions = [self.context.functions[func] for func in self.context.functions
                         if self.context.functions[func] == node.identifier and len(self.context.functions) == len(args)]
            if functions == 0:
                self.context.functions[node.identifier].append(Method(node.identifier, args_names, args_types, type_annotation))
            else:
                self.errors.append(SemanticError(f'La funcion {node.identifier} ya esta definida con {len(args)} argumentos'))
    @visitor.when(ProtocolNode)
    def visit(self, node:ProtocolNode):
        pass



    #TODO: Terminar Protocolos
