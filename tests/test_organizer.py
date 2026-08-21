# tests/test_organizer.py

from file_organizer.organizer import mover_archivo


def test_mover_archivo_real(tmp_path):
    """
    Comprueba el caso normal: el archivo se mueve de verdad
    a la carpeta de su categoría.
    """

    # Creamos un archivo de origen dentro de la carpeta temporal.
    archivo_origen = tmp_path / "foto.jpg"
    archivo_origen.write_text("contenido falso")

    resultado = mover_archivo(archivo_origen, "Images", tmp_path, dry_run=False)

    # El archivo debe existir ahora en el destino...
    assert resultado.exists()
    # ...y ya NO debe existir en el origen, porque se movió (no se copió).
    assert not archivo_origen.exists()
    # Comprobamos también que la ruta final es la esperada.
    assert resultado == tmp_path / "Images" / "foto.jpg"


def test_mover_archivo_dry_run_no_toca_disco(tmp_path):
    """
    En modo dry_run, la función debe devolver la ruta destino
    SIN mover el archivo ni crear ninguna carpeta.
    """

    archivo_origen = tmp_path / "foto.jpg"
    archivo_origen.write_text("contenido falso")

    resultado = mover_archivo(archivo_origen, "Images", tmp_path, dry_run=True)

    # El archivo original NO debe haberse movido.
    assert archivo_origen.exists()
    # La carpeta "Images" no debe haberse creado siquiera.
    assert not (tmp_path / "Images").exists()
    # Pero el resultado sí debe indicar dónde ACABARÍA el archivo.
    assert resultado == tmp_path / "Images" / "foto.jpg"


def test_mover_archivo_resuelve_colision_de_nombre(tmp_path):
    """
    Si ya existe un archivo con el mismo nombre en el destino,
    el nuevo archivo debe renombrarse en vez de sobrescribir.
    """

    # Preparamos la carpeta destino con un archivo YA existente ahí.
    carpeta_destino = tmp_path / "Images"
    carpeta_destino.mkdir()
    (carpeta_destino / "foto.jpg").write_text("archivo original, no tocar")

    # Ahora movemos un archivo NUEVO que también se llama "foto.jpg".
    archivo_origen = tmp_path / "foto.jpg"
    archivo_origen.write_text("archivo nuevo")

    resultado = mover_archivo(archivo_origen, "Images", tmp_path, dry_run=False)

    # El archivo original no debe haberse sobrescrito.
    assert (carpeta_destino / "foto.jpg").read_text() == "archivo original, no tocar"
    # El nuevo debe haberse guardado con un nombre distinto.
    assert resultado.name == "foto (1).jpg"
    assert resultado.read_text() == "archivo nuevo"


def test_mover_archivo_crea_carpeta_destino_si_no_existe(tmp_path):
    """
    Si la carpeta de categoría (por ejemplo "Music") no existe todavía,
    mover_archivo() debe crearla automáticamente.
    """

    archivo_origen = tmp_path / "cancion.mp3"
    archivo_origen.write_text("contenido falso")

    # Antes de mover, "Music" no existe en absoluto.
    assert not (tmp_path / "Music").exists()

    mover_archivo(archivo_origen, "Music", tmp_path, dry_run=False)

    # Después de mover, la carpeta debe haberse creado sola.
    assert (tmp_path / "Music").exists()