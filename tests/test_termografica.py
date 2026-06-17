import numpy as np
from bioimagenes.core.imagen import Imagen
from bioimagenes.medicas.imagen_termografica import ImagenTermografica 

# Ruta de tu imagen real
RUTA_TERMOGRAFIA_REAL = "tests/imagenes_test/termografias/N11102.jpg"


# ==========================================================
# PARTE 1: TESTS ESTRUCTURALES (MATRICES MANUALES)
# ==========================================================

def test_creacion_imagen_termografica_manual():
    """Verifica la carga inicial de una matriz uint8 en escala de grises."""
    data = np.array([
        [0, 64, 128],
        [192, 255, 0]
    ], dtype=np.uint8)
    
    img = ImagenTermografica(data)
    assert isinstance(img, ImagenTermografica)
    assert img.data.ndim == 2
    assert img.data.dtype == np.uint8


def test_convertir_a_temperatura_error_rango_invertido_manual():
    """Valida que el sistema de seguridad rechace rangos invertidos."""
    data = np.zeros((5, 5), dtype=np.uint8)
    img = ImagenTermografica(data)
    try:
        img.convertir_a_temperatura(39.0, 35.0)
        assert False
    except ValueError:
        assert True


def test_mapa_calor_manual():
    """Prueba la transformación estructural correcta a canales RGB (uint8)."""
    data = np.array([[0, 127], [255, 64]], dtype=np.uint8)
    img = ImagenTermografica(data)
    
    img.convertir_a_temperatura(30.0, 40.0)
    img.mapa_calor()
    
    assert img.data.ndim == 3          
    assert img.data.dtype == np.uint8  
    assert img.data.shape == (2, 2, 3)


def test_segmentar_por_rangos_manual():
    """Verifica que la segmentación genere la salida de imagen RGB correcta."""
    data = np.array([[0, 127, 255]], dtype=np.uint8)
    img = ImagenTermografica(data)
    
    img.convertir_a_temperatura(30.0, 40.0)
    img.segmentar_por_rangos(34.0, 36.0)

    assert img.data.ndim == 3
    assert img.data.dtype == np.uint8
    assert img.data.shape == (1, 3, 3)


def test_detectar_puntos_calientes_manual():
    """Verifica la detección de focos térmicos usando el parámetro corregido 'tolerancia'."""
    data = np.array([[0, 127, 255]], dtype=np.uint8)
    img = ImagenTermografica(data)
    
    img.convertir_a_temperatura(30.0, 40.0)
    img.detectar_puntos_calientes(temperatura=40.0, tolerancia=0.5)

    assert img.data.ndim == 3
    assert img.data.dtype == np.uint8


def test_historial_modificaciones_manual():
    """Asegura el registro secuencial de operaciones en el historial de cambios."""
    data = np.array([[0, 255]], dtype=np.uint8)
    img = ImagenTermografica(data)
    
    img.convertir_a_temperatura(30.0, 40.0)
    img.segmentar_por_rangos(32.0, 38.0)
    
    assert len(img.historial) >= 2


# ==========================================================
# PARTE 2: TESTS INTEGRALES SIN VISUALIZACIÓN (IMÁGENES REALES)
# ==========================================================

def test_creacion_desde_imagen_real():
    """Verifica que la imagen del paciente se cargue con el formato inicial uint8."""
    imagen_base = Imagen.cargar(RUTA_TERMOGRAFIA_REAL)
    assert imagen_base is not None
    
    img_termica = ImagenTermografica(imagen_base.data)
    assert img_termica.data.ndim == 2
    assert img_termica.data.dtype == np.uint8


def test_mapa_calor_real():
    """Aplica la paleta JET y controla que la matriz real mute correctamente a RGB."""
    imagen_base = Imagen.cargar(RUTA_TERMOGRAFIA_REAL)
    alto, ancho = imagen_base.data.shape
    img = ImagenTermografica(imagen_base.data)
    
    img.convertir_a_temperatura(30.0, 42.0)
    img.mapa_calor()
    
    assert img.data.ndim == 3
    assert img.data.shape == (alto, ancho, 3)
    assert img.data.dtype == np.uint8


def test_segmentar_por_rangos_real():
    """Segmenta rangos térmicos dinámicos en el paciente y valida la salida tridimensional."""
    imagen_base = Imagen.cargar(RUTA_TERMOGRAFIA_REAL)
    alto, ancho = imagen_base.data.shape
    img = ImagenTermografica(imagen_base.data)
    
    img.convertir_a_temperatura(30.0, 42.0)
    
    t_min = img.data.min()
    t_max = img.data.max()
    
    corte_inf = float(t_min + (t_max - t_min) * 0.3)
    corte_sup = float(t_min + (t_max - t_min) * 0.7)
    
    img.segmentar_por_rangos(corte_inf, corte_sup)
    
    assert img.data.ndim == 3
    assert img.data.shape == (alto, ancho, 3)
    assert img.data.dtype == np.uint8


def test_detectar_puntos_calientes_real():
    """Busca el foco febril más alto en la imagen real y valida su consistencia formal."""
    imagen_base = Imagen.cargar(RUTA_TERMOGRAFIA_REAL)
    alto, ancho = imagen_base.data.shape
    img = ImagenTermografica(imagen_base.data)
    
    img.convertir_a_temperatura(30.0, 42.0)
    max_temp = float(img.data.max())
    
    img.detectar_puntos_calientes(temperatura=max_temp, tolerancia=1.0)
    
    assert img.data.ndim == 3
    assert img.data.shape == (alto, ancho, 3)
    assert img.data.dtype == np.uint8


# ==========================================================
# PANEL DE EJECUCIÓN CONTINUA
# ==========================================================

if __name__ == "__main__":
    todos_los_tests = [
        test_creacion_imagen_termografica_manual,
        test_convertir_a_temperatura_error_rango_invertido_manual,
        test_mapa_calor_manual,
        test_segmentar_por_rangos_manual,
        test_detectar_puntos_calientes_manual,
        test_historial_modificaciones_manual,
        
        test_creacion_desde_imagen_real,
        test_mapa_calor_real,
        test_segmentar_por_rangos_real,
        test_detectar_puntos_calientes_real
    ]

    print("\n=== EJECUTANDO REVISIÓN INTEGRAL SIN INTERFAZ GRÁFICA (10 TESTS) ===\n")
    aprobados = 0

    for test in todos_los_tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            aprobados += 1
        except AssertionError:
            print(f"✗ {test.__name__} -> ERROR: Aserción lógica fallida.")
        except Exception as e:
            print(f"✗ {test.__name__} -> CRASH NO CONTROLADO: {e}")

    print(f"\n[Resultado del Panel]: {aprobados}/{len(todos_los_tests)} aprobados sin ventanas.")



termografia1 = ImagenTermografica.cargar("tests/imagenes_test/termografias/N11102.jpg")
termografia1.convertir_a_temperatura(32, 40)
termografia1.mapa_calor()
termografia1.visualizar()

termografia2 = ImagenTermografica.cargar("tests/imagenes_test/termografias/N11108.jpg")
termografia2.convertir_a_temperatura(33,42)
termografia2.detectar_puntos_calientes(41)
termografia2.visualizar()

termografia3 = ImagenTermografica.cargar("tests/imagenes_test/termografias/N11105.jpg")
termografia3.convertir_a_temperatura(30,43)
termografia3.segmentar_por_rangos(35.5,40.0)
termografia3.visualizar()

#Si queremos ver la imagen original
termografia1.ver_imgOriginal("Imagen Termografica 1 Original Recuperada")
termografia2.ver_imgOriginal("Imagen Termografica 2 Original Recuperada")
termografia3.ver_imgOriginal("Imagen Termografica 3 Original Recuperada")