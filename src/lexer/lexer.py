from lexer.regex.regex import Regex
from cmp.automata import State
from cmp.utils import Token, UnknownToken
from utils.serialize import load_cache, get_cache_path


IGNORE = ("IGNORE",)
COMMENT = "COMMENT"
ERROR = "ERROR"
NEWLINE = "NEWLINE"
SPACE = "SPACE"


class LexerError(Exception):
    def __init__(self, errors, text, tokens):
        """
        Inicializa la excepción con los errores formateados.
        :param errors: Lista de tuplas (lexeme, line, column) indicando los errores.
        :param text: El texto original del código fuente.
        """
        self.errors = errors  # Almacena los errores originales
        self.text = text      # Almacena el texto fuente
        self.tokens = tokens
        formatted_errors = self.format_errors()  # Formatea los errores
        super().__init__(f"\n\n💥 Lexer errors encountered:\n{formatted_errors}")

    def format_errors(self):
        """
        Formatea todos los errores en una cadena.
        """
        return "\n\n".join(
            [self.report_error(lexeme, line, column) for lexeme, line, column in self.errors]
        )

    def report_error(self, lexeme, line, column):
        """
        Genera un mensaje de error formateado para un único error.
        :param lexeme: Lexema que causó el error.
        :param line: Línea donde ocurrió el error.
        :param column: Columna donde ocurrió el error.
        :return: Mensaje de error formateado.
        """

        lines = self.text.splitlines()
        error_line = lines[line] if 0 <= line < len(lines) else ""

        # Formato de puntero usando ^ y la extensión ──
        pointer_line = " " * (column) + "^"  # Coloca el ^ debajo del error en la columna correcta
        pointer_line += "---Here."  # Añade el texto 'Here' para indicar la ubicación
        length_line = len(str(line))
        return (
            f"Error: Unrecognized symbol '{lexeme}' at line {line}, column {column}\n"
            f"    {line} | {error_line} \n"
            f"    {" " * length_line}   {pointer_line}"
        )


class Lexer:

    def __init__(self, table, eof):
        self.eof = eof
        self._prepare_table(table)
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()

    @load_cache("regex_automata")
    def _build_regexs(self, table):

        regexs = []
        # Recorre el diccionario
        for n, (token_type, regex) in enumerate(table.items()):
            if token_type in [NEWLINE, SPACE, COMMENT, IGNORE]:
                # Si el tipo de token corresponde a un tipo especial como NEWLINE, SPACE... usa Regex con skip_whitespaces en Flase
                automaton = Regex(regex, False).automaton
            else:
                automaton = Regex(regex).automaton

            # Convertir el NFA en un DFA
            automaton = State.from_nfa(automaton)
            for state in automaton:
                if state.final:
                    state.tag = (token_type, n)  # Marca el estado con un tag
            regexs.append(automaton)
        return regexs

    def _prepare_table(self, table):
        # Obtén los tipos de tokens de las claves del diccionario
        type_tokens = list(table.keys())

        # Agregar nuevos tokens si no están presentes
        if NEWLINE not in type_tokens:
            table[NEWLINE] = "\n"
        if SPACE not in type_tokens:
            table[SPACE] = " +"
        if COMMENT not in type_tokens:
            table[COMMENT] = "#[^\n]*"
        if IGNORE not in type_tokens:
            table[IGNORE] = "//[^\n]*"

    @load_cache("lexer_automaton")
    def _build_automaton(self):
        start = State("start")
        for automaton in self.regexs:
            start.add_epsilon_transition(automaton)
        return start.to_deterministic()

    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ""

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
                token_type, _ = min(tags, key=lambda x: x[1])
                yield lexeme, token_type
            else:
                yield current_text[0], ERROR
                current_text = current_text[1:]
        yield "$", self.eof

    def __call__(self, text):
        tokens = []
        errors = []
        column = line = index = 0

        for lexeme, token_type in self._tokenize(text):
            if token_type == NEWLINE:
                line += 1
                index = column = 0

            elif token_type in [COMMENT, IGNORE, SPACE]:
                continue

            elif token_type == ERROR:
                tokens.append(UnknownToken(lexeme, line, column, index))
                errors.append((lexeme, line, column))
            else:
                tokens.append(Token(lexeme, token_type, line, column, index))

            column += len(lexeme)  # Incrementa la columna según la longitud del lexema
            index += 1  # Incrementa la posición del token en la lista

        if errors:
            raise LexerError(errors, text, tokens)

        return tokens
