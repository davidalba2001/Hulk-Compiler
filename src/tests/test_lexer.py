from typing import List
import unittest
from cmp.languages import HulkLang
from lexer.lexer import Lexer, LexerError
from cmp.utils import Token
from tests.test_logger import TestLogger


class Test_Lexer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inicializamos el Lexer una vez para todas las pruebas
        cls.lexer = Lexer(HulkLang.lexer_table(), "EOF")
        cls.test_case_manager: TestLogger = TestLogger()

    def _test_expression(self, code: str, expected_tokens: List[tuple]):
        """
        Función generalizada para probar una expresión.
        Recibe el código y los tokens esperados como parámetros.
        """
        tokens: List[Token] = []
        try:
            # Genera los tokens del código proporcionado
            tokens = list(self.lexer(code))

            # Compara cada token generado con el esperado
            for token, expected in zip(tokens, expected_tokens):
                self.assertEqual(token.ttype, expected[1])
                self.assertEqual(token.lex, expected[0])
            # Verifica que la cantidad de tokens sea correcta
            self.assertEqual(len(tokens), len(expected_tokens))  # Excluyendo el EOF token

        except LexerError as e:
            raise e

        except Exception as e:
            raise Exception("Unexpected exception occurred") from e

    def test_function_call(self):

        description = "Prueba de llamada a funcion con argumentos."

        code = "foo(1, 2);"

        expected_tokens = [
            ('foo', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('1', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('2', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)

        self._test_expression(code, expected_tokens)

    def test_arithmetic_expressions_with_functions_and_identifiers(self):
        description = "Expresiones aritméticas con funciones anidadas, operadores..."

        code = """
        add(1, 2) * multiply(3, 4);
        5 + subtract(10, 3);
        6 ^ 2;
        (a + b) / 10;
        (result - c) % 7;
        print(add(a, b) + multiply(c, subtract(result, d)));
        """
        expected_tokens = [
            # Expresión: add(1, 2) * multiply(3, 4);
            ('add', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('1', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('2', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('*', 'MULTIPLY'),
            ('multiply', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('3', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('4', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),

            # Expresión: 5 + subtract(10, 3);
            ('5', 'NUMBER_LITERAL'),
            ('+', 'PLUS'),
            ('subtract', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('10', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('3', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),

            # Expresión: 6 ^ 2;
            ('6', 'NUMBER_LITERAL'),
            ('^', 'POWER'),
            ('2', 'NUMBER_LITERAL'),
            (';', 'SEMICOLON'),

            # Expresión: (a + b) / 10;
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            ('+', 'PLUS'),
            ('b', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('/', 'DIVIDE'),
            ('10', 'NUMBER_LITERAL'),
            (';', 'SEMICOLON'),

            # Expresión: (result - c) % 7;
            ('(', 'PAREN_OPEN'),
            ('result', 'IDENTIFIER'),
            ('-', 'MINUS'),
            ('c', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('%', 'PERCENT'),
            ('7', 'NUMBER_LITERAL'),
            (';', 'SEMICOLON'),

            # Expresión: print(add(a, b) + multiply(c, subtract(result, d)));
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('add', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            (',', 'COMMA'),
            ('b', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('+', 'PLUS'),
            ('multiply', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('c', 'IDENTIFIER'),
            (',', 'COMMA'),
            ('subtract', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('result', 'IDENTIFIER'),
            (',', 'COMMA'),
            ('d', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),

            # Fin de archivo
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)

        self._test_expression(code, expected_tokens)

    def test_string_literals(self):
        description = "Cadena simple."
        code = 'print("Hello World");'
        expected_tokens = [
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"Hello World"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_escape_double_quote(self):
        description = "Comillas dobles escapadas en una cadena."
        code = 'print("The message is \\"Hello World\\"");'
        expected_tokens = [
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"The message is \\"Hello World\\""', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_escape_newline(self):
        description = "Saltos de línea escapados en una cadena."
        code = 'print("Hello\\nWorld");'
        expected_tokens = [
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"Hello\\nWorld"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_escape_tab(self):
        description = "Tabulaciones escapadas en cadenas."

        code = 'print("Hello\\tWorld");'
        expected_tokens = [
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"Hello\\tWorld"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_string_concatenation(self):
        description = "Concatenación de cadenas usando el operador @."
        code = 'print("The meaning of life is " @ 42);'
        expected_tokens = [
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"The meaning of life is "', 'STRING_LITERAL'),
            ('@', 'AT_SYMBOL'),
            ('42', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_expression_block(self):
        description = "Bloque de múltiples expresiones ."
        code = """
            {
                print(42);
                print(sin(PI/2));
                print("Hello World");
            }
            """

        expected_tokens = [
            # Bloque de expresión: {
            ('{', 'BRACE_OPEN'),         # Apertura del bloque de expresión
            ('print', 'IDENTIFIER'),     # Primera expresión: print
            ('(', 'PAREN_OPEN'),
            ('42', 'NUMBER_LITERAL'),    # Argumento 42
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),

            ('print', 'IDENTIFIER'),     # Segunda expresión: print
            ('(', 'PAREN_OPEN'),
            ('sin', 'IDENTIFIER'),       # Llamada a sin
            ('(', 'PAREN_OPEN'),
            ('PI', 'IDENTIFIER'),        # Argumento PI
            ('/', 'DIVIDE'),             # Operador de división
            ('2', 'NUMBER_LITERAL'),     # Argumento 2
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),

            ('print', 'IDENTIFIER'),     # Tercera expresión: print
            ('(', 'PAREN_OPEN'),
            ('"Hello World"', 'STRING_LITERAL'),  # Cadena de texto
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),        # Cierre del bloque de expresión
            ('$', 'EOF')                 # Fin de archivo
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_inline_function_definitions(self):
        description = "Definiciones de funciones en línea."
        code = """
        function tan(x) => sin(x) / cos(x);
        function cot(x) => 1 / tan(x);
        function square(x) => x * x;
        print(tan(PI) ^ 2 + cot(PI) ^ 2);
        """
        expected_tokens = [
            # tan(x)
            ('function', 'FUNCTION_KEYWORD'),
            ('tan', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('=>', 'ARROW'),
            ('sin', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('/', 'DIVIDE'),
            ('cos', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            # cot(x)
            ('function', 'FUNCTION_KEYWORD'),
            ('cot', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('=>', 'ARROW'),
            ('1', 'NUMBER_LITERAL'),
            ('/', 'DIVIDE'),
            ('tan', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            # square(x)
            ('function', 'FUNCTION_KEYWORD'),
            ('square', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('=>', 'ARROW'),
            ('x', 'IDENTIFIER'),
            ('*', 'MULTIPLY'),
            ('x', 'IDENTIFIER'),
            (';', 'SEMICOLON'),

            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('tan', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('PI', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('^', 'POWER'),
            ('2', 'NUMBER_LITERAL'),
            ('+', 'PLUS'),
            ('cot', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('PI', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('^', 'POWER'),
            ('2', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),

            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_full_form_function_definition(self):
        description = "Definiciones de funciones en su forma completa."

        code = """
        function operate(x, y) {
            print(x + y);
            print(x - y);
            print(x * y);
            print(x / y);
        }
        """
        expected_tokens = [
            ('function', 'FUNCTION_KEYWORD'),
            ('operate', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (',', 'COMMA'),
            ('y', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('{', 'BRACE_OPEN'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('+', 'PLUS'),
            ('y', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('-', 'MINUS'),
            ('y', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('*', 'MULTIPLY'),
            ('y', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('/', 'DIVIDE'),
            ('y', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_single_variable(self):
        description = "Declarcion de una variable con let"

        code = 'let msg = "Hello World" in print(msg);'
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('msg', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('"Hello World"', 'STRING_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('msg', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_multiple_variables(self):
        decription = "Declaración de múltiples variables con let."
        code = 'let number = 42, text = "The meaning of life is" in print(text @ number);'
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('number', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('42', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('text', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('"The meaning of life is"', 'STRING_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('text', 'IDENTIFIER'),
            ('@', 'AT_SYMBOL'),
            ('number', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(decription, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_scope_rules(self):
        description = "Declaracion de una variable al definir otra con let."
        code = 'let a = 6, b = a * 7 in print(b);'
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('6', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('b', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('a', 'IDENTIFIER'),
            ('*', 'MULTIPLY'),
            ('7', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('b', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_expression_block_body(self):
        description = "Bloque de expresión como cuerpo de un let"
        code = """
        let a = 5, b = 10, c = 20 in {
            print(a + b);
            print(b * c);
            print(c / a);
        }
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('5', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('b', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('10', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('c', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('20', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('{', 'BRACE_OPEN'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            ('+', 'PLUS'),
            ('b', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('b', 'IDENTIFIER'),
            ('*', 'MULTIPLY'),
            ('c', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('c', 'IDENTIFIER'),
            ('/', 'DIVIDE'),
            ('a', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_let_return_value(self):
        description = "Expresiones let anidadas en la declarción de un variable."
        code = 'let a = (let b = 6 in b * 7) in print(a);'
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('(', 'PAREN_OPEN'),
            ('let', 'LET_KEYWORD'),
            ('b', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('6', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('b', 'IDENTIFIER'),
            ('*', 'MULTIPLY'),
            ('7', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_symbol_redefinition(self):
        description = "Expresiones let anidadas en el cuerpo y con redefinición de variables."
        code = """
        let a = 20 in {
            let a = 42 in print(a);
            print(a);
        }
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('20', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('{', 'BRACE_OPEN'),
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('42', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_destructive_assignment(self):
        description = "Asignación destructiva de variables."
        code = """
        let a = 0 in {
            print(a);
            a := 1;
            print(a);
        }
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('0', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('{', 'BRACE_OPEN'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('a', 'IDENTIFIER'),
            (':=', 'DASSIGN'),
            ('1', 'NUMBER_LITERAL'),
            (';', 'SEMICOLON'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_basic_if(self):
        description = "Prueba básica de un if."
        code = 'let a = 42 in if (a % 2 == 0) print("Even") else print("Odd");'
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('42', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('if', 'IF_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            ('%', 'PERCENT'),
            ('2', 'NUMBER_LITERAL'),
            ('==', 'EQUAL'),
            ('0', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"Even"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('else', 'ELSE_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"Odd"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_if_as_expression(self):
        description = "Prueba básica de un if."
        code = 'let a = 42 in print(if (a % 2 == 0) "Even" else "Odd");'
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('42', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('if', 'IF_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            ('%', 'PERCENT'),
            ('2', 'NUMBER_LITERAL'),
            ('==', 'EQUAL'),
            ('0', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('"Even"', 'STRING_LITERAL'),
            ('else', 'ELSE_KEYWORD'),
            ('"Odd"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_boolean_operators(self):
        description = "Operadores lógicos básicos."
        code = 'let a = true, b = false | a in if (a & !b) print("Yes") else print("No");'
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('true', 'TRUE_KEYWORD'),
            (',', 'COMMA'),
            ('b', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('false', 'FALSE_KEYWORD'),
            ('|', 'PIPE'),
            ('a', 'IDENTIFIER'),
            ('in', 'IN_KEYWORD'),
            ('if', 'IF_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            ('&', 'AND_OP'),
            ('!', 'NOT_OP'),
            ('b', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"Yes"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('else', 'ELSE_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"No"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_expression_block_in_conditionals(self):
        description = "Bloque de expresión en condicionales."
        code = """
        let a = 42 in
            if (a % 2 == 0) {
                print(a);
                print("Even");
            }
            else print("Odd");
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('42', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('if', 'IF_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            ('%', 'PERCENT'),
            ('2', 'NUMBER_LITERAL'),
            ('==', 'EQUAL'),
            ('0', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('{', 'BRACE_OPEN'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"Even"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('else', 'ELSE_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"Odd"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_multiple_branches(self):
        description = "Múltiples ramas en un condicional."
        code = """
        let a = 42, mod = a % 3 in
            print(
                if (mod == 0) "Magic"
                elif (mod % 3 == 1) "Woke"
                else "Dumb"
            );
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('42', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('mod', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('a', 'IDENTIFIER'),
            ('%', 'PERCENT'),
            ('3', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('if', 'IF_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('mod', 'IDENTIFIER'),
            ('==', 'EQUAL'),
            ('0', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('"Magic"', 'STRING_LITERAL'),
            ('elif', 'ELIF_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('mod', 'IDENTIFIER'),
            ('%', 'PERCENT'),
            ('3', 'NUMBER_LITERAL'),
            ('==', 'EQUAL'),
            ('1', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('"Woke"', 'STRING_LITERAL'),
            ('else', 'ELSE_KEYWORD'),
            ('"Dumb"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_while_loop(self):
        description = "Bucle while como cuerpo de un let."
        code = """
        let a = 10 in while (a >= 0) {
            print(a);
            a := a - 1;
        };
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('10', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('while', 'WHILE_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            ('>=', 'GREATER_EQUAL'),
            ('0', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('{', 'BRACE_OPEN'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('a', 'IDENTIFIER'),
            (':=', 'DASSIGN'),
            ('a', 'IDENTIFIER'),
            ('-', 'MINUS'),
            ('1', 'NUMBER_LITERAL'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_while_as_function_body(self):
        description = "Bucle while como cuerpo de una función en linea."
        code = """
        function gcd(a, b) => while (a > 0)
            let m = a % b in {
                b := a;
                a := m;
            };
        """
        expected_tokens = [
            ('function', 'FUNCTION_KEYWORD'),
            ('gcd', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            (',', 'COMMA'),
            ('b', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('=>', 'ARROW'),
            ('while', 'WHILE_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('a', 'IDENTIFIER'),
            ('>', 'GREATER_THAN'),
            ('0', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('m', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('a', 'IDENTIFIER'),
            ('%', 'PERCENT'),
            ('b', 'IDENTIFIER'),
            ('in', 'IN_KEYWORD'),
            ('{', 'BRACE_OPEN'),
            ('b', 'IDENTIFIER'),
            (':=', 'DASSIGN'),
            ('a', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('a', 'IDENTIFIER'),
            (':=', 'DASSIGN'),
            ('m', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_for_loop(self):
        description = "Bucle for como cuerpo de un let."
        code = 'for (x in range(0, 10)) print(x);'
        expected_tokens = [
            ('for', 'FOR_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('in', 'IN_KEYWORD'),
            ('range', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('0', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('10', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_for_loop_as_while_equivalent(self):
        description = "Bucle while equivalente Bucle for."
        code = """
        let iterable = range(0, 10) in
            while (iterable.next())
                let x = iterable.current() in
                    print(x);
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('iterable', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('range', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('0', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('10', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('while', 'WHILE_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('iterable', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('next', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('x', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('iterable', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('current', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_declare_type(self):
        description = "Declaración de un tipo."
        code = """
        type Point {
            x = 0;
            y = 0;

            getX() => self.x;
            getY() => self.y;

            setX(x) => self.x := x;
            setY(y) => self.y := y;
        }
        """
        expected_tokens = [
            ('type', 'TYPE_KEYWORD'),
            ('Point', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('x', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('0', 'NUMBER_LITERAL'),
            (';', 'SEMICOLON'),
            ('y', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('0', 'NUMBER_LITERAL'),
            (';', 'SEMICOLON'),
            ('getX', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('=>', 'ARROW'),
            ('self', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('x', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('getY', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('=>', 'ARROW'),
            ('self', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('y', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('setX', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('=>', 'ARROW'),
            ('self', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('x', 'IDENTIFIER'),
            (':=', 'DASSIGN'),
            ('x', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('setY', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('y', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('=>', 'ARROW'),
            ('self', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('y', 'IDENTIFIER'),
            (':=', 'DASSIGN'),
            ('y', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_instantiate_type(self):
        description = "Instanciación de un tipo."
        code = """
        let pt = new Point() in
            print("x: " @ pt.getX() @ "; y: " @ pt.getY());
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('pt', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('new', 'NEW_KEYWORD'),
            ('Point', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"x: "', 'STRING_LITERAL'),
            ('@', 'AT_SYMBOL'),
            ('pt', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('getX', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('@', 'AT_SYMBOL'),
            ('"; y: "', 'STRING_LITERAL'),
            ('@', 'AT_SYMBOL'),
            ('pt', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('getY', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_inherit_type(self):
        description = "Herencia de un tipo."
        code = """
        type Knight inherits Person {
            name() => "Sir" @@ base();
        }

        let p = new Knight("Phil", "Collins") in
            print(p.name());
        """
        expected_tokens = [
            ('type', 'TYPE_KEYWORD'),
            ('Knight', 'IDENTIFIER'),
            ('inherits', 'INHERITS_KEYWORD'),
            ('Person', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('name', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('=>', 'ARROW'),
            ('"Sir"', 'STRING_LITERAL'),
            ('@@', 'AT_AT_SYMBOL'),
            ('base', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('p', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('new', 'NEW_KEYWORD'),
            ('Knight', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"Phil"', 'STRING_LITERAL'),
            (',', 'COMMA'),
            ('"Collins"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('p', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('name', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_instantiate_with_arguments(self):
        description = "Instanciación de un tipo con argumentos."
        code = """
        type Point(x, y) {
            x = x;
            y = y;
        }

        let pt = new Point(3, 4) in
            print("x: " @ pt.getX() @ "; y: " @ pt.getY());
        """
        expected_tokens = [
            ('type', 'TYPE_KEYWORD'),
            ('Point', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (',', 'COMMA'),
            ('y', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('{', 'BRACE_OPEN'),
            ('x', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('x', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('y', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('y', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('pt', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('new', 'NEW_KEYWORD'),
            ('Point', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('3', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('4', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"x: "', 'STRING_LITERAL'),
            ('@', 'AT_SYMBOL'),
            ('pt', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('getX', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('@', 'AT_SYMBOL'),
            ('"; y: "', 'STRING_LITERAL'),
            ('@', 'AT_SYMBOL'),
            ('pt', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('getY', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_typing_variables(self):
        description = "Anotaciones de tipos en variables."
        code = """
        let x: Number = 42 in print(x);
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('x', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('42', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_typing_functions(self):
        description = "Anotaciones de tipos en funciones."
        code = """
        function tan(x: Number): Number => sin(x) / cos(x);
        """
        expected_tokens = [
            ('function', 'FUNCTION_KEYWORD'),
            ('tan', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            ('=>', 'ARROW'),
            ('sin', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('/', 'DIVIDE'),
            ('cos', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_typing_attributes(self):
        description = "Anotaciones de tipos en atributos."
        code = """
        type Point(x: Number, y: Number) {
            x: Number = x;
            y: Number = y;
        }
        """
        expected_tokens = [
            ('type', 'TYPE_KEYWORD'),
            ('Point', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            (',', 'COMMA'),
            ('y', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('{', 'BRACE_OPEN'),
            ('x', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('x', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('y', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('y', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_type_conforming(self):
        description = "Verificación de conformidad de tipos."
        code = """
        type Animal {}
        type Dog inherits Animal {}
        let a: Animal = new Dog();
        """
        expected_tokens = [
            ('type', 'TYPE_KEYWORD'),
            ('Animal', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('}', 'BRACE_CLOSE'),
            ('type', 'TYPE_KEYWORD'),
            ('Dog', 'IDENTIFIER'),
            ('inherits', 'INHERITS_KEYWORD'),
            ('Animal', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('}', 'BRACE_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('a', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Animal', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('new', 'NEW_KEYWORD'),
            ('Dog', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_dynamic_type_checking(self):
        description = "Verificación dinámica de tipos."
        code = """
        type Bird {}
        type Plane {}
        type Superman {}

        let x = new Superman() in
            print(
                if (x is Bird) "It's bird!"
                elif (x is Plane) "It's a plane!"
                else "No, it's Superman!"
            );
        """
        expected_tokens = [
            ('type', 'TYPE_KEYWORD'),
            ('Bird', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('}', 'BRACE_CLOSE'),
            ('type', 'TYPE_KEYWORD'),
            ('Plane', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('}', 'BRACE_CLOSE'),
            ('type', 'TYPE_KEYWORD'),
            ('Superman', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('}', 'BRACE_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('x', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('new', 'NEW_KEYWORD'),
            ('Superman', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('if', 'IF_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('is', 'IS_KEYWORD'),
            ('Bird', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('"It\'s bird!"', 'STRING_LITERAL'),
            ('elif', 'ELIF_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('is', 'IS_KEYWORD'),
            ('Plane', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('"It\'s a plane!"', 'STRING_LITERAL'),
            ('else', 'ELSE_KEYWORD'),
            ('"No, it\'s Superman!"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]

        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_downcasting(self):
        description = "Prueba de downcasting."
        code = """
        type A {}
        type B inherits A {}
        type C inherits A {}

        let x: A = if (rand() < 0.5) new B() else new C() in
            if (x is B)
                let y: B = x as B in {
                    print(y);
                }
            else {
                print("Cannot downcast to B");
            }
        """
        expected_tokens = [
            ('type', 'TYPE_KEYWORD'),
            ('A', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('}', 'BRACE_CLOSE'),
            ('type', 'TYPE_KEYWORD'),
            ('B', 'IDENTIFIER'),
            ('inherits', 'INHERITS_KEYWORD'),
            ('A', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('}', 'BRACE_CLOSE'),
            ('type', 'TYPE_KEYWORD'),
            ('C', 'IDENTIFIER'),
            ('inherits', 'INHERITS_KEYWORD'),
            ('A', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('}', 'BRACE_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('x', 'IDENTIFIER'),
            (':', 'COLON'),
            ('A', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('if', 'IF_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('rand', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('<', 'LESS_THAN'),
            ('0.5', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('new', 'NEW_KEYWORD'),
            ('B', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('else', 'ELSE_KEYWORD'),
            ('new', 'NEW_KEYWORD'),
            ('C', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('if', 'IF_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('is', 'IS_KEYWORD'),
            ('B', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('y', 'IDENTIFIER'),
            (':', 'COLON'),
            ('B', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('x', 'IDENTIFIER'),
            ('as', 'AS_KEYWORD'),
            ('B', 'IDENTIFIER'),
            ('in', 'IN_KEYWORD'),
            ('{', 'BRACE_OPEN'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('y', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('else', 'ELSE_KEYWORD'),
            ('{', 'BRACE_OPEN'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('"Cannot downcast to B"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_defining_protocols(self):
        description = "Definición de protocolos."
        code = """
        protocol Hashable {
            hash(): Number;
        }
        """
        expected_tokens = [
            ('protocol', 'PROTOCOL_KEYWORD'),
            ('Hashable', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('hash', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_extending_protocols(self):
        description = "Extensión de protocolos."
        code = """
        protocol Equatable extends Hashable {
            equals(other: Object): Boolean;
        }
        """
        expected_tokens = [
            ('protocol', 'PROTOCOL_KEYWORD'),
            ('Equatable', 'IDENTIFIER'),
            ('extends', 'EXTENDS_KEYWORD'),
            ('Hashable', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('equals', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('other', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Object', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Boolean', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_implementing_protocols(self):
        description = "Implementación de protocolos."
        code = """
        type Person {
            hash() : Number {
                42;
            }
        }

        let x : Hashable = new Person() in print(x.hash());
        """
        expected_tokens = [
            ('type', 'TYPE_KEYWORD'),
            ('Person', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('hash', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('42', 'NUMBER_LITERAL'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('}', 'BRACE_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('x', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Hashable', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('new', 'NEW_KEYWORD'),
            ('Person', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('hash', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_protocol_variance(self):
        description = "Varianza de protocolos."
        code = """
        protocol Comparator {
            compare(other: Object): Boolean;
        }

        type Person {
            compare(other: Person): Boolean {
                true;
            }
        }

        let p1: Comparator = new Person();
        """
        expected_tokens = [
            ('protocol', 'PROTOCOL_KEYWORD'),
            ('Comparator', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('compare', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('other', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Object', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Boolean', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('type', 'TYPE_KEYWORD'),
            ('Person', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('compare', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('other', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Person', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Boolean', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('true', 'TRUE_KEYWORD'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('}', 'BRACE_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('p1', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Comparator', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('new', 'NEW_KEYWORD'),
            ('Person', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_protocol_conforming(self):
        description = "Conformidad de protocolos."
        code = """
        protocol Hashable {
            hash(): Number;
        }

        type Person {
            hash() : Number {
                42;
            }
        }

        let x: Hashable = new Person() in print(x.hash());
        """
        expected_tokens = [
            ('protocol', 'PROTOCOL_KEYWORD'),
            ('Hashable', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('hash', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('type', 'TYPE_KEYWORD'),
            ('Person', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('hash', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('42', 'NUMBER_LITERAL'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('}', 'BRACE_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('x', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Hashable', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('new', 'NEW_KEYWORD'),
            ('Person', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('hash', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_defining_iterable_protocol(self):
        description = "Definición del protocolo Iterable."
        code = """
        protocol Iterable {
            next(): Boolean;
            current(): Object;
        }
        """
        expected_tokens = [
            ('protocol', 'PROTOCOL_KEYWORD'),
            ('Iterable', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('next', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Boolean', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('current', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Object', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_range_type_implementation(self):
        description = "Implementación del tipo Range."
        code = """
        type Range(min: Number, max: Number) {
            min = min;
            max = max;
            current = min - 1;

            next(): Boolean => (self.current := self.current + 1) < max;
            current(): Number => self.current;
        }

        let r = new Range(0, 10) in print(r.current());
        """
        expected_tokens = [
            ('type', 'TYPE_KEYWORD'),
            ('Range', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('min', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            (',', 'COMMA'),
            ('max', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('{', 'BRACE_OPEN'),
            ('min', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('min', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('max', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('max', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('current', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('min', 'IDENTIFIER'),
            ('-', 'MINUS'),
            ('1', 'NUMBER_LITERAL'),
            (';', 'SEMICOLON'),
            ('next', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Boolean', 'IDENTIFIER'),
            ('=>', 'ARROW'),
            ('(', 'PAREN_OPEN'),
            ('self', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('current', 'IDENTIFIER'),
            (':=', 'DASSIGN'),
            ('self', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('current', 'IDENTIFIER'),
            ('+', 'PLUS'),
            ('1', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('<', 'LESS_THAN'),
            ('max', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('current', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            ('=>', 'ARROW'),
            ('self', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('current', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('r', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('new', 'NEW_KEYWORD'),
            ('Range', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('0', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('10', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('r', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('current', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_iterable_with_for_loop(self):
        description = "Iteración con un ciclo `for`."
        code = """
        for (x in range(0, 10)) {
            // code that uses `x`
        }
        """
        expected_tokens = [
            ('for', 'FOR_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('in', 'IN_KEYWORD'),
            ('range', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('0', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('10', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            ('{', 'BRACE_OPEN'),
            ('}', 'BRACE_CLOSE'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_typing_iterables(self):
        description = "Anotaciones de tipos en iterables."
        code = """
        function sum(numbers: Number*): Number =>
            let total = 0 in
                for (x in numbers)
                    total := total + x;
        """
        expected_tokens = [
            ('function', 'FUNCTION_KEYWORD'),
            ('sum', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('numbers', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            ('*', 'MULTIPLY'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            ('=>', 'ARROW'),
            ('let', 'LET_KEYWORD'),
            ('total', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('0', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('for', 'FOR_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('in', 'IN_KEYWORD'),
            ('numbers', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('total', 'IDENTIFIER'),
            (':=', 'DASSIGN'),
            ('total', 'IDENTIFIER'),
            ('+', 'PLUS'),
            ('x', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_enumerable_protocol(self):
        description = "Protocolo `Enumerable`."
        code = """
        protocol Enumerable {
            iter(): Iterable;
        }

        type Collection {
            iter(): Iterable {
                range(0, 10);
            }
        }

        let c = new Collection() in
            for (x in c) {
                print(x);
            }
        """
        expected_tokens = [
            ('protocol', 'PROTOCOL_KEYWORD'),
            ('Enumerable', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('iter', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Iterable', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('type', 'TYPE_KEYWORD'),
            ('Collection', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('iter', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Iterable', 'IDENTIFIER'),
            ('{', 'BRACE_OPEN'),
            ('range', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('0', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('10', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('}', 'BRACE_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('c', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('new', 'NEW_KEYWORD'),
            ('Collection', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('for', 'FOR_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('in', 'IN_KEYWORD'),
            ('c', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('{', 'BRACE_OPEN'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_explicit_vector_syntax(self):
        description = "Sintaxis explícita de vectores."
        code = """
        let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9] in
            for (x in numbers)
                print(x);
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('numbers', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('[', 'SQUARE_BRACKET_OPEN'),
            ('1', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('2', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('3', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('4', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('5', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('6', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('7', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('8', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('9', 'NUMBER_LITERAL'),
            (']', 'SQUARE_BRACKET_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('for', 'FOR_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('in', 'IN_KEYWORD'),
            ('numbers', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_vector_indexing_syntax(self):
        description = "Sintaxis de indexación de vectores."
        code = """
        let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9] in
            print(numbers[7]);
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('numbers', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('[', 'SQUARE_BRACKET_OPEN'),
            ('1', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('2', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('3', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('4', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('5', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('6', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('7', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('8', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('9', 'NUMBER_LITERAL'),
            (']', 'SQUARE_BRACKET_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('numbers', 'IDENTIFIER'),
            ('[', 'SQUARE_BRACKET_OPEN'),
            ('7', 'NUMBER_LITERAL'),
            (']', 'SQUARE_BRACKET_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_implicit_vector_syntax(self):
        description = "Sintaxis implícita de vectores."
        code = """
        let squares = [x^2 || x in range(1, 10)] in print(squares);
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('squares', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('[', 'SQUARE_BRACKET_OPEN'),
            ('x', 'IDENTIFIER'),
            ('^', 'POWER'),
            ('2', 'NUMBER_LITERAL'),
            ('||', 'DOUBLE_PIPE'),
            ('x', 'IDENTIFIER'),
            ('in', 'IN_KEYWORD'),
            ('range', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('1', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('10', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (']', 'SQUARE_BRACKET_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('squares', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_typing_vector_argument(self):
        description = "Anotación de tipos en argumentos de vectores."
        code = """
        function mean(numbers: Number[]): Number =>
            let total = 0 in {
                for (x in numbers)
                    total := total + x;

                total / numbers.size();
            }

        let numbers = [1, 2, 3, 4, 5] in
            print(mean(numbers));
        """
        expected_tokens = [
            ('function', 'FUNCTION_KEYWORD'),
            ('mean', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('numbers', 'IDENTIFIER'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            ('[', 'SQUARE_BRACKET_OPEN'),
            (']', 'SQUARE_BRACKET_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (':', 'COLON'),
            ('Number', 'IDENTIFIER'),
            ('=>', 'ARROW'),
            ('let', 'LET_KEYWORD'),
            ('total', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('0', 'NUMBER_LITERAL'),
            ('in', 'IN_KEYWORD'),
            ('{', 'BRACE_OPEN'),
            ('for', 'FOR_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('x', 'IDENTIFIER'),
            ('in', 'IN_KEYWORD'),
            ('numbers', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            ('total', 'IDENTIFIER'),
            (':=', 'DASSIGN'),
            ('total', 'IDENTIFIER'),
            ('+', 'PLUS'),
            ('x', 'IDENTIFIER'),
            (';', 'SEMICOLON'),
            ('total', 'IDENTIFIER'),
            ('/', 'DIVIDE'),
            ('numbers', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('size', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE'),
            ('let', 'LET_KEYWORD'),
            ('numbers', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('[', 'SQUARE_BRACKET_OPEN'),
            ('1', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('2', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('3', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('4', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('5', 'NUMBER_LITERAL'),
            (']', 'SQUARE_BRACKET_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('mean', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('numbers', 'IDENTIFIER'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)

    def test_vector_size_method(self):
        description = "Método `size` de vectores."
        code = """
        let numbers = [1, 2, 3, 4, 5] in
            print(numbers.size());
        """
        expected_tokens = [
            ('let', 'LET_KEYWORD'),
            ('numbers', 'IDENTIFIER'),
            ('=', 'ASSIGN'),
            ('[', 'SQUARE_BRACKET_OPEN'),
            ('1', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('2', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('3', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('4', 'NUMBER_LITERAL'),
            (',', 'COMMA'),
            ('5', 'NUMBER_LITERAL'),
            (']', 'SQUARE_BRACKET_CLOSE'),
            ('in', 'IN_KEYWORD'),
            ('print', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            ('numbers', 'IDENTIFIER'),
            ('.', 'DOT'),
            ('size', 'IDENTIFIER'),
            ('(', 'PAREN_OPEN'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('$', 'EOF')
        ]
        self.test_case_manager.add(description, code, expected_tokens)
        self._test_expression(code, expected_tokens)


if __name__ == '__main__':
    unittest.main()
