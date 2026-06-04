#from bioimagenes.core.imagen import Imagen
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

    def __init__(self, nombre:str, tamaño:int=3):

       
        self.tipo = nombre.lower()
        self.tamaño = tamaño
        self.kernel = self.obtener_kernel()

    
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
        Tamaño: {self.tamaño}x{self.tamaño}
        """
        return texto
    

    def convolucion(self, objeto_imagen: object):
        """
        Método que realiza la operación de convolución para imágenes 2D en escala de grises.

        NOTA: Este método está diseñado específicamente para imágenes 2D (escala de grises).
        Si necesita procesar imágenes en color, considere adaptarlo para procesar cada canal por separado.

        Parámetro:
            - objeto_imagen: objeto o instancia de la clase Imagen con datos 2D

        Retorna:
            - Un array de numpy de la imagen procesada en formato uint8 (valores entre 0 y 255)
        """
        # Convertimos a float para preservar precisión durante los cálculos
        matriz_original = objeto_imagen.data.astype(np.float32)
        kernel = self.kernel.astype(np.float32)

        # Normalizamos el kernel
        suma_kernel = np.sum(np.abs(kernel))
        if suma_kernel != 0:
            kernel_normalizado = kernel / suma_kernel
        else:
            kernel_normalizado = kernel

        # Aplicamos la convolución 2D con parámetros optimizados para imágenes 2D
        array_filtrado = convolve2d(
            matriz_original,
            kernel_normalizado,
            mode="same",              # Mantiene el tamaño original de la imagen
            boundary="fill",          # Rellena los bordes
            fillvalue=0               # Con ceros
                                )
        # Tratamiento especial para gradientes (como Sobel) para recuperar bordes bidireccionales
        if "sobel" in self.tipo:
            array_filtrado = np.abs(array_filtrado)

        # Convertimos cualquier profundidad de bits (uint16, uint32, uint64) a uint8
        if objeto_imagen.data.dtype != np.uint8:
            # np.iinfo nos da las propiedades del tipo de dato (ej: uint16 -> max = 65535)
            valor_maximo_original = np.iinfo(objeto_imagen.data.dtype).max
            
            # Normalizamos dinámicamente usando ese máximo y escalamos a 255.0
            array_filtrado = (array_filtrado / float(valor_maximo_original)) * 255.0

        # Aseguramos que los valores están en el rango (0, 255) y convertimos a uint8
        array_convolucionado = np.clip(array_filtrado, 0, 255).astype(np.uint8)
        return array_convolucionado

    def aplicar(self, imagen:object):
        """
        Aplica el filtro de convolución a una imagen.
    
        Parámetro:
            - imagen: objeto de la clase Imagen
    
        Retorna:
            - la matriz filtrada
        """
        # Retornamos la matriz de numpy filtrada
        matriz_filtrada = self.convolucion(imagen)
        return matriz_filtrada
    

    def obtener_kernel(self):
        """
        Catalogo de kernels precargados.

        Retorna:
            np.ndarray: La matriz del kernel correspondiente.

        Raises:
            ValueError: Si el nombre del filtro no existe en el diccionario.
        """
        # Guardamos todos los kernels matemáticos en un diccionario 
        catalogo_kernels = {
            # Filtro de Suavizado Promedio (Se calcula dinámicamente según el tamaño)
            "suavizado": np.ones((self.tamaño, self.tamaño), dtype=np.float32)
            / (self.tamaño * self.tamaño),
            # Filtro Sobel Horizontal (Detecta bordes superiores/inferiores)
            "sobelhorizontal": np.array(
                [[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32
            ),
            "topsobel": np.array(
                [[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32
            ),
            # Filtro Sobel Vertical (Detecta bordes laterales)
            "sobelvertical": np.array(
                [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32
            ),
            # Filtro Sobel Izquierdo
            "leftsobel": np.array(
                [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32
            ),
            # Filtro Sobel Derecho
            "rightsobel": np.array(
                [[1, 0, -1], [2, 0, -2], [1, 0, -1]], dtype=np.float32
            ),
            # Filtro de Realce de Detalles (Sharpening)
            "sharpen": np.array(
                [[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32
            ),
            # Filtro Laplaciano
            "laplaciano": np.array(
                [[0, -1, 0], [-1, 4, -1],[0, -1, 0]], dtype=np.float32
            )
        }

        # Obtenemos el kernel usando el método .get() del diccionario
        kernel_encontrado = catalogo_kernels.get(self.tipo)

        # Si el resultado es None, significa que el usuario escribió un filtro que no existe
        if kernel_encontrado is None:
            raise ValueError(
                f"Error: El filtro '{self.tipo}' no existe. "
                f"Los filtros disponibles son: {list(catalogo_kernels.keys())}"
            )
        return kernel_encontrado
        