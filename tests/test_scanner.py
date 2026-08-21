import pytest
from file_organizer.scanner import obtener_archivos


def test_obtener_archivos_lista_solo_archivos(tmp_path):
    """
    Comprueba que obtener_archivos() devuelve los archivos de una carpeta,
    pero ignora las subcarpetas que haya dentro.
    """

    # tmp_path es una "fixture" que nos da pytest automáticamente:
    # es una carpeta temporal real en disco, creada solo para este test,
    # que se borra sola al terminar. Así no ensuciamos tu proyecto real
    # ni dependemos de que exista una carpeta concreta en tu ordenador.

    # Creamos dos archivos de prueba dentro de esa carpeta temporal.
    (tmp_path / "foto.jpg").write_text("contenido falso")
    (tmp_path / "factura.pdf").write_text("contenido falso")

    # Creamos también una subcarpeta, para comprobar que se ignora.
    (tmp_path / "subcarpeta").mkdir()

    resultado = obtener_archivos(tmp_path)

    # Convertimos a un set de nombres porque no nos importa el ORDEN
    # en que vienen los archivos, solo que estén los correctos.
    nombres_resultado = {archivo.name for archivo in resultado}

    assert nombres_resultado == {"foto.jpg", "factura.pdf"}


def test_obtener_archivos_ignora_ocultos(tmp_path):
    """
    Comprueba que los archivos ocultos (que empiezan por punto)
    no aparecen en el resultado.
    """

    (tmp_path / "visible.txt").write_text("contenido falso")
    (tmp_path / ".oculto").write_text("contenido falso")

    resultado = obtener_archivos(tmp_path)
    nombres_resultado = {archivo.name for archivo in resultado}

    assert nombres_resultado == {"visible.txt"}


def test_obtener_archivos_carpeta_vacia(tmp_path):
    """
    Si la carpeta existe pero no tiene nada dentro, debe devolver
    una lista vacía, no un error.
    """

    resultado = obtener_archivos(tmp_path)
    assert resultado == []


def test_obtener_archivos_carpeta_inexistente(tmp_path):
    """
    Si la ruta no existe, la función debe lanzar FileNotFoundError,
    tal como decidimos en scanner.py.
    """

    ruta_falsa = tmp_path / "esta_carpeta_no_existe"

    # pytest.raises comprueba que, al ejecutar el código de dentro del "with",
    # se lance exactamente esa excepción. Si no se lanza ninguna, o se lanza
    # una distinta, el test falla.
    with pytest.raises(FileNotFoundError):
        obtener_archivos(ruta_falsa)


def test_obtener_archivos_ruta_no_es_carpeta(tmp_path):
    """
    Si la ruta existe pero es un archivo (no una carpeta),
    debe lanzar NotADirectoryError.
    """

    archivo_no_carpeta = tmp_path / "esto_es_un_archivo.txt"
    archivo_no_carpeta.write_text("soy un archivo, no una carpeta")

    with pytest.raises(NotADirectoryError):
        obtener_archivos(archivo_no_carpeta)