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
    
    Representa una imagen como una matriz de datos y proporciona 
    herramientas para su manipulación, visualización y análisis.
    Permite aplicar operaciones como filtrado, recorte, conversión
    de escala de grises y ajustes de contraste o brillo.
    
    Además, integra metadatos mediante la clase Info y mantiene 
    un registro de cambios a través de la clase Historial 
    """
    def __init__(self, data: np.ndarray, info: Info = None):
        """
        Parámetros:
            - data: recibe un np.ndarray, contiene los valores de los píxeles de la imagen.
                Puede ser 2D (escala de grises) o 3D (RGB).
            - info: recibe un objeto Info que contiene los metadatos asociados a la imagen.
                 Si no se proporciona, se genera uno por defecto.
        Errores:
            - ValueError si data no tiene datos, si data no es de 2 o 3 dimensiones y si es una imagen RGB que no tiene 3 canales
            - TypeError si data no es un np.ndarray
        """
       
        #Comprobamos de que data sea valido
        if data is None:
            raise ValueError ("La imagen no tiene datos (data es None)")
    
        if not isinstance(data, np.ndarray):
            raise TypeError (f"data debe ser np.ndarray, no {type(data)}")
        
        # Verificamos la dimension de la imagen
        if data.ndim not in (2, 3):
            raise ValueError(f"data debe tener 2 o 3 dimensiones, no {data.ndim}")
        
        #verificar que si la imagen es RGB tenga los 3 canales
        if data.ndim == 3:
            if data.shape[2] == 3:
                # Si es RGB común, nos quedamos con un canal
                array = data[:, :, 0]
            else:
                #Si tiene mas de 3 canales es una imagen tomografica, el ultimo valor corresponde a los cortes, deja
                array = data
        else:
            array = data
        
        self.original = array.copy()
        self.__data = self.original

        # Verificamos el parametro info
        if info is not None:
            self.__info = info
        else:
            self.__info = Info()
        
        # Instanciamos el historial de manera encapsulada privada
        self.__historial = Historial()
        
        
        # Asignamos a la variable historial el objeto Historial()
    @property
    def historial(self):
        """
        Proporcionar acceso controlado al objeto de historial de la imagen.
        Retorna:
            Historial: Instancia de la clase Historial que gestiona la bitácora de cambios.
        """
        return self.__historial
    
    @property
    def data(self):
        """
        Garantiza el acceso a la matriz de datos de la imagen.
        Retorna:
            - np.ndarray: El contenido de la variable privada __data que representa los píxeles.
        """
        return self.__data
    
    @data.setter
    def data(self, nuevo_array: np.ndarray):
        """
        Args:
            nueva_matriz (np.ndarray)

        Raises:
            TypeError: Si el parámetro ingresado no es un arrau de NumPy.
        """

        # Verificamos que el parametro ingresado sea un array de numpy
        if not isinstance(nuevo_array, np.ndarray):
            raise TypeError(
                f"Error de tipo: Se espera una array de Numpy (np.ndarray), "
                f"se recibió un dato del tipo '{type(nuevo_array)}'.")
        # Asignamos la matriz o array de numpy a la variable privada encapsulada
        self.__data = nuevo_array
    
    @property
    def info(self):
        """
        Proporciona acceso a los metadatos asociados a la imagen.
        Retorna:
            - Info: Objeto de la clase Info que contiene la información técnica de la imagen.
        """
        return self.__info
    
    @info.setter
    def info(self, nueva_info):
        """
        Parámetro:
            nueva_info (Info)
        Raises:
            TypeError: Si el parámetro ingresado no es una instancia válida de la clase Info.
        """
        # Verificamos que el parametro ingresado sea una instancia de la clase Info
        if not isinstance(nueva_info, Info):
            raise TypeError(f"Error de tipo: Se espera un objeto de la clase 'Info', "
                f"se recibió un dato del tipo '{type(nueva_info)}'.")

        # Asignamos el objeto nueva_info a la variable privada encapsulada
        self.__info = nueva_info
        
    
    # ----  Metodo de clase para leer archivos ----
    @classmethod
    def cargar(cls, ruta:str):
        """ 
        Metodo de clase que se usa para cargar la imagen. Soporta formatos png, jpg, jpeg, nii, dicom y gz

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

        #logica para imagenes volumétricas"
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
            # Lanzamos un ValueError si el formato no es soportado
            raise ValueError(f"Formato {extension} no soportado")
    
    def visualizar(self, titulo:str, data:np.ndarray=None):
        """
        Permite mostrar una imagen almacenada utilizando la librería Matplotlib
        Para ver imagenes tomograficas, primero se debe obtener un slice o corte y despues visualizar

        Retorna:
            La apertura de una ventana de Matplotlib con la imagen
        """
        if data is None:
            img = self.data
        else:
            img = data
        
        #Visualizamos la imagen usando matplotlib
        fig, ax = plt.subplots(figsize=(10, 8)) #plt.subplots() crea la ventana y un conjunto de ejes (area donde va la imagen)
                                                    #figsize - define el tamaño de la ventana
                                                    #fig - representa toda la ventanta
                                                    #ax - representa el area donde va la imagen

        
        if img.dtype.kind == "f":
            img = np.clip(img, 0.0, 1.0)

        if img.ndim == 2:
            im = ax.imshow(img, cmap="gray", interpolation="none")
        else:
            ax.imshow(img, interpolation="none")

        ax.set_title(titulo)
        plt.tight_layout()
        plt.axis("off")
        plt.show()

    def bn(self):
        """
        Metodo que convierte una imagen RGB a blanco y negro.
        """
        # Verificamos la dimension de la imagen
        if len(self.data.shape) == 3: 
            #Promediamos los canales para pasar a gris
            blanco_negro = np.mean(self.data, axis=2).astype(np.uint8)

            # Guardamos el cambio en el historial 
            mensaje = "Se modificó la imagen a blanco y negro"
            self.historial.modificar_historial(mensaje) 

            # retornamos el array de numpy modificado
            return blanco_negro 
        
        #si la imagen es 2D, se devuelve a si misma
        return self

                       

    def __len__(self):
        """Permite acceder a la cantidad total de píxeles de la imagen usando la función len()."""
        # .size devuelve automáticamente el total de píxeles (filas * columnas * cortes) si tiene 3 dimensiones o (filas * columnas) si es de 2 dimensiones
        return self.data.size
    
    def __str__(self):
        """
        Método que retorna una representación en texto de la imagen.
        Se ejecuta cuando haces print(imagen)
        """
        
        # Obtenemos las dimensiones de la imagen
        filas = self.data.shape[0]
        columnas = self.data.shape[1]
        
        # Verificamos si la imagen tiene 3 dimensiones (RGB) o 2 (escala de grises)
        if self.data.ndim == 3:
            # Si tiene 3 dimensiones, obtenemos el número de canales
            canales = self.data.shape[2]
            # Si el tercer eje tiene 3 canales, asumimos un formato RGB
            if canales == 3:
                tipo_imagen = f"Color / RGB (3 canales)"
            else:
                # Si tiene más, representa cortes
                tipo_imagen = f"Resonancia/Tomografía ({canales} cortes)"
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
         # Validamos el rango, que los índices estén dentro de los límites del array
        filas = self.data.shape[0]
        columnas = self.data.shape[1] 

        # Asumimos que index es una tupla válida
        y, x = index  

        #Si son enteros, verificamos que estén dentro del rango
        if isinstance(y, int) and not (0 <= y < filas):
            raise IndexError(f"Índice de fila fuera de rango: {y}")
        if isinstance(x, int) and not (0 <= x < columnas):
            raise IndexError(f"Índice de columna fuera de rango: {x}")

        # Si son slices, NumPy ya maneja los límites, no hace falta validarlos
        return self.data[index]

    def aplicar_filtro(self, filtro: object = None):
        """
        Aplica un objeto de tipo Filtro sobre la imagen. Registra el evento en la imagen original
        Parametro:
            - filtro: Filtro es un objeto
        Retorna:
            - una nueva instancia de la clase Imagen
        """
        from bioimagenes.filtros.filtro import Filtro

        if filtro is None:
            return print("No se proporcionó ningun filtro")

        try:
            # Invocamos el método aplicar de la clase Filtro pasándole la instancia completa
            #de la imagen (self) para que el filtro pueda acceder a sus atributos.
            imagen_filtrada = filtro.aplicar(self)
            
            # Verificamos si el objeto devuelto es válido y actualizamos los datos internos con la nueva versión filtrada.
            if imagen_filtrada is not None:

                # Modificamos la matriz original y la guardamos en la copia de 'data'
                self.data = imagen_filtrada

                #Registramos el cambio en el historial de la original
                self.historial.modificar_historial(f"Se aplicó filtro: {filtro.tipo.upper()} (Tamaño: {filtro.tamaño}x{filtro.tamaño})")
            
        # Capturamos cualquier error surgido durante el procesamiento interno del filtro.
        except Exception as e:
            raise RuntimeError(f"Error al procesar el filtro en la imagen: {e}")
        
    
    @staticmethod
    def normalizar(matriz: np.ndarray) -> np.ndarray:
        """
        Método que normaliza una matriz al rango estándar 0-255 y la convierte a np.uint8.
        Si la matriz original es un tipo entero superior a uint8 (ej: uint16), normaliza 
        usando el máximo teórico del formato (np.iinfo). De lo contrario, aplica Min-Max.
        """
        # Guardamos el tipo de dato original antes de convertir a float
        tipo_original = matriz.dtype
        
        # Forzamos a float32 para evitar desbordamientos en las operaciones
        matriz_float = matriz.astype(np.float32)
        
        # Si es un tipo entero y es superior a uint8 (ej: int16, uint16, int32)
        if np.issubdtype(tipo_original, np.integer) and tipo_original != np.uint8:
            
            # Obtenemos las propiedades del formato original (ej: para uint16 el max es 65535)
            valor_maximo_original = np.iinfo(matriz_float.data.dtype).max

        
            # Escalamos a 0 y 255
            matriz_normalizada = (matriz_float/float(valor_maximo_original)) * 255.0
            
        else:
            # por defecto escalamos Min-Max para float32, uint8, etc.
            valor_min = np.min(matriz_float)
            valor_max = np.max(matriz_float)
            rango = valor_max - valor_min
            
            if rango != 0:
                matriz_normalizada = ((matriz_float - valor_min) / rango) * 255.0
            else:
                matriz_normalizada = matriz_float
        
        # Usamos .clip por seguridad y convertimos a uint8
        matriz_normalizada = np.clip(matriz_normalizada, 0, 255).astype(np.uint8)

        return matriz_normalizada
    

    def ver_imgOriginal(self, titulo: str = "Imagen Original"):
        """
        Extrae la matriz original (self.original) y la envía
        al método visualizar..
        """
        return self.visualizar(titulo=titulo, data=self.original)
    
            
       