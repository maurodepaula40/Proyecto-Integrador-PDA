import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image as PILImage
import nibabel as nb
from .info import Info

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
        """ 
         #Comprobar de que data sea valido
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
        
    # ----  Metodo de clase para leer archivos ----
    @classmethod
    def leer_archivos(cls, ruta):
        """ 
        Metodo de clase que detecta el formato de la imagen y retorna una instancia de la clase Imagen
        """
        extension = os.path.splitext(ruta)[1].lower()   #accede a la ruta del archivo y obtiene en string la extension de la imagen ".png", ".nii"
                                                        # os.path.splitext es una función de Python en el módulo os.path que se 
                                                        # utiliza para dividir una ruta de acceso en un par (raíz, extensión) . 

        #logica para imagenes tomograficas"
        if extension in (".nii", ".gz",".dcm"):         #verificamos si extension existe dentro de la tupla
            img_nifti = nb.load(ruta)                   #cargamos la imagen con nibabel
            datos = img_nifti.get_fdata()               #cargamos los datos de la imagen como un array de numpy con get_fdata()
            return cls(data = datos, info=None)         #Retorna una instancia de la clase Imagen
                
        #Lógica para imagenes en 2D"
        elif extension in (".png",".jpg",".jpeg"):      #verificamos si extension existe dentro de la tupla
            with PILImage.open(ruta) as img_pil:        #cargamos la imagen con pillow
                if img_pil.mode in ("RGB","P"):         # verificamos si la imagen ya es color (RGB) o usa una paleta (formato comprimido) (P)
                    img_pil = img_pil.convert("RGB")    #la convertimos a RGB para estandarizar los canales de color
                elif img_pil.mode in ("1","I","F"):     # verificamos si imagen es blanco y negro puro (1) o tiene formatos de datos científicos (I) o (F)
                    img_pil = img_pil.convert("L")      #La convertimos a escala de grises de 8 bits (0-255)
                datos = np.asarray(img_pil)             # Convertimos la imagen ya normalizada en una matriz de números (NumPy)
                return  cls(data = datos, info=None)    #retornamos una instancia de la clase Imagen
            
        else:
            raise ValueError(f"Formato {extension} no soportado")
    
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
        if img.dtype.kind == "f":
            img = np.clip(img, 0.0, 1.0)

        if img.ndim == 2:
            im = ax.imshow(img, cmap="gray", interpolation="none")
            ax.set_title("Escala de grises")
        else:
            ax.imshow(img, interpolation="none")
            ax.set_title("RGB")

        plt.tight_layout()
        plt.show()

    def bn(self):
        """
        Metodo que convierte una imagen RGB a blanco y negro.
        """
        if len(self.data.shape) == 3: # verificamos la dimension de la imagen
            #Promediamos los canales para pasar a gris
            self.data = np.mean(self.data, axis=2).astype(np.uint8) 

