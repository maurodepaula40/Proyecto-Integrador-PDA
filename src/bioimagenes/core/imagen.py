import numpy as np
import matplotlib.pyplot as plt
from src.bioimagenes.core.info import Info

class Imagen:
    """
    Clase base para el manejo y procesamiento de imágenes digitales.

    Representa una imagen como una matriz de datos y proporciona 
    herramientas para su manipulación, visualización y análisis.
    Permite aplicar operaciones como filtrado, recorte, conversión
    de escala de grises y ajustes de contraste o brillo.
    
    Además, integra metadatos mediante la clase Info y mantiene 
    un registro de cambios a través de la clase Historial 
    """
    def __init__(self, data: np.ndarray, info: Info = None):
        """ 
        Inicializa una instancia de la clase Imagen.
        Parámetros
        ---------- 
        data : np.ndarray Matriz que contiene los valores de los píxeles de la imagen.
        Puede ser 2D (escala de grises) o 3D (RGB).

        info : Info Objeto que contiene los metadatos asociados a la imagen.
        Si no se proporciona, se genera uno por defecto.

        Raises
         ------
        ValueError
            Si "data" es None o tiene dimensiones inválidas.
        TypeError
            Si "data" no es un np.ndarray.
        """ 
         #Comprobar de que self.data sea valido
        if data is None:
            raise ValueError ("La imagen no tiene datos (data es None)")
    
        if not isinstance(data, np.ndarray):
            raise TypeError (f"data debe ser np.ndarray, no {type(data)}")
        
        #verificar la dimension de la imagen
        if data.ndim not in (2, 3):
            raise ValueError(f"data debe tener 2 o 3 dimensiones, no {data.ndim}")
        
        #verificar que si la imagen es 3D tenga los 3 canales
        if data.ndim == 3 and data.shape[2] != 3:
            raise ValueError("La imagen RGB debe tener 3 canales")
        
        self.data = data
        self.info = info
        if self.info is None:
            self.info = Info()

    def visualizar(self):
        """
        Visualiza la imagen utilizando matplotlib
        """
        
        #Visualizacion de la imagen usando matplotlib
        fig, ax = plt.subplots(figsize=(10, 8)) #plt.subplots() crea la ventana y un conjunto de ejes (area donde va la imagen)
                                                    #figsize - define el tamaño de la ventana
                                                    #fig - representa toda la ventanta
                                                    #ax - representa el area donde va la imagen

        img = self.data
        #Ajuste para imágenes float, los recorta para que esten entre 0 y 1
        if img.dtype.kind == "f":
            img = np.clip(img, 0.0, 1.0)

        if img.ndim == 2:
            im = ax.imshow(img, cmap="gray", interpolation="none")
            plt.colorbar(im, ax=ax)
            ax.set_title("Escala de grises")
        else:
            ax.imshow(img, interpolation="none")
            ax.set_title("RGB")

        plt.tight_layout()
        plt.show()

