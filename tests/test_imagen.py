import sys
import os
#Esto hace lo mismo que el comando 'set PYTHONPATH=src' pero automáticamente
sys.path.append(os.path.abspath("src"))
from bioimagenes.core.imagen import Imagen
from bioimagenes.core.historial import Historial
from bioimagenes.core.info import Info
from PIL import Image as PILImage
import numpy as np
import matplotlib.pyplot as plt
import pytest

# Ruta de la imagen de prueba
RUTA_IMAGEN = "tests/imagenes_test/radiografias/216840111366964013829543166512013358092118761_02-089-145.png"


# ==========================================================
# FIXTURES (Estructuras base para reutilizar en los tests)
# ==========================================================

@pytest.fixture
def matriz_2d_valida():
    """Genera una matriz simulada 2D de 10x10 (Escala de grises)."""
    return np.random.randint(0, 256, size=(10, 10), dtype=np.uint8)

@pytest.fixture
def matriz_3d_rgb_valida():
    """Genera una matriz simulada 3D con 3 canales (Color RGB)."""
    return np.random.randint(0, 256, size=(10, 10, 3), dtype=np.uint8)


# ==========================================================
# 1. TESTS DEL CONSTRUCTOR Y VALIDACIONES DE SEGURIDAD
# ==========================================================

def test_inicializacion_correcta_2d(matriz_2d_valida):
    """Verifica que un objeto Imagen 2D se cree correctamente con sus propiedades encapsuladas."""
    img = Imagen(matriz_2d_valida)
    assert img.data is not None
    assert img.data.ndim == 2
    assert isinstance(img.historial, Historial)
    assert isinstance(img.info, Info)


def test_inicializacion_correcta_rgb(matriz_3d_rgb_valida):
    """Verifica que si recibe una imagen RGB, extraiga un solo canal para procesar."""
    img = Imagen(matriz_3d_rgb_valida)
    # Tu código hace: array = data[:, :, 0] si tiene 3 canales
    assert img.data.ndim == 2  
    assert img.data.shape == (10, 10)


def test_error_constructor_data_none():
    """Valida que lance ValueError si data es None."""
    with pytest.raises(ValueError, match="La imagen no tiene datos"):
        Imagen(None)


def test_error_constructor_tipo_incorrecto():
    """Valida que lance TypeError si data no es un array de NumPy."""
    with pytest.raises(TypeError, match="data debe ser np.ndarray"):
        Imagen([[1, 2], [3, 4]])  # Una lista común


def test_error_constructor_dimensiones_invalidas():
    """Valida que lance ValueError si la matriz es de 1D o más de 3D."""
    matriz_1d = np.array([1, 2, 3, 4], dtype=np.uint8)
    with pytest.raises(ValueError, match="data debe tener 2 o 3 dimensiones"):
        Imagen(matriz_1d)


# ==========================================================
# 2. TESTS DE SETTERS, GETTERS Y ENCAPSULAMIENTO
# ==========================================================

def test_data_setter_valido(matriz_2d_valida):
    """Prueba que el setter de data actualice la matriz correctamente."""
    img = Imagen(matriz_2d_valida)
    nueva_matriz = np.zeros((5, 5), dtype=np.uint8)
    img.data = nueva_matriz
    assert np.array_equal(img.data, nueva_matriz)


def test_data_setter_error_tipo(matriz_2d_valida):
    """Prueba que el setter de data rechace tipos que no sean arrays."""
    img = Imagen(matriz_2d_valida)
    with pytest.raises(TypeError, match="Se espera una array de NumPy"):
        img.data = "esto es un string, no una matriz"


def test_info_setter_y_getter(matriz_2d_valida):
    """Verifica el correcto funcionamiento del getter y setter de metadatos (Info)."""
    img = Imagen(matriz_2d_valida)
    nueva_info = Info()
    img.info = nueva_info
    assert img.info == nueva_info


def test_info_setter_error_tipo(matriz_2d_valida):
    """Asegura que el setter de info valide estrictamente instancias de la clase Info."""
    img = Imagen(matriz_2d_valida)
    with pytest.raises(TypeError, match="Se espera un objeto de la clase 'Info'"):
        img.info = "Metadato falso"


# ==========================================================
# 3. TESTS DE MÉTODOS MÁGICOS (__len__, __str__, __getitem__)
# ==========================================================

def test_metodo_len(matriz_2d_valida):
    """Verifica que len() retorne el número total de píxeles (filas * columnas)."""
    img = Imagen(matriz_2d_valida)
    assert len(img) == 100  # 10 x 10


def test_metodo_str(matriz_2d_valida):
    """Comprueba que la representación en string contenga las palabras clave técnicas."""
    img = Imagen(matriz_2d_valida)
    texto_inf = str(img)
    assert "INFORMACIÓN DE LA IMAGEN" in texto_inf
    assert "Dimensiones:" in texto_inf
    assert "Total de píxeles:" in texto_inf


def test_metodo_getitem_píxel_individual(matriz_2d_valida):
    """Prueba el acceso indexado por corchetes img[y, x]."""
    matriz_2d_valida[3, 4] = 175
    img = Imagen(matriz_2d_valida)
    assert img[3, 4] == 175


def test_metodo_getitem_fuera_de_rango(matriz_2d_valida):
    """Valida que los corchetes lancen IndexError si se pide un píxel fuera de la anatomía."""
    img = Imagen(matriz_2d_valida)
    with pytest.raises(IndexError, match="fuera de rango"):
        _ = img[15, 4]  # Fila 15 no existe en una de 10x10


# ==========================================================
# 4. TESTS DE PROCESAMIENTO DIGITAL (NORMALIZACIÓN Y FILTROS)
# ==========================================================

def test_normalizacion_min_max():
    """Verifica que el método estático escale floats crudos al rango uint8 [0-255]."""
    matriz_float = np.array([[0.0, 0.5], [1.0, 2.0]], dtype=np.float32)
    matriz_norm = Imagen.normalizar(matriz_float)
    
    assert matriz_norm.dtype == np.uint8
    assert matriz_norm[0, 0] == 0    # Mínimo absoluto pasa a 0
    assert matriz_norm[1, 1] == 255  # Máximo absoluto pasa a 255


def test_normalizacion_enteros_altos():
    """Verifica el comportamiento con enteros de alto rango (como uint16 médico)."""
    matriz_uint16 = np.array([[0, 65535]], dtype=np.uint16)
    matriz_norm = Imagen.normalizar(matriz_uint16)
    
    assert matriz_norm.dtype == np.uint8
    assert matriz_norm[0, 0] == 0
    assert matriz_norm[0, 1] == 255


def test_convertir_blanco_negro_2d(matriz_2d_valida):
    """Comprueba que si la imagen ya es 2D, el método .bn() se retorne a sí mismo sin romperse."""
    img = Imagen(matriz_2d_valida)
    resultado = img.bn()
    assert resultado == img


# ==========================================================
# 5. TESTS DE CARGA DE ARCHIVOS (MOCKING)
# ==========================================================

def test_cargar_formato_no_soportado():
    """Asegura que el lector tire un ValueError si la extensión no es médica ni de imagen estándar."""
    with pytest.raises(ValueError, match="Formato .txt no soportado"):
        Imagen.cargar("carpeta/archivo_falso.txt")


def test_cargar_imagen_png_real(tmp_path):
    """Crea una imagen PNG temporal en el disco para validar que la lógica de Pillow funcione de punta a punta."""
    # Creamos una ruta de archivo falsa pero segura usando tmp_path de pytest
    ruta_temp_png = os.path.join(tmp_path, "test_placa.png")
    
    # Creamos un archivo físico real con Pillow
    img_pil = PILImage.new("L", (5, 5), color=120)
    img_pil.save(ruta_temp_png)
    
    # Ejecutamos tu método de clase
    objeto_cargado = Imagen.cargar(ruta_temp_png)
    
    assert isinstance(objeto_cargado, Imagen)
    assert objeto_cargado.data.shape == (5, 5)
    assert objeto_cargado.data[2, 2] == 120

# ==========================================================
# 6. TESTS CON IMÁGENES REALES
# ==========================================================

def test_metodos_con_radiografia_real():
    """
    Carga una radiografía real desde el disco y prueba que los métodos
    de procesamiento y manipulación de datos funcionen de punta a punta.
    """
    ruta_real = "tests/imagenes_test/radiografias/216840111366964012373310883942009084123158919_00-069-064.png" 
    
    if not os.path.exists(ruta_real):
        pytest.skip(f"El archivo real en '{ruta_real}' no está disponible para la prueba.")

    # Probamos la carga desde la clase base o la heredada
    rx = Imagen.cargar(ruta_real)
    assert isinstance(rx, Imagen)
    assert rx.data.ndim == 2  # Debe ser 2D por ser radiografía

    # Verificamos métodos básicos sobre la imagen real
    assert "INFORMACIÓN DE LA IMAGEN" in str(rx)
    assert len(rx) == rx.data.shape[0] * rx.data.shape[1]
    
    # Como ya es 2D, .bn() devuelve la misma instancia intacta
    assert rx.bn() == rx


def test_conversion_bn_desde_matriz_3d_aleatoria():
    """
    Genera una matriz color artificial (3D / RGB) y comprueba que .bn()
    fusione los canales haciendo el promedio y devuelva una matriz uint8 de 2D.
    """
    # 1. Creamos una matriz RGB simulada (Alto: 10, Ancho: 10, Canales: 3)
    # Valores aleatorios de píxeles entre 0 y 255
    matriz_rgb_aleatoria = np.random.randint(0, 256, size=(10, 10, 3), dtype=np.uint8)
    
    # 2. Instanciamos el objeto Imagen pasándole la matriz 3D
    # Ojo: Tu constructor para imágenes de 3 canales se queda con data[:, :, 0]
    # para estandarizar, pero vamos a forzar que simule datos 3D válidos en .data
    img_3d = Imagen(matriz_rgb_aleatoria)
    
    # Para probar el método .bn() al 100% en su bloque "if len(self.data.shape) == 3",
    # le inyectamos la matriz 3D directamente a la propiedad data
    img_3d.data = matriz_rgb_aleatoria
    assert img_3d.data.ndim == 3

    # 3. 🌟 Ejecutamos tu método de conversión a blanco y negro
    matriz_gris_resultado = img_3d.bn()

    # 4. ASERCIONES DE CONTROL MATEMÁTICO:
    assert isinstance(matriz_gris_resultado, np.ndarray)
    assert matriz_gris_resultado.ndim == 2          # ¡Pasó de 3D a 2D!
    assert matriz_gris_resultado.shape == (10, 10)  # Mantiene el alto y ancho
    assert matriz_gris_resultado.dtype == np.uint8  # Se convirtió a enteros de 8 bits

    # 5. CONTROL DEL ALGORITMO: Verificamos que el píxel [0,0] sea el promedio de los 3 canales
    canal_r = matriz_rgb_aleatoria[0, 0, 0]
    canal_g = matriz_rgb_aleatoria[0, 0, 1]
    canal_b = matriz_rgb_aleatoria[0, 0, 2]
    promedio_esperado = int((int(canal_r) + int(canal_g) + int(canal_b)) / 3)
    
    # Tolerancia de +/- 1 por el casteo automático a .astype(np.uint8) de tu código
    assert abs(int(matriz_gris_resultado[0, 0]) - promedio_esperado) <= 1

# ==========================================================
# 7. TESTS DE VISUALIZACIÓN (USANDO MOCKS)
# ==========================================================

def test_metodo_visualizar_y_original(matriz_2d_valida, monkeypatch):
    """
    Verifica que los métodos de renderizado de la imagen (visualizar y ver_imgOriginal)
    se ejecuten y configuren Matplotlib de forma correcta sin bloquear la consola.
    """
    import matplotlib.pyplot as plt

    # 1. Instanciamos la imagen de prueba
    ruta_real = "tests/imagenes_test/radiografias/216840111366964013829543166512013358092118761_02-089-145.png"
    img = Imagen.cargar(ruta_real)
    
    # Variables de control para verificar si Matplotlib es invocado
    historial_llamados = {"imshow": False, "show": False, "subplots": False}

    # 2. Objetos Mock mínimos para imitar el comportamiento de Fig y Ax de Matplotlib
    class MockAx:
        def imshow(self, *args, **kwargs):
            historial_llamados["imshow"] = True
            class MockAxesImage:
                def __init__(self):
                    self.dtype = np.uint8
                    self.ndim = 2
            return MockAxesImage()
            
        def set_title(self, *args, **kwargs): pass
        def axis(self, *args, **kwargs): pass

    class MockFig:
        def colorbar(self, *args, **kwargs):
            class MockColorbar:
                def set_label(self, *args, **kwargs): pass
            return MockColorbar()

    # 3. Reemplazos temporales (Mocks) con monkeypatch
    def mock_subplots(*args, **kwargs):
        historial_llamados["subplots"] = True
        return MockFig(), MockAx()

    def mock_show():
        historial_llamados["show"] = True

    # Inyectamos las funciones simuladas en el módulo pyplot
    monkeypatch.setattr(plt, "subplots", mock_subplots)
    monkeypatch.setattr(plt, "show", mock_show)

    # 4.  PROBAMOS EL MÉTODO .visualizar()
    img.visualizar(titulo="Test Ventana Radiografía")
    
    assert historial_llamados["subplots"] is True
    assert historial_llamados["imshow"] is True
    assert historial_llamados["show"] is True

    # 5.  PROBAMOS EL MÉTODO .ver_imgOriginal()
    # Reseteamos el historial de control
    historial_llamados["subplots"] = False
    historial_llamados["imshow"] = False
    historial_llamados["show"] = False

    img.ver_imgOriginal(titulo="Test Ventana Original")
    
    assert historial_llamados["subplots"] is True
    assert historial_llamados["imshow"] is True
    assert historial_llamados["show"] is True