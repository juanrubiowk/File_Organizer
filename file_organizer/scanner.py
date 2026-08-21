from pathlib import Path


def obtener_archivos(ruta_carpeta):
    """
    Devuelve una lista de archivos (no carpetas) dentro de la ruta indicada.

    Parámetros:
        ruta_carpeta (str o Path): carpeta que queremos escanear.

    Retorna:
        list[Path]: lista de objetos Path, uno por cada archivo encontrado.
    """

    # Convertimos el string a un objeto Path por si nos llega como texto plano.
    # Si ya es un Path, esto no hace nada raro, simplemente lo "reconfirma".
    carpeta = Path(ruta_carpeta)

    # Comprobamos que la ruta exista antes de seguir.
    # Si no existe, lanzamos un error claro en vez de dejar que falle más adelante
    # con un mensaje confuso.
    if not carpeta.exists():
        raise FileNotFoundError(f"La carpeta '{carpeta}' no existe.")

    if not carpeta.is_dir():
        raise NotADirectoryError(f"'{carpeta}' no es una carpeta.")

    lista_archivos = []

    # iterdir() nos da TODO lo que hay dentro: archivos y subcarpetas.
    # Por eso filtramos con is_file() para quedarnos solo con archivos.
    for elemento in carpeta.iterdir():

        # Ignoramos archivos ocultos (los que empiezan por punto, típico en Linux/Mac,
        # como .DS_Store o .gitignore). No queremos organizar archivos de sistema.
        if elemento.name.startswith("."):
            continue

        if elemento.is_file():
            lista_archivos.append(elemento)

    return lista_archivos