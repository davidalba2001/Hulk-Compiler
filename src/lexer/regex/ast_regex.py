import sys
import os

# Obtener la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Moverse a la raíz del proyecto
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir, os.pardir))

# Agregar la carpeta raíz del proyecto al sys.path
sys.path.append(project_root)

try:
    from cmp.automata import NFA,DFA,automata_closure,automata_concatenation,automata_union
    from cmp.ast import AtomicNode,UnaryNode,BinaryNode
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")
    

EPSILON = 'ε'

class EpsilonNode(AtomicNode):
    def evaluate(self):
        e = self.lex
        return DFA(states=1, finals=[0], transitions={})

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return NFA(states = 2,finals = [1],transitions={(0,s):[1]})

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)
        
class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue,rvalue)
    
class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue,rvalue)