import numpy as np
from bioimagenes.core.imagen import Imagen

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

    def convolucion(self):
        pass

    def aplicar(imagen=Imagen):
        pass

    def __str__(self):
        pass