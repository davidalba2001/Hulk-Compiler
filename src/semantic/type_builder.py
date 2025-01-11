from cmp.hulk_ast import *
from semantic.semantic import *
import cmp.visitor as visitor
from typing import List


class TypeBuilderVisitor:
    def __init__(self, context: Context, scope: Scope, errors) -> None:
        self.context: Context = context
        self.scope: Scope = scope
        self.errors: List[str] = errors
        self.currentType: Type = None

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

        self.currentType: Type = self.context.get_type(node.identifier)

        if isinstance(self.current_type, ErrorType):
            return


        if node.base_type in ["Number", "Boolean", "String"]:
            self.errors.append(
                SemanticError(
                    f"Base type '{node.base_type}' is not allowed at line {node.line}."
                )
            )

        try:
            # Detect circular inheritance dependencies and validate parent type
            inheritance = self.context.get_type(node.base_type)
            ancestor = inheritance
            while ancestor:
                if ancestor.name == self.currentType.name:
                    self.errors.append(
                        SemanticError(
                            f'Circular dependency detected involving type "{node.identifier}" at line {node.line}.'
                        )
                    )
                    break
                ancestor = ancestor.parent

        except SemanticError:
            self.errors.append(
                SemanticError(
                    f'The inherited type "{node.base_type}" is not defined at line {node.line}.'
                )
            )
            return

        try:
            self.currentType.set_parent(inheritance)
        except SemanticError:
            self.errors.append(
                SemanticError(
                    f"Parent type is already set for {self.node.name} at line {node.line}."
                )
            )

        for pname, ptype in node.params:
            try:
                if ptype:
                    ptype = self.context.get_type(ptype)
                else:
                    ptype = VarType
            except:
                self.errors.append(
                    SemanticError(
                        f'The type "{ptype}" annotated for argument "{pname}" is not defined at line {node.line}.'
                    )
                )
                return
            try:
                self.currentType.define_arguments(pname, ptype)
            except SemanticError:
                self.errors.append(
                    SemanticError(
                        f'Argument with the name "{pname}" already exists in type "{self.currentType.name}" at line {node.line}.'
                    )
                )

        for attribute in node.attributes:
            self.visit(attribute)

        for method in node.methods:
            self.visit(method)

    @visitor.when(AssignmentNode)
    def visit(self, node: AssignmentNode):
        try:
            attribute_type = self.context.get_type(node.type_annotation)
        except SemanticError as e:
            self.errors.append(
                SemanticError(
                    f'The type "{node.type_annotation}" annotated for the field "{node.identifier}" is not defined at line {node.line}.'
                )
            )
            return

        if self.current_type:
            try:
                self.current_type.define_attribute(node.identifier, attribute_type)
            except SemanticError as e:
                self.errors.append(
                    SemanticError(
                        f'Error defining attribute "{node.identifier}" with type "{attribute_type.name}" at line {node.line}.'
                    )
                )

    @visitor.when(MethodNode)
    def visit(self, node: MethodNode):
        # Try to get the return type annotation
        try:
            return_type = self.context.get_type(node.type_annotation)
        except SemanticError:
            self.errors.append(
                SemanticError(
                    f'The return type "{node.type_annotation}" is not defined at line {node.line}.'
                )
            )
            return

        param_names = []
        param_types = []
        params: List = node.params

        # Process parameters
        for pname, ptype in params:
            # Check for duplicate parameter names
            if pname in param_names:
                self.errors.append(
                    SemanticError(
                        f'The variable name "{pname}" is already in use at line {node.line}.'
                    )
                )
                return
            else:
                param_names.append(pname)

            # Try to get the parameter type
            try:
                param_type = self.context.get_type(ptype)
                param_types.append(param_type)
            except SemanticError:
                self.errors.append(
                    SemanticError(
                        f'The type of parameter "{ptype}" in function "{node.identifier}" is not defined at line {node.line}.'
                    )
                )
                return

        # Define the method if current_type is set
        if self.current_type:
            try:
                try:
                    method = self.currentType.get_method()
                    if isinstance(method,ErrorType):
                        return
                    self.currentType.methods[node.identifier,len(param_names)] = ErrorType
                except:    
                    self.current_type.define_method(
                        node.identifier, param_names, param_types, return_type)
                
            except SemanticError:
                self.errors.append(
                    SemanticError(
                        f'The function "{node.identifier}" already exists in the context of "{self.current_type.name}" at line {node.line}.'
                    )
                )

    @visitor.when(FuncNode)
    def visit(self, node: FuncNode):
        # Try to retrieve the return type annotation
        try:
            return_type = self.context.get_type(node.type_annotation)
        except SemanticError:
            self.errors.append(
                SemanticError(
                    f'The return type "{node.type_annotation}" is not defined at line {node.line}.'
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
                        f'The parameter name "{pname}" is already in use at line {node.line}.'
                    )
                )
                return
            param_names.append(pname)

            # Try to retrieve the parameter type
            try:
                param_type = self.context.get_type(ptype)
                param_types.append(param_type)
            except SemanticError:
                self.errors.append(
                    SemanticError(
                        f'The type "{ptype}" for parameter "{pname}" in function "{node.identifier}" is not defined at line {node.line}.'
                    )
                )
                return

        # Attempt to create or register the function in the context
        try:
            function = self.context.get_function(node.identifier,len(param_names))
            if isinstance(function,ErrorType):
                return
            self.context.create_function(
                node.identifier, param_names, param_types, return_type
            )
        except SemanticError:
            self.errors.append(
                SemanticError(
                    f'The function "{node.identifier}" is already defined with {len(node.params)} parameters at line {node.line}.'
                )
            )

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode):
        protocol = self.context.get_protocol(node.identifier)
        
        if isinstance(self.current_type, ErrorType):
            return
        
        if node.superProtocol:
            try:
                extend: Protocol = self.context.get_protocol(node.superProtocol)
                ancestor = extend
                while ancestor:
                    if ancestor.name == self.current_type.name:
                        self.errors.append(SemanticError(
                            f'Circular dependency detected involving protocol "{node.identifier}" at line {node.line}.'))
                        break
                    ancestor = ancestor.parent
            except:
                self.errors.append(
                SemanticError(
                    f"El protocolo {node.superProtocol} extendido en el protocolo {node.identifier} no esta definido {node.line}"
                )
            )
            return

        for mname, (param_names, param_types), ptype in node.body:
            try:
                protocol.define_method(mname, param_names, param_types, ptype)
            except:
                self.errors.append(
                    SemanticError(
                        f"El metodo {mname} ya esta definido con {protocol.methods} parametros {node.lien}"
                    )
                )
            
            

