from bioimagenes.core.imagen import Imagen
import numpy as np
from scipy.signal import convolve2d


class Filtro:
    """"
    Clase que permite realizar operaciones sobre la imagen

    Paramentros:
        -tipo (str): indica el tipo de filtro (ej: suavizado, detección de bordes).
        -kernel (np.ndarray): matriz que define el filtro a aplicar en la imagen.
        -tamaño (str): dimensión del kernel (ej: 3x3, 5x5).
    
    """

    def __init__(self, tipo:str, kernel:np.ndarray, tamaño:str):
       
        self.tipo = tipo
        self.kernel = kernel
        self.tamaño = tamaño
    
    def __str__(self):
        """
        Retorna una representación en string del filtro.
    
        Retorna:
            - El nombre del filtro
            - El tamaño del kernel
        """
        texto = f"""
        Información del Filtro
        Nombre: {self.tipo}
        Tamaño: {self.tamaño}
        """
        return texto
    

    def convolucion(self, objeto_imagen: object):
        """
        Método que realiza la operación de convolución para imágenes 2D en escala de grises.

        NOTA: Este método está optimizado específicamente para imágenes 2D (escala de grises).
        Si necesita procesar imágenes en color, considere adaptarlo para procesar cada canal por separado.

        Parámetro:
            - objeto_imagen: objeto o instancia de la clase Imagen con datos 2D

        Retorna:
            - Una imagen procesada en formato uint8 (valores entre 0 y 255)
        """
        # Convertimos a float para preservar precisión durante los cálculos
        matriz_original = objeto_imagen.data.astype(float)
        kernel_actual = self.kernel.astype(float)

        # Normalizamos el kernel
        suma_kernel = np.sum(np.abs(kernel_actual))
        if suma_kernel != 0:
            kernel_normalizado = kernel_actual / suma_kernel
        else:
            kernel_normalizado = kernel_actual

        # Aplicamos la convolución 2D con parámetros optimizados para imágenes 2D
        resultado = convolve2d(
            matriz_original,
            kernel_normalizado,
            mode="same",              # Mantiene el tamaño original de la imagen
            boundary="fill",          # Rellena los bordes
            fillvalue=0               # Con ceros
                                )

        # Convertimos de uint16 a uint8 si es necesario
        if objeto_imagen.data.dtype == np.uint16:
            resultado = (resultado / 65535.0) * 255.0
        else:
            resultado = resultado

        # Aseguramos que los valores están en el rango válido [0, 255] y convertimos a uint8
        return np.clip(resultado, 0, 255).astype(np.uint8)

    def aplicar(self, imagen):
        """
        Aplica el filtro de convolución a una imagen.
    
        Parámetro:
            - imagen: objeto de la clase Imagen
    
        Retorna:
            - Un nuevo objeto Imagen con la convolución aplicada
        """
        # Obtenemos la matriz procesada llamando al método convolucion
        matriz = self.convolucion(imagen)
    
        # Creamos un nuevo objeto Imagen con los datos procesados
        imagen_filtrada = Imagen(data=matriz)
    
        # Retornamos la instancia procesada
        return imagen_filtrada