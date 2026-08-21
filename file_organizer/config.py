import json
from pathlib import Path


# Reglas por defecto que se usan si el usuario no tiene un rules.json propio,
# o si el archivo existe pero está vacío/corrupto.
# Las definimos aquí como una "red de seguridad" para que el programa
# nunca se quede sin ninguna regla con la que trabajar.
REGLAS_POR_DEFECTO = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".pdf": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".xlsx": "Documents",
    ".mp3": "Music",
    ".wav": "Music",
    ".mp4": "Videos",
    ".mov": "Videos",
    ".zip": "Compressed",
    ".rar": "Compressed",
}


def cargar_reglas(ruta_json):
    """
    Carga el diccionario de reglas (extensión -> categoría) desde un archivo JSON.

    Parámetros:
        ruta_json (str o Path): ruta al archivo rules.json.

    Retorna:
        dict: diccionario de reglas listo para usar en classifier.py.
    """

    ruta = Path(ruta_json)

    # Caso 1: el archivo no existe todavía.
    # En vez de fallar, creamos uno con las reglas por defecto para que
    # el usuario tenga un punto de partida editable.
    if not ruta.exists():
        crear_config_por_defecto(ruta)
        return REGLAS_POR_DEFECTO

    # Caso 2: el archivo existe, intentamos leerlo.
    # Usamos try/except porque un JSON mal escrito por el usuario
    # (una coma de más, comillas mal cerradas) lanzaría json.JSONDecodeError,
    # y preferimos avisar con un mensaje claro en vez de que el programa
    # se caiga con un traceback confuso.
    try:
        with open(ruta, "r", encoding="utf-8") as archivo_config:
            reglas = json.load(archivo_config)
    except json.JSONDecodeError:
        raise ValueError(
            f"El archivo '{ruta}' tiene un formato JSON inválido. "
            f"Revisa que las comillas y comas estén bien escritas."
        )

    # Validamos que lo que hemos cargado tenga la forma que esperamos:
    # un diccionario de string -> string. Si el usuario mete una lista
    # o un número por error, lo detectamos aquí en vez de que falle
    # más adelante en classifier.py con un error menos claro.
    validar_reglas(reglas)

    return reglas


def crear_config_por_defecto(ruta_json):
    """
    Crea un archivo rules.json con las reglas por defecto.
    Se usa cuando el usuario ejecuta el programa por primera vez.

    Parámetros:
        ruta_json (str o Path): ruta donde se debe crear el archivo.
    """

    ruta = Path(ruta_json)

    # Nos aseguramos de que la carpeta "config/" exista antes de escribir
    # el archivo dentro. parents=True crea también carpetas intermedias
    # si hicieran falta, y exist_ok=True evita un error si ya existe.
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo_config:
        # indent=4 hace que el JSON se guarde legible (con saltos de línea
        # y sangría), para que el usuario pueda abrirlo y editarlo a mano
        # sin que sea una sola línea ilegible.
        json.dump(REGLAS_POR_DEFECTO, archivo_config, indent=4, ensure_ascii=False)


def validar_reglas(reglas):
    """
    Comprueba que las reglas cargadas tengan el formato correcto:
    un diccionario donde cada clave es una extensión (string) y
    cada valor es un nombre de categoría (string).

    Lanza un error si algo no cuadra, en vez de dejar pasar datos corruptos.

    Parámetros:
        reglas: el objeto cargado desde el JSON, cuyo tipo aún no confirmamos.
    """

    if not isinstance(reglas, dict):
        raise ValueError(
            "El archivo de reglas debe contener un objeto JSON (diccionario), "
            "no una lista ni otro tipo de dato."
        )

    for extension, categoria in reglas.items():
        if not isinstance(extension, str) or not extension.startswith("."):
            raise ValueError(
                f"La clave '{extension}' no es una extensión válida "
                f"(debe ser un texto que empiece por un punto, como '.pdf')."
            )

        if not isinstance(categoria, str):
            raise ValueError(
                f"El valor para '{extension}' debe ser un texto (nombre de carpeta), "
                f"no {type(categoria).__name__}."
            )