# main.py

import argparse
from pathlib import Path

from file_organizer.config import cargar_reglas
from file_organizer.scanner import obtener_archivos
from file_organizer.classifier import clasificar_archivo
from file_organizer.organizer import mover_archivo
from file_organizer.logger import configurar_logger


def parsear_argumentos():
    """
    Define y lee los argumentos que el usuario escribe en la terminal.

    Retorna:
        argparse.Namespace: objeto con los valores leídos, por ejemplo
                             args.carpeta y args.dry_run.
    """

    # ArgumentParser es el objeto que sabe leer lo que el usuario escribe
    # después de "python main.py". description aparece si el usuario
    # ejecuta "python main.py --help".
    parser = argparse.ArgumentParser(
        description="Organiza automáticamente los archivos de una carpeta según su extensión."
    )

    # Este es un argumento POSICIONAL (obligatorio, sin guiones):
    # el usuario simplemente escribe la ruta, por ejemplo:
    # python main.py C:\Users\Juan\Descargas
    parser.add_argument(
        "carpeta",
        type=str,
        help="Ruta de la carpeta que se quiere organizar.",
    )

    # Este es un argumento OPCIONAL (con guiones --), tipo bandera:
    # action="store_true" significa que si el usuario escribe --dry-run,
    # el valor de args.dry_run será True; si no lo escribe, será False.
    # No hace falta que el usuario pase ningún valor detrás, es solo un "sí/no".
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula la organización sin mover ningún archivo de verdad.",
    )

    # Argumento opcional para indicar dónde está el rules.json,
    # con un valor por defecto razonable si el usuario no dice nada.
    parser.add_argument(
        "--reglas",
        type=str,
        default="config/rules.json",
        help="Ruta al archivo de reglas (por defecto: config/rules.json).",
    )

    # parse_args() lee sys.argv (lo que el usuario escribió realmente
    # en la terminal) y lo convierte en este objeto Namespace.
    return parser.parse_args()


def organizar_carpeta(carpeta, ruta_reglas, dry_run, logger):
    """
    Orquesta el proceso completo: carga reglas, escanea, clasifica
    y mueve (o simula) cada archivo encontrado.

    Parámetros:
        carpeta (str): ruta de la carpeta a organizar.
        ruta_reglas (str): ruta al archivo rules.json.
        dry_run (bool): si True, no mueve nada, solo muestra qué haría.
        logger (logging.Logger): logger ya configurado, para registrar eventos.
    """

    reglas = cargar_reglas(ruta_reglas)
    archivos = obtener_archivos(carpeta)

    if not archivos:
        logger.info(f"No se encontraron archivos para organizar en '{carpeta}'.")
        return

    if dry_run:
        logger.info("=== MODO DRY-RUN: no se moverá ningún archivo ===")

    for archivo in archivos:
        categoria = clasificar_archivo(archivo, reglas)

        # Aquí es donde realmente se decide si se mueve de verdad o se simula,
        # porque mover_archivo() ya sabe manejar ambos casos internamente.
        ruta_destino = mover_archivo(archivo, categoria, carpeta, dry_run=dry_run)

        if dry_run:
            # En simulación, mostramos la ruta relativa a la carpeta base
            # para que se lea limpio, por ejemplo "Images/foto.jpg"
            # en vez de una ruta absoluta larguísima.
            ruta_relativa = ruta_destino.relative_to(carpeta)
            logger.info(f"{archivo.name:<20} → {ruta_relativa}")
        else:
            logger.info(f"Movido: {archivo.name} → {categoria}/")


def main():
    """
    Punto de entrada del programa. Se ejecuta al hacer:
    python main.py <carpeta> [--dry-run] [--reglas ruta]
    """

    args = parsear_argumentos()
    logger = configurar_logger()

    try:
        organizar_carpeta(
            carpeta=args.carpeta,
            ruta_reglas=args.reglas,
            dry_run=args.dry_run,
            logger=logger,
        )
    except (FileNotFoundError, NotADirectoryError, ValueError) as error:
        # Capturamos aquí los errores "esperables" que ya identificamos
        # en scanner.py y config.py, para mostrarlos de forma clara
        # en vez de que el usuario vea un traceback de Python.
        logger.error(str(error))


# Este "if" es un patrón estándar de Python: el código de dentro
# solo se ejecuta si el archivo se corre directamente
# (python main.py), no si alguien lo importa desde otro archivo
# (por ejemplo, en los tests).
if __name__ == "__main__":
    main()