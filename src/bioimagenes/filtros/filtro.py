import numpy as np
import scipy.ndimage

class Filtro:
    """"
    Clase que permite realizar operaciones sobre la imagen
    """

    def __init__(self, tipo:str, kernel:np.ndarray, tamaño:str):
        """
        Inincia una instancia de la clase Filtro
        Paramentro:
        tipo (str): indica el tipo de filtro (ej: suavizado, detección de bordes).
        kernel (np.ndarray): matriz que define el filtro a aplicar en la imagen.
        tamaño (str): dimensión del kernel (ej: 3x3, 5x5).
        """
        self.tipo = tipo
        self.kernel = kernel
        self.tamaño = tamaño

    def convolucion(self, objeto_imagen):
        #Convertimos a float para no perder info
        matriz_original = objeto_imagen.data.astype(float)
        kernel_actual = self.kernel.astype(float)

        #Normalizamos el kernel
        suma_kernel = np.sum(kernel_actual)
        if suma_kernel != 0:
            c_normalizado = float(suma_kernel)
        else:
            c_normalizado = 1.0   

        #Convolución (Scipy detecta si es 2D o 3D solo)
        canal_procesado = scipy.ndimage.convolve(matriz_original, kernel_actual, mode="constant")
        resultado = canal_procesado / c_normalizado

        # Si la imagen es uint16, debemos llevarla al rango 0-255 antes de convertir a uint8
        if objeto_imagen.data.dtype == np.uint16:
             resultado = (resultado / 65535.0) * 255.0

        return np.clip(resultado, 0, 255).astype(np.uint8)


    def aplicar(self, imagen):
        from bioimagenes.core.imagen import Imagen

        #Obtenemos la matriz procesada llamando al metodo convolucion
        matriz_resultado = self.convolucion(imagen)

        #Creamos un OBJETO nuevo
        #usamos el constructor de Imagen para que sea un objeto completo
        imagen_filtrada = Imagen(data=matriz_resultado)
        
        #Retornamos una instancia de la clase Imagen
        return imagen_filtrada

    def __str__(self):
        pass