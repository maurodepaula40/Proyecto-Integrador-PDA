import sys
import os
#Esto hace lo mismo que el comando 'set PYTHONPATH=src' pero automáticamente
sys.path.append(os.path.abspath("src"))
from bioimagenes.core.imagen import Imagen
import numpy as np
import matplotlib.pyplot as plt
import cv2

#Prueba con imagen en escala de grises

#datovich = np.random.randint(0, 255, (100, 100)) 
#img = Imagen(data=datovich, info=None)
#img.visualizar()

#prueba con imagen RGB
#hola = np.ndarray()
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

#img =cv2.imread(r"N11102.jpg",  cv2.IMREAD_GRAYSCALE)
#prueba = Imagen(data=img, info=None)
#prueba.visualizar()
#print(img.shape)

#Prueba con imagen RADIOGRAFICA

#data=cv2.imread(r"329608354535639464795481936214199434429_kzcyhb.png", cv2.IMREAD_GRAYSCALE)
#img = Imagen(data=data, info=None)
#img.visualizar()

#Prueba con imagen TOMOGRAFICA

#imagen_tomografia = nib.load("AC421363f.nii")
#data_tomografia = imagen_tomografia.get_fdata()
#print(data_tomografia)

#Usando las siguientes 4 lineas, el slice no se ve porque esta fuera de rango 
#plt.imshow(data[:, :, data.shape[2]//2], cmap="gray")
#plt.title("Slice axial")
#plt.axis("off")
#plt.show()

#Aca lo normalizamos y se ve el slice
#slice_img = data_tomografia[:, :, data_tomografia.shape[2]//2]

#plt.imshow(slice_img, cmap="gray", vmin=slice_img.min(), vmax=slice_img.max())
#plt.title("Slice axial")
#plt.axis("off")
#plt.show()
#imagen_radiografica = Imagen.leer_archivos("N11102.jpg")
#imagen_radiografica.visualizar()


#imagen_rgb = Imagen.leer_archivos("espacios-color-fotografia.jpg")
#imagen_rgb.visualizar()
#imagen_rgb.bn()
#imagen_rgb.visualizar()


# Ruta de la imagen de prueba
RUTA_IMAGEN = r"tests\imagenes_test\termografias\N11102.jpg"

# TEST 1: Cargar imagen real y verificar len()
print("TEST 1: Verificar len() con imagen real")

# Verificamos que el archivo existe
if os.path.exists(RUTA_IMAGEN):
    # Cargamos la imagen usando el método de clase
    img = Imagen.leer_archivos(RUTA_IMAGEN)
    
    # Obtenemos el resultado de len()
    resultado = len(img)
    
    # Calculamos manualmente cuántos píxeles debería tener
    filas, columnas = img.data.shape[:2]
    esperado = filas * columnas
    
    # Comparamos resultado con lo esperado
    if resultado == esperado:
        print(f"PASÓ: len() = {resultado}")
        print(f"  Imagen: {filas} x {columnas} píxeles")
    else:
        print(f"FALLÓ: esperado {esperado}, obtuvo {resultado}")
else:
    print(f"No se encontró la imagen en {RUTA_IMAGEN}")

print()

# TEST 2: Verificar que len() retorna un número positivo
print("TEST 2: Verificar que len() es positivo")

if os.path.exists(RUTA_IMAGEN):
    img = Imagen.leer_archivos(RUTA_IMAGEN)
    resultado = len(img)
    
    # Verificamos que sea mayor a 0
    if resultado > 0:
        print(f"PASÓ: len() = {resultado} (positivo)")
    else:
        print(f"FALLÓ: len() debería ser > 0")
else:
    print(f"No se encontró la imagen")

print()

# TEST 3: Verificar que len() retorna un entero
print("TEST 3: Verificar que len() retorna un entero")

if os.path.exists(RUTA_IMAGEN):
    img = Imagen.leer_archivos(RUTA_IMAGEN)
    resultado = len(img)
    
    # Verificamos el tipo de dato
    if isinstance(resultado, int):
        print(f"PASÓ: len() retorna tipo int")
    else:
        print(f"FALLÓ: len() retorna {type(resultado)}, esperado int")
else:
    print(f"No se encontró la imagen")

print()

# TEST 4: Mostrar información de la imagen
print("TEST 4: Información de la imagen")

if os.path.exists(RUTA_IMAGEN):
    img = Imagen.leer_archivos(RUTA_IMAGEN)
    
    # Mostramos los datos de la imagen
    print(f"Forma de la imagen: {img.data.shape}")
    print(f"Total de píxeles: {len(img)}")
    print(f"Tipo de dato: {img.data.dtype}")
    print(f"Valor mínimo: {img.data.min()}")
    print(f"Valor máximo: {img.data.max()}")
else:
    print(f"No se encontró la imagen")