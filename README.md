BIOIMÁGENES

Librería Python para el procesamiento, análisis y visualización de imágenes digitales y médicas. Permite trabajar con radiografías, tomografías y termografías a través de una jerarquía de clases orientada a objetos.

DESCRIPCIÓN GENERAL
El proyecto implementa una biblioteca de procesamiento de imágenes médicas organizada en tres capas:

Core: 
    clases base Imagen, Info e Historial que proveen la estructura común a todas las imágenes.
Médicas:
    clases especializadas ImagenRadiografia, ImagenTomografica e imagen_termografica que extienden la clase base con operaciones propias de cada modalidad.
Filtros:
    módulo de filtrado aplicable sobre imágenes.

Cada operación realizada sobre una imagen queda registrada automáticamente en un historial de cambios.
Instalación

REQUISITOS PREVIOS:
    Python 3.10 o superior
    pip

PASOS:
- Clonar el repositorio:
    bashgit clone https://github.com/tu-usuario/Proyecto-Integrador-PDA.git
    cd Proyecto-Integrador-PDA

- Crear y activar un entorno virtual:
    bashpython -m venv venv
    venv\Scripts\activate

- Instalar el paquete en modo editable:
    bashpip install -e .
    Esto instalará también las dependencias necesarias: numpy, matplotlib, opencv-python y pydicom.

ESTRUCTURA DE CARPETAS:
Proyecto-Integrador-PDA/
│
├── src/
│   └── bioimagenes/
│       ├── core/
│       │   ├── imagen.py          # Clase base Imagen
│       │   ├── info.py            # Clase Info (metadatos)
│       │   └── historial.py       # Clase Historial
│       ├── medicas/
│       │   ├── imagen_radiografia.py
│       │   ├── imagen_tomografia.py
│       │   └── imagen_termografica.py
│       └── filtros/
│           └── filtro.py
│
├── tests/
│   ├── test_imagen.py
│   ├── test_info.py
│   ├── test_historial.py
│   ├── test_radiografia.py
│   ├── test_tomografia.py
│   └── test_termografica.py
│
├── docs/
│   └── uml/
│       └── Diagrama UML.png
│
├── pyproject.toml
└── README.md

EJECUTAR LOS TESTS:
- Desde la raíz del proyecto, con el entorno virtual activado:
    bashpytest
- Para ver más detalle por test:
    bashpytest -v
- Para ejecutar solo los tests de una clase en particular:
    bashpytest tests/test_radiografia.py
    pytest tests/test_tomografia.py

EJEMPLO MÍNIMO DE USO

- Radiografía:
pythonimport numpy as np
import matplotlib.pyplot as plt
from bioimagenes.medicas.imagen_radiografia import ImagenRadiografia

# Cargar imagen (debe ser 2D, escala de grises)
data = plt.imread("docs/mi_radiografia.png")

# Crear instancia
img = ImagenRadiografia(data, tipo_estudio="Torax", brillo=0)

# Aplicar operaciones
contraste  = img.mejorar_contraste(factor=1.5)
invertida  = img.invertir_intensidades()
ecualizada = img.ecualizar_intensidades()

# Visualizar resultado
ecualizada.visualizar()

- Tomografía
pythonimport numpy as np
from bioimagenes.medicas.imagen_tomografia import ImagenTomografica

data = np.random.randint(0, 256, (256, 256, 30), dtype=np.uint8)

img = ImagenTomografica(data)
img.visualizar()

- Termografía
pythonimport numpy as np
from bioimagenes.medicas.imagen_termografica import imagen_termografica

data = np.random.randint(0, 256, (128, 128), dtype=np.uint8)

img = imagen_termografica(data)
img.mapa_calor()