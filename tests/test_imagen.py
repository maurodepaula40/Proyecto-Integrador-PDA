import sys
import os
#Esto hace lo mismo que el comando 'set PYTHONPATH=src' pero automáticamente
sys.path.append(os.path.abspath("src"))
from bioimagenes.core.imagen import Imagen
from bioimagenes.core.historial import Historial
from bioimagenes.filtros.filtro import Filtro
import numpy as np
import matplotlib.pyplot as plt
from bioimagenes.medicas.imagen_radiografia import ImagenRadiografica
import pydicom


#Prueba con imagen en escala de grises

#datovich = np.random.randint(0, 255, (100, 100)) 
#img = Imagen(data=datovich, info=None)
#img.visualizar()

#prueba con imagen RGB
#dato = np.random.randint(0, 255, (100, 100,3)) 
#img = Imagen(data=dato, info=None)
#img.visualizar()

#Prueba de tipo de dato (error)
#data = [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]]
#image = Imagen(data=data, info=None)
#image.visualizar()

#PRUEBA DE TIPO DE DIMENSIONES

#data = np.random.randint(0,255,(100,100,5))
#dimensiones = Imagen(data=data, info=None)
#dimensiones.visualizar()

#Prueba con una imagen termografica

#img =Imagen.cargar("tests/imagenes_test/termografias/N11102.jpg")
#img.visualizar()
#print(img)

#imagen_radiografica = Imagen.cargar("tests/imagenes_test/termografias/N11103.jpg")
#imagen_radiografica.visualizar()



# Ruta de la imagen de prueba
RUTA_IMAGEN = "tests/imagenes_test/radiografias/46523715740384360192496023767246369337_veyewt.png"

# # TEST 1: Cargar imagen real y verificar len()
#print("TEST 1: Verificar len() con imagen real")

# # Verificamos que el archivo existe
#if os.path.exists(RUTA_IMAGEN):
    # Cargamos la imagen usando el método de clase
#    img = Imagen.cargar(RUTA_IMAGEN)
    
#     # Obtenemos el resultado de len()
#    resultado = len(img)
    
#     # Calculamos manualmente cuántos píxeles debería tener
#    filas, columnas = img.data.shape[:2]
#    esperado = filas * columnas
    
#     # Comparamos resultado con lo esperado
#    if resultado == esperado:
#        print(f"PASÓ: len() = {resultado}")
#        print(f"  Imagen: {filas} x {columnas} píxeles")
#    else:
#        print(f"FALLÓ: esperado {esperado}, obtuvo {resultado}")
#else:
#   print(f"No se encontró la imagen en {RUTA_IMAGEN}")

# print()

# # TEST 2: Verificar que len() retorna un número positivo
# print("TEST 2: Verificar que len() es positivo")

# if os.path.exists(RUTA_IMAGEN):
#     img = Imagen.leer_archivos(RUTA_IMAGEN)
#     resultado = len(img)
    
#     # Verificamos que sea mayor a 0
#     if resultado > 0:
#         print(f"PASÓ: len() = {resultado} (positivo)")
#     else:
#         print(f"FALLÓ: len() debería ser > 0")
# else:
#     print(f"No se encontró la imagen")

# print()

# # TEST 3: Verificar que len() retorna un entero
# print("TEST 3: Verificar que len() retorna un entero")

# if os.path.exists(RUTA_IMAGEN):
#     img = Imagen.leer_archivos(RUTA_IMAGEN)
#     resultado = len(img)
    
#     # Verificamos el tipo de dato
#     if isinstance(resultado, int):
#         print(f"PASÓ: len() retorna tipo int")
#     else:
#         print(f"FALLÓ: len() retorna {type(resultado)}, esperado int")
# else:
#     print(f"No se encontró la imagen")

# print()

# # TEST 4: Mostrar información de la imagen
# print("TEST 4: Información de la imagen")

# if os.path.exists(RUTA_IMAGEN):
#     img = Imagen.leer_archivos(RUTA_IMAGEN)
    
#     # Mostramos los datos de la imagen
#     print(f"Forma de la imagen: {img.data.shape}")
#     print(f"Total de píxeles: {len(img)}")
#     print(f"Tipo de dato: {img.data.dtype}")
#     print(f"Valor mínimo: {img.data.min()}")
#     print(f"Valor máximo: {img.data.max()}")
# else:
#     print(f"No se encontró la imagen")

# TEST 1: Verificar que __str__() retorna un string
#print("TEST 1: Verificar que __str__() retorna un string")

#if os.path.exists(RUTA_IMAGEN):
    #img = Imagen.leer_archivos(RUTA_IMAGEN)
    
    # Obtenemos el resultado de str()
    #resultado = str(img)
    
    # Verificamos que sea un string
    #if isinstance(resultado, str):
    #   print("PASÓ: __str__() retorna un string")
    #else:
    #    print(f"FALLÓ: __str__() retorna {type(resultado)}, esperado str")
#else:
#    print(f"No se encontró la imagen")

#print()

# TEST 2: Verificar que __str__() contiene información de dimensiones
#print("TEST 2: Verificar que __str__() contiene dimensiones")

#if os.path.exists(RUTA_IMAGEN):
#    img = Imagen.leer_archivos(RUTA_IMAGEN)
#    resultado = str(img)
    
    # Obtenemos las dimensiones
#    filas, columnas = img.data.shape[:2]
    
    # Verificamos que el string contenga las dimensiones
#    if str(filas) in resultado and str(columnas) in resultado:
##        print(f"PASÓ: __str__() contiene dimensiones ({filas} x {columnas})")
#    else:
#        print(f"FALLÓ: __str__() no contiene las dimensiones")
#else:
#    print(f"No se encontró la imagen")

#print()

# TEST 3: Verificar que __str__() contiene el tipo de imagen
#print("TEST 3: Verificar que __str__() contiene tipo de imagen")

#if os.path.exists(RUTA_IMAGEN):
#    img = Imagen.leer_archivos(RUTA_IMAGEN)
#    resultado = str(img)
    
    # Verificamos si es RGB o escala de grises
#    if img.data.ndim == 3:
#        tipo_esperado = "RGB"
#    else:
#        tipo_esperado = "Escala de grises"
    
    # Verificamos que el string contenga el tipo
#    if tipo_esperado in resultado:
#        print(f"PASÓ: __str__() contiene tipo de imagen ({tipo_esperado})")
#    else:
#        print(f"FALLÓ: __str__() no contiene el tipo de imagen")
#else:
#    print(f"No se encontró la imagen")

#print()

# TEST 4: Verificar que __str__() contiene valores mín y máx
#print("TEST 4: Verificar que __str__() contiene valores mín y máx")

#if os.path.exists(RUTA_IMAGEN):
#    img = Imagen.leer_archivos(RUTA_IMAGEN)
#    resultado = str(img)
    
    # Obtenemos los valores mín y máx
#    valor_min = str(img.data.min())
#    valor_max = str(img.data.max())
    
    # Verificamos que estén en el string
##    if valor_min in resultado and valor_max in resultado:
#        print(f"PASÓ: __str__() contiene valores mín ({valor_min}) y máx ({valor_max})")
#    else:
#        print(f"FALLÓ: __str__() no contiene los valores mín y máx")
#else:
#    print(f"No se encontró la imagen")

#print()

# TEST 5: Verificar que __str__() no está vacío
#print("TEST 5: Verificar que __str__() no está vacío")
#print("-" * 50)

#if os.path.exists(RUTA_IMAGEN):
#    img = Imagen.leer_archivos(RUTA_IMAGEN)
#    resultado = str(img)
    
    # Verificamos que el string no esté vacío
#    if len(resultado) > 0:
#        print(f"PASÓ: __str__() retorna {len(resultado)} caracteres")
#    else:
#        print(f"FALLÓ: __str__() está vacío")
#else:
#    print(f"No se encontró la imagen")

#print()

# TEST 6: Verificar que print(imagen) funciona
#print("TEST 6: Verificar que print(imagen) funciona")

#if os.path.exists(RUTA_IMAGEN):
#    img = Imagen.leer_archivos(RUTA_IMAGEN)
    
    # Obtenemos el resultado de str()
#    resultado = str(img)
    
    # Verificamos que no esté vacío
#    if len(resultado) > 0:
#        print("PASÓ: print(imagen) funciona")
#        print(resultado)
#    else:
#        print("FALLÓ: str(imagen) está vacío")
#else:
#    print(f"No se encontró la imagen")

# TEST 7: Verificar que __str__() contiene el total de píxeles
#print("TEST 7: Verificar que __str__() contiene total de píxeles")

#if os.path.exists(RUTA_IMAGEN):
#    img = Imagen.leer_archivos(RUTA_IMAGEN)
#    resultado = str(img)
    
    # Obtenemos el total de píxeles
#    total_pixeles = str(len(img))
    
    # Verificamos que esté en el string
#    if total_pixeles in resultado:
#        print(f"PASÓ: __str__() contiene total de píxeles ({total_pixeles})")
#    else:
#        print(f"FALLÓ: __str__() no contiene el total de píxeles")
#else:
#    print(f"No se encontró la imagen")



#PRUEBA DEL METODO __getitem__
#img = Imagen.leer_archivos(RUTA_IMAGEN)
#print(img)
#print(img[1,3:8])
#print(img["500",122])
#print(img[400,500])
#print(len(img))

#help(Imagen)

#PRUEBA DEL METODO aplicar_filtro()

#img = Imagen.cargar(RUTA_IMAGEN)
## Detector de bordes inferiores (Bottom Sobel)
#bottomSobel = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
#blur = np.array([[0.0625, 0.125,0.0625],[0.125, 0.25, 0.125],[0.0625, 0.125,0.0625]])

##Outline
#ouutline = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
##Sharpen
#sharpen = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])

## Detector de bordes superiores (Top Sobel)
#topSobel = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])

## Detector de bordes izquierdos (Left Sobel)
#leftSobel = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
## Detector de bordes derechos (Right Sobel)
#rightSobel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

#f = Filtro(tipo="rightSobel", kernel=rightSobel, tamaño="3x3")
#***** Aplicamos el filtro a la imagen *****
##imagen_filtrada = f.aplicar(img)
#imagen_filtrada.visualizar()
#img.visualizar()

#img.aplicar_filtro(f)
#img.visualizar

#print(f)

#img_tomografica= Imagen.cargar(RUTA_IMAGEN)
#print(type(img_tomografica.data))

img_rx = ImagenRadiografica.cargar(RUTA_IMAGEN)
img_rx.visualizar(titulo="RX de torax")
img_rx.seleccionar_region_interes(500,1000,300,1500)
img_rx.visualizar()
img_rx.detectar_bordes()
img_rx.visualizar()
img_rx.ver_imgOriginal()
img_rx.detectar_bordes()
img_rx.visualizar()
print(img_rx.historial)


# =====================================================================
# SCRIPT DE PRUEBA CON UNA IMAGEN REAL
# =====================================================================
if __name__ == "__main__":
    # 1. Cargamos una imagen real de tu computadora (reemplazá 'radiografia.jpg' por tu archivo)
    # cv2.IMREAD_GRAYSCALE la lee directamente en escala de grises
    ruta = "tests/imagenes_test/radiografias/216840111366964013829543166512013358092118761_02-089-145.png"
    imagen_real = Imagen.cargar(ruta)

    if imagen_real is None:
        print(
            f"No se pudo encontrar o abrir la imagen en '{ruta}'. Asegurate de que el nombre sea correcto."
        )
    else:
        print(
            f"Imagen real cargada con éxito. Tamaño original: {imagen_real.data.shape}"
        )

        # 2. SIMULACIÓN DE PROCESAMIENTO MÉDICO (Generamos valores fuera de rango)
        # Para probar que nuestra función de normalización realmente funciona, vamos a alterar
        # la imagen multiplicándola por un factor flotante y sumándole números.
        # Esto simula lo que pasaría tras aplicar filtros complejos como convoluciones o Sobel.
        imagen_alterada = (imagen_real.data.astype(np.float32) * 4.5) - 300.0

        print(
            f"--- Antes de normalizar ---"
            f"\nMínimo valor en la matriz alterada: {np.min(imagen_alterada)}"
            f"\nMáximo valor en la matriz alterada: {np.max(imagen_alterada)}"
        )

        # 3. PROBAMOS NUESTRA FUNCIÓN
        # Le pasamos la matriz con valores "rotos" (negativos y mayores a 255)
        imagen_resultado = Imagen.normalizar(imagen_alterada)

        print(
            f"--- Después de normalizar ---"
            f"\nMínimo valor resultante: {np.min(imagen_resultado)}"
            f"\nMáximo valor resultante: {np.max(imagen_resultado)}"
            f"\nTipo de dato final: {imagen_resultado.dtype}"
        )