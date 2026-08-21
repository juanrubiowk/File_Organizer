from pathlib import Path


def clasificar_archivo(archivo, reglas):
    """
    Decide a qué categoría pertenece un archivo, según su extensión.

    Parámetros:
        archivo (Path): el archivo que queremos clasificar (viene de scanner.py).
        reglas (dict): diccionario que mapea extensión -> categoría.
                       Ejemplo: {".jpg": "Images", ".pdf": "Documents"}

    Retorna:
        str: el nombre de la categoría (carpeta destino).
             Si la extensión no está en las reglas, devuelve "Others".
    """

    # .suffix nos da la extensión CON el punto incluido, por ejemplo ".jpg".
    # Usamos .lower() porque no queremos que "Foto.JPG" y "foto.jpg"
    # acaben en carpetas distintas solo por las mayúsculas.
    extension = archivo.suffix.lower()

    # .get() es más seguro que reglas[extension], porque si la extensión
    # no existe en el diccionario, no lanza un error (KeyError),
    # simplemente devuelve el segundo argumento como valor por defecto.
    categoria = reglas.get(extension, "Others")

    return categoria