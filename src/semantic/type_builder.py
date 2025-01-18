from cmp.hulk_ast import *
from semantic.semantic import *
import cmp.visitor as visitor
from typing import List


class TypeBuilderVisitor:
    def __init__(self, context: Context, scope: Scope, errors) -> None:
        self.context: Context = context
        self.scope: Scope = scope
        self.errors: List[str] = errors
        self.current_type: Type = None

    @visitor.on("node")
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for typex in node.statements_type:
            self.visit(typex)
        for func in node.statements_func:
            self.visit(func)
        for protocol in node.statements_protocol:
            self.visit(protocol)

            
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):

        self.current_type: Type = self.context.get_type(node.identifier.lex)

        if isinstance(self.current_type, ErrorType):
            return


        if node.super_type.lex in ["Number", "Boolean", "String"]:
            self.errors.append(
                SemanticError(
                    f"Base type '{node.super_type.lex}' is not allowed at line {node.identifier.line}."
                )
            )

        try:
            # Detect circular inheritance dependencies and validate parent type
            inheritance = self.context.get_type(node.super_type.lex)
            ancestor = inheritance
            while ancestor:
                if ancestor.name == self.current_type.name:
                    self.errors.append(
                        SemanticError(
                            f'Circular dependency detected involving type "{node.identifier.lex}" at line {node.identifier.line}.'
                        )
                    )
                    break
                ancestor = ancestor.parent

        except SemanticError:
            self.errors.append(
                SemanticError(
                    f'The inherited type "{node.super_type.lex}" is not defined at line {node.identifier.line}.'
                )
            )
            return

        try:
            self.current_type.set_parent(inheritance)
        except SemanticError:
            self.errors.append(
                SemanticError(
                    f"Parent type is already set for {node.identifier.lex} at line {node.line}."
                )
            )

        for pname, ptype in node.params:
            try:
                if ptype:
                    ptype = self.context.get_type(ptype.lex)
                else:
                    ptype = VarType
            except:
                self.errors.append(
                    SemanticError(
                        f'The type "{ptype.lex}" annotated for argument "{pname.lex}" is not defined at line {node.identifier.line}.'
                    )
                )
                return
            try:
                self.current_type.define_arguments(pname.lex, ptype)
            except SemanticError:
                self.errors.append(
                    SemanticError(
                        f'Argument with the name "{pname.lex}" already exists in type "{self.current_type.name}" at line {node.identifier.line}.'
                    )
                )

        for attribute in node.attributes:
            self.visit(attribute)

        for method in node.methods:
            self.visit(method)

        self.current_type = None

    @visitor.when(AssignmentNode)
    def visit(self, node: AssignmentNode):
        try:
            attribute_type = self.context.get_type(node.type_annotation.lex)
        except SemanticError as e:
            self.errors.append(
                SemanticError(
                    f'The type "{node.type_annotation.lex}" annotated for the field "{node.identifier.lex}" is not defined at line {node.identifier.line}.'
                )
            )
            return

        if self.current_type:
            try:
                self.current_type.define_attribute(node.identifier.lex, attribute_type)
            except SemanticError as e:
                self.errors.append(
                    SemanticError(
                        f'Error defining attribute "{node.identifier.lex}" with type "{attribute_type.name}" at line {node.identifier.line}.'
                    )
                )

    @visitor.when(MethodNode)
    def visit(self, node: MethodNode):
        # Try to get the return type annotation
        try:
            return_type = self.context.get_type(node.type_annotation.lex)
        except SemanticError:
            self.errors.append(
                SemanticError(
                    f'The return type "{node.type_annotation.lex}" is not defined at line {node.identifier.line}.'
                )
            )
            return

        param_names = []
        param_types = []
        params: List[Tuple[IdentifierNode, IdentifierNode]] = node.params

        # Process parameters
        for pname, ptype in params:
            # Check for duplicate parameter names
            if pname in param_names:
                self.errors.append(
                    SemanticError(
                        f'The variable name "{pname.lex}" is already in use at line {node.identifier.line}.'
                    )
                )
                return
            else:
                param_names.append(pname.lex)

            # Try to get the parameter type
            try:
                param_type = self.context.get_type(ptype.lex)
                param_types.append(param_type)
            except SemanticError:
                self.errors.append(
                    SemanticError(
                        f'The type of parameter "{ptype.lex}" in function "{node.identifier.lex}" is not defined at line {node.identifier.line}.'
                    )
                )
                return

        # Define the method if current_type is set
        if self.current_type:
            try:
                try:
                    method = self.current_type.get_method()
                    if isinstance(method,ErrorType):
                        return
                    self.current_type.methods[node.identifier,len(param_names)] = ErrorType
                except:    
                    self.current_type.define_method(
                        node.identifier.lex, param_names, param_types, return_type, node)
                
            except SemanticError:
                self.errors.append(
                    SemanticError(
                        f'The function "{node.identifier.lex}" already exists in the context of "{self.current_type.name}" at line {node.identifier.line}.'
                    )
                )

    @visitor.when(FuncNode)
    def visit(self, node: FuncNode):
        # Try to retrieve the return type annotation

        try:
            if node.type_annotation.lex != 'UnknownType':
                return_type = self.context.get_type(node.type_annotation.lex)
            else: return_type = VarType()
        except SemanticError:
            self.errors.append(
                SemanticError(
                    f'The return type "{node.type_annotation.lex}" is not defined at line {node.identifier.line}.'
                )
            )
            return

        param_names = []
        param_types = []

        # Process function parameters
        for pname, ptype in node.params:
            # Check for duplicate parameter names
            if pname in param_names:
                self.errors.append(
                    SemanticError(
                        f'The parameter name "{pname.lex}" is already in use at line {node.identifier.line}.'
                    )
                )
                return
            param_names.append(pname.lex)

            # Try to retrieve the parameter type
            try:
                if node.type_annotation.lex != 'UnknownType':
                    param_type = self.context.get_type(ptype.lex)
                else:
                    param_types.append(VarType())
            except SemanticError:
                self.errors.append(
                    SemanticError(
                        f'The type "{ptype.lex}" for parameter "{pname.lex}" in function "{node.identifier.lex}" is not defined at line {node.identifier.line}.'
                    )
                )
                return

        # Attempt to create or register the function in the context
        try:
            function = self.context.get_function(node.identifier.lex,len(param_names))
            if isinstance(function,ErrorType):
                return
            self.context.create_function(
                node.identifier.lex, param_names, param_types, return_type, node
            )
        except SemanticError:
            self.errors.append(
                SemanticError(
                    f'The function "{node.identifier.lex}" is already defined with {len(node.params)} parameters at line {node.identifier.line}.'
                )
            )

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode):
        protocol = self.context.get_protocol(node.identifier.lex)
        
        if isinstance(self.current_type, ErrorType):
            return
        
        if node.super_protocol:
            try:
                extend: Protocol = self.context.get_protocol(node.super_protocol.lex)
                ancestor = extend
                while ancestor:
                    if ancestor.name == self.current_type.name:
                        self.errors.append(SemanticError(
                            f'Circular dependency detected involving protocol "{node.identifier.lex}" at line {node.identifier.line}.'))
                        break
                    ancestor = ancestor.parent
            except:
                self.errors.append(
                SemanticError(
                    f"El protocolo {node.super_protocol.lex} extendido en el protocolo {node.identifier.lex} no esta definido {node.identifier.line}"
                )
            )
            return

        for method in node.body:
            try:
                pnames = []
                ptypes = []
                for param in method.params:
                    pnames.append(param[0].lex)
                    ptypes.append(param[1].lex)

                protocol.define_method(method.identifier.lex, pnames, ptypes, method.type_annotation.lex)
            except:
                self.errors.append(
                    SemanticError(
                        f"El metodo {method.identifier.lex} ya esta definido con {len(method.params)} parametros, linia {method.identifier.line}"
                    )
                )
            
            

