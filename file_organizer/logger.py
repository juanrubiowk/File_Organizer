# file_organizer/logger.py

import logging
from pathlib import Path


def configurar_logger(ruta_log="logs/organizer.log"):
    """
    Configura y devuelve un logger que escribe tanto en consola como
    en un archivo de texto, para llevar un registro de todo lo que
    hace el programa (qué se movió, qué falló, qué se ignoró).

    Parámetros:
        ruta_log (str o Path): ruta donde se guardará el archivo de log.

    Retorna:
        logging.Logger: el objeto logger ya configurado, listo para usar.
    """

    ruta_log = Path(ruta_log)

    # Nos aseguramos de que la carpeta "logs/" exista antes de escribir
    # el archivo dentro, igual que hicimos con "config/" en config.py.
    ruta_log.parent.mkdir(parents=True, exist_ok=True)

    # getLogger con un nombre concreto (en vez de logging.getLogger() a secas)
    # evita que, si este módulo se importa varias veces o desde distintos
    # sitios, se dupliquen las líneas o se mezcle con logs de otras librerías.
    logger = logging.getLogger("file_organizer")

    # Establecemos el nivel mínimo de gravedad que queremos capturar.
    # INFO significa: "guarda cosas normales (INFO) y también las graves
    # (WARNING, ERROR)", pero ignora detalles muy finos (DEBUG).
    logger.setLevel(logging.INFO)

    # Este "if" es importante: si esta función se llama más de una vez
    # (por ejemplo, porque el programa la ejecuta dos veces en la misma
    # sesión), sin este control se irían acumulando handlers duplicados
    # y cada mensaje se imprimiría varias veces.
    if logger.handlers:
        return logger

    # El formato define cómo se ve cada línea del log.
    # Ejemplo real que generaría: "2025-06-10 14:32:01 - INFO - Movido: foto.jpg -> Images/"
    formato = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Un "handler" es quien decide A DÓNDE va cada mensaje.
    # Este primero escribe en el archivo .log en disco.
    handler_archivo = logging.FileHandler(ruta_log, encoding="utf-8")
    handler_archivo.setFormatter(formato)

    # Este segundo handler imprime los mismos mensajes en la terminal,
    # para que el usuario vea en tiempo real lo que está pasando
    # sin tener que abrir el archivo de log.
    handler_consola = logging.StreamHandler()
    handler_consola.setFormatter(formato)

    # Añadimos ambos handlers al logger: cada mensaje que se registre
    # se enviará automáticamente a los dos sitios (archivo + consola).
    logger.addHandler(handler_archivo)
    logger.addHandler(handler_consola)

    return logger