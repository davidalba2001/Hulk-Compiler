import hashlib
import json
import os

TEST_JSON_PATH = "src/tests/test_cases.json"


class TestLogger:
    def __init__(self):
        # Lista para almacenar los casos de prueba
        self.test_cases = {}

    def add(self, description, code, expected_tokens):
        """
        Añade un caso de prueba a la lista.
        :param description: Descripción breve del caso de prueba.
        :param code: Código del caso de prueba.
        :param expected_tokens: Tokens esperados del caso de prueba.
        """
        if code in self.test_cases:
            return
        
        self.test_cases[code] = {
            "description": description,
            "code": code,  # Se guarda también como parte del valor
            "expected_tokens": expected_tokens
        }
        self.save_to_file(TEST_JSON_PATH)

    
    def to_json(self):
        """
        Convierte los casos de prueba en una representación JSON formateada.
        :return: Una cadena JSON con una representación legible de los casos de prueba.
        """
        return json.dumps(self.test_cases, indent=4)


    def from_json(self, json_data):
        """
        Carga los casos de prueba desde una cadena JSON y los almacena en el atributo `test_cases`.
        :param json_data: Cadena JSON que contiene los casos de prueba.
        :raises ValueError: Si la cadena JSON no tiene un formato válido.
        """
        try:
            self.test_cases = json.loads(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"El JSON proporcionado no es válido: {e}")


    def save_to_file(self, file_path):
        """
        Guarda los casos de prueba en un archivo JSON.
        :param file_path: Nombre del archivo donde se guardarán los casos de prueba.
        """
        try:
            existing_tests = {}
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    existing_data = file.read()
                    if existing_data:
                        existing_tests = json.loads(existing_data)
            
            for code, test_case in self.test_cases.items():
                if code not in existing_tests:
                    existing_tests[code] = test_case
                    
            with open(file_path, 'w') as json_file:
                json.dump(existing_tests, json_file, indent=4)
        except (OSError, json.JSONDecodeError) as e:
            raise IOError(f"Error al manejar el archivo: {e}")

    def load_from_file(self, file_path):
        """
        Carga casos de prueba desde un archivo JSON y los procesa en el sistema.
        
        :param file_path: Ruta completa del archivo JSON que contiene los casos de prueba.
        :raises IOError: Si ocurre un error al abrir o leer el archivo.
        :raises ValueError: Si el contenido del archivo no es un JSON válido.
        """
        try:
            with open(file_path, 'r') as file:
                file_data = file.read()
                if file_data:
                    self.from_json(file_data)
                else:
                    raise ValueError("El archivo está vacío.")
        except (OSError, json.JSONDecodeError) as e:
            raise IOError(f"Error al leer el archivo '{file_path}': {e}")
