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
        """
        Ejecuta la operacion de convolucion sobre los datos de una imagen
        """
        #Extraemos la matriz de datos y la convertimos a float para hacer los calculos mas precisos
        matriz_original =objeto_imagen.data.astype(float)

        #Accedemos al kernel almacenado en la instancia self.kernel
        kernel_actual = self.kernel

        #Calculamos los suma de los coeficientes del kernel para la normalizacion
        # Si la suma es 0 (como en filtros de detección de bordes), establecemos C=1 para evitar divisiones por cero
        suma_kernel = np.sum(self.kernel_actual)
        if suma_kernel != 0:
            c_normalizado = suma_kernel
        else:
            c_normalizado = 1
        
        #Preparamos una matriz vacia con ceros con las mismas dimensiones de la imagen para almacenar el resultado
        matriz_filtrada = np.zeros_like(matriz_original)

        #Procesamos la imagen segun su dimensionalidad (Escala de grise o RGB)
        if len(matriz_original.shape) == 3:
            #Iteramos sobre los 3 canalas RGB
            for i in range(3):
                #Realizamos la convolucion en el canal actual
                canal_procesado = scipy.ndimage.convolve(matriz_original[:,:,i], kernel_actual, mode="constant")
                #Aplicamos la normalizacion y aseguramos que los valores esten en 0 y 255
                matriz_filtrada[:,:,i] = np.clip(canal_procesado/c_normalizado,0,255)
        else:
            #Procesamos imagenes en blanco y negro (un solo canal)
            canal_procesado = scipy.ndimage.convolve(matriz_original, kernel_actual, mode="constant")
            matriz_filtrada =np.clip(canal_procesado/c_normalizado,0,255)

        return matriz_filtrada.astype(np.uint8)

    def aplicar(self, imagen):
        from bioimagenes.core.imagen import Imagen

        if not isinstance(imagen, Imagen):
            print(f"Error: No es un objeto Imagen")
            return None

    def __str__(self):
        pass