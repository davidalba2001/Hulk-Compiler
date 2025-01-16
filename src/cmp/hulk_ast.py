"""
██╗░░██╗██╗███████╗██████╗░░█████╗░██████╗░░█████╗░██╗░░██╗██╗░█████╗░░█████╗░██╗░░░░░
██║░░██║██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║░░██║██║██╔══██╗██╔══██╗██║░░░░░
███████║██║█████╗░░██████╔╝███████║██████╔╝██║░░╚═╝███████║██║██║░░╚═╝███████║██║░░░░░
██╔══██║██║██╔══╝░░██╔══██╗██╔══██║██╔══██╗██║░░██╗██╔══██║██║██║░░██╗██╔══██║██║░░░░░
██║░░██║██║███████╗██║░░██║██║░░██║██║░░██║╚█████╔╝██║░░██║██║╚█████╔╝██║░░██║███████╗
╚═╝░░╚═╝╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝

███╗░░██╗░█████╗░██████╗░███████╗   ████████╗██████╗░███████╗███████╗
████╗░██║██╔══██╗██╔══██╗██╔════╝   ╚══██╔══╝██╔══██╗██╔════╝██╔════╝
██╔██╗██║██║░░██║██║░░██║█████╗░░   ░░░██║░░░██████╔╝█████╗░░█████╗░░
██║╚████║██║░░██║██║░░██║██╔══╝░░   ░░░██║░░░██╔══██╗██╔══╝░░██╔══╝░░
██║░╚███║╚█████╔╝██████╔╝███████╗   ░░░██║░░░██║░░██║███████╗███████╗
╚═╝░░╚══╝░╚════╝░╚═════╝░╚══════╝   ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚══════╝

└─── Node ──┬── ProgramNode
            │
            │
            ├── ExpressionNode ─┬── BinaryNode ─────────┬── StringOperationNode ──────┬── StringConcatNode
            │                   │                       │                             └── StringConcatSpaceNode
            │                   │                       │
            │                   │                       ├── ArithmeticOperationNode ──┬── ModNode
            │                   │                       │                             ├── MinusNode
            │                   │                       │                             ├── MultiplyNode
            │                   │                       │                             ├── DivideNode
            │                   │                       │                             └── PowerNode
            │                   │                       │
            │                   │                       ├── BooleanOperationNode ─────┬── OrNode
            │                   │                       │                             └── AndNode
            │                   │                       │
            │                   │                       ├── RelationalOperationNode ──┬── LessThanNode
            │                   │                       │                             ├── GreaterThanNode
            │                   │                       │                             ├── LessEqualNode
            │                   │                       │                             └── GreaterEqualNode
            │                   │                       │
            │                   │                       └── EqualityOperationNode ────┬── EqualNode
            │                   │                                                     └── NotEqualNode
            │                   │
            │                   ├── TypeOperationNode ──┬── AsNode
            │                   │                       └── IsNode
            │                   │
            │                   ├── TypeInstanceNode ───┬── InstanceNode
            │                   │                       ├── ImplicitVectorNode
            │                   │                       └── ExplicitVectorNode
            │                   │
            │                   ├── CallNode ───────────┬── FunctionCallNode
            │                   │                       └── MethodCallNode
            │                   │
            │                   ├── LoopNode ───────────┬── WhileNode
            │                   │                       └── ForNode
            │                   │
            │                   ├── BindingNode ────────┬── AssignmentNode
            │                   │                       └── DassignmentNode
            │                   │
            │                   ├── ConditionalNode ────┬── IfNode
            │                   │                       ├── ElifNode
            │                   │                       └── ElseNode
            │                   │
            │                   ├── AtomicNode ─────────┬── BooleanNode
            │                   │                       ├── NumberNode
            │                   │                       ├── StringNode
            │                   │                       └── IdentifierNode
            │                   │
            │                   ├── UnaryNode ──────────┬── NotNode
            │                   │                       └── NegativeNode
            │                   ├── BlockNode
            │                   │
            │                   ├── LetNode
            │                   │
            │                   └── VectorIndexNode
            │
            └── StatementNode ──┬── ExtendableNode ─────┬── TypeNode
                                │                       └── ProtocolNode
                                │
                                └── CallableNode ───────┬── FuncNode
                                                        └── MethodNode





└── ProgramNode(statements,main_expression)
                    │            │
                    │            └───┬── ExpressionNode()
                    │                │
                    │                └── BlockNode(expressions)
                    │
                    └─── StatementsNode(statements_type,statements_func,statements_protocol)
                                                │               │                │
                                                │               │                └── ProtocolNode(identifier:Str,super_protocol:Str,body)
                                                │               │
                                                │               └── FuncNode(identifier:Str,params:,type_annotation:, body)
                                                │
                                                └── TypeNode()

"""
from __future__ import annotations
from typing import List, Optional, Union, Tuple, Dict, Any

from cmp.utils import Token

from typing import List, Union, Tuple


class Node:
    """Clase base para todos los nodos."""
    pass


class ProgramNode(Node):
    """
    Nodo para representar un programa completo.
    """
    def __init__(
        self,
        statements_type: List['TypeNode'],  # Lista de declaraciones de tipos
        statements_protocol: List['ProtocolNode'],  # Lista de protocolos
        statements_func: List['FuncNode'],  # Lista de funciones
        main_expression: Union['ExpressionNode', 'BlockNode'],  # Expresión principal
    ) -> None:
        super().__init__()
        self.statements_type = statements_type
        self.statements_protocol = statements_protocol
        self.statements_func = statements_func
        self.main_expression = main_expression


class StatementNode(Node):
    """
    Nodo base para declaraciones, como tipos, funciones, o protocolos.
    """
    pass


class CallableNode(StatementNode):
    """
    Nodo base para funciones y métodos invocables.
    """
    def __init__(
        self,
        identifier: 'Token',  # Identificador como token
        params: List[Tuple['Token', 'Token']],  # Lista de parámetros como tokens
        return_type_annotation: 'Token',  # Tipo de retorno como token
        body: Union['ExpressionNode', 'BlockNode'],  # Cuerpo de la función o método
    ) -> None:
        super().__init__()
        self.identifier = IdentifierNode(identifier)  # Convertir a IdentifierNode
        # Convertir parámetros a tuplas de IdentifierNode
        self.params: List[Tuple[IdentifierNode, IdentifierNode]] = [
            (IdentifierNode(param[0]), IdentifierNode(param[1])) for param in params
        ]
        self.return_type_annotation = IdentifierNode(return_type_annotation)  # Convertir a IdentifierNode
        self.body = body


class ExtendableNode(StatementNode):
    """
    Nodo base para tipos y protocolos que pueden extenderse.
    """
    def __init__(
        self,
        identifier: 'Token',  # Identificador como token
    ) -> None:
        super().__init__()
        self.identifier = IdentifierNode(identifier)  # Convertir a IdentifierNode


class ExpressionNode(Node):
    """
    Nodo base para expresiones.
    """
    pass


# ###############################################################################
# ░██████╗████████╗░█████╗░████████╗███████╗███╗░░░███╗███████╗███╗░░██╗████████╗
# ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██╔════╝████╗░████║██╔════╝████╗░██║╚══██╔══╝
# ╚█████╗░░░░██║░░░███████║░░░██║░░░█████╗░░██╔████╔██║█████╗░░██╔██╗██║░░░██║░░░
# ░╚═══██╗░░░██║░░░██╔══██║░░░██║░░░██╔══╝░░██║╚██╔╝██║██╔══╝░░██║╚████║░░░██║░░░
# ██████╔╝░░░██║░░░██║░░██║░░░██║░░░███████╗██║░╚═╝░██║███████╗██║░╚███║░░░██║░░░
# ╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░
#################################################################################
# NOTE: Una lista de parametro una lista de elementos de la forma  (nombre, tipo)
# (en detalles de implementacion se puede ver que es un diccionario)
# NOTE: Una lista de argumentos es una lista de expresiones
class TypeNode(ExtendableNode):
    """
    Nodo para definir un tipo (clase o estructura).
    """
    def __init__(
        self,
        identifier: "Token",  # Identificador como token
        params: List[Tuple["Token", "Token"]],  # Lista de parámetros como tokens
        super_type: Tuple["Token", List[ExpressionNode]],  # Tipo padre y sus argumentos
        body: Tuple[List[AssignmentNode], List["MethodNode"]],  # Atributos y métodos
    ) -> None:
        super().__init__(IdentifierNode(identifier))
        self.params = [(IdentifierNode(param[0]), IdentifierNode(param[1])) for param in params]
        self.super_type = IdentifierNode(super_type[0])  # Tipo padre como IdentifierNode
        self.super_type_args = super_type[1]  # Argumentos del tipo padre
        self.attributes = body[0]  # Atributos del tipo
        self.methods = body[1]  # Métodos del tipo


class ProtocolNode(ExtendableNode):
    """
    Nodo para definir un protocolo.
    """
    def __init__(
        self,
        identifier: "Token",  # Identificador como token
        super_protocol: "Token",  # Protocolo padre como token
        body: List["MethodNode"],  # Métodos del protocolo
    ) -> None:
        super().__init__(IdentifierNode(identifier))
        self.super_protocol = IdentifierNode(super_protocol)  # Convertido a IdentifierNode
        self.body = body


class CallableNode(ExpressionNode):
    """
    Nodo base para definiciones invocables (funciones o métodos).
    """
    def __init__(
        self,
        identifier: "Token",  # Identificador como token
        params: List[Tuple["Token", "Token"]],  # Lista de parámetros como tokens
        type_annotation: "Token",  # Anotación de tipo como token
        body: Union[ExpressionNode, BlockNode],  # Cuerpo de la función o método
    ) -> None:
        super().__init__()
        self.identifier = IdentifierNode(identifier)  # Convertido a IdentifierNode
        self.params = [(IdentifierNode(param[0]), IdentifierNode(param[1])) for param in params]
        self.type_annotation = IdentifierNode(type_annotation)  # Convertido a IdentifierNode
        self.body = body


class FuncNode(CallableNode):
    """
    Nodo para definir funciones.
    """
    def __init__(
        self,
        identifier: "Token",  # Identificador como token
        params: List[Tuple["Token", "Token"]],  # Lista de parámetros como tokens
        type_annotation: "Token",  # Anotación de tipo como token
        body: Union[ExpressionNode, BlockNode],  # Cuerpo de la función
    ) -> None:
        super().__init__(identifier, params, type_annotation, body)


class MethodNode(CallableNode):
    """
    Nodo para definir métodos.
    """
    def __init__(
        self,
        identifier: "Token",  # Identificador como token
        params: List[Tuple["Token", "Token"]],  # Lista de parámetros como tokens
        type_annotation: "Token",  # Anotación de tipo como token
        body: Optional[Union[ExpressionNode, BlockNode]] = None,  # Cuerpo opcional
    ) -> None:
        super().__init__(identifier, params, type_annotation, body)


# region Top-level expressions
#################################################################################
# ███████╗██╗░░██╗██████╗░██████╗░███████╗░██████╗░██████╗██╗░█████╗░███╗░░██╗
# ██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██║██╔══██╗████╗░██║
# █████╗░░░╚███╔╝░██████╔╝██████╔╝█████╗░░╚█████╗░╚█████╗░██║██║░░██║██╔██╗██║
# ██╔══╝░░░██╔██╗░██╔═══╝░██╔══██╗██╔══╝░░░╚═══██╗░╚═══██╗██║██║░░██║██║╚████║
# ███████╗██╔╝╚██╗██║░░░░░██║░░██║███████╗██████╔╝██████╔╝██║╚█████╔╝██║░╚███║
# ╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚═════╝░╚═════╝░╚═╝░╚════╝░╚═╝░░╚══╝
#################################################################################

# TODO Quizas Pueda decir que tipos son esos Anys

class ExpressionNode:
    """
    Clase base para todos los nodos de expresión.
    """
    def __init__(self) -> None:
        pass


class BinaryNode(ExpressionNode):
    """
    Nodo para operaciones binarias (dos operandos).
    """
    def __init__(self, left: "ExpressionNode", right: "ExpressionNode") -> None:
        super().__init__()
        self.left: ExpressionNode = left
        self.right: ExpressionNode = right


class UnaryNode(ExpressionNode):
    """
    Nodo para operaciones unarias (un solo operando).
    """
    def __init__(self, expression: "ExpressionNode") -> None:
        super().__init__()
        self.expression: ExpressionNode = expression


class BlockNode(ExpressionNode):
    """
    Nodo para un bloque de expresiones.
    """
    def __init__(self, expressions: List["ExpressionNode"]) -> None:
        super().__init__()
        self.expressions: List[ExpressionNode] = expressions


class LetNode(ExpressionNode):
    """
    Nodo para declaraciones 'let' con bindings y un cuerpo.
    """
    def __init__(
        self,
        bindings: List[Union["AssignmentNode", "DassignmentNode"]],
        body: Union[ExpressionNode, BlockNode],
    ) -> None:
        super().__init__()
        self.bindings: List[Union["AssignmentNode", "DassignmentNode"]] = bindings
        self.body: Union[ExpressionNode, BlockNode] = body


class VectorIndexNode(ExpressionNode):
    """
    Nodo para acceder a un elemento de un vector por índice.
    """
    def __init__(self, identifier: "Token", index: "ExpressionNode") -> None:
        super().__init__()
        self.identifier: IdentifierNode = IdentifierNode(identifier)  # Convertimos a IdentifierNode
        self.index: ExpressionNode = index

# endregion
##########################################################################


# region Type Instance Nodes
# ██╗███╗░░██╗░██████╗████████╗░█████╗░███╗░░██╗░█████╗░███████╗
# ██║████╗░██║██╔════╝╚══██╔══╝██╔══██╗████╗░██║██╔══██╗██╔════╝
# ██║██╔██╗██║╚█████╗░░░░██║░░░███████║██╔██╗██║██║░░╚═╝█████╗░░
# ██║██║╚████║░╚═══██╗░░░██║░░░██╔══██║██║╚████║██║░░██╗██╔══╝░░
# ██║██║░╚███║██████╔╝░░░██║░░░██║░░██║██║░╚███║╚█████╔╝███████╗
# ╚═╝╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝░╚════╝░╚══════╝
class TypeInstanceNode(ExpressionNode):
    """
    Nodo base para instancias de tipos.
    """

    def __init__(self) -> None:
        super().__init__()


class InstanceNode(TypeInstanceNode):
    def __init__(self, identifier: "Token", arguments: List[ExpressionNode]) -> None:
        """
        Nodo para instanciar un tipo específico.
        """
        super().__init__()
        self.identifier = IdentifierNode(identifier)  # Siempre un IdentifierNode
        self.arguments = arguments  # Lista de nodos de expresión como argumentos


class ExplicitVectorNode(TypeInstanceNode):
    def __init__(self, arguments: List[ExpressionNode]) -> None:
        """
        Nodo para vectores explícitos (con valores directamente especificados).
        """
        super().__init__()
        self.arguments = arguments  # Lista de argumentos


class ImplicitVectorNode(TypeInstanceNode):
    def __init__(
        self,
        expression: ExpressionNode,
        identifier: "Token",
        iterable: ExpressionNode
    ) -> None:
        """
        Nodo para vectores implícitos (generados por una expresión iterable).
        """
        super().__init__()
        self.expression = expression
        self.identifier = IdentifierNode(identifier)  # Siempre un IdentifierNode
        self.iterable = iterable


class TypeOperationNode(ExpressionNode):
    """
    Clase base para operaciones relacionadas con tipos (AS, IS, etc.).
    """

    def __init__(self, expression: ExpressionNode, identifier: "Token") -> None:
        super().__init__()
        self.expression = expression
        self.identifier = IdentifierNode(identifier)  # Siempre un IdentifierNode


class IsNode(TypeOperationNode):
    """
    Nodo para la operación 'is' (verificar si un objeto es de un tipo específico).
    """
    pass


class AsNode(TypeOperationNode):
    """
    Nodo para la operación 'as' (convertir un objeto a un tipo específico).
    """
    pass


# endregion


# region Call Nodes
# ░█████╗░░█████╗░██╗░░░░░██╗░░░░░░██████╗
# ██╔══██╗██╔══██╗██║░░░░░██║░░░░░██╔════╝
# ██║░░╚═╝███████║██║░░░░░██║░░░░░╚█████╗░
# ██║░░██╗██╔══██║██║░░░░░██║░░░░░░╚═══██╗
# ╚█████╔╝██║░░██║███████╗███████╗██████╔╝
# ░╚════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚═════╝░
class CallNode(ExpressionNode):
    def __init__(self, identifier: "Token", arguments: List[ExpressionNode]) -> None:
        """
        Nodo base para llamadas (funciones o métodos).
        """
        super().__init__()
        self.identifier = IdentifierNode(identifier)  # Siempre un IdentifierNode
        self.arguments = arguments  # Lista de nodos de expresión como argumentos


class FunctionCallNode(CallNode):
    """
    Nodo para llamadas a funciones (sin modificaciones respecto a CallNode).
    """
    pass


class MethodCallNode(CallNode):
    def __init__(
        self,
        type_identifier: "Token",
        identifier: "Token",
        arguments: List[ExpressionNode],
    ) -> None:
        """
        Nodo para llamadas a métodos, incluyendo un tipo explícito.
        """
        super().__init__(identifier, arguments)
        self.type_identifier = IdentifierNode(
            type_identifier)  # Siempre un IdentifierNode
        

class MemberAccessNode:
    """
        Nodo para acceso de atributos
    """

    def __init__(
        self,
        arguments: List[ExpressionNode],
    ) -> None:
        self.arguments = arguments
  
# endregion

# region String Operations Nodes
# ░█████╗░░█████╗░███╗░░██╗░█████╗░░█████╗░████████╗███████╗███╗░░██╗░█████╗░████████╗██╗░█████╗░███╗░░██╗
# ██╔══██╗██╔══██╗████╗░██║██╔══██╗██╔══██╗╚══██╔══╝██╔════╝████╗░██║██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║
# ██║░░╚═╝██║░░██║██╔██╗██║██║░░╚═╝███████║░░░██║░░░█████╗░░██╔██╗██║███████║░░░██║░░░██║██║░░██║██╔██╗██║
# ██║░░██╗██║░░██║██║╚████║██║░░██╗██╔══██║░░░██║░░░██╔══╝░░██║╚████║██╔══██║░░░██║░░░██║██║░░██║██║╚████║
# ╚█████╔╝╚█████╔╝██║░╚███║╚█████╔╝██║░░██║░░░██║░░░███████╗██║░╚███║██║░░██║░░░██║░░░██║╚█████╔╝██║░╚███║
# ░╚════╝░░╚════╝░╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚══╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝


class BinaryStringOperationNode(BinaryNode):
    """
    Clase base para operaciones binarias específicas con cadenas.
    """

    def __init__(self, left: ExpressionNode, right: ExpressionNode) -> None:
        super().__init__(left, right)


class StringConcatNode(BinaryStringOperationNode):
    pass


class StringConcatSpaceNode(BinaryStringOperationNode):
    pass

# endregion

# region Loops Nodes
# ██╗░░░░░░█████╗░░█████╗░██████╗░░██████╗
# ██║░░░░░██╔══██╗██╔══██╗██╔══██╗██╔════╝
# ██║░░░░░██║░░██║██║░░██║██████╔╝╚█████╗░
# ██║░░░░░██║░░██║██║░░██║██╔═══╝░░╚═══██╗
# ███████╗╚█████╔╝╚█████╔╝██║░░░░░██████╔╝
# ╚══════╝░╚════╝░░╚════╝░╚═╝░░░░░╚═════╝░


class LoopNode(ExpressionNode):
    def __init__(self, body: Union[ExpressionNode, BlockNode]) -> None:
        """
        Nodo base para estructuras de bucle.
        """
        super().__init__()
        self.body = body


class WhileNode(LoopNode):
    def __init__(self, condition: ExpressionNode,
                 body: Union[ExpressionNode, BlockNode]) -> None:
        """
        Nodo para bucles tipo 'while'.
        """
        super().__init__(body)
        self.condition = condition  # Condición para la ejecución del bucle


class ForNode(LoopNode):
    def __init__(self, identifier: Token, iterable: ExpressionNode,
                 body: Union[ExpressionNode, BlockNode]) -> None:
        """
        Nodo para bucles tipo 'for'.
        """
        super().__init__(body)
        self.identifier = IdentifierNode(identifier)  # Siempre un IdentifierNode
        self.iterable = iterable  # Expresión que genera los elementos a iterar


# endregion


# region Assignment Nodes
# ░█████╗░░██████╗░██████╗██╗░██████╗░███╗░░██╗███╗░░░███╗███████╗███╗░░██╗████████╗░██████╗
# ██╔══██╗██╔════╝██╔════╝██║██╔════╝░████╗░██║████╗░████║██╔════╝████╗░██║╚══██╔══╝██╔════╝
# ███████║╚█████╗░╚█████╗░██║██║░░██╗░██╔██╗██║██╔████╔██║█████╗░░██╔██╗██║░░░██║░░░╚█████╗░
# ██╔══██║░╚═══██╗░╚═══██╗██║██║░░╚██╗██║╚████║██║╚██╔╝██║██╔══╝░░██║╚████║░░░██║░░░░╚═══██╗
# ██║░░██║██████╔╝██████╔╝██║╚██████╔╝██║░╚███║██║░╚═╝░██║███████╗██║░╚███║░░░██║░░░██████╔╝
# ╚═╝░░╚═╝╚═════╝░╚═════╝░╚═╝░╚═════╝░╚═╝░░╚══╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░╚═════╝░

class BindingNode(ExpressionNode):
    def __init__(self, identifier: Token, expression: ExpressionNode) -> None:
        """
        Nodo de binding que une un identificador con una expresión.
        """
        super().__init__()
        # Se garantiza que siempre sea un IdentifierNode
        self.identifier = IdentifierNode(identifier)
        self.expression = expression  # Se espera que ya sea un ExpressionNode


class AssignmentNode(BindingNode):
    def __init__(
            self,
            identifier: Token,
            type_annotation: Token,
            expression: ExpressionNode) -> None:
        """
        Nodo de asignación con anotación de tipo.
        """
        super().__init__(identifier, expression)
        # Se garantiza que siempre sea un IdentifierNode
        self.type_annotation = IdentifierNode(type_annotation)


class DassignmentNode(BindingNode):
    pass


# endregion

# region Control Flow Nodes
# ░█████╗░░█████╗░███╗░░██╗██████╗░██╗████████╗██╗░█████╗░███╗░░██╗░█████╗░██╗░░░░░
# ██╔══██╗██╔══██╗████╗░██║██╔══██╗██║╚══██╔══╝██║██╔══██╗████╗░██║██╔══██╗██║░░░░░
# ██║░░╚═╝██║░░██║██╔██╗██║██║░░██║██║░░░██║░░░██║██║░░██║██╔██╗██║███████║██║░░░░░
# ██║░░██╗██║░░██║██║╚████║██║░░██║██║░░░██║░░░██║██║░░██║██║╚████║██╔══██║██║░░░░░
# ╚█████╔╝╚█████╔╝██║░╚███║██████╔╝██║░░░██║░░░██║╚█████╔╝██║░╚███║██║░░██║███████╗
# ░╚════╝░░╚════╝░╚═╝░░╚══╝╚═════╝░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═╝░░╚═╝╚══════╝


class ConditionalNode(ExpressionNode):
    def __init__(self,
                 condition: Optional[BooleanNode],
                 body: Union[ExpressionNode,
                             BlockNode]) -> None:
        super().__init__()
        self.condition = condition
        self.body = body


class IfNode(ConditionalNode):
    def __init__(self,
                 condition: BooleanNode,
                 body: Union[ExpressionNode,
                             BlockNode],
                 elif_nodes: List["ElifNode"] = None,
                 else_body: "ElseNode" = None) -> None:
        super().__init__(condition, body)
        self.elif_nodes = elif_nodes or []
        self.else_body = else_body


class ElifNode(ConditionalNode):
    pass


class ElseNode(ConditionalNode):
    def __init__(self, body: Union[ExpressionNode, BlockNode]) -> None:
        super().__init__(None, body)


# endregion

# region Arithmetic Operators Nodes
# ░█████╗░██████╗░██╗████████╗██╗░░██╗███╗░░░███╗███████╗████████╗██╗░█████╗░
# ██╔══██╗██╔══██╗██║╚══██╔══╝██║░░██║████╗░████║██╔════╝╚══██╔══╝██║██╔══██╗
# ███████║██████╔╝██║░░░██║░░░███████║██╔████╔██║█████╗░░░░░██║░░░██║██║░░╚═╝
# ██╔══██║██╔══██╗██║░░░██║░░░██╔══██║██║╚██╔╝██║██╔══╝░░░░░██║░░░██║██║░░██╗
# ██║░░██║██║░░██║██║░░░██║░░░██║░░██║██║░╚═╝░██║███████╗░░░██║░░░██║╚█████╔╝
# ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝░░░╚═╝░░░╚═╝░╚════╝░


class ArithmeticOperationNode(BinaryNode):
    def __init__(self, left: "ArithmeticOperationNode",
                 right: "ArithmeticOperationNode") -> None:
        super().__init__(left, right, )


class PlusNode(ArithmeticOperationNode):
    pass


class ModNode(ArithmeticOperationNode):
    pass


class MinusNode(ArithmeticOperationNode):
    pass


class MultiplyNode(ArithmeticOperationNode):
    pass


class DivideNode(ArithmeticOperationNode):
    pass


class PowerNode(ArithmeticOperationNode):
    pass


class NegativeNode(UnaryNode):
    def __init__(
            self,
            expression: "ArithmeticOperationNode",
            ntype: str = "NEGATIVE") -> None:
        super().__init__(expression, ntype)
# endregion

# region Logical Operators Nodes
# ██████╗░░█████╗░░█████╗░██╗░░░░░███████╗░█████╗░███╗░░██╗
# ██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔════╝██╔══██╗████╗░██║
# ██████╦╝██║░░██║██║░░██║██║░░░░░█████╗░░███████║██╔██╗██║
# ██╔══██╗██║░░██║██║░░██║██║░░░░░██╔══╝░░██╔══██║██║╚████║
# ██████╦╝╚█████╔╝╚█████╔╝███████╗███████╗██║░░██║██║░╚███║
# ╚═════╝░░╚════╝░░╚════╝░╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝


class BooleanNode(BinaryNode):
    """
    Nodo base para cualquier operación booleana, relacional o de igualdad.
    """

    def __init__(self, left: "ExpressionNode", right: "ExpressionNode") -> None:
        super().__init__(left, right)


class BooleanOperationNode(BinaryNode):
    def __init__(self, left: "BooleanNode", right: "BooleanNode") -> None:
        super().__init__(left, right)


class RelationalOperationNode(BooleanNode):
    """
    Nodo para operaciones relacionales (<, <=, >, >=) que operan sobre ArithmeticOperationNodes.
    """

    def __init__(self, left: "ArithmeticOperationNode",
                 right: "ArithmeticOperationNode") -> None:
        super().__init__(left, right)


class EqualityOperationNode(BooleanNode):
    """
    Nodo para operaciones de igualdad (==, !=) que operan sobre ArithmeticOperationNodes.
    """

    def __init__(self, left: "ArithmeticOperationNode",
                 right: "ArithmeticOperationNode") -> None:
        super().__init__(left, right)


class OrNode(BooleanOperationNode):
    pass


class AndNode(BooleanOperationNode):
    pass


class NotNode(UnaryNode):
    def __init__(self, expression: "BooleanNode") -> None:
        super().__init__(expression)


class LessThanNode(RelationalOperationNode):
    pass


class GreaterThanNode(RelationalOperationNode):
    pass


class LessEqualNode(RelationalOperationNode):
    pass


class GreaterEqualNode(RelationalOperationNode):
    pass


class EqualNode(EqualityOperationNode):
    pass


class NotEqualNode(EqualityOperationNode):
    pass

# endregion
# region Atomic Nodes
# ██████╗░██████╗░██╗███╗░░░███╗██╗████████╗██╗██╗░░░██╗███████╗░██████╗
# ██╔══██╗██╔══██╗██║████╗░████║██║╚══██╔══╝██║██║░░░██║██╔════╝██╔════╝
# ██████╔╝██████╔╝██║██╔████╔██║██║░░░██║░░░██║╚██╗░██╔╝█████╗░░╚█████╗░
# ██╔═══╝░██╔══██╗██║██║╚██╔╝██║██║░░░██║░░░██║░╚████╔╝░██╔══╝░░░╚═══██╗
# ██║░░░░░██║░░██║██║██║░╚═╝░██║██║░░░██║░░░██║░░╚██╔╝░░███████╗██████╔╝
# ╚═╝░░░░░╚═╝░░╚═╝╚═╝╚═╝░░░░░╚═╝╚═╝░░░╚═╝░░░╚═╝░░░╚═╝░░░╚══════╝╚═════╝░


class AtomicNode(ExpressionNode):
    def __init__(self, token) -> None:
        super().__init__()
        self.lex = token.lex
        self.line = token.line
        self.column = token.column


class BooleanNode(AtomicNode):
    pass


class NumberNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass


class IdentifierNode(AtomicNode):
    pass
