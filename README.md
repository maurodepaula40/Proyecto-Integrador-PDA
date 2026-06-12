# Bioimagenes

Librería en Python para el procesamiento, análisis y visualización de imágenes digitales y médicas. El proyecto permite trabajar con imágenes generales y con estudios médicos como radiografías, tomografías y termografías, incorporando herramientas para cargar imágenes, modificar brillo y contraste, aplicar filtros, visualizar cortes y registrar cambios mediante historial.

---

## Índice

- [Descripción general](#descripción-general)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso básico](#uso-básico)
- [Clases principales](#clases-principales)
- [Pruebas](#pruebas)
- [Prueba de ImagenTomografica con archivo NIfTI](#prueba-de-imagentomografica-con-archivo-nifti)
- [Documentación](#documentación)
- [Notas importantes](#notas-importantes)
- [Autoría](#autoría)

---

## Descripción general

`bioimagenes` es una librería orientada a la manipulación de imágenes biomédicas. El objetivo del proyecto es centralizar funcionalidades básicas y específicas para distintos tipos de imágenes médicas, manteniendo una estructura clara, reutilizable y extensible.

El proyecto incluye:

- Carga de imágenes 2D y volumétricas.
- Manejo de metadatos mediante la clase `Info`.
- Registro de modificaciones mediante la clase `Historial`.
- Aplicación de filtros por convolución.
- Procesamiento específico de radiografías, tomografías y termografías.
- Visualización de imágenes, cortes tomográficos y reconstrucciones interactivas.

---

## Estructura del proyecto

La estructura principal del proyecto es la siguiente:

```text
Proyecto-Integrador-PDA/
│
├── docs/
│   ├── api_reference.md
│   └── uml/
│       └── Diagrama UML.png
│
├── src/
│   └── bioimagenes/
│       ├── core/
│       │   ├── historial.py
│       │   ├── imagen.py
│       │   └── info.py
│       │
│       ├── filtros/
│       │   └── filtro.py
│       │
│       ├── medicas/
│       │   ├── imagen_radiografia.py
│       │   ├── imagen_termografica.py
│       │   └── imagen_tomografia.py
│       │
│       ├── utils/
│       └── visualizacion/
│           ├── histogramas.py
│           └── visualizar.py
│
└── tests/
│    └── imagenes_test/
         ├──carpeta_tc
            └── AC421363f.nii

│    └──test_filtro
│    └──test_historial
│    └──test_imagen
│    └──test_info
│    └──test_radiografia
│    └──test_termografica
│    └──test_tomografia
│       
├── .gitignore
├── LICENSE.txt
├── pyproject.toml
└── README.md

```

---

## Requisitos

El proyecto requiere Python 3.10 o superior.

Dependencias principales:

```text
numpy
matplotlib
opencv-python
pydicom
nibabel
Pillow
scipy
plotly
scikit-learn
pytest
```

> Nota: aunque algunas dependencias pueden no aparecer en el archivo de configuración del paquete, se utilizan dentro del código fuente. Por ejemplo, `nibabel` se usa para cargar archivos `.nii`, `scipy` para convoluciones, `plotly` para reconstrucción tomográfica interactiva y `scikit-learn` para agrupamiento de radiografías.

---

## Instalación

Primero, clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd Proyecto-Integrador-PDA
```

Crear y activar un entorno virtual:

### En Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### En Linux o macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar las dependencias:

```bash
pip install numpy matplotlib opencv-python pydicom nibabel Pillow scipy plotly scikit-learn pytest
```

Si el proyecto tiene un archivo `pyproject.toml`, `setup.py` o configuración equivalente, también puede instalarse en modo editable:

```bash
pip install -e .
```

---

## Uso básico

Ejemplo de carga de una imagen 2D:

```python
from bioimagenes.core.imagen import Imagen

imagen = Imagen.cargar("ruta/a/imagen.png")
imagen.visualizar()
```

Ejemplo de uso de metadatos:

```python
from bioimagenes.core.info import Info

info = Info({
    "dimensiones": (512, 512, 1),
    "brillo": 0,
    "tipo_estudio": "radiografia"
})

print(info["dimensiones"])
print(info.cantidad_voxel())
```

Ejemplo de imagen tomográfica:

```python
from bioimagenes.medicas.imagen_tomografia import ImagenTomografica

ruta = "tests/imagenes_test/AC421363f.nii"
tomografia = ImagenTomografica.cargar(ruta)

tomografia.seleccionar_corte(50)
tomografia.mostrar_corte()
```

---

## Clases principales

### `Imagen`

Clase base para representar imágenes mediante arreglos de NumPy.

Funcionalidades principales:

- Cargar imágenes desde archivos.
- Acceder a los datos de la imagen.
- Visualizar imágenes.
- Convertir a blanco y negro.
- Aplicar filtros.
- Normalizar matrices.

Formatos soportados por el método `cargar()`:

- `.png`
- `.jpg`
- `.jpeg`
- `.nii`
- `.gz`
- `.dcm`

---

### `Info`

Clase para almacenar metadatos asociados a una imagen.

Metadatos principales:

- `dimensiones`
- `brillo`
- `cortada`
- `tipo_estudio`
- `tamano_voxel`
- `historial`

Permite acceder a los valores de forma similar a un diccionario:

```python
info["brillo"]
"brillo" in info
```

---

### `Historial`

Clase encargada de registrar los cambios aplicados sobre una imagen.

Permite:

- Agregar modificaciones.
- Consultar el último cambio.
- Recorrer el historial.
- Obtener la cantidad de cambios registrados.

---

### `Filtro`

Clase para aplicar filtros mediante convolución.

Permite crear filtros con un nombre y tamaño determinado, obtener su kernel y aplicarlo sobre una imagen.

---

### `ImagenRadiografia`

Clase especializada para trabajar con radiografías.

Incluye métodos para:

- Ajustar brillo.
- Mejorar contraste.
- Invertir intensidades.
- Ecualizar intensidades.
- Detectar bordes.
- Seleccionar una región de interés.
- Visualizar agrupamientos de imágenes mediante PCA y K-Means.

---

### `ImagenTermografica`

Clase especializada para imágenes termográficas.

Incluye métodos para:

- Convertir intensidades a temperatura.
- Generar mapas de calor.
- Segmentar por rangos de temperatura.
- Detectar puntos calientes.

---

### `ImagenTomografica`

Clase especializada para imágenes tomográficas volumétricas.

Incluye métodos para:

- Obtener cortes de un volumen 3D.
- Seleccionar un corte actual.
- Mostrar cortes tomográficos.
- Ajustar ventanas de visualización.
- Aplicar presets según tejido.
- Visualizar tejidos coloreados por rango de intensidad.
- Generar una reconstrucción interactiva de cortes en HTML.

Presets disponibles:

```python
"cerebro"
"hueso"
"pulmon"
"higado"
"tejido"
"angio"
```

---

## Pruebas

Las pruebas se ejecutan con `pytest` desde la raíz del proyecto:

```bash
pytest
```

También se puede ejecutar una carpeta completa o un archivo específico de pruebas. Por ejemplo:

```bash
pytest tests/
pytest tests/test_imagen_tomografia.py
```

> Si el archivo de test tiene otro nombre, reemplazar `test_imagen_tomografia.py` por el nombre correspondiente.

Si aparece un error de importación del paquete `bioimagenes`, verificar que el proyecto esté instalado en modo editable:

```bash
pip install -e .
```

En caso de no contar con instalación editable, puede definirse temporalmente el `PYTHONPATH` apuntando a la carpeta `src`.

### En Windows PowerShell

```powershell
$env:PYTHONPATH="src"
pytest
```

### En Linux o macOS

```bash
PYTHONPATH=src pytest
```

---

## Prueba de `ImagenTomografica` con archivo NIfTI

Para probar correctamente la clase `ImagenTomografica`, es necesario contar con una imagen tomográfica real en formato NIfTI.

El archivo requerido es:

```text
AC421363f.nii
```

Este archivo no se incluye directamente en el repositorio porque puede ser pesado. Antes de ejecutar los tests relacionados con tomografía, el usuario debe ubicar manualmente la imagen en la siguiente carpeta:

```text
Proyecto-Integrador-PDA\tests\imagenes_test\AC421363f.nii
```

La carpeta esperada es:

```text
Proyecto-Integrador-PDA\tests\imagenes_test
```

En caso de que la carpeta no exista, debe crearse manualmente:

```text
tests/imagenes_test/
```

Ejemplo de estructura esperada:

```text
Proyecto-Integrador-PDA/
└── tests/
    └── imagenes_test/
        └── AC421363f.nii
```

Una vez ubicada la imagen, ejecutar el test correspondiente a tomografía. Por ejemplo, si el archivo de prueba se llama `test_imagen_tomografia.py`:

```bash
pytest tests/test_imagen_tomografia.py
```

O bien ejecutar todos los tests:

```bash
pytest
```

> Importante: si el archivo `AC421363f.nii` no está en la carpeta indicada, los tests de `ImagenTomografica` que dependan de imágenes reales pueden fallar por archivo no encontrado.

---

## Documentación

La documentación del proyecto se encuentra en la carpeta `docs/`.

Incluye:

- `api_reference.md`: referencia de la API del proyecto.
- `docs/uml/Diagrama UML.png`: diagrama UML de la estructura de clases.

---

## Notas importantes

- No se recomienda subir archivos médicos pesados directamente al repositorio.
- Las imágenes de prueba grandes deben almacenarse localmente en `tests/imagenes_test/` o gestionarse mediante un sistema externo.
- Para evitar errores al subir el proyecto a GitHub, se recomienda excluir archivos pesados como `.nii`, `.nii.gz`, `.dcm` o grandes carpetas de imágenes mediante `.gitignore`.

Ejemplo recomendado para `.gitignore`:

```gitignore
# Entornos virtuales
.venv/
venv/

# Caché de Python
__pycache__/
*.pyc
.pytest_cache/

# Archivos médicos pesados
*.nii
*.nii.gz
*.dcm

# Imágenes de prueba locales pesadas
tests/imagenes_test/

# Archivos generados
reconstruccion_tomografia.html
```

---

## Autoría

Proyecto Integrador PDA.

Librería desarrollada con fines académicos para el procesamiento y análisis de bioimágenes.
# Bioimagenes

Librería en Python para el procesamiento, análisis y visualización de imágenes digitales y médicas. El proyecto permite trabajar con imágenes generales y con estudios médicos como radiografías, tomografías y termografías, incorporando herramientas para cargar imágenes, modificar brillo y contraste, aplicar filtros, visualizar cortes y registrar cambios mediante historial.

---

## Índice

- [Descripción general](#descripción-general)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso básico](#uso-básico)
- [Clases principales](#clases-principales)
- [Pruebas](#pruebas)
- [Prueba de ImagenTomografica con archivo NIfTI](#prueba-de-imagentomografica-con-archivo-nifti)
- [Documentación](#documentación)
- [Notas importantes](#notas-importantes)
- [Autoría](#autoría)

---

## Descripción general

`bioimagenes` es una librería orientada a la manipulación de imágenes biomédicas. El objetivo del proyecto es centralizar funcionalidades básicas y específicas para distintos tipos de imágenes médicas, manteniendo una estructura clara, reutilizable y extensible.

El proyecto incluye:

- Carga de imágenes 2D y volumétricas.
- Manejo de metadatos mediante la clase `Info`.
- Registro de modificaciones mediante la clase `Historial`.
- Aplicación de filtros por convolución.
- Procesamiento específico de radiografías, tomografías y termografías.
- Visualización de imágenes, cortes tomográficos y reconstrucciones interactivas.

---

## Estructura del proyecto

La estructura principal del proyecto es la siguiente:

```text
Proyecto-Integrador-PDA/
│
├── docs/
│   ├── api_reference.md
│   └── uml/
│       └── Diagrama UML.png
│
├── src/
│   └── bioimagenes/
│       ├── core/
│       │   ├── historial.py
│       │   ├── imagen.py
│       │   └── info.py
│       │
│       ├── filtros/
│       │   └── filtro.py
│       │
│       ├── medicas/
│       │   ├── imagen_radiografia.py
│       │   ├── imagen_termografica.py
│       │   └── imagen_tomografia.py
│       │
│       ├── utils/
│       └── visualizacion/
│           ├── histogramas.py
│           └── visualizar.py
```
---

## Requisitos

El proyecto requiere Python 3.10 o superior.

Dependencias principales:

```text
numpy
matplotlib
opencv-python
pydicom
nibabel
Pillow
scipy
plotly
scikit-learn
pytest
```

> Nota: aunque algunas dependencias pueden no aparecer en el archivo de configuración del paquete, se utilizan dentro del código fuente. Por ejemplo, `nibabel` se usa para cargar archivos `.nii`, `scipy` para convoluciones, `plotly` para reconstrucción tomográfica interactiva y `scikit-learn` para agrupamiento de radiografías.

---

## Instalación

Primero, clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd Proyecto-Integrador-PDA
```

Crear y activar un entorno virtual:

### En Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### En Linux o macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar las dependencias:

```bash
pip install numpy matplotlib opencv-python pydicom nibabel Pillow scipy plotly scikit-learn pytest
```

El proyecto tiene un archivo `pyproject.toml`, por ende también puede instalarse en modo editable:

```bash
pip install -e .
```

---

## Uso básico

Ejemplo de carga de una imagen 2D:

```python
from bioimagenes.core.imagen import Imagen

imagen = Imagen.cargar("ruta/a/imagen.png")
imagen.visualizar()
```

Ejemplo de uso de metadatos:

```python
from bioimagenes.core.info import Info

info = Info({
    "dimensiones": (512, 512, 1),
    "brillo": 0,
    "tipo_estudio": "radiografia"
})

print(info["dimensiones"])
print(info.cantidad_voxel())
```

Ejemplo de imagen tomográfica:

```python
from bioimagenes.medicas.imagen_tomografia import ImagenTomografica

ruta = "tests/imagenes_test/AC421363f.nii"
tomografia = ImagenTomografica.cargar(ruta)

tomografia.seleccionar_corte(50)
tomografia.mostrar_corte()
```

---

## Clases principales

### `Imagen`

Clase base para representar imágenes mediante arreglos de NumPy.

Funcionalidades principales:

- Cargar imágenes desde archivos.
- Acceder a los datos de la imagen.
- Visualizar imágenes.
- Convertir a blanco y negro.
- Aplicar filtros.
- Normalizar matrices.

Formatos soportados por el método `cargar()`:

- `.png`
- `.jpg`
- `.jpeg`
- `.nii`
- `.gz`
- `.dcm`

---

### `Info`

Clase para almacenar metadatos asociados a una imagen.

Metadatos principales:

- `dimensiones`
- `brillo`
- `cortada`
- `tipo_estudio`
- `tamano_voxel`
- `historial`

Permite acceder a los valores de forma similar a un diccionario:

```python
info["brillo"]
"brillo" in info
```

---

### `Historial`

Clase encargada de registrar los cambios aplicados sobre una imagen.

Permite:

- Agregar modificaciones.
- Consultar el último cambio.
- Recorrer el historial.
- Obtener la cantidad de cambios registrados.

---

### `Filtro`

Clase para aplicar filtros mediante convolución.

Permite crear filtros con un nombre y tamaño determinado, obtener su kernel y aplicarlo sobre una imagen.

---

### `ImagenRadiografia`

Clase especializada para trabajar con radiografías.

Incluye métodos para:

- Ajustar brillo.
- Mejorar contraste.
- Invertir intensidades.
- Ecualizar intensidades.
- Detectar bordes.
- Seleccionar una región de interés.
- Visualizar agrupamientos de imágenes mediante PCA y K-Means.

---

### `ImagenTermografica`

Clase especializada para imágenes termográficas.

Incluye métodos para:

- Convertir intensidades a temperatura.
- Generar mapas de calor.
- Segmentar por rangos de temperatura.
- Detectar puntos calientes.

---

### `ImagenTomografica`

Clase especializada para imágenes tomográficas volumétricas.

Incluye métodos para:

- Obtener cortes de un volumen 3D.
- Seleccionar un corte actual.
- Mostrar cortes tomográficos.
- Ajustar ventanas de visualización.
- Aplicar presets según tejido.
- Visualizar tejidos coloreados por rango de intensidad.
- Generar una reconstrucción interactiva de cortes en HTML.

Presets disponibles:

```python
"cerebro"
"hueso"
"pulmon"
"higado"
"tejido"
"angio"
```

---

## Pruebas

Las pruebas se ejecutan con `pytest` desde la raíz del proyecto:

```bash
pytest
```

También se puede ejecutar una carpeta completa o un archivo específico de pruebas. Por ejemplo:

```bash
pytest tests/
pytest tests/test_imagen_tomografia.py
```

> Si el archivo de test tiene otro nombre, reemplazar `test_imagen_tomografia.py` por el nombre correspondiente.

Si aparece un error de importación del paquete `bioimagenes`, verificar que el proyecto esté instalado en modo editable:

```bash
pip install -e .
```

En caso de no contar con instalación editable, puede definirse temporalmente el `PYTHONPATH` apuntando a la carpeta `src`.

### En Windows PowerShell

```powershell
$env:PYTHONPATH="src"
pytest
```

### En Linux o macOS

```bash
PYTHONPATH=src pytest
```

---

## Prueba de `ImagenTomografica` con archivo NIfTI

Para probar correctamente la clase `ImagenTomografica`, es necesario contar con una imagen tomográfica real en formato NIfTI.

El archivo requerido es:

```text
AC421363f.nii
```

Este archivo no se incluye directamente en el repositorio porque puede ser pesado. Antes de ejecutar los tests relacionados con tomografía, el usuario debe ubicar manualmente la imagen en la siguiente carpeta:

```text
Proyecto-Integrador-PDA\tests\imagenes_test\AC421363f.nii
```

La carpeta esperada es:

```text
Proyecto-Integrador-PDA\tests\imagenes_test
```

En caso de que la carpeta no exista, debe crearse manualmente:

```text
tests/imagenes_test/
```

Ejemplo de estructura esperada:

```text
Proyecto-Integrador-PDA/
└── tests/
    └── imagenes_test/
        └── AC421363f.nii
```

Una vez ubicada la imagen, ejecutar el test correspondiente a tomografía. Por ejemplo, si el archivo de prueba se llama `test_imagen_tomografia.py`:

```bash
pytest tests/test_imagen_tomografia.py
```

O bien ejecutar todos los tests:

```bash
pytest
```

> Importante: si el archivo `AC421363f.nii` no está en la carpeta indicada, los tests de `ImagenTomografica` que dependan de imágenes reales pueden fallar por archivo no encontrado.

---

## Documentación

La documentación del proyecto se encuentra en la carpeta `docs/`.

Incluye:

- `api_reference.md`: referencia de la API del proyecto.
- `docs/uml/Diagrama UML.png`: diagrama UML de la estructura de clases.

---

## Notas importantes

- No se recomienda subir archivos médicos pesados directamente al repositorio.
- Las imágenes de prueba grandes deben almacenarse localmente en `tests/imagenes_test/` o gestionarse mediante un sistema externo.
- Para evitar errores al subir el proyecto a GitHub, se recomienda excluir archivos pesados como `.nii`, `.nii.gz`, `.dcm` o grandes carpetas de imágenes mediante `.gitignore`.

Ejemplo recomendado para `.gitignore`:

```gitignore
# Entornos virtuales
.venv/
venv/

# Caché de Python
__pycache__/
*.pyc
.pytest_cache/

# Archivos médicos pesados
*.nii
*.nii.gz
*.dcm

# Imágenes de prueba locales pesadas
tests/imagenes_test/

# Archivos generados
reconstruccion_tomografia.html
```

---

## Autoría

Proyecto desarrollado por:

- Valentino de Paula
- Belén Echenique

Proyecto Integrador PDA.

Librería desarrollada con fines académicos para el procesamiento y análisis de bioimágenes.