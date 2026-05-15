import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image as PILImage
import nibabel as nb
from bioimagenes.core.info import Info
from bioimagenes.core.historial import Historial

class Imagen:
    """
    Clase base para el manejo y procesamiento de imágenes digitales.
sa
    Representa una imagen como una matriz de datos y proporciona 
    herramientas para su manipulación, visualización y análisis.
    Permite aplicar operaciones como filtrado, recorte, conversión
    de escala de grises y ajustes de contraste o brillo.
    
    Además, integra metadatos mediante la clase Info y mantiene 
    un registro de cambios a través de la clase Historial 

    Parámetros:
        - data: recibe un np.ndarray, contiene los valores de los píxeles de la imagen.
                Puede ser 2D (escala de grises) o 3D (RGB).
        - info : recibe un objeto llamado Info que contiene los metadatos asociados a la imagen.
                 Si no se proporciona, se genera uno por defecto.
    Errores:
        - ValueError si data no tiene datos, si data no es de 2 o 3 dimensiones y si es una clase RGB que no tiene 3 canales
        - TypeError si data no es un np.ndarray
    """
    def __init__(self, data: np.ndarray, info: Info = None):
       
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
        
        self.original = data.copy()
        self.data = self.original.copy()

        if info is None:
            self.__info = Info()
            
    # ----  Metodo de clase para leer archivos ----
    @classmethod
    def cargar(cls, ruta):
        """ 
        Metodo de clase que detecta el formato de la imagen. Soporta formatos png, jpg, jpeg, nii, dicom y gz

        Parametro:
            - ruta: recibe la direccion de la imagen como string
        Retorna:
            Una instancia de la clase Imagen
        Errores:
            Retorna ValueError si el formato de la imagen no es soportado
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
        Permite mostrar una imagen almacenada utilizando la librería Matplotlib

        Retorna:
            La apertura de una ventana de Matplotlib con la imagen
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

    def __len__(self):
        """Permite acceder a la cantidad total de pixeles de la imagen usando la funcion len()"""
        # Tomamos solo las dos primeras dimensiones del array:
        # shape puede ser (filas, columnas) o (filas, columnas, canales)
        filas, columnas = self.data.shape[:2]

        # Calculamos el total de píxeles multiplicando filas por columnas
        total_pixeles = filas * columnas

        # Retornamos ese valor cuando se usa len(imagen)
        return total_pixeles
    
    def __str__(self):
        """
        Método que retorna una representación en texto de la imagen.
        Se ejecuta cuando haces print(imagen)
        """
        
        # Obtenemos las dimensiones de la imagen
        # shape[:2] toma solo las dos primeras dimensiones (filas, columnas)
        filas, columnas = self.data.shape[:2]
        
        # Verificamos si la imagen tiene 3 dimensiones (RGB) o 2 (escala de grises)
        if self.data.ndim == 3:
            # Si tiene 3 dimensiones, obtenemos el número de canales
            canales = self.data.shape[2]
            tipo_imagen = f"RGB ({canales} canales)"
        else:
            # Si tiene 2 dimensiones, es escala de grises
            tipo_imagen = "Escala de grises"
        
        # Obtenemos el tipo de dato de los píxeles (uint8, float32, etc)
        tipo_dato = str(self.data.dtype)
        
        # Obtenemos el valor mínimo y máximo de los píxeles
        valor_min = self.data.min()
        valor_max = self.data.max()
        
        # Creamos el texto que se mostrará
        texto = f"""
        INFORMACIÓN DE LA IMAGEN
        Dimensiones: {filas} x {columnas} píxeles
        Tipo de imagen: {tipo_imagen}
        Tipo de dato: {tipo_dato}
        Valor mínimo: {valor_min}
        Valor máximo: {valor_max}
        Total de píxeles: {len(self)}
        """
        # Retornamos el texto
        return texto

    def __getitem__(self, index):
        """
        Permite acceder a los píxeles de la imagen usando corchetes.
        Ejemplo: objeto_imagen[y, x]

        Retorna:
            - El valor del píxel en la posición indicada.
            - Un bloque de píxeles si se usan slices.
        """
         #Validacion de rango, que los índices estén dentro de los límites de la matriz
        filas, columnas = self.data.shape[:2]  #soporta imágenes 2D o 3D

        y, x = index  #asumimos que index es una tupla válida

        #Si son enteros, verificamos que estén dentro del rango
        if isinstance(y, int) and not (0 <= y < filas):
            raise IndexError(f"Índice de fila fuera de rango: {y}")
        if isinstance(x, int) and not (0 <= x < columnas):
            raise IndexError(f"Índice de columna fuera de rango: {x}")

        # Si son slices, NumPy ya maneja los límites, no hace falta validarlos
        return self.data[index]

    def aplicar_filtro(self, filtro = None):
        """
        Aplica un objeto de tipo Filtro sobre la imagen
        Parametro:

            - filtro: Filtro es un objeto
        Retorna:

        """
        try:
            #Invocamos el método aplicar de la clase Filtro pasándole la instancia completa
            #de la imagen (self) para que el filtro pueda acceder a sus atributos.
            imagen_procesada = filtro.aplicar(self)
            
            #Verificamos si el objeto devuelto es válido y actualizamos los datos internos con la nueva versión procesada.
            if imagen_procesada is not None:
                self.data = imagen_procesada.data
                print("El filtro se aplicó exitosamente sobre el objeto Imagen.")
            
        #Manejamos errores cuando el objeto filtro no cumple con la estructura esperada.
        except AttributeError:
            print("Error: El objeto filtro no es válido.")
            
        #Capturan cualquier error surgida durante el procesamiento interno del filtro.
        except Exception as e:
            print(f"El tipo de lo que se recibio es: {type(filtro)}")
            print(f"El error real es: {e}")