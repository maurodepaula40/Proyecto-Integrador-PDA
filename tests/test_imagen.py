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


def test_len_imagen_valido():
    print("\n--- Test len válido ---")

    try:
        img = Imagen()
        img.data = np.zeros((4, 5))  # 20 píxeles

        resultado = len(img)
        esperado = 20

        if resultado == esperado:
            print("OK: Caso válido 4x5")
        else:
            print(f"ERROR: esperado {esperado}, obtenido {resultado}")

    except Exception as e:
        print(f"ERROR inesperado en caso válido: {e}")
