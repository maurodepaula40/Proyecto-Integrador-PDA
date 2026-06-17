import os
import numpy as np
from bioimagenes.core.imagen import Imagen
from bioimagenes.filtros.filtro import Filtro

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
# PANEL DE EJECUCIÓN CONTINUA E INTEGRACIÓN VISUAL (DOCENTE)
# ==========================================================

def test_pipeline_demostracion_visual_docente():
    """
    Este módulo actúa como el cierre interactivo de la suite de pruebas.
    Se ejecuta nativamente tanto en IDEs como en el Símbolo del Sistema (CMD) 
    vía pytest, abriendo consecutivamente las ventanas de Matplotlib para el docente.
    """
    # 1. Verificación de la ruta física de la radiografía
    if not os.path.exists(RUTA_RADIOGRAFIA_REAL):
        print(f"\n Saltando demostración visual: No se encontró la radiografía en: {RUTA_RADIOGRAFIA_REAL}")
        print("Por favor, verifica el nombre del archivo en tu carpeta de pruebas.")
        return

    print("\n" + "="*60)
    print(" INICIANDO PIPELINE DE DEMOSTRACIÓN RADIOGRÁFICA INTERACTIVA ")
    print("="*60)
    
    # 2. Cargamos la imagen original del paciente
    print("\n Cargando radiografía original...")
    img_original = Imagen.cargar(RUTA_RADIOGRAFIA_REAL)
    
    print(" Abriendo: Radiografía Original... (Cerrá la ventana para aplicar el Filtro 1)")
    img_original.visualizar(titulo="1. DOCENTE: Radiografía Original (Control)")

    # ==========================================================
    # CASO 1: Reducción de Ruido (Filtro de Suavizado)
    # ==========================================================
    print("\n[1/3] Aplicando Filtro de Suavizado...")
    filtro_suave = Filtro("suavizado", tamaño=3) 
    matriz_suave = filtro_suave.aplicar(img_original) 
    
    img_suavizada = Imagen(matriz_suave)
    
    print(" Abriendo: Resultado Suavizado... (Cerrá la ventana para aplicar el Filtro 2)")
    img_suavizada.visualizar(titulo="2. DOCENTE: Filtro Suavizado (Reducción de Ruido)")

    # ==========================================================
    # CASO 2: Realce de Estructuras Óseas (Filtro Sharpen)
    # ==========================================================
    print("\n[2/3] Aplicando Filtro Sharpen (Realce de Detalles)...")
    filtro_sharpen = Filtro("sharpen", tamaño=3)
    matriz_sharpen = filtro_sharpen.aplicar(img_original)
    
    img_sharpen = Imagen(matriz_sharpen)
    
    print(" Abriendo: Resultado Sharpen... (Cerrá la ventana para aplicar el Filtro 3)")
    img_sharpen.visualizar(titulo="3. DOCENTE: Filtro Sharpen (Nitidez Ósea)")

    # ==========================================================
    # CASO 3: Detección de Bordes (Sobel Vertical)
    # ==========================================================
    print("\n[3/3] Aplicando Filtro Sobel Vertical para Bordes Corticales...")
    # Asegúrate de que el catálogo reciba el texto en minúsculas según tu test_creacion
    filtro_sobel = Filtro("sobelvertical", tamaño=3) 
    matriz_sobel = filtro_sobel.aplicar(img_original)
    
    img_sobel = Imagen(matriz_sobel)
    
    print(" Abriendo: Detección de Bordes... (Cerrá la ventana para finalizar el test)")
    img_sobel.visualizar(titulo="4. DOCENTE: Gradientes Verticales (Sobel)")

    print("\n" + "="*60)
    print(" PIPELINE DE PROCESAMIENTO COMPLETADO CON ÉXITO ✅")
    print("="*60)


# Este bloque opcional queda de respaldo por si alguien arrastra y ejecuta 
# el archivo de manera directa con 'python' en vez de usar 'pytest'
if __name__ == "__main__":
    todos_los_tests = [
        test_creacion_e_inicializacion_filtro,
        test_error_filtro_inexistente,
        test_filtrado_no_altera_dimensiones,
        test_filtro_suavizado_reduce_varianza_global,
        test_aplicar_suavizado_radiografia_real,
        test_aplicar_sobel_horizontal_radiografia_real,
        test_aplicar_sharpen_radiografia_real,
        test_pipeline_demostracion_visual_docente
    ]

    print("\n=== EJECUTANDO CONTROLES DE CALIDAD AUTOMÁTICOS (8 TESTS) ===\n")
    aprobados = 0
    for test in todos_los_tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            aprobados += 1
        except AssertionError:
            print(f"✗ {test.__name__} -> ERROR: Aserción fallida.")
        except Exception as e:
            print(f"✗ {test.__name__} -> CRASH NO CONTROLADO: {e}")

    print(f"\n[Resultado]: {aprobados}/{len(todos_los_tests)} módulos aprobados.")