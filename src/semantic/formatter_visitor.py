from cmp.hulk_ast import *
import cmp.visitor as visitor


def analyze_type(obj: Any) -> str:
    """
    Función que intenta inferir el tipo de una variable de forma profunda y detallada,
    incluyendo tipos complejos como List[Tuple[Clase, int]].
    """
    # Si es una lista, analizamos los tipos de los elementos
    if isinstance(obj, list):
        if len(obj) == 0:
            return "List[Empty]"  # Caso donde la lista está vacía
        
        # Analizamos el tipo de los elementos de la lista
        element_types = {analyze_type(item) for item in obj}
        return f"List[{ ' | '.join(sorted(element_types)) }]"

    # Si es un diccionario, analizamos los tipos de las claves y los valores
    elif isinstance(obj, dict):
        if len(obj) == 0:
            return "Dict[Empty, Empty]"  # Diccionario vacío
        
        # Analizamos los tipos de las claves y valores
        types = set()
        for key, value in obj.items():
            key_type = analyze_type(key)
            value_type = analyze_type(value)
            types.add(f"{key_type}: {value_type}")
        
        # Unimos las combinaciones de tipo de claves y valores
        types_union = ' | '.join(sorted(types))
        return f"Dict[{types_union}]"

    # Si es una tupla, analizamos los tipos de los elementos
    elif isinstance(obj, tuple):
        if len(obj) == 0:
            return "Tuple[Empty]"
        
        # Analizamos los tipos de los elementos de la tupla
        element_types = {analyze_type(item) for item in obj}
        return f"Tuple[{', '.join(sorted(element_types))}]"

    # Si es una instancia de una clase, devolvemos el nombre de la clase
    elif isinstance(obj, type):
        return obj.__name__

    # Si es un tipo primitivo, devolvemos el tipo directamente
    return type(obj).__name__






class TreeFormatter(object):
    def __init__(self):
        self.indentation_unit = "   "  # Unidad de indentación (3 espacios)
        self.vertical_connector = "│"  # Conector vertical
        self.branch_connector = "├──"  # Conector para nodos intermedios
        self.last_connector = "└──"  # Conector para el último nodo
        self.indent_prefix = self.vertical_connector + self.indentation_unit  # Prefijo de indentación + conector vertical
    
   
    def _connector(self, is_last: bool):
        """Devuelve el conector correspondiente para el nodo."""
        return self.last_connector if is_last else self.branch_connector
    
    def _format_node_line(self, node_label, depth, is_last=False):
        """Genera una línea formateada para un nodo, considerando si es el último hijo o no."""
        connector = self._connector(is_last)
        return f"{self.indent_prefix * depth}{connector} {node_label}\n"
    
    def _format_label(self, label: str, contained_var: Any, depth: int, is_last: bool) -> str:
        """Genera una línea formateada con parametros del nodo."""
        connector = self._connector(is_last)
        return f"{self.indent_prefix * depth}{connector} {label} -> Type: {analyze_type(contained_var)}\n"
        
    
    def _format_value(self, value: Any, depth: int, is_last: bool) -> str:
        """Genera una línea formateada con el valor del nodo."""
        connector = self._connector(is_last)
        return f"{self.indent_prefix * depth}{connector} Value:{value}\n"
    
    def _format_param(self, param: Tuple[str, str], depth: int, is_last: bool) -> str:
        """Genera una línea formateada con el valor del parámetro."""
        connector = self._connector(is_last)
        return  f"{self.indent_prefix * depth}{connector} Param: {param[0]} -> Type: {param[1]}\n"
        
    def _format_params(self,params, depth: int, is_last: bool) -> str:
        """Genera una línea formateada con los valores de los parámetros."""
        
        params_label = self._format_label("Params",params,depth)
        params_values = ''.join(self._format_param(param,depth+1,is_last=(i == len(params) - 1))
                                for i, param in enumerate(params))
        return  params_label + params_values

    def _format_identifier(self, identifier: str, depth: int, is_last: bool) -> str:
        """Genera una línea formateada con el valor del identificador."""
        identifier_label = self._format_label("Identifier",identifier,depth)
        identifier_value = self._format_value(identifier,depth+1,is_last)

    @visitor.on('node')
    def visit(self, node, depth):
        """Método genérico para visitar cualquier nodo."""
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, depth=0,is_last=False):
        """Método para visitar un nodo de tipo ProgramNode."""
        # Formatear la línea del nodo principal
        formatted_line = self._format_node_line(node.ntype,depth,True)
        
        # Visitar las declaraciones dentro del nodo de tipo ProgramNode
        type_lines = ''.join(self.visit(statement_type, depth + 1, is_last=(i == len(node.statements_type) - 1)) 
                                for i, statement_type in enumerate(node.statements_type))
        protocol_lines = ''.join(self.visit(statement_protocol, depth + 1, is_last=(i == len(node.statements_protocol) - 1)) 
                                    for i, statement_protocol in enumerate(node.statements_protocol))
        function_lines = ''.join(self.visit(statement_func, depth + 1, is_last=(i == len(node.statements_func) - 1)) 
                                    for i, statement_func in enumerate(node.statements_func))
        
        expression_lines = self.visit(node.expression, depth + 1, is_last=True)  # La expresión suele ser el último hijo

        # Concatenar todas las líneas generadas
        return formatted_line + type_lines + protocol_lines + function_lines + expression_lines
    TypeNode()
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, depth=0,is_last=False):
        formatted_line = self._format_node_line(node.ntype,depth,is_last)
        identifier_line = self._format_identifier(node.identifier,depth+1)
        params_lines = self._format_params(node.params,depth+1)
        super_type_line = self._format_label("Super Type",node.super_type,depth,is_last)
        super_type_args
        attribute_lines = ''.join(self.visit(attribute, depth + 1, is_last=(i == len(node.attributes) - 1)) 
                                    for i, attribute in enumerate(node.attributes))
        
        method_lines = ''.join(self.visit(method, depth + 1, is_last=(i == len(node.methods) - 1)) 
                                    for i, method in enumerate(node.methods))
        
        return formatted_line + identifier_line + params_lines + attribute_lines + method_lines
    def visit(self, node:ProgramNode, tabs=0):
        pass

    @visitor.when(StatementNode)
    def visit(self, node:StatementNode, tabs=0):
        pass

    @visitor.when(CallableNode)
    def visit(self, node:StatementNode, tabs=0):
        pass
    
    @visitor.when(ExtendableNode)
    def visit(self, node:ExtendableNode, tabs=0):
        pass
    
    @visitor.when(ExpressionNode)
    def visit(self, node:ExpressionNode, tabs=0):
        pass
    @visitor.when(TypeNode)
    def visit(self, node:TypeNode, tabs=0):
        pass
    @visitor.when(ProtocolNode)
    def visit(self, node:ProtocolNode, tabs=0):
        pass
    @visitor.when(FuncNode)
    def visit(self, node:FuncNode, tabs=0):
        pass
    @visitor.when(AtomicNode)
    def visit(self, node:AtomicNode, tabs=0):
        pass
    @visitor.when(BinaryNode)
    def visit(self, node:BinaryNode, tabs=0):
        pass
    @visitor.when(UnaryNode)
    def visit(self, node:UnaryNode, tabs=0):
        pass
    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode, tabs=0):
        pass
    @visitor.when(LoopNode)
    def visit(self, node:LoopNode, tabs=0):
        pass
    @visitor.when(BlockNode)
    def visit(self, node:BlockNode, tabs=0):
        pass
    @visitor.when(TypeInstanceNode)
    def visit(self, node:TypeInstanceNode, tabs=0):
        pass
    @visitor.when(AsNode)
    def visit(self, node:AsNode, tabs=0):
        pass
    @visitor.when(CallNode)
    def visit(self, node:CallNode, tabs=0):
        pass
    @visitor.when(LetNode)
    def visit(self, node:LetNode, tabs=0):
        pass
    @visitor.when(VectorIndexNode)
    def visit(self, node:VectorIndexNode, tabs=0):
        pass
    @visitor.when(IsNode)
    def visit(self, node:IsNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass
    @visitor.when(BindingNode)
    def visit(self, node:BindingNode, tabs=0):
        pass