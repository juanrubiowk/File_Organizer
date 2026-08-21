File-Organizer

Organiza automáticamente los archivos de una carpeta en subcarpetas según su tipo (Imágenes, Documentos, Música, Vídeos, etc.), sin tener que moverlos a mano uno por uno.

¿Qué hace exactamente?

Imagina que tienes una carpeta de Descargas llena de todo tipo de archivos mezclados: fotos, PDFs, canciones, vídeos... Este programa los revisa uno por uno y los mueve a su carpeta correspondiente automáticamente:

Antes:
Descargas/
├── foto.jpg
├── factura.pdf
├── cancion.mp3
└── video.mp4

Después:
Descargas/
├── Images/
│   └── foto.jpg
├── Documents/
│   └── factura.pdf
├── Music/
│   └── cancion.mp3
└── Videos/
    └── video.mp4
Características principales
Clasificación automática por tipo de archivo (extensión).
Reglas personalizables: puedes decidir qué extensión va a qué carpeta, editando un simple archivo de texto, sin tocar ni una línea de código.
Modo de simulación (--dry-run): te muestra qué haría el programa ANTES de mover nada de verdad. Ideal para probarlo con confianza la primera vez.
Protección contra sobrescritura: si ya existe un archivo con el mismo nombre en el destino, el nuevo se renombra automáticamente en lugar de borrar el anterior.
Registro de actividad: guarda un historial de todo lo que hace, por si necesitas revisar qué se movió y cuándo.
Requisitos
Tener Python instalado (versión 3.8 o superior). Puedes comprobarlo escribiendo en tu terminal:
  python --version
Instalación
Descarga o clona esta carpeta del proyecto en tu ordenador.
Abre una terminal (o símbolo del sistema) dentro de la carpeta del proyecto.
Instala la única dependencia necesaria:
   pip install -r requirements.txt

Y ya está. No hace falta ninguna configuración adicional.

Cómo usarlo
Paso 1: Pruébalo primero en modo seguro (recomendado)

Antes de mover ningún archivo de verdad, puedes simular el resultado:

python main.py "C:\Users\TuUsuario\Descargas" --dry-run

(En Mac o Linux, la ruta se escribiría distinto, por ejemplo /Users/TuUsuario/Descargas)

Esto te mostrará algo así en pantalla, sin mover absolutamente nada:

2026-08-21 10:15:32 - INFO - === MODO DRY-RUN: no se moverá ningún archivo ===
2026-08-21 10:15:32 - INFO - foto.jpg             → Images/foto.jpg
2026-08-21 10:15:32 - INFO - factura.pdf          → Documents/factura.pdf
2026-08-21 10:15:32 - INFO - cancion.mp3          → Music/cancion.mp3
Paso 2: Organiza de verdad

Si el resultado de la simulación te parece bien, ejecuta el mismo comando sin --dry-run:

python main.py "C:\Users\TuUsuario\Descargas"

Y esta vez sí, los archivos se moverán a sus carpetas correspondientes.

Personalizar qué va a dónde

La primera vez que ejecutes el programa, se crea automáticamente un archivo llamado rules.json dentro de la carpeta config/. Ábrelo con cualquier editor de texto (incluso el Bloc de notas) y edítalo a tu gusto:

json
{
    ".jpg": "Images",
    ".png": "Images",
    ".pdf": "Documents",
    ".docx": "Documents",
    ".mp3": "Music",
    ".mp4": "Videos",
    ".zip": "Compressed"
}

Cada línea significa "esta extensión va a esta carpeta". Puedes añadir, borrar o cambiar líneas libremente. Cualquier tipo de archivo que no hayas indicado se guardará en una carpeta llamada Others, para que nunca se quede nada sin organizar.

Preguntas frecuentes

¿Puede perder o borrar mis archivos? No. El programa nunca borra archivos. En el peor de los casos, un archivo se mueve a una carpeta distinta a la que esperabas, y siempre puedes deshacerlo manualmente. Además, si detecta que ya existe un archivo con el mismo nombre en el destino, no lo sobrescribe: guarda el nuevo con un nombre distinto (por ejemplo, foto (1).jpg).

¿Qué pasa si ejecuto el programa dos veces seguidas? No hay problema. La segunda vez simplemente no encontrará archivos nuevos que mover (ya estarán organizados), o organizará únicamente los archivos nuevos que hayas añadido desde la última vez.

¿Dónde puedo ver qué hizo el programa exactamente? En la carpeta logs/, se genera automáticamente un archivo organizer.log con el registro completo de cada ejecución, con fecha y hora.

¿Necesito saber programar para usarlo? No. Solo necesitas ejecutar el comando indicado en la terminal. Para personalizar las reglas, basta con editar un archivo de texto sencillo.

Ejecutar las pruebas automatizadas (para desarrolladores)

Si quieres verificar que todo el código funciona correctamente:

pytest
Estructura del proyecto
File-Organizer/
│
├── file_organizer/          Código fuente principal
│   ├── scanner.py            Encuentra los archivos en la carpeta
│   ├── classifier.py         Decide la categoría de cada archivo
│   ├── organizer.py          Mueve (o simula mover) cada archivo
│   ├── config.py             Carga y valida las reglas de clasificación
│   └── logger.py             Registra la actividad del programa
│
├── config/
│   └── rules.json             Reglas de clasificación (editable)
│
├── logs/
│   └── organizer.log          Historial de ejecuciones (se genera solo)
│
├── tests/                     Pruebas automatizadas
│
├── main.py                     Punto de entrada del programa
├── requirements.txt
└── README.md
Nota de seguridad

Se recomienda siempre ejecutar primero con --dry-run antes de organizar una carpeta importante, para confirmar que el resultado es el que esperas.