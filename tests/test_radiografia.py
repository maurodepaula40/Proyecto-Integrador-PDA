import numpy as np
from bioimagenes.medicas.imagen_radiografia import ImagenRadiografia
from bioimagenes.core.imagen import Imagen
import numpy as np

RUTA_RADIOGRAFIA = "tests/imagenes_test/radiografias/216840111366964012558082906712010004133151165_00-119-134.png"


# ==========================================================
# TESTS UNITARIOS - IMAGEN RADIOGRAFICA
# ==========================================================

def test_creacion_imagen_radiografica():
    """
    Verifica que una ImagenRadiografia se cree correctamente
    a partir de una matriz 2D.
    """

    data = np.array([
        [0, 50, 100],
        [150, 200, 255],
        [30, 80, 120]
    ], dtype=np.uint8)

    img = ImagenRadiografia(data, tipo_estudio="torax", brillo=0)

    assert isinstance(img, ImagenRadiografia)
    assert img.data.shape == (3, 3)
    assert img.data.dtype == np.uint8
    assert img.tipo_estudio == "torax"
    assert img.brillo == 0
    assert img.region_interes is None


def test_rechazar_imagen_3d():
    """
    Verifica que ImagenRadiografia rechace matrices 3D.
    """

    data = np.zeros((10, 10, 3), dtype=np.uint8)

    try:
        ImagenRadiografia(data)

        assert False

    except ValueError:
        assert True


def test_conversion_float_0_1_a_uint8():
    """
    Verifica que una imagen float entre 0 y 1 se convierta a uint8.
    """

    data = np.array([
        [0.0, 0.5],
        [0.75, 1.0]
    ], dtype=float)

    img = ImagenRadiografia(data, tipo_estudio="mano")

    assert img.data.dtype == np.uint8
    assert img.data.min() == 0
    assert img.data.max() == 255


def test_ajustar_brillo_positivo():
    """
    Verifica que ajustar_brillo modifique self.data,
    actualice el brillo y retorne self.
    """

    data = np.array([
        [0, 50, 100],
        [150, 200, 250]
    ], dtype=np.uint8)

    img = ImagenRadiografia(data, tipo_estudio="torax", brillo=0)

    resultado = img.ajustar_brillo(30)

    assert resultado is img
    assert img.brillo == 30
    assert img.data.dtype == np.uint8
    assert img.data.min() >= 0
    assert img.data.max() <= 255
    assert img.titulo_actual == "Radiografía — brillo 30"


def test_ajustar_brillo_negativo():
    """
    Verifica que ajustar_brillo funcione con valores negativos.
    """

    data = np.array([
        [20, 60, 100],
        [150, 200, 255]
    ], dtype=np.uint8)

    img = ImagenRadiografia(data, tipo_estudio="torax", brillo=0)

    resultado = img.ajustar_brillo(-40)

    assert resultado is img
    assert img.brillo == -40
    assert img.data.dtype == np.uint8
    assert img.data.min() >= 0
    assert img.data.max() <= 255
    assert img.titulo_actual == "Radiografía — brillo -40"


def test_ajustar_brillo_rango_alto():
    """
    Verifica que ajustar_brillo funcione con imágenes cuyo rango
    original supera 0-255.
    """

    data = np.array([
        [0, 1000, 2000],
        [3000, 4000, 5000]
    ], dtype=np.uint16)

    img = ImagenRadiografia(data, tipo_estudio="columna", brillo=0)

    img.ajustar_brillo(20)

    assert img.data.dtype == np.uint8
    assert img.data.min() >= 0
    assert img.data.max() <= 255


def test_mejorar_contraste():
    """
    Verifica que mejorar_contraste modifique self.data y retorne self.
    """

    data = np.array([
        [80, 100, 120],
        [130, 150, 170]
    ], dtype=np.uint8)

    img = ImagenRadiografia(data, tipo_estudio="abdomen")

    resultado = img.mejorar_contraste(factor=1.5)

    assert resultado is img
    assert img.data.shape == data.shape
    assert img.data.dtype == np.uint8
    assert img.data.min() >= 0
    assert img.data.max() <= 255
    assert img.titulo_actual == "RX con contraste ajustado (1.5)"


def test_invertir_intensidades():
    """
    Verifica que invertir_intensidades genere el negativo de la imagen.
    """

    data = np.array([
        [0, 100],
        [200, 255]
    ], dtype=np.uint8)

    img = ImagenRadiografia(data, tipo_estudio="torax")

    resultado = img.invertir_intensidades()

    esperado = np.array([
        [255, 155],
        [55, 0]
    ], dtype=np.uint8)

    assert resultado is img
    assert np.array_equal(img.data, esperado)
    assert img.titulo_actual == "RX con intensidades invertidas"


def test_ecualizar_intensidades():
    """
    Verifica que ecualizar_intensidades modifique self.data,
    conserve las dimensiones y retorne self.
    """

    data = np.array([
        [0, 0, 50],
        [100, 150, 255]
    ], dtype=np.uint8)

    img = ImagenRadiografia(data, tipo_estudio="torax")

    resultado = img.ecualizar_intensidades()

    assert resultado is img
    assert img.data.shape == data.shape
    assert img.data.dtype == np.uint8
    assert img.data.min() >= 0
    assert img.data.max() <= 255
    assert img.titulo_actual == "RX con intensidades ecualizadas"


def test_seleccionar_region_interes():
    """
    Verifica que seleccionar_region_interes retorne una nueva instancia
    de ImagenRadiografia con la región recortada.
    """

    data = np.arange(100).reshape(10, 10).astype(np.uint8)

    img = ImagenRadiografia(data, tipo_estudio="mano")

    recorte = img.seleccionar_region_interes(
        y_min=2,
        y_max=6,
        x_min=3,
        x_max=8
    )

    assert isinstance(recorte, ImagenRadiografia)
    assert recorte is not img
    assert recorte.data.shape == (4, 5)
    assert np.array_equal(recorte.data, data[2:6, 3:8])
    assert recorte.titulo_actual == "Recorte [3:8, 2:6]"


def test_seleccionar_region_interes_invalida_minimo_mayor():
    """
    Verifica que se lance ValueError si los mínimos son mayores
    o iguales que los máximos.
    """

    data = np.zeros((10, 10), dtype=np.uint8)

    img = ImagenRadiografia(data)

    try:
        img.seleccionar_region_interes(
            y_min=7,
            y_max=3,
            x_min=2,
            x_max=5
        )

        assert False

    except ValueError:
        assert True


def test_seleccionar_region_interes_fuera_de_rango():
    """
    Verifica que se lance ValueError si las coordenadas exceden
    las dimensiones de la imagen.
    """

    data = np.zeros((10, 10), dtype=np.uint8)

    img = ImagenRadiografia(data)

    try:
        img.seleccionar_region_interes(
            y_min=2,
            y_max=12,
            x_min=1,
            x_max=5
        )

        assert False

    except ValueError:
        assert True


def test_detectar_bordes():
    """
    Verifica que detectar_bordes modifique self.data, conserve
    dimensiones y retorne self.
    """

    data = np.zeros((30, 30), dtype=np.uint8)
    data[10:20, 10:20] = 255

    img = ImagenRadiografia(data, tipo_estudio="torax")

    resultado = img.detectar_bordes()

    assert resultado is img
    assert img.data.shape == data.shape
    assert img.data.dtype == np.uint8
    assert img.data.min() >= 0
    assert img.data.max() <= 255
    assert img.titulo_actual == "RX con detección de bordes"


def test_historial_ajustar_brillo():
    """
    Verifica que ajustar_brillo agregue un registro al historial.
    """

    data = np.zeros((10, 10), dtype=np.uint8)

    img = ImagenRadiografia(data)

    cantidad_inicial = len(img.historial)

    img.ajustar_brillo(20)

    assert len(img.historial) == cantidad_inicial + 1


def test_historial_invertir_intensidades_info():
    """
    Verifica que invertir_intensidades agregue un registro
    al historial guardado en Info.
    """

    data = np.array([
        [0, 100],
        [150, 255]
    ], dtype=np.uint8)

    img = ImagenRadiografia(data)

    cantidad_inicial = len(img.info.historial)

    img.invertir_intensidades()

    assert len(img.info.historial) == cantidad_inicial + 1


def test_ver_imagen_original_no_es_nula():
    """
    Verifica que la imagen original quede guardada en el atributo original
    heredado de Imagen.
    """

    data = np.array([
        [0, 50],
        [100, 150]
    ], dtype=np.uint8)

    img = ImagenRadiografia(data)

    assert img.original is not None
    assert np.array_equal(img.original, data)


def test_modificar_data_no_modifica_original_en_brillo():
    """
    Verifica que ajustar_brillo use self.original como base y que
    self.original siga existiendo.
    """

    data = np.array([
        [0, 50],
        [100, 150]
    ], dtype=np.uint8)

    img = ImagenRadiografia(data)

    original_antes = img.original.copy()

    img.ajustar_brillo(50)

    assert not np.array_equal(img.data, original_antes)
    assert np.array_equal(img.original, original_antes)


# ==========================================================
# TESTS CON RADIOGRAFÍA REAL
# ==========================================================

def test_cargar_radiografia_real():
    """
    Verifica que pueda cargarse una radiografía real.
    Cambiar RUTA_RADIOGRAFIA por una ruta válida antes de ejecutar.
    """

    imagen_base = Imagen.cargar(RUTA_RADIOGRAFIA)

    rx = ImagenRadiografia(
        imagen_base.data,
        tipo_estudio="radiografia real",
        brillo=0
    )

    assert rx.data is not None
    assert rx.data.ndim == 2
    assert isinstance(rx, ImagenRadiografia)


def test_dimensiones_radiografia_real():
    """
    Verifica que la radiografía real tenga dimensiones válidas.
    """

    imagen_base = Imagen.cargar(RUTA_RADIOGRAFIA)

    rx = ImagenRadiografia(
        imagen_base.data,
        tipo_estudio="radiografia real",
        brillo=0
    )

    filas, columnas = rx.data.shape

    assert filas > 0
    assert columnas > 0


def test_ajustar_brillo_radiografia_real():
    """
    Verifica que se pueda ajustar el brillo en una radiografía real.
    """

    imagen_base = Imagen.cargar(RUTA_RADIOGRAFIA)

    rx = ImagenRadiografia(
        imagen_base.data,
        tipo_estudio="radiografia real",
        brillo=0
    )

    rx.ajustar_brillo(40)

    assert rx.data.dtype == np.uint8
    assert rx.data.min() >= 0
    assert rx.data.max() <= 255
    assert rx.brillo == 40


def test_mejorar_contraste_radiografia_real():
    """
    Verifica que se pueda mejorar el contraste en una radiografía real.
    """

    imagen_base = Imagen.cargar(RUTA_RADIOGRAFIA)

    rx = ImagenRadiografia(
        imagen_base.data,
        tipo_estudio="radiografia real",
        brillo=0
    )

    rx.mejorar_contraste(1.5)

    assert rx.data.dtype == np.uint8
    assert rx.data.min() >= 0
    assert rx.data.max() <= 255


def test_invertir_intensidades_radiografia_real():
    """
    Verifica que se puedan invertir las intensidades de una radiografía real.
    """

    imagen_base = Imagen.cargar(RUTA_RADIOGRAFIA)

    rx = ImagenRadiografia(
        imagen_base.data,
        tipo_estudio="radiografia real",
        brillo=0
    )

    rx.invertir_intensidades()

    assert rx.data.dtype == np.uint8
    assert rx.data.min() >= 0
    assert rx.data.max() <= 255


def test_ecualizar_intensidades_radiografia_real():
    """
    Verifica que se pueda ecualizar una radiografía real.
    """

    imagen_base = Imagen.cargar(RUTA_RADIOGRAFIA)

    rx = ImagenRadiografia(
        imagen_base.data,
        tipo_estudio="radiografia real",
        brillo=0
    )

    rx.ecualizar_intensidades()

    assert rx.data.dtype == np.uint8
    assert rx.data.min() >= 0
    assert rx.data.max() <= 255


def test_detectar_bordes_radiografia_real():
    """
    Verifica que se puedan detectar bordes en una radiografía real.
    """

    imagen_base = Imagen.cargar(RUTA_RADIOGRAFIA)

    rx = ImagenRadiografia(
        imagen_base.data,
        tipo_estudio="radiografia real",
        brillo=0
    )

    rx.detectar_bordes()

    assert rx.data.dtype == np.uint8
    assert rx.data.min() >= 0
    assert rx.data.max() <= 255


def test_recortar_region_radiografia_real():
    """
    Verifica que se pueda recortar una región central de una radiografía real.
    """

    imagen_base = Imagen.cargar(RUTA_RADIOGRAFIA)

    rx = ImagenRadiografia(
        imagen_base.data,
        tipo_estudio="radiografia real",
        brillo=0
    )

    alto, ancho = rx.data.shape

    y_min = alto // 4
    y_max = alto // 2
    x_min = ancho // 4
    x_max = ancho // 2

    recorte = rx.seleccionar_region_interes(
        y_min=y_min,
        y_max=y_max,
        x_min=x_min,
        x_max=x_max
    )

    assert isinstance(recorte, ImagenRadiografia)
    assert recorte.data.ndim == 2
    assert recorte.data.shape == (y_max - y_min, x_max - x_min)


# ==========================================================
# EJECUCIÓN MANUAL
# ==========================================================

if __name__ == "__main__":

    tests = [
        test_creacion_imagen_radiografica,
        test_rechazar_imagen_3d,
        test_conversion_float_0_1_a_uint8,
        test_ajustar_brillo_positivo,
        test_ajustar_brillo_negativo,
        test_ajustar_brillo_rango_alto,
        test_mejorar_contraste,
        test_invertir_intensidades,
        test_ecualizar_intensidades,
        test_seleccionar_region_interes,
        test_seleccionar_region_interes_invalida_minimo_mayor,
        test_seleccionar_region_interes_fuera_de_rango,
        test_detectar_bordes,
        test_historial_ajustar_brillo,
        test_historial_invertir_intensidades_info,
        test_ver_imagen_original_no_es_nula,
        test_modificar_data_no_modifica_original_en_brillo,
    ]

    tests_reales = [
        test_cargar_radiografia_real,
        test_dimensiones_radiografia_real,
        test_ajustar_brillo_radiografia_real,
        test_mejorar_contraste_radiografia_real,
        test_invertir_intensidades_radiografia_real,
        test_ecualizar_intensidades_radiografia_real,
        test_detectar_bordes_radiografia_real,
        test_recortar_region_radiografia_real,
    ]

    print("\n=== EJECUCIÓN DE TESTS DE IMAGEN RADIOGRÁFICA ===\n")

    aprobados = 0

    for test in tests:

        try:
            test()

            print(f"✓ {test.__name__}")

            aprobados += 1

        except AssertionError:

            print(f"✗ {test.__name__}")

        except Exception as e:

            print(f"✗ {test.__name__} -> ERROR: {e}")

    print(f"\nResultado tests unitarios: {aprobados}/{len(tests)} tests aprobados")

    print("\n=== EJECUCIÓN DE TESTS CON RADIOGRAFÍA REAL ===\n")
    print("Recordá cambiar RUTA_RADIOGRAFIA antes de ejecutar estos tests.\n")

    aprobados_reales = 0

    for test in tests_reales:

        try:
            test()

            print(f"✓ {test.__name__}")

            aprobados_reales += 1

        except AssertionError:

            print(f"✗ {test.__name__}")

        except Exception as e:

            print(f"✗ {test.__name__} -> ERROR: {e}")

    print(f"\nResultado tests reales: {aprobados_reales}/{len(tests_reales)} tests aprobados")


# ==========================================================
# PRUEBA VISUAL CON IMÁGENES REALES
# ==========================================================

# # Para usar esta sección:
# # 1. Cambiar RUTA_RADIOGRAFIA por la ruta real.
# # 2. Descomentar las líneas que quieras probar.
# # 3. Ejecutar el archivo.

imagen_base = Imagen.cargar(RUTA_RADIOGRAFIA)

rx = ImagenRadiografia(
    imagen_base.data,
    tipo_estudio="radiografia real",
    brillo=0
)

# 1. Ver imagen original
rx.visualizar(titulo="Radiografía original")

# 2. Ajustar brillo
rx.ajustar_brillo(50)
rx.visualizar()

# 3. Volver a ver la imagen original guardada
rx.ver_imgOriginal(titulo="Radiografía original guardada")

# 4. Mejorar contraste
rx.mejorar_contraste(1.5)
rx.visualizar()

# # 5. Invertir intensidades
rx.invertir_intensidades()
rx.visualizar()

# # 6. Ecualizar intensidades
rx.ecualizar_intensidades()
rx.visualizar()

# 7. Detectar bordes
rx.detectar_bordes()
rx.visualizar()

# 8. Recortar región de interés
alto, ancho = rx.data.shape
recorte = rx.seleccionar_region_interes(
    y_min=alto // 4,
    y_max=alto // 2,
    x_min=ancho // 4,
    x_max=ancho // 2
)
recorte.visualizar()
print(rx.historial)
print(rx.info.datos)


#Probamos el metodo visualizar_cluster
carpeta_rx = "tests/imagenes_test/radiografias"
rx = ImagenRadiografia.cargar(ruta=RUTA_RADIOGRAFIA)
rx.visualizar_cluster(carpeta_radiografias=carpeta_rx)
print(rx.historial)
