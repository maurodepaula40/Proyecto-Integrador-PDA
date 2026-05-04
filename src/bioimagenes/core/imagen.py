import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image as PILImage
import nibabel as nb
from bioimagenes.core.info import Info
from bioimagenes.core.historial import Historial
from bioimagenes.filtros import filtro as fl

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
        
        self.original = data.copy()
        self.data = self.original.copy()

        if info is None:
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

    def __len__(self):
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
        Permite acceder a los píxeles usando corchetes: objeto_imagen[y, x]
        """
        errores = []

        # Caso para cuando se pasan varios índices (Tupla: [y, x])
        if isinstance(index, tuple):
            for i in index:
                if not isinstance(i, (int, slice)):
                    errores.append(str(i))
        
        # Caso cuando se pasa un solo índice (ej: img["a"])
        elif not isinstance(index, (int, slice)):
            errores.append(str(index))

        #MANEJO DE MENSAJES DE ERROR DE TIPO
        if len(errores) > 0:
            #Formateamos todos los errores detectados con comillas
            errores_con_comillas = []
            for e in errores:
                errores_con_comillas.append(f"'{e}'")
            
            #Decidimos si el mensaje es en singular o plural
            if len(errores) == 1:
                print(f"Error de TIPO: El valor {errores_con_comillas[0]} en {index} debe ser número entero.")
            else:
                valores_mal = " y ".join(errores_con_comillas)
                print(f"Error de TIPO: Los valores {valores_mal} en {index} deben ser números enteros.")
            
            return None

        try:
            return self.data[index]
        
        except IndexError:
            dimensiones = self.data.shape
            print(f"Error de RANGO: Las coordenadas {index} exceden el tamaño {dimensiones}.")
            return None
            
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            return None

    def aplicar_filtro(self, filtro=None):
        """
        Aplica un objeto Filtro sobre la imagen
        Parametro:
        filtro=Filtro - que es un objteto, se le pasa una instancia de la clase Filtro
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
            print(f"DEBUG: El tipo de lo que se recibio es: {type(filtro)}")
            print(f"DEBUG: El error real es: {e}")