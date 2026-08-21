# file_organizer/organizer.py

import shutil
from pathlib import Path


def mover_archivo(archivo, categoria, ruta_base, dry_run=False):
    """
    Mueve un archivo a la subcarpeta correspondiente a su categoría.
    Si dry_run es True, no mueve nada, solo devuelve la información
    de lo que HARÍA (para poder imprimirlo en pantalla sin tocar disco).

    Parámetros:
        archivo (Path): archivo a mover (viene de scanner.py).
        categoria (str): nombre de la categoría (viene de classifier.py),
                          por ejemplo "Images" o "Documents".
        ruta_base (Path): carpeta raíz donde se está organizando
                           (la misma que se escaneó en scanner.py).
        dry_run (bool): si es True, simula la acción sin mover el archivo.

    Retorna:
        Path: la ruta destino final del archivo (exista ya o no todavía).
    """

    ruta_base = Path(ruta_base)

    # La carpeta destino es "ruta_base/categoria", por ejemplo
    # "Descargas/Images". La construimos con el operador "/" de pathlib,
    # que concatena rutas de forma legible.
    carpeta_destino = ruta_base / categoria

    # Calculamos cuál sería la ruta final del archivo dentro de esa carpeta,
    # gestionando colisiones de nombre (ver la función de abajo).
    ruta_destino = _resolver_colision(carpeta_destino / archivo.name)

    # En modo simulación, no tocamos el disco para nada: ni creamos carpetas
    # ni movemos archivos. Solo devolvemos dónde ACABARÍA el archivo,
    # para que main.py pueda imprimirlo.
    if dry_run:
        return ruta_destino

    # mkdir crea la carpeta destino si no existe.
    # parents=True crea también carpetas intermedias si hicieran falta.
    # exist_ok=True evita un error si la carpeta ya existía de antes.
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    # shutil.move hace el movimiento real del archivo (funciona incluso
    # entre discos distintos, a diferencia de Path.rename en algunos casos).
    shutil.move(str(archivo), str(ruta_destino))

    return ruta_destino


def _resolver_colision(ruta_destino):
    """
    Si ya existe un archivo con ese nombre en el destino, genera un nombre
    alternativo añadiendo un número, en vez de sobrescribir el archivo existente.

    Ejemplo: si "foto.jpg" ya existe, prueba "foto (1).jpg", luego "foto (2).jpg", etc.

    Parámetros:
        ruta_destino (Path): ruta destino original, antes de comprobar colisiones.

    Retorna:
        Path: una ruta que no colisiona con ningún archivo existente.
    """

    # Si el destino no existe todavía, no hay nada que resolver.
    if not ruta_destino.exists():
        return ruta_destino

    # .stem es el nombre sin extensión (por ejemplo "foto" de "foto.jpg").
    # .suffix es la extensión con el punto (por ejemplo ".jpg").
    # Los guardamos aparte porque vamos a reconstruir el nombre varias veces.
    carpeta = ruta_destino.parent
    nombre_base = ruta_destino.stem
    extension = ruta_destino.suffix

    contador = 1

    # Vamos probando "foto (1).jpg", "foto (2).jpg"... hasta encontrar
    # un nombre que no exista todavía. El bucle siempre termina porque
    # en algún momento el contador genera un nombre que no existe.
    nueva_ruta = carpeta / f"{nombre_base} ({contador}){extension}"

    while nueva_ruta.exists():
        contador += 1
        nueva_ruta = carpeta / f"{nombre_base} ({contador}){extension}"

    return nueva_ruta