from file_organizer .classifier import clasificar_archivo
from pathlib import Path


def test_clasificar_extension_conocida():
    """
    Si la extensión está en las reglas, debe devolver la categoría correcta.
    """

    reglas = {".jpg": "Images", ".pdf": "Documents"}
    archivo = Path("foto.jpg")

    resultado = clasificar_archivo(archivo, reglas)

    assert resultado == "Images"


def test_clasificar_extension_desconocida():
    """
    Si la extensión NO está en las reglas, debe devolver "Others"
    en vez de lanzar un error.
    """

    reglas = {".jpg": "Images"}
    archivo = Path("misterioso.xyz")

    resultado = clasificar_archivo(archivo, reglas)

    assert resultado == "Others"


def test_clasificar_es_insensible_a_mayusculas():
    """
    "Foto.JPG" debe clasificarse igual que "foto.jpg",
    gracias al .lower() que aplicamos en classifier.py.
    """

    reglas = {".jpg": "Images"}
    archivo = Path("Foto.JPG")

    resultado = clasificar_archivo(archivo, reglas)

    assert resultado == "Images"


def test_clasificar_archivo_sin_extension():
    """
    Un archivo sin extensión (por ejemplo "README" o "Makefile")
    debe caer también en "Others", no romper el programa.
    """

    reglas = {".jpg": "Images"}
    archivo = Path("README")

    resultado = clasificar_archivo(archivo, reglas)

    assert resultado == "Others"