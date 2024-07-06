import sys
import os

# Obtener la ruta del directorio actual (por ejemplo, donde se encuentra este script)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Subir tres niveles para llegar a la raíz del proyecto
project_root = os.path.abspath(os.path.join(current_dir, '../../..'))

# Agregar 'src/parsers' a sys.path para que Python pueda encontrar el módulo 'll1_parser'
regex_path = os.path.join(project_root, 'src/lexer/regex')
sys.path.append(regex_path)
print(f"sys.path: {sys.path}")

try:
    import dill as pickle 
    from .regex import Regex
    from cmp.automata import State
    from cmp.utils import Token
    from enum import Enum
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")

IGNORE = "IGNORE",
COMMENT ='COMMENT'
ERROR = 'ERROR'
NEWLINE = 'NEWLINE'
SPACE = 'SPACE'
  
class LexerError(Exception):
    
    def __init__(self, errors):
        formatted_errors = '\n'.join(errors)
        super().__init__(f"Lexer errors encountered:\n{formatted_errors}")


def load_or_build(path):
    def decorator(build_method):
        def wrapper(self, *args, **kwargs):
            if os.path.exists(path):
                with open(path, 'rb') as file:
                    obj = pickle.load(file)
            else:
                obj = build_method(self, *args, **kwargs)
                with open(path, 'wb') as file:
                    pickle.dump(obj, file)
            return obj
        return wrapper
    return decorator




class Lexer:
     
    def __init__(self, table, eof):
        self.eof = eof
        self._prepare_table(table)
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
       
    @load_or_build('src/lexer/serialized/regexs.pkl')          
    def _build_regexs(self, table):
        
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            if(token_type == NEWLINE or token_type == SPACE or token_type == COMMENT or token_type == IGNORE ):
                automaton = Regex(regex,False).automaton
            else:
                automaton = Regex(regex).automaton
            automaton = State.from_nfa(automaton)
            for state in automaton:
                if state.final:
                    state.tag = (token_type,n)
            regexs.append(automaton)
        return regexs
     
    def _prepare_table(self,table):
        type_tokens = [type_token for type_token,_ in table] 
        if NEWLINE not in type_tokens:
            table.append((NEWLINE, '\n'))
        if SPACE not in type_tokens:
            table.append((SPACE,' +'))
        if COMMENT not in type_tokens:
            table.append((COMMENT,'#[^\n]*'))
        if IGNORE not in type_tokens:
             table.append((IGNORE,'//[^\n]*'))
             
    @load_or_build('src/lexer/serialized/lexer_automaton.pkl')
    def _build_automaton(self):
        start = State('start')
        for automaton in self.regexs:
            start.add_epsilon_transition(automaton)
        return start.to_deterministic()
    
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''
        
        for symbol in string:
            if state.has_transition(symbol):
                state = state.transitions[symbol][0]
                lex = lex + symbol
                if state.final:
                    final = state if state.final else None
                    final_lex = lex
                continue
            break
                
        return final, final_lex
        
    def _tokenize(self, text):
        current_text = text
        
        while len(current_text):
            state, lexeme = self._walk(current_text)
            if state is not None:
                current_text = current_text[len(lexeme):]
                tags = [s.tag for s in state.state if s.tag is not None]
                token_type,_= min(tags, key= lambda x : x[1])
                yield lexeme, token_type
            else:
                yield current_text[0], ERROR
                current_text = current_text[1:]
        yield '$', self.eof
         
    def __call__(self, text):
        tokens = []
        errors = []
        column = line = 1
        
        for lexeme,token_type in self._tokenize(text):
            if(token_type == NEWLINE):
                line += 1
                column = 0 
            elif(token_type == COMMENT or token_type == IGNORE or token_type == SPACE):
                continue
            
            elif(token_type == ERROR):
                errors.append(f"Unrecognized symbol '{lexeme}' at line {line}, column {column}")
            else:
                tokens.append(Token(lexeme, token_type, line, column))
            
            column += 1
                
        if errors:
            raise LexerError(errors)
       
        return tokens