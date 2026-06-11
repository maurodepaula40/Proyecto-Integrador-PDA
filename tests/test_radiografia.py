import unittest
import numpy as np
import matplotlib.pyplot as plt
from bioimagenes.medicas.imagen_radiografia import ImagenRadiografica
from bioimagenes.core.imagen import Imagen


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



# 1. 'objeto_img' YA ES una instancia de ImagenRadiografica gracias a tu método .cargar()
# objeto_img = ImagenRadiografia.cargar("tests/imagenes_test/radiografias/216840111366964013307756408102012093111819763_01-114-013.png")
# objeto_img.visualizar()
# objeto_img.detectar_bordes()
# objeto_img.visualizar()
# radiografia = ImagenRadiografia.cargar("tests/imagenes_test/radiografias/216840111366964013829543166512013358092118761_02-089-145.png")
# radiografia.visualizar()
# radiografia.detectar_bordes()
# radiografia.visualizar()



# # =====================================================================
# # 2. EJECUCIÓN DEL TEST AUTOMÁTICO
# # =====================================================================

# def ejecutar_pruebas():
#     print("Iniciando pruebas del método 'detectar_bordes'...")
    
#     # 2. CORRECCIÓN: Asignamos el objeto directamente. 
#     # Modificamos sus atributos si el test lo requiere (como el tipo_estudio o brillo)
#     #img.tipo_estudio = "Imagen pixeleada"
#     #img.brillo = 50
    
#     # Guardamos las dimensiones originales tomándolas desde el .data interno del objeto
#     dimensiones_originales = objeto_img.data.shape
    
#     # 3. Ejecutamos el método a evaluar
#     objeto_img.detectar_bordes()

#     # --- VALIDACIONES ---
    
#     # Validación 1: Conservación de dimensiones
#     assert objeto_img.data.shape == dimensiones_originales, f"Error: Las dimensiones cambiaron. Esperado: {dimensiones_originales}, Obtenido: {objeto_img.data.shape}"
#     print(f"  [PASÓ] Validación de dimensiones correctas {objeto_img.data.shape}.")

#     # Validación 2: Existencia de bordes
#     assert np.any(objeto_img.data > 0), "Error matemático: El operador Sobel devolvió solo ceros. No detectó bordes."
#     print("  [PASÓ] Validación de contenido (Se detectaron bordes anatómicos).")

#     # Validación 3: Tipo de dato de salida
#     assert objeto_img.data.dtype == np.uint8, f"Error de tipo. Esperado: uint8, Obtenido: {objeto_img.data.dtype}"
#     print("  [PASÓ] Validación de tipo de dato (uint8).")

#         # --- VALIDACIÓN 4: Registro en el historial ---
#     mensaje_esperado = "Se realizó Detección de Bordes con operador Sobel"
    
#     # Comprobamos que el último movimiento coincida exactamente
#     assert objeto_img.historial.ultimo_cambio == mensaje_esperado, f"Error: El último cambio no coincide. Obtenido: {img.historial.ultimo_cambio}"
#     print("  [PASÓ] Validación del registro en el historial.")


#     print("\n¡Todas las pruebas pasaron exitosamente con la radiografía real!")

# if __name__ == "__main__":
#     ejecutar_pruebas()

# objeto_img = ImagenRadiografica.cargar("tests/imagenes_test/radiografias/216840111366964013307756408102012093111819763_01-114-013.png")
# objeto_img.visualizar("RX original de torax")
# objeto_img.detectar_bordes()
# objeto_img.visualizar("deteccion de bordes con sobel")
# objeto_img.ver_imgOriginal()
radiografia = ImagenRadiografica.cargar("tests/imagenes_test/radiografias/216840111366964013829543166512013358092118761_02-089-145.png")
radiografia.ajustar_brillo(0)
radiografia.visualizar()



# ==========================================
# EJECUCIÓN PRINCIPAL
# ==========================================
# if __name__ == "__main__":
#     # ➡️ REEMPLAZA ESTO por el nombre de tu carpeta real (ej: "mis_radiografias" o "dataset")
#    
    
#     # El método se ejecuta y automáticamente va a leer todo, procesar y abrir el gráfico
#     ImagenRadiografica.visualizar_cluster(carpeta_dataset, k=3)
