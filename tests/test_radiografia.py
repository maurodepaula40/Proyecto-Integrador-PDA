import numpy as np
import matplotlib.pyplot as plt
from bioimagenes.medicas.imagen_radiografia import ImagenRadiografia


# # #==========================================================
# # #TESTS UNITARIOS
# # #==========================================================

# def test_creacion_radiografia():
#     """
#     Verifica que la radiografía se cree correctamente.
#     """

#     data = np.random.randint(0, 256, (20, 20), dtype=np.uint8)

#     img = ImagenRadiografia(
#         data,
#         tipo_estudio="Torax",
#         brillo=20
#     )

#     assert img.tipo_estudio == "Torax"
#     assert img.brillo == 20


# def test_conversion_float_a_uint8():
#     """
#     Verifica que imágenes float normalizadas se conviertan a uint8.
#     """

#     data = np.random.rand(20, 20)

#     img = ImagenRadiografia(data)

#     assert img.data.dtype == np.uint8


# def test_mejorar_contraste():
#     """
#     Verifica que mejorar_contraste retorne una ImagenRadiografia.
#     """

#     data = np.array([
#         [50, 100],
#         [150, 200]
#     ], dtype=np.uint8)

#     img = ImagenRadiografia(data)

#     resultado = img.mejorar_contraste()

#     assert isinstance(resultado, ImagenRadiografia)


# def test_mejorar_contraste_modifica_imagen():
#     """
#     Verifica que los datos resultantes sean distintos.
#     """

#     data = np.array([
#         [50, 100],
#         [150, 200]
#     ], dtype=np.uint8)

#     img = ImagenRadiografia(data)

#     resultado = img.mejorar_contraste()

#     assert not np.array_equal(img.data, resultado.data)


# def test_invertir_intensidades():
#     """
#     Verifica la inversión correcta de intensidades.
#     """

#     data = np.array([
#         [0, 255],
#         [100, 200]
#     ], dtype=np.uint8)

#     img = ImagenRadiografia(data)

#     resultado = img.invertir_intensidades()

#     esperado = np.array([
#         [255, 0],
#         [155, 55]
#     ], dtype=np.uint8)

#     assert np.array_equal(resultado.data, esperado)


# def test_ecualizar_intensidades():
#     """
#     Verifica que la ecualización retorne una ImagenRadiografia.
#     """

#     data = np.array([
#         [50, 50, 50],
#         [100, 100, 100],
#         [150, 150, 150]
#     ], dtype=np.uint8)

#     img = ImagenRadiografia(data)

#     resultado = img.ecualizar_intensidades()

#     assert isinstance(resultado, ImagenRadiografia)


# def test_historial_mejorar_contraste():
#     """
#     Verifica que se registre la operación en el historial.
#     """

#     data = np.random.randint(0, 256, (20, 20), dtype=np.uint8)

#     img = ImagenRadiografia(data)

#     cantidad_inicial = len(img.info.historial)

#     img.mejorar_contraste()

#     assert len(img.info.historial) == cantidad_inicial + 1


# def test_historial_invertir_intensidades():
#     """
#     Verifica que la inversión quede registrada.
#     """

#     data = np.random.randint(0, 256, (20, 20), dtype=np.uint8)

#     img = ImagenRadiografia(data)

#     cantidad_inicial = len(img.info.historial)

#     img.invertir_intensidades()

#     assert len(img.info.historial) == cantidad_inicial + 1


# def test_historial_ecualizar_intensidades():
#     """
#     Verifica que la ecualización quede registrada.
#     """

#     data = np.random.randint(0, 256, (20, 20), dtype=np.uint8)

#     img = ImagenRadiografia(data)

#     cantidad_inicial = len(img.info.historial)

#     img.ecualizar_intensidades()

#     assert len(img.info.historial) == cantidad_inicial + 1


# # #==========================================================
# # #TESTS DE ERRORES
# # #==========================================================

# def test_data_none():
#     """
#     Debe lanzar ValueError si data es None.
#     """

#     try:

#         ImagenRadiografia(None)

#         assert False

#     except ValueError:

#         assert True


# def test_data_no_numpy():
#     """
#     Debe lanzar TypeError si data no es ndarray.
#     """

#     try:

#         ImagenRadiografia([[1, 2], [3, 4]])

#         assert False

#     except TypeError:

#         assert True


# def test_imagen_1d():
#     """
#     Debe lanzar ValueError para arrays de dimensión inválida.
#     """

#     try:

#         ImagenRadiografia(np.array([1, 2, 3]))

#         assert False

#     except ValueError:

#         assert True


# def test_imagen_rgb():
#     """
#     Debe lanzar ValueError porque la radiografía debe ser 2D.
#     """

#     try:

#         ImagenRadiografia(
#             np.random.randint(0, 255, (20, 20, 3))
#         )

#         assert False

#     except ValueError:

#         assert True

# # #==========================================================
# # #EJECUCIÓN MANUAL
# # #==========================================================

# if __name__ == "__main__":

#     tests = [
#         test_creacion_radiografia,
#         test_conversion_float_a_uint8,
#         test_mejorar_contraste,
#         test_mejorar_contraste_modifica_imagen,
#         test_invertir_intensidades,
#         test_ecualizar_intensidades,
#         test_historial_mejorar_contraste,
#         test_historial_invertir_intensidades,
#         test_historial_ecualizar_intensidades,
#         test_data_none,
#         test_data_no_numpy,
#         test_imagen_1d,
#         test_imagen_rgb,
#     ]

#     print("\n=== EJECUCIÓN DE TESTS DE IMAGEN RADIOGRÁFICA ===\n")

#     aprobados = 0

#     for test in tests:

#         try:
#             test()

#             print(f"✓ {test.__name__}")

#             aprobados += 1

#         except AssertionError:

#             print(f"✗ {test.__name__}")

#         except Exception as e:

#             print(f"✗ {test.__name__} -> ERROR: {e}")

#     print(f"\nResultado: {aprobados}/{len(tests)} tests aprobados")

## Prueba con imagenes reales:
data = plt.imread("docs/216840111366964013451228379692012257110540618_02-006-005.png")

img = ImagenRadiografia(data, tipo_estudio="Torax", brillo=0)
# resultado = img.mejorar_contraste(2)
# resultado.visualizar()


# invertida  = img.invertir_intensidades()
# invertida.visualizar()

# ecualizada = img.ecualizar_intensidades()
# ecualizada.visualizar()
