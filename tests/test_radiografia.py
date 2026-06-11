import unittest
import numpy as np
import matplotlib.pyplot as plt
from bioimagenes.medicas.imagen_radiografia import ImagenRadiografia
from bioimagenes.core.imagen import Imagen

import numpy as np
import matplotlib.pyplot as plt

from bioimagenes.medicas.imagen_radiografia import ImagenRadiografia


# ============================================================
# TESTS DE FUNCIONAMIENTO - IMAGEN RADIOGRAFIA
# ============================================================

print("\n==============================")
print("TESTS DE FUNCIONAMIENTO")
print("==============================")


# ------------------------------------------------------------
# TEST 1 - Crear una radiografía válida
# ------------------------------------------------------------

print("\nTEST 1 - Crear ImagenRadiografia con matriz 2D")

matriz = np.array([
    [0, 50, 100],
    [150, 200, 255],
    [30, 80, 120]
], dtype=np.uint8)

rx = ImagenRadiografia(matriz, tipo_estudio="tórax", brillo=0)

assert isinstance(rx, ImagenRadiografia)
assert isinstance(rx.data, np.ndarray)
assert rx.data.shape == (3, 3)
assert rx.tipo_estudio == "tórax"
assert rx.brillo == 0

print("OK - La radiografía se creó correctamente.")


# ------------------------------------------------------------
# TEST 2 - Validar que no acepte imagen 3D
# ------------------------------------------------------------

print("\nTEST 2 - Validar error con matriz 3D")

matriz_3d = np.zeros((10, 10, 3), dtype=np.uint8)

try:
    rx_3d = ImagenRadiografia(matriz_3d)
    print("ERROR - La clase aceptó una matriz 3D y no debería.")
except ValueError:
    print("OK - La clase rechaza matrices 3D correctamente.")


# ------------------------------------------------------------
# TEST 3 - Conversión de imagen float normalizada
# ------------------------------------------------------------

print("\nTEST 3 - Crear radiografía desde valores float entre 0 y 1")

matriz_float = np.array([
    [0.0, 0.5],
    [0.75, 1.0]
], dtype=float)

rx_float = ImagenRadiografia(matriz_float, tipo_estudio="mano")

assert rx_float.data.dtype == np.uint8
assert rx_float.data.max() == 255
assert rx_float.data.min() == 0

print("OK - La imagen float se convirtió correctamente a uint8.")


# ------------------------------------------------------------
# TEST 4 - Ajustar brillo positivo
# ------------------------------------------------------------

print("\nTEST 4 - Ajustar brillo positivo")

matriz_brillo = np.array([
    [0, 50, 100],
    [150, 200, 250]
], dtype=np.uint8)

rx_brillo = ImagenRadiografia(matriz_brillo, tipo_estudio="tórax")

rx_brillo.ajustar_brillo(20)

assert rx_brillo.brillo == 20
assert rx_brillo.data.dtype == np.uint8
assert rx_brillo.data.min() >= 0
assert rx_brillo.data.max() <= 255

print("OK - El brillo positivo se aplicó correctamente.")


# ------------------------------------------------------------
# TEST 5 - Ajustar brillo negativo
# ------------------------------------------------------------

print("\nTEST 5 - Ajustar brillo negativo")

matriz_brillo_negativo = np.array([
    [20, 60, 100],
    [150, 200, 255]
], dtype=np.uint8)

rx_brillo_negativo = ImagenRadiografia(matriz_brillo_negativo, tipo_estudio="tórax")

rx_brillo_negativo.ajustar_brillo(-30)

assert rx_brillo_negativo.brillo == -30
assert rx_brillo_negativo.data.dtype == np.uint8
assert rx_brillo_negativo.data.min() >= 0
assert rx_brillo_negativo.data.max() <= 255

print("OK - El brillo negativo se aplicó correctamente.")


# ------------------------------------------------------------
# TEST 6 - Ajustar brillo en imagen con rango mayor a 255
# ------------------------------------------------------------

print("\nTEST 6 - Ajustar brillo en imagen con rango mayor a 255")

matriz_rango_alto = np.array([
    [0, 1000, 2000],
    [3000, 4000, 5000]
], dtype=np.uint16)

rx_rango_alto = ImagenRadiografia(matriz_rango_alto, tipo_estudio="columna")

rx_rango_alto.ajustar_brillo(30)

assert rx_rango_alto.data.dtype == np.uint8
assert rx_rango_alto.data.min() >= 0
assert rx_rango_alto.data.max() <= 255

print("OK - El brillo funciona con imágenes fuera del rango 0-255.")


# ------------------------------------------------------------
# TEST 7 - Mejorar contraste
# ------------------------------------------------------------

print("\nTEST 7 - Mejorar contraste")

matriz_contraste = np.array([
    [80, 100, 120],
    [130, 150, 170]
], dtype=np.uint8)

rx_contraste = ImagenRadiografia(matriz_contraste, tipo_estudio="abdomen")

rx_contraste_mejorada = rx_contraste.mejorar_contraste(factor=1.5)

assert isinstance(rx_contraste_mejorada, np.ndarray)
assert rx_contraste_mejorada.data.shape == rx_contraste.data.shape
assert rx_contraste_mejorada.data.dtype == np.uint8
assert rx_contraste_mejorada.data.min() >= 0
assert rx_contraste_mejorada.data.max() <= 255

print("OK - El contraste se mejoró correctamente.")


# ------------------------------------------------------------
# TEST 8 - Invertir intensidades
# ------------------------------------------------------------

print("\nTEST 8 - Invertir intensidades")

matriz_invertir = np.array([
    [0, 100],
    [200, 255]
], dtype=np.uint8)

rx_invertir = ImagenRadiografia(matriz_invertir, tipo_estudio="tórax")

rx_invertida = rx_invertir.invertir_intensidades()

esperado = np.array([
    [255, 155],
    [55, 0]
], dtype=np.uint8)

assert isinstance(rx_invertida, ImagenRadiografia)
assert np.array_equal(rx_invertida.data, esperado)

print("OK - Las intensidades se invirtieron correctamente.")


# ------------------------------------------------------------
# TEST 9 - Ecualizar intensidades
# ------------------------------------------------------------

print("\nTEST 9 - Ecualizar intensidades")

matriz_ecualizar = np.array([
    [0, 0, 50],
    [100, 150, 255]
], dtype=np.uint8)

rx_ecualizar = ImagenRadiografia(matriz_ecualizar, tipo_estudio="tórax")

rx_ecualizada = rx_ecualizar.ecualizar_intensidades()

assert isinstance(rx_ecualizada, ImagenRadiografia)
assert rx_ecualizada.data.shape == rx_ecualizar.data.shape
assert rx_ecualizada.data.dtype == np.uint8
assert rx_ecualizada.data.min() >= 0
assert rx_ecualizada.data.max() <= 255

print("OK - La ecualización de intensidades funciona correctamente.")


# ------------------------------------------------------------
# TEST 10 - Seleccionar región de interés válida
# ------------------------------------------------------------

print("\nTEST 10 - Seleccionar región de interés válida")

matriz_region = np.arange(100).reshape(10, 10).astype(np.uint8)

rx_region = ImagenRadiografia(matriz_region, tipo_estudio="mano")

recorte = rx_region.seleccionar_region_interes(
    y_min=2,
    y_max=6,
    x_min=3,
    x_max=8
)

assert isinstance(recorte, ImagenRadiografia)
assert recorte.data.shape == (4, 5)

print("OK - La región de interés se recortó correctamente.")


# ------------------------------------------------------------
# TEST 11 - Seleccionar región con coordenadas inválidas
# ------------------------------------------------------------

print("\nTEST 11 - Validar error en región de interés inválida")

rx_region_error = ImagenRadiografia(np.zeros((10, 10), dtype=np.uint8))

try:
    rx_region_error.seleccionar_region_interes(
        y_min=7,
        y_max=3,
        x_min=2,
        x_max=5
    )
    print("ERROR - Aceptó una región inválida.")
except ValueError:
    print("OK - La clase rechaza regiones inválidas correctamente.")


# ------------------------------------------------------------
# TEST 12 - Detección de bordes
# ------------------------------------------------------------

print("\nTEST 12 - Detectar bordes")

matriz_bordes = np.zeros((20, 20), dtype=np.uint8)
matriz_bordes[5:15, 5:15] = 255

rx_bordes = ImagenRadiografia(matriz_bordes, tipo_estudio="tórax")

rx_bordes.detectar_bordes()

assert rx_bordes.data.shape == matriz_bordes.shape
assert rx_bordes.data.dtype == np.uint8
assert rx_bordes.data.min() >= 0
assert rx_bordes.data.max() <= 255

print("OK - La detección de bordes se ejecutó correctamente.")


# ------------------------------------------------------------
# TEST 13 - Propiedad region_interes
# ------------------------------------------------------------

print("\nTEST 13 - Verificar propiedad region_interes")

rx_propiedad = ImagenRadiografia(np.zeros((10, 10), dtype=np.uint8))

assert rx_propiedad.region_interes is None

print("OK - La propiedad region_interes funciona correctamente.")


print("\n==============================")
print("TODOS LOS TESTS DE FUNCIONAMIENTO FINALIZARON")
print("==============================")


# ============================================================
# TESTS CON IMÁGENES REALES
# ============================================================

print("\n==============================")
print("TESTS CON IMÁGENES REALES")
print("==============================")


# ------------------------------------------------------------
# IMPORTANTE:
# Cambiar esta ruta por la ruta real de tu imagen radiográfica.
# Por ejemplo:
# ruta_radiografia = r"C:\Users\belen\Proyecto-Integrador-PDA\imagenes\radiografia_torax.png"
# ------------------------------------------------------------

ruta_radiografia = r"tests/imagenes_test/radiografias/46523715740384360192496023767246369337_veyewt.png"


# ------------------------------------------------------------
# TEST REAL 1 - Cargar imagen real
# ------------------------------------------------------------

print("\nTEST REAL 1 - Cargar imagen radiográfica real")

try:
    from bioimagenes.core.imagen import Imagen

    imagen_base = Imagen.cargar(ruta_radiografia)

    rx_real = ImagenRadiografia(
        imagen_base.data,
        tipo_estudio="radiografía real",
        brillo=0
    )

    assert isinstance(rx_real, ImagenRadiografia)
    assert isinstance(rx_real.data, np.ndarray)
    assert rx_real.data.ndim == 2

    print("OK - La imagen real se cargó correctamente.")

except Exception as e:
    print(f"No se pudo cargar la imagen real. Revisar ruta o formato. Error: {e}")


# ------------------------------------------------------------
# TEST REAL 2 - Visualizar imagen real original
# ------------------------------------------------------------

print("\nTEST REAL 2 - Visualizar imagen real original")

try:
    rx_real.visualizar()
    print("OK - La imagen real original se visualizó correctamente.")

except Exception as e:
    print(f"No se pudo visualizar la imagen real original. Error: {e}")


# ------------------------------------------------------------
# TEST REAL 3 - Ajustar brillo y visualizar
# ------------------------------------------------------------

print("\nTEST REAL 3 - Ajustar brillo en imagen real")

try:
    rx_real.ajustar_brillo(50)
    rx_real.visualizar()
    print("OK - El brillo de la imagen real se ajustó correctamente.")

except Exception as e:
    print(f"No se pudo ajustar el brillo de la imagen real. Error: {e}")


# ------------------------------------------------------------
# TEST REAL 4 - Mejorar contraste y visualizar
# ------------------------------------------------------------

print("\nTEST REAL 4 - Mejorar contraste en imagen real")

try:
    rx_real_contraste = rx_real.mejorar_contraste(factor=1.5)
    rx_real_contraste.visualizar()
    print("OK - El contraste de la imagen real se mejoró correctamente.")

except Exception as e:
    print(f"No se pudo mejorar el contraste de la imagen real. Error: {e}")


# ------------------------------------------------------------
# TEST REAL 5 - Invertir intensidades y visualizar
# ------------------------------------------------------------

print("\nTEST REAL 5 - Invertir intensidades en imagen real")

try:
    rx_real_invertida = rx_real.invertir_intensidades()
    rx_real_invertida.visualizar()
    print("OK - Las intensidades de la imagen real se invirtieron correctamente.")

except Exception as e:
    print(f"No se pudo invertir la imagen real. Error: {e}")


# ------------------------------------------------------------
# TEST REAL 6 - Ecualizar intensidades y visualizar
# ------------------------------------------------------------

print("\nTEST REAL 6 - Ecualizar intensidades en imagen real")

try:
    rx_real_ecualizada = rx_real.ecualizar_intensidades()
    rx_real_ecualizada.visualizar()
    print("OK - La imagen real se ecualizó correctamente.")

except Exception as e:
    print(f"No se pudo ecualizar la imagen real. Error: {e}")


# ------------------------------------------------------------
# TEST REAL 7 - Detectar bordes y visualizar
# ------------------------------------------------------------

print("\nTEST REAL 7 - Detectar bordes en imagen real")

try:
    rx_real_bordes = ImagenRadiografia(
        imagen_base.data,
        tipo_estudio="radiografía real",
        brillo=0
    )

    rx_real_bordes.detectar_bordes()
    rx_real_bordes.visualizar()

    print("OK - Los bordes de la imagen real se detectaron correctamente.")

except Exception as e:
    print(f"No se pudo detectar bordes en la imagen real. Error: {e}")


# ------------------------------------------------------------
# TEST REAL 8 - Seleccionar región de interés en imagen real
# ------------------------------------------------------------

print("\nTEST REAL 8 - Seleccionar región de interés en imagen real")

try:
    alto, ancho = rx_real.data.shape

    y_min = alto // 4
    y_max = alto // 2
    x_min = ancho // 4
    x_max = ancho // 2

    rx_real_recorte = rx_real.seleccionar_region_interes(
        y_min=y_min,
        y_max=y_max,
        x_min=x_min,
        x_max=x_max
    )

    rx_real_recorte.visualizar()

    print("OK - La región de interés de la imagen real se recortó correctamente.")

except Exception as e:
    print(f"No se pudo seleccionar la región de interés en la imagen real. Error: {e}")


print("\n==============================")
print("TESTS CON IMÁGENES REALES FINALIZADOS")
print("==============================")
