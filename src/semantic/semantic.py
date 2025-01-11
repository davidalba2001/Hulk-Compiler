import itertools as itt
from collections import OrderedDict
from cmp.hulk_ast import FuncNode

class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]

class FuncInfo:
    def __init__(self, params, node: FuncNode):
        self.params = params
        self.function = node

class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class Argument:
    def __init__(self, name, typex):
        self.name = name
        self.atype: Type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Type:
    def __init__(self, name:str):
        self.name = name
        self.arguments: list[Argument] = []
        self.attributes: list[Attribute] = []
        self.methods:dict[(str,int),Method] = {}
        self.parent: Type = None
        self.arguments_parent = None

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def decget_attribute(self, name):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            
    def define_arguments(self,name,typex):
        if name not in [argument.name for argument in self.arguments]:
            self.arguments.append(Argument(name,typex))
        else: 
            raise SemanticError(f'Argument "{name}" is already defined in {self.name}.')
       
    def define_attribute(self, name, typex):
        try:
            self.get_attribute(name)
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')
        
        except SemanticError:
    
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute

    def get_method(self, name: str, nparams: int):
        try:
            return self.methods[name, nparams]
        except KeyError:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" with {nparams} parameters is not defined in {self.name}.')
            try:
                return self.parent.get_method(name, nparams)
            except SemanticError:
                raise SemanticError(f'Method "{name}" with {nparams} parameters is not defined in {self.name} or its parents.')
    
    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        try:
            self.methods[name,len(param_names)]
            raise SemanticError(f'Method "{name}" already defined in {self.name} with {len(param_names)} params')
        except KeyError:
            self.methods[name,len(param_names)] = Method(name, param_names, param_types, return_type)
            
        return True 
        
    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output


class Protocol:
    def __init__(self, name: str):
        self.name = name
        self.methods: dict[(str,int), Method] = {}
        self.parent:Protocol = None
    
    def get_method(self, name: str, nparams: int):
        try:
            return self.methods[name, nparams]
        except KeyError:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" with {nparams} parameters is not defined in {self.name}.')
            try:
                return self.parent.get_method(name, nparams)
            except SemanticError:
                raise SemanticError(f'Method "{name}" with {nparams} parameters is not defined in {self.name} or its parents.')
    
    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        try:
            self.methods[name,len(param_names)]
            raise SemanticError(f'Method "{name}" already defined in {self.name} with {len(param_names)} params')
        except KeyError:
            self.methods[name,len(param_names)] = Method(name, param_names, param_types, return_type)
            
        return True 
        
    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent protocol is already set for {self.name}.')
        self.parent = parent
        
    def get_all_methods(self):
        if self.parent:
            methods = self.methods.copy()
            return methods.update(self.parent.get_all_methods())
        else:
            return self.methods.copy()
        
    def implemented_by(self,other: Type):
        
        if(other.bypass()):
            return other.bypass()
        
        pmethods = [method for method in self.get_all_methods()]
        
        for pname,nparams in pmethods:
            try:
                return self.methods[pname,nparams]  == other.get_method(pname,nparams) 
            except:
                return False
            
        return True
          
class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)

class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'int')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)

class VarType(Type):
    def __init__(self):
        super().__init__('Var')
   
    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class Context:
    def __init__(self):
        self.types: dict[str, Type] = {}
        self.functions: dict[(str,int),Method] = {}
        self.protocols: dict[str, Protocol] = {}
        
    def create_type(self, name: str) -> Type:
        if name in self.types:
            raise SemanticError(f'The type name "{name}" has already been taken.')
        typex = Type(name)
        self.types[name] = typex
        return typex
    
    def register_function_name(self, name: str,nparam:int) -> list[Method]:
        """Register function name only, not its overloads"""
        if (name,nparam) in self.functions:
            raise SemanticError(f'The function name "{name}" has already been taken.')
        self.functions[name,nparam] = None
    
    def create_function(self, name: str, param_names: list[str], param_types: list[str], return_type: str):
        try:
            is_defined = self.functions[name,len(param_names)]
            if is_defined:
                raise SemanticError(f'The function name "{name}" with {len(param_names)} parameters is already defined.')
            else:
                self.functions[name,len(param_names)] = Method(name, param_names, param_types, return_type)
        except KeyError:

            self.functions[name,len(param_names)] = Method(name, param_names, param_types, return_type)

    def create_protocol(self, name: str) -> Protocol:
        if name in self.types or name in self.protocols or name in self.functions:
            raise SemanticError(f'The protocol name "{name}" has already been taken.')
        protocol = Protocol(name)
        self.protocols[name] = protocol
        return protocol
    
    def get_function(self,name,nparams):
        if (name,nparams) not in self.functions:
            raise SemanticError(f'The type "{name}" is not defined in the context.')
        return self.functions[name,nparams]
    
    
    def get_type(self, name: str) -> Type:
        if name not in self.types:
            raise SemanticError(f'The type "{name}" is not defined in the context.')
        return self.types[name]
    
    def get_protocol(self, name: str) -> Protocol:
        if name not in self.protocols:
            raise SemanticError(f'The protocol "{name}" is not defined in the context.')
        return self.protocols[name]
    
    def __str__(self) -> str:
        types_str = '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n'))
        return f'{{\n\t{types_str}\n}}'
    
    def __repr__(self) -> str:
        return str(self)
    
class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.functions: dict = {}
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if not(self.parent is None) else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)
