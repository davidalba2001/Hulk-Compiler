import sys
import os
from functools import wraps
import dill as pickle


CACHE_PATH = os.path.join("src", "cache")
os.makedirs(CACHE_PATH, exist_ok=True)
        
def serialize_object(obj, filename):
    """ Serializa el objeto a un archivo con el nombre dado. """
    path = os.path.join(CACHE_PATH, f"{filename}.pkl")
    original_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(10000)
        with open(path, "wb") as file:
            pickle.dump(obj, file)
    finally:
        sys.setrecursionlimit(original_limit)


def deserialize_object(filename):
    """ Deserializa el objeto desde un archivo con el nombre dado. """
    path = os.path.join(CACHE_PATH, f"{filename}.pkl")
    original_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(10000)
        with open(path, "rb") as file:
            return pickle.load(file)
    finally:
        sys.setrecursionlimit(original_limit)
        
        
def load_cache(filename:str):
    """
    Decorador que carga el objeto desde el caché si existe.
    Si no existe, ejecuta la función y guarda el resultado en el caché.
    """
    def decorator(build_method):
        @wraps(build_method)
        def wrapper(self, *args, **kwargs):
            path = os.path.join(CACHE_PATH, f"{filename}.pkl")
            if os.path.exists(path):
                obj = deserialize_object(filename)
            else:
                obj = build_method(self, *args, **kwargs)
                serialize_object(obj, filename) 
            return obj

        return wrapper

    return decorator    

def get_cache_path(filename):
    """
    Dado un nombre de archivo (sin el sufijo '.pkl'), retorna la ruta completa dentro del directorio de caché.
    """
    return os.path.join(CACHE_PATH, f"{filename}.pkl")