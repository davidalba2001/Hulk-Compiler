try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath("src"))

finally:
    from typing import List
    import unittest
    from src.cmp.languages import HulkLang
    from src.lexer.lexer import Lexer, LexerError
    from src.cmp.utils import Token


class TestLexer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inicializamos el Lexer una vez para todas las pruebas
        cls.lexer = Lexer(HulkLang.lexer_table(), "EOF")

    def _test_expression(self, code: str, expected_tokens: List[tuple]):
        """
        Función generalizada para probar una expresión.
        Recibe el código y los tokens esperados como parámetros.
        """
        tokens: List[Token] = []
        try:
            # Genera los tokens del código proporcionado
            tokens = list(self.lexer(code))

            # Verifica que la cantidad de tokens sea correcta
            self.assertEqual(len(tokens), len(expected_tokens))  # Excluyendo el EOF token

            # Compara cada token generado con el esperado
            for token, expected in zip(tokens, expected_tokens):
                self.assertEqual(token.ttype, expected[1])
                self.assertEqual(token.lex, expected[0])

        except LexerError as e:
            print(f"Input Code: {code}")
            print(f"Tokens processed: {[(token.lex, token.ttype) for token in e.tokens]}")
            raise e
        except Exception as e:
            # Captura cualquier otro tipo de excepción no anticipada
            print(f"Unexpected error occurred:\n{str(e)}")

            raise Exception("Unexpected exception occurred") from e

    def test_function_call(self):
        # Probar una llamada a función con argumentos
        code = "$foo(1, 2);"

        expected_tokens = [
            ('!foo', 'IDENTIFIER'),        # Nombre de la función
            ('(', 'PAREN_OPEN'),          # Paréntesis de apertura
            ('1', 'NUMBER_LITERAL'),      # Primer argumento
            (',', 'COMMA'),               # Coma separadora
            ('2', 'NUMBER_LITERAL'),      # Segundo argumento
            (')', 'PAREN_CLOSE'),         # Paréntesis de cierre
            (';', 'SEMICOLON'),           # Punto y coma
            ('$', 'EOF')                  # Fin de archivo (EOF)
        ]

        # Llamar a la función generalizada para verificar la expresión
        self._test_expression(code, expected_tokens)

    def test_arithmetic_expressions_with_functions_and_identifiers(self):
        # Código de prueba con operadores +, -, *, /, %, ^, identificadores y llamadas a funciones
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
            (';', 'SEMICOLON'),

            # Fin de archivo
            ('$', 'EOF')
        ]

        # Llamar a la función generalizada para verificar la expresión
        self._test_expression(code, expected_tokens)

    def test_string_concatenation(self):
        # Probar concatenación de cadenas: "The meaning of life is " @ 42
        code = 'print("The meaning of life is " @ 42);'
        tokens = list(self.lexer(code))
        expected_tokens = [
            ('print', 'FUNCTION_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('"The meaning of life is "', 'STRING_LITERAL'),
            ('@', 'AT_SYMBOL'),
            ('42', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON')
        ]
        self.assertEqual(len(tokens), len(expected_tokens))
        for token, expected in zip(tokens, expected_tokens):
            self.assertEqual(token, expected)

    def test_builtin_math_functions(self):
        # Probar el uso de una función matemática: sqrt(16)
        code = 'print(sqrt(16));'
        tokens = list(self.lexer(code))
        expected_tokens = [
            ('print', 'FUNCTION_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('sqrt', 'FUNCTION_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('16', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON')
        ]
        self.assertEqual(len(tokens), len(expected_tokens))
        for token, expected in zip(tokens, expected_tokens):
            self.assertEqual(token, expected)

    def test_expression_block(self):
        # Probar un bloque de expresiones:
        # {
        #     print(42);
        #     print(sin(PI/2));
        #     print("Hello World");
        # }
        code = """
        {
            print(42);
            print(sin(PI/2));
            print("Hello World");
        }
        """
        tokens = list(self.lexer(code))
        expected_tokens = [
            ('{', 'BRACE_OPEN'),
            ('print', 'FUNCTION_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('42', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('print', 'FUNCTION_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('sin', 'FUNCTION_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('PI', 'IDENTIFIER'),
            ('/', 'DIVIDE'),
            ('2', 'NUMBER_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('print', 'FUNCTION_KEYWORD'),
            ('(', 'PAREN_OPEN'),
            ('"Hello World"', 'STRING_LITERAL'),
            (')', 'PAREN_CLOSE'),
            (';', 'SEMICOLON'),
            ('}', 'BRACE_CLOSE')
        ]
        self.assertEqual(len(tokens), len(expected_tokens))
        for token, expected in zip(tokens, expected_tokens):
            self.assertEqual(token, expected)


if __name__ == '__main__':
    unittest.main()
