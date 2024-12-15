from lexer.regex.regex import Regex
from cmp.automata import State
from cmp.utils import Token
from utils.serialize import load_cache, get_cache_path


IGNORE = ("IGNORE",)
COMMENT = "COMMENT"
ERROR = "ERROR"
NEWLINE = "NEWLINE"
SPACE = "SPACE"


class LexerError(Exception):
    def __init__(self, errors, text):
        formatted_errors = "\n\n".join(
            self.report_error(text, line, column, lexeme)
            for lexeme, line, column in errors
        )
        super().__init__(f"Lexer errors encountered:\n{formatted_errors}")

    @staticmethod
    def report_error(text, line, column, lexeme):
        lines = text.splitlines()
        error_line = lines[line - 1] if 0 < line <= len(lines) else ""
        pointer_line = " " * column + f"└{'─' * (len(lexeme)-1)}▲"
        return (
            f"❌ Error: Unrecognized symbol '{lexeme}' at line {line}, column {column}\n"
            f"{error_line}\n"
            f"{pointer_line}"
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
        for n, (token_type, regex) in enumerate(table):
            if (
                token_type == NEWLINE
                or token_type == SPACE
                or token_type == COMMENT
                or token_type == IGNORE
            ):
                automaton = Regex(regex, False).automaton
            else:
                automaton = Regex(regex).automaton
            automaton = State.from_nfa(automaton)
            for state in automaton:
                if state.final:
                    state.tag = (token_type, n)
            regexs.append(automaton)
        return regexs

    def _prepare_table(self, table):
        type_tokens = [type_token for type_token, _ in table]
        if NEWLINE not in type_tokens:
            table.append((NEWLINE, "\n"))
        if SPACE not in type_tokens:
            table.append((SPACE, " +"))
        if COMMENT not in type_tokens:
            table.append((COMMENT, "#[^\n]*"))
        if IGNORE not in type_tokens:
            table.append((IGNORE, "//[^\n]*"))

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
                current_text = current_text[len(lexeme) :]
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
        column = line = 1

        for lexeme, token_type in self._tokenize(text):
            if token_type == NEWLINE:
                line += 1
                column = 0
            elif token_type == COMMENT or token_type == IGNORE or token_type == SPACE:
                continue

            elif token_type == ERROR:
                errors.append(
                    f"Unrecognized symbol '{lexeme}' at line {line}, column {column}"
                )
            else:
                tokens.append(Token(lexeme, token_type, line, column))

            column += 1

        if errors:
            raise LexerError(errors)
        return tokens
