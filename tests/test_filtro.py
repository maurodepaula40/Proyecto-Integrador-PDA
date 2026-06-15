import os
import numpy as np
from bioimagenes.core.imagen import Imagen
from bioimagenes.filtros.filtro import Filtro
from bioimagenes.medicas.imagen_radiografia import ImagenRadiografia

# ==========================================================
# CONFIGURACIÓN: Ajustá la ruta a tu carpeta de radiografías
# ==========================================================
RUTA_RADIOGRAFIA_REAL = "tests/imagenes_test/radiografias/216840111366964013515091760022012318080539431_01-152-111.png" 


# ==========================================================
# PARTE 1: TESTS UNITARIOS / ESTRUCTURALES (MATRICES MANUALES)
# ==========================================================

def test_creacion_e_inicializacion_filtro():
    """Verifica que el filtro configure correctamente su nombre en minúsculas y su kernel."""
    filtro = Filtro("SobelHorizontal", tamaño=3)
    assert filtro.tipo == "sobelhorizontal"
    assert isinstance(filtro.kernel, np.ndarray)


def test_error_filtro_inexistente():
    """Valida que el catálogo lance un ValueError si el nombre del filtro no existe."""
    try:
        Filtro("filtro_fantasma_medico")
        assert False  # Si no lanza error, el test falló
    except ValueError:
        assert True   # Pasó la prueba de seguridad con éxito


def test_filtrado_no_altera_dimensiones():
    """Asegura que tras la convolución, las dimensiones (alto, ancho) se mantengan idénticas."""
    matriz_manual = np.array([
        [50, 100, 150],
        [200, 250, 30],
        [80, 90, 110]
    ], dtype=np.uint8)
    
    img = Imagen(matriz_manual)
    filtro = Filtro("suavizado", tamaño=3)
    
    matriz_filtrada = filtro.aplicar(img)
    
    assert isinstance(matriz_filtrada, np.ndarray)
    assert matriz_filtrada.shape == (3, 3)
    assert matriz_filtrada.dtype == np.uint8


def test_filtro_suavizado_reduce_varianza_global():
    """Verifica que el filtro de suavizado reduzca la dispersión general de los tonos de gris."""
    # Creamos una matriz con transiciones muy bruscas (ruido blanco y negro alternado)
    matriz_ruido = np.array([
        [0, 255,   0, 255,   0],
        [255,   0, 255,   0, 255],
        [0, 255,   0, 255,   0],
        [255,   0, 255,   0, 255],
        [0, 255,   0, 255,   0]
    ], dtype=np.uint8)
    
    img = Imagen(matriz_ruido)
    varianza_original = np.std(img.data)  # Medimos qué tan dispersos están los valores originales
    
    filtro = Filtro("suavizado", tamaño=3)
    matriz_filtrada = filtro.aplicar(img)
    varianza_filtrada = np.std(matriz_filtrada)  # Medimos la dispersión después del filtro
    
    # El filtro DEBE disminuir la desviación estándar general porque difumina los contrastes violentos
    assert varianza_filtrada < varianza_original


# ==========================================================
# PARTE 2: TESTS INTEGRALES (CON IMAGEN RADIOGRÁFICA REAL)
# ==========================================================

def test_aplicar_suavizado_radiografia_real():
    """Carga la radiografía real, aplica suavizado y controla dimensiones y formato 2D."""
    img_real = Imagen.cargar(RUTA_RADIOGRAFIA_REAL)
    assert img_real is not None, f"No se pudo cargar la imagen en {RUTA_RADIOGRAFIA_REAL}"
    
    alto, ancho = img_real.data.shape
    
    filtro = Filtro("suavizado", tamaño=5)
    resultado = filtro.aplicar(img_real)
    
    assert resultado.ndim == 2  # Garantiza que siga siendo escala de grises estricta
    assert resultado.shape == (alto, ancho)
    assert resultado.dtype == np.uint8


def test_aplicar_sobel_horizontal_radiografia_real():
    """Aplica detección de bordes Sobel horizontal para realzar límites corticales del hueso."""
    img_real = Imagen.cargar(RUTA_RADIOGRAFIA_REAL)
    alto, ancho = img_real.data.shape
    
    filtro = Filtro("sobelhorizontal", tamaño=3)
    resultado = filtro.aplicar(img_real)
    
    assert resultado.ndim == 2
    assert resultado.shape == (alto, ancho)
    assert resultado.dtype == np.uint8


def test_aplicar_sharpen_radiografia_real():
    """Prueba el filtro de realce de detalles (sharpen) para mejorar la nitidez de la radiografía."""
    img_real = Imagen.cargar(RUTA_RADIOGRAFIA_REAL)
    alto, ancho = img_real.data.shape
    
    filtro = Filtro("sharpen", tamaño=3)
    resultado = filtro.aplicar(img_real)
    
    assert resultado.ndim == 2
    assert resultado.shape == (alto, ancho)
    assert resultado.dtype == np.uint8


# ==========================================================
# PANEL DE EJECUCIÓN CONTINUA
# ==========================================================

if __name__ == "__main__":
    todos_los_tests = [
        test_creacion_e_inicializacion_filtro,
        test_error_filtro_inexistente,
        test_filtrado_no_altera_dimensiones,
        test_filtro_suavizado_reduce_varianza_global,
        
        test_aplicar_suavizado_radiografia_real,
        test_aplicar_sobel_horizontal_radiografia_real,
        test_aplicar_sharpen_radiografia_real
    ]

    print("\n=== EJECUTANDO CONTROLES DE CALIDAD: FILTROS EN RADIOGRAFÍAS (7 TESTS) ===\n")
    aprobados = 0

    for test in todos_los_tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            aprobados += 1
        except AssertionError:
            print(f"✗ {test.__name__} -> ERROR: Aserción fallida (revisar normalización o dimensiones).")
        except Exception as e:
            print(f"✗ {test.__name__} -> CRASH NO CONTROLADO: {e}")

    print(f"\n[Resultado del Panel]: {aprobados}/{len(todos_los_tests)} módulos radiográficos aprobados.")


def demo_procesamiento_radiografia():
    # 1. Definimos la ruta de la radiografía real
    
    if not os.path.exists(RUTA_RADIOGRAFIA_REAL):
        print(f"Error: No se encontró la radiografía en la ruta: {RUTA_RADIOGRAFIA_REAL}")
        print("Por favor, verifica el nombre del archivo en tu carpeta 'tests/imagenes_test/radiografias/'.")
        return

    print("=== Iniciando Pipeline de Procesamiento Radiográfico ===")
    
    # 2. Cargamos la imagen original del paciente
    img_original = Imagen.cargar(RUTA_RADIOGRAFIA_REAL)
    img_original.titulo_actual = "Radiografía Original (Control)"
    
    # Mostramos la imagen base para tener el punto de comparación médico
    img_original.visualizar()

    # ==========================================================
    # CASO 1: Reducción de Ruido (Filtro de Suavizado de 5x5)
    # ==========================================================
    print("\n[1/3] Aplicando Filtro de Suavizado (Promedio 5x5)...")
    filtro_suave = Filtro("suavizado")
    
    # Obtenemos la matriz procesada uint8
    matriz_suave = filtro_suave.aplicar(img_original) 
    
    # Instanciamos un nuevo objeto Imagen con el resultado para poder visualizarlo
    img_suavizada = Imagen(matriz_suave)
    img_suavizada.titulo_actual = "Radiografía: Filtro Suavizado (3x3)"
    img_suavizada.visualizar()

    # ==========================================================
    # CASO 2: Realce de Estructuras Óseas (Filtro Sharpen)
    # ==========================================================
    print("\n[2/3] Aplicando Filtro Sharpen (Realce de Detalles)...")
    filtro_sharpen = Filtro("sharpen", tamaño=3)
    
    matriz_sharpen = filtro_sharpen.aplicar(img_original)
    
    img_sharpen = Imagen(matriz_sharpen)
    img_sharpen.titulo_actual = "Radiografía: Realce de Detalles (Sharpen)"
    img_sharpen.visualizar()

    # ==========================================================
    # CASO 3: Detección de Bordes (Sobel Vertical de 5x5)
    # ==========================================================
    print("\n[3/3] Aplicando Filtro Sobel Vertical (5x5) para Bordes Corticales...")
    filtro_sobel = Filtro("sobelverticalx5")
    
    matriz_sobel = filtro_sobel.aplicar(img_original)
    
    img_sobel = Imagen(matriz_sobel)
    img_sobel.titulo_actual = "Radiografía: Bordes Verticales (Sobel 5x5)"
    
    # Usamos un mapa de grises para ver los gradientes óseos bien definidos
    img_sobel.visualizar(cmap_gris="gray")

    print("\n=== Fin del Pipeline de Demostración ===")

if __name__ == "__main__":
    demo_procesamiento_radiografia()



# # 1. Cargamos la radiografía real (Crea el objeto de tipo Imagen)
# rx = ImagenRadiografia.cargar(RUTA_RADIOGRAFIA_REAL)
# rx2 = ImagenRadiografia.cargar(RUTA_RADIOGRAFIA_REAL)

#     # 2 INSTANCIAMOS EL FILTRO: Creamos un objeto de la clase Filtro (ej: sharpen)
#     # Al hacer esto, se ejecuta el __init__ y se carga el kernel matemático en el objeto
# mi_filtro = Filtro("sobelhorizontalx7", tamaño=7)

#     # 3. APLICAMOS EL FILTRO: Invocamos el método desde el objeto creado
# matriz_filtrada = mi_filtro.aplicar(rx)

#     # 4. ENCAPSULAMOS Y VISUALIZAMOS: Envolvemos la matriz uint8 resultante en un objeto Imagen
# rx_procesada = Imagen(matriz_filtrada)
# rx_procesada.titulo_actual = "Radiografía con Filtro sobel horizontal x7"
# rx_procesada.visualizar()

# rx2.detectar_bordes()
# rx2.visualizar()


marcapaso = Imagen.cargar("tests/imagenes_test/radiografias/216840111366964013829543166512013358092118761_02-089-145.png")
mi_filtro2 = Filtro("sobelhorizontalx5", tamaño=5)

    # 3. APLICAMOS EL FILTRO: Invocamos el método desde el objeto creado
img_filtrada = mi_filtro2.aplicar(marcapaso)
rx_filtrado = Imagen(img_filtrada)
rx_filtrado.visualizar()
print(rx_filtrado.data.shape)

