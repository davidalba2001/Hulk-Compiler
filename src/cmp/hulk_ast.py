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
            │                   │                       └── IdNode
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
from cmp.utils import Token
from typing import List, Optional, Union, Tuple, Dict, Any, str
from __future__ import annotations


class Node:
    def __init__(
        self,
        token: Optional[Token] = None,
        ntype: str = "NODE"
    ) -> None:

        # Un token opcional con información del análisis léxico (lexer).
        self.token: Optional[Token] = token,
        self.ntype: str = ntype  # El tipo de nodo


class ProgramNode(Node):
    def __init__(
        self,
        statements_type: List[TypeNode],
        statements_protocol: List[ProtocolNode],
        statements_func: List[FuncNode],
        main_expression: Union[ExpressionNode, BlockNode],
        token: Optional[Token] = None,
        ntype: str = "PROGRAM"
    ) -> None:

        super().__init__(token, ntype)

        # Inicialización de declaraciones (statements)
        self.statements_type: List[TypeNode] = statements_type  # Lista de tipos
        self.statements_func: List[FuncNode] = statements_func  # Lista de funciones
        # Lista de protocolos
        self.statements_protocol: List[ProtocolNode] = statements_protocol

        # Expresión principal (puede ser única o un bloque)
        self.main_expression: Union[ExpressionNode, BlockNode] = main_expression


class StatementNode(Node):
    def __init__(
        self,
        token: Optional[Token] = None,
        ntype: str = "STATEMENT"
    ) -> None:

        super().__init__(token, ntype)


# Nodo invocable, como una función o método
class CallableNode(StatementNode):
    def __init__(
        self,
        identifier: str,
        params: Dict[str, str],
        return_type_annotation: str,
        body: Union[ExpressionNode, BlockNode],
        token: Optional[Token] = None,
        ntype: str = "CALLABLE"
    ) -> None:
        # Inicialización de la clase base StatementNode con el token y el tipo de nodo.
        super().__init__(token, ntype)

        # Asignación de las propiedades del nodo con anotaciones de tipo explícitas.
        self.identifier: str = identifier  # Nombre de la función o método.
        self.params: Dict[str, str] = params  # Parámetros con sus tipos.
        # Anotación del tipo de retorno de la función o método.
        self.return_type_annotation: str = return_type_annotation
        # El cuerpo de la función o método
        self.body: Union[ExpressionNode, BlockNode] = body


# TODO: Verificar si se puede mejorar
class ExtendableNode(StatementNode):
    def __init__(
        self,
        identifier: str,
        token: Optional[Token] = None,
        ntype: str = "EXTENDABLE"
    ) -> None:

        super().__init__(token, ntype)
        self.identifier: str = identifier


class ExpressionNode(Node):
    def __init__(
        self,
        token: Optional[Token] = None,
        ntype: str = "EXPRESSION"
    ) -> None:

        super().__init__(token, ntype)


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
    def __init__(
        self,
        identifier: str,
        params: Dict[str, str],
        super_type: str,
        body: Tuple[List[AssignmentNode], List[AssignmentNode]],
        token: Optional[Token] = None,
        ntype: str = "TYPE"
    ) -> None:

        super().__init__(identifier, token, ntype)
        self.params: Dict[str, str] = params  # Lista de parametros
        self.super_type: str = super_type[0]  # Tipo del padre
        # Argumentos del tipo del padre
        self.super_type_args: List[ExpressionNode] = super_type[1]
        self.attributes: List[AssignmentNode] = body[0]  # Atributos del tipo
        self.methods: List[AssignmentNode] = body[1]  # Metodos del tipo


class ProtocolNode(ExtendableNode):
    def __init__(
        self,
        identifier: str,
        super_protocol: str,
        body: List[MethodNode],
        token: Optional[Token] = None,
        ntype: str = "PROTOCOL"
    ) -> None:

        super().__init__(identifier, token, ntype)
        self.super_protocol: str = super_protocol
        self.body: List[MethodNode] = body


class FuncNode(CallableNode):
    def __init__(
        self,
        identifier: str,
        params: Dict[str, str],
        type_annotation: str,
        body: Union[ExpressionNode, BlockNode],
        token: Optional[Token] = None,
        ntype: str = "FUNCTION"
    ) -> None:

        super().__init__(self, identifier, params, type_annotation, body, token, ntype)


class MethodNode(CallableNode):
    def __init__(
        self,
        identifier: str,
        params: Dict[str, str],
        type_annotation: str,
        body: Union[ExpressionNode, BlockNode],
        token: Optional[Token] = None,
        ntype: str = "FUNCTION"
    ) -> None:

        super().__init__(self, identifier, params, type_annotation, body, token, ntype)

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


class BinaryNode(ExpressionNode):
    def __init__(
        self,
        left: Any,
        right: Any,
        token: Optional[Token] = None,
        ntype: str = "BINARY"
    ) -> None:

        super().__init__(token, ntype)
        self.left: Any = left  # Expressions left
        self.right: Any = right  # Expressions right


class UnaryNode(ExpressionNode):
    def __init__(
        self,
        expression: Any,
        token: Optional[Token] = None,
        ntype: str = "UNARY"
    ) -> None:

        super().__init__(token, ntype)
        self.expression: Any = expression  # Expression


class BlockNode(ExpressionNode):
    def __init__(
        self,
        expressions: List[ExpressionNode],
        token: Optional[Token] = None,
        ntype: str = "BLOCK"
    ) -> None:

        super().__init__(token, ntype)
        self.expressions: List[ExpressionNode] = expressions  # List of expressions

# TODO ACLARAR bien que otros tipos puede ser binding


class LetNode(ExpressionNode):
    def __init__(
        self,
        bindings: List[AssignmentNode],
        body: Union[ExpressionNode, BlockNode],
        token: Optional[Token] = None,
        ntype: str = "LET"
    ) -> None:

        super().__init__(token, ntype)
        self.bindings: List[AssignmentNode] = bindings  # List of bindings
        self.body: Union[ExpressionNode, BlockNode] = body  # Body


class VectorIndexNode(ExpressionNode):
    def __init__(
        self,
        identifier: str,
        index: str,
        token: Optional[Token] = None,
        ntype: str = "VECTOR_INDEX"
    ) -> None:

        super().__init__(token, ntype)

        self.identifier: str = identifier  # Asignación del identificador.
        try:
            self.index: int = int(index)  # Conversión del índice a entero.
        except ValueError:
            raise ValueError(
                f"El índice debe ser un número entero, recibido: '{index}'")


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
    def __init__(
        self,
        token: Optional[Token] = None,
        ntype: str = "TYPE_INSTANCE"
    ) -> None:

        super().__init__(token, ntype)


class TypeOperationNode(ExpressionNode):
    """
    Clase base para operaciones relacionadas con tipos (AS, IS, etc.).
    """

    def __init__(
        self,
        expression: ExpressionNode,
        identifier: IdNode,
        token: Optional[Token] = None,
        ntype: str = "IS"
    ) -> None:
        super().__init__(identifier, expression, token, ntype)


class IsNode(TypeOperationNode):
    def __init__(
        self,
        expression: ExpressionNode,
        identifier: IdNode,
        token: Optional[Token] = None,
        ntype: str = "IS"
    ) -> None:
        super().__init__(identifier, expression, token, ntype)


class AsNode(TypeOperationNode):
    def __init__(
        self,
        expression: ExpressionNode,
        identifier: IdNode,
        token: Optional[Token] = None,
        ntype: str = "AS"
    ) -> None:

        super().__init__(expression, identifier, token, ntype)


class InstanceNode(TypeInstanceNode):
    def __init__(
        self,
        identifier: str,
        arguments: List[ExpressionNode],
        token: List[Token] = None,
        ntype: str = "INSTANCE"
    ) -> None:

        super().__init__(token, ntype)
        self.identifier: str = identifier  # Identificador
        self.arguments: List[ExpressionNode] = arguments  # Lista de Argumentos


class ExplicitVectorNode(TypeInstanceNode):
    def __init__(
        self,
        arguments: List[ExpressionNode],
        token: List[Token] = None,
        ntype: str = "EXPLICIT_VECTOR"
    ) -> None:

        super().__init__(token, ntype)
        self.arguments: List[ExpressionNode] = arguments  # Lista de argumentos


class ImplicitVectorNode(TypeInstanceNode):
    def __init__(
        self,
        expression: ExpressionNode,
        identifier: str,
        iterable: ExpressionNode,
        token: List[Token] = None,
        ntype: str = "IMPLICIT_VECTOR"
    ) -> None:

        super().__init__(token, ntype)
        self.expression: ExpressionNode = expression  # Expression
        self.identifier: str = identifier  # Identificador
        self.iterable: ExpressionNode = iterable  # Una expression que devuelve un iterable
# endregion


# region Call Nodes
# ░█████╗░░█████╗░██╗░░░░░██╗░░░░░░██████╗
# ██╔══██╗██╔══██╗██║░░░░░██║░░░░░██╔════╝
# ██║░░╚═╝███████║██║░░░░░██║░░░░░╚█████╗░
# ██║░░██╗██╔══██║██║░░░░░██║░░░░░░╚═══██╗
# ╚█████╔╝██║░░██║███████╗███████╗██████╔╝
# ░╚════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚═════╝░


class CallNode(ExpressionNode):
    def __init__(
        self,
        identifier: str,
        arguments: List[ExpressionNode],
        token: Optional[Token] = None,
        ntype: str = "CALL"
    ) -> None:

        super().__init__(token, ntype)
        self.identifier = identifier
        self.arguments = arguments


class FunctionCallNode(CallNode):
    def __init__(
        self,
        identifier: str,
        arguments: List[ExpressionNode],
        token: Optional[Token] = None,
        ntype: str = "FUNCTION_CALL"
    ) -> None:

        super().__init__(identifier, arguments, token, ntype)


class MethodCallNode(CallNode):
    def __init__(
        self,
        type_identifier: str,
        identifier: str,
        arguments: List[ExpressionNode],
        token: Optional[Token] = None,
        ntype: str = "METHOD_CALL"
    ) -> None:

        super().__init__(identifier, arguments, token, ntype)
        self.type_identifier: str = type_identifier
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

    def __init__(
        self,
        left: ExpressionNode,
        right: ExpressionNode,
        token: Optional[Token] = None,
        ntype: str = "BINARY_STRING_OPERATION"
    ) -> None:
        super().__init__(left, right, token, ntype)


class StringConcatNode(BinaryStringOperationNode):
    def __init__(
        self,
        left: ExpressionNode,
        right: ExpressionNode,
        token: Optional[Token] = None,
        ntype: str = "STRING_CONCAT"
    ) -> None:

        super().__init__(left, right, token, ntype)


class StringConcatSpaceNode(BinaryStringOperationNode):
    def __init__(
        self,
        left: ExpressionNode,
        right: ExpressionNode,
        token: Optional[Token] = None,
        ntype: str = "STRING_CONCAT_SPACE"
    ) -> None:

        super().__init__(left, right, token, ntype)
# endregion

# region Loops Nodes
# ██╗░░░░░░█████╗░░█████╗░██████╗░░██████╗
# ██║░░░░░██╔══██╗██╔══██╗██╔══██╗██╔════╝
# ██║░░░░░██║░░██║██║░░██║██████╔╝╚█████╗░
# ██║░░░░░██║░░██║██║░░██║██╔═══╝░░╚═══██╗
# ███████╗╚█████╔╝╚█████╔╝██║░░░░░██████╔╝
# ╚══════╝░╚════╝░░╚════╝░╚═╝░░░░░╚═════╝░


class LoopNode(ExpressionNode):
    def __init__(
        self,
        body: Union[ExpressionNode, BlockNode],
        token=None, ntype="LOOP"
    ) -> None:

        super().__init__(token, ntype)
        self.body: Union[ExpressionNode, BlockNode] = body

# TODO:Se puede refinar anadiendo mas capas en los nodos de expressiones
# como la booleana


class WhileNode(LoopNode):
    def __init__(

        self,
        condition: ExpressionNode,
        body: Union[ExpressionNode, BlockNode],
        token: Optional[Token] = None,
        ntype="WHILE"
    ) -> None:

        super().__init__(body, token, ntype)
        self.condition: ExpressionNode = condition


class ForNode(LoopNode):
    def __init__(
        self,
        identifier: str,
        iterable: ExpressionNode,
        body: Union[ExpressionNode, BlockNode],
        token: Optional[Token] = None,
        ntype: str = "FOR"
    ) -> None:

        super().__init__(body, token, ntype)
        self.identifier: str = identifier
        self.iterable: ExpressionNode = iterable
# endregion

# region Assignment Nodes
# ░█████╗░░██████╗░██████╗██╗░██████╗░███╗░░██╗███╗░░░███╗███████╗███╗░░██╗████████╗░██████╗
# ██╔══██╗██╔════╝██╔════╝██║██╔════╝░████╗░██║████╗░████║██╔════╝████╗░██║╚══██╔══╝██╔════╝
# ███████║╚█████╗░╚█████╗░██║██║░░██╗░██╔██╗██║██╔████╔██║█████╗░░██╔██╗██║░░░██║░░░╚█████╗░
# ██╔══██║░╚═══██╗░╚═══██╗██║██║░░╚██╗██║╚████║██║╚██╔╝██║██╔══╝░░██║╚████║░░░██║░░░░╚═══██╗
# ██║░░██║██████╔╝██████╔╝██║╚██████╔╝██║░╚███║██║░╚═╝░██║███████╗██║░╚███║░░░██║░░░██████╔╝
# ╚═╝░░╚═╝╚═════╝░╚═════╝░╚═╝░╚═════╝░╚═╝░░╚══╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░╚═════╝░


class BindingNode(ExpressionNode):
    def __init__(
        self,
        identifier: str,
        expression: ExpressionNode,
        token: Optional[Token] = None,
        ntype: str = "BINDING"
    ) -> None:

        super().__init__(token, ntype)
        self.identifier: str = identifier
        self.expression: ExpressionNode = expression


class AssignmentNode(BindingNode):
    def __init__(
        self, identifier: str,
        type_annotation: str,
        expression: ExpressionNode,
        token: Optional[Token] = None,
        ntype="ASSIGNMENT"
    ) -> None:

        super().__init__(identifier, expression, token, ntype)
        self.type_annotation: ExpressionNode = type_annotation


class DassignmentNode(BindingNode):
    def __init__(
        self, identifier: str,
        expression: ExpressionNode,
        token: Optional[Token] = None,
        ntype: str = "DASSIGNMENT"
    ) -> None:

        super().__init__(identifier, expression, token, ntype)

# endregion

# region Control Flow Nodes
# ░█████╗░░█████╗░███╗░░██╗██████╗░██╗████████╗██╗░█████╗░███╗░░██╗░█████╗░██╗░░░░░
# ██╔══██╗██╔══██╗████╗░██║██╔══██╗██║╚══██╔══╝██║██╔══██╗████╗░██║██╔══██╗██║░░░░░
# ██║░░╚═╝██║░░██║██╔██╗██║██║░░██║██║░░░██║░░░██║██║░░██║██╔██╗██║███████║██║░░░░░
# ██║░░██╗██║░░██║██║╚████║██║░░██║██║░░░██║░░░██║██║░░██║██║╚████║██╔══██║██║░░░░░
# ╚█████╔╝╚█████╔╝██║░╚███║██████╔╝██║░░░██║░░░██║╚█████╔╝██║░╚███║██║░░██║███████╗
# ░╚════╝░░╚════╝░╚═╝░░╚══╝╚═════╝░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═╝░░╚═╝╚══════╝


class ConditionalNode(ExpressionNode):
    def __init__(
        self,
        body: Union[ExpressionNode, BlockNode],
        token: Optional[Token] = None,
        ntype: str = "CONDITIONAL"
    ) -> None:
        super().__init__(token, ntype)
        self.body: Union[ExpressionNode, BlockNode] = body


class IfNode(ConditionalNode):
    def __init__(
        self,
        if_condition: ExpressionNode,
        if_body: Union[ExpressionNode, BlockNode],
        elif_nodes: List[ElifNode] = None,
        else_body: ElseNode = None,
        token: Optional[Token] = None,
        ntype: str = "If"
    ) -> None:

        super().__init__(if_body, token, ntype)
        self.if_condition: ExpressionNode = if_condition
        self.elif_nodes: List[ElifNode] = elif_nodes if elif_nodes else []
        self.else_body: ElseNode = else_body


class ElifNode(ConditionalNode):
    def __init__(
        self,
        condition: ExpressionNode,
        body: Union[ExpressionNode, BlockNode],
        token: Optional[Token] = None,
        ntype: str = "ELIF"
    ) -> None:

        super().__init__(body, token, ntype)
        self.condition: ExpressionNode = condition


class ElseNode(ConditionalNode):
    def __init__(
        self,
        body: Union[ExpressionNode, BlockNode],
        token: Optional[Token] = None,
        ntype: str = "ELSE"
    ) -> None:

        super().__init__(body, token, ntype)
# endregion

# region Arithmetic Operators Nodes
# ░█████╗░██████╗░██╗████████╗██╗░░██╗███╗░░░███╗███████╗████████╗██╗░█████╗░
# ██╔══██╗██╔══██╗██║╚══██╔══╝██║░░██║████╗░████║██╔════╝╚══██╔══╝██║██╔══██╗
# ███████║██████╔╝██║░░░██║░░░███████║██╔████╔██║█████╗░░░░░██║░░░██║██║░░╚═╝
# ██╔══██║██╔══██╗██║░░░██║░░░██╔══██║██║╚██╔╝██║██╔══╝░░░░░██║░░░██║██║░░██╗
# ██║░░██║██║░░██║██║░░░██║░░░██║░░██║██║░╚═╝░██║███████╗░░░██║░░░██║╚█████╔╝
# ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝░░░╚═╝░░░╚═╝░╚════╝░


class ArithmeticOperationNode(BinaryNode):
    """
    Clase base para operaciones aritméticas (+, -, *, /, %, ^, etc.).
    """

    def __init__(
            self,
            left: ExpressionNode,
            right: ExpressionNode,
            token=None,
            ntype="ARITHMETIC_OPERATION"):
        super().__init__(left, right, token, ntype)


class PlusNode(ArithmeticOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="PLUS"):
        super().__init__(left, right, token, ntype)


class ModNode(ArithmeticOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="MOD"):
        super().__init__(left, right, token, ntype)


class MinusNode(ArithmeticOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="MINUS"):
        super().__init__(left, right, token, ntype)


class MultiplyNode(ArithmeticOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="MULTIPLY"):
        super().__init__(left, right, token, ntype)


class DivideNode(ArithmeticOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="DIVIDE"):
        super().__init__(left, right, token, ntype)


class PowerNode(ArithmeticOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="POWER"):
        super().__init__(left, right, token, ntype)
        
        
        
class NegativeNode(UnaryNode):
    def __init__(
        self,
        expression:ExpressionNode, 
        token:Optional[Token] = None, 
        ntype = "NEGATIVE"):
        super().__init__(expression, token, ntype)
    
            
# endregion

# region Logical Operators Nodes
# ██████╗░░█████╗░░█████╗░██╗░░░░░███████╗░█████╗░███╗░░██╗
# ██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔════╝██╔══██╗████╗░██║
# ██████╦╝██║░░██║██║░░██║██║░░░░░█████╗░░███████║██╔██╗██║
# ██╔══██╗██║░░██║██║░░██║██║░░░░░██╔══╝░░██╔══██║██║╚████║
# ██████╦╝╚█████╔╝╚█████╔╝███████╗███████╗██║░░██║██║░╚███║
# ╚═════╝░░╚════╝░░╚════╝░╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝


class BooleanOperationNode(BinaryNode):
    """
    Clase base para operaciones booleanas (OR, AND,etc.).
    """

    def __init__(
        self,
        left: ExpressionNode,
        right: ExpressionNode,
        token: Optional[Token] = None,
        ntype="BOOLEAN_OPERATION"
    ) -> None:

        super().__init__(left, right, token, ntype)


class RelationalOperationNode(BinaryNode):
    """
    Clase base para operaciones relacionales (<, <=, >, >=).
    """

    def __init__(
        self,
        left: ExpressionNode,
        right: ExpressionNode,
        token: Optional[Token] = None,
        ntype="RELATIONAL_OPERATION"
    ) -> None:

        super().__init__(left, right, token, ntype)


class EqualityOperationNode(BinaryNode):
    """
    Clase base para operaciones de igualdad (==, !=).
    """

    def __init__(
        self,
        left: ExpressionNode,
        right: ExpressionNode,
        token: Optional[Token] = None,
        ntype="EQUALITY_OPERATION"
    ) -> None:

        super().__init__(left, right, token, ntype)


class OrNode(BooleanOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="OR"):
        super().__init__(left, right, token, ntype)


class AndNode(BooleanOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="AND"):
        super().__init__(left, right, token, ntype)


class NotNode(BooleanOperationNode):
    def __init__(self, expression:ExpressionNode, token:Optional[Token]=None, ntype:str="NOT"):
        super().__init__(expression, token, ntype)


class LessThanNode(RelationalOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="LESS_THAN"):
        super().__init__(left, right, token, ntype)


class GreaterThanNode(RelationalOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="GREATER_THAN"):
        super().__init__(left, right, token, ntype)


class LessEqualNode(RelationalOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="LESS_EQUAL"):
        super().__init__(left, right, token, ntype)


class GreaterEqualNode(RelationalOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="GREATER_EQUAL"):
        super().__init__(left, right, token, ntype)


class EqualNode(EqualityOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="EQUAL"):
        super().__init__(left, right, token, ntype)


class NotEqualNode(EqualityOperationNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, token:Optional[Token]=None, ntype:str="NOT_EQUAL"):
        super().__init__(left, right, token, ntype)


# endregion

# region Atomic Nodes
# ██████╗░██████╗░██╗███╗░░░███╗██╗████████╗██╗██╗░░░██╗███████╗░██████╗
# ██╔══██╗██╔══██╗██║████╗░████║██║╚══██╔══╝██║██║░░░██║██╔════╝██╔════╝
# ██████╔╝██████╔╝██║██╔████╔██║██║░░░██║░░░██║╚██╗░██╔╝█████╗░░╚█████╗░
# ██╔═══╝░██╔══██╗██║██║╚██╔╝██║██║░░░██║░░░██║░╚████╔╝░██╔══╝░░░╚═══██╗
# ██║░░░░░██║░░██║██║██║░╚═╝░██║██║░░░██║░░░██║░░╚██╔╝░░███████╗██████╔╝
# ╚═╝░░░░░╚═╝░░╚═╝╚═╝╚═╝░░░░░╚═╝╚═╝░░░╚═╝░░░╚═╝░░░╚═╝░░░╚══════╝╚═════╝░


class AtomicNode(ExpressionNode):
    def __init__(self, lex: str, token:Optional[Token]=None, ntype="ATOMIC"):
        super().__init__(token, ntype)
        self.lex = lex
        self.token = token


class BooleanNode(AtomicNode):
    def __init__(self, lex: str, token:Optional[Token]=None, ntype:str="BOOLEAN"):
        super().__init__(lex, token, ntype)


class NumberNode(AtomicNode):
    def __init__(self, lex: str, token:Optional[Token]=None, ntype:str="NUMBER"):
        super().__init__(lex, token, ntype)


class StringNode(AtomicNode):
    def __init__(self, lex: str, token:Optional[Token]=None, ntype:str="STRING"):
        super().__init__(lex, token, ntype)

##########################################################################


class IdNode(AtomicNode):
    def __init__(self, lex: str, token:Optional[Token]=None, ntype:str="IDENTIFIER"):
        super().__init__(lex, token, ntype)
# endregion
