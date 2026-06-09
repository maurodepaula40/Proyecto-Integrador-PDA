import numpy as np
import matplotlib.pyplot as plt
from bioimagenes.core.imagen import Imagen
from bioimagenes.core.info import Info
from bioimagenes.filtros.filtro import Filtro

class ImagenRadiografica(Imagen):
    """
    Clase heredada de Imagen especializada en radiografías digitales.

    Trabaja con imágenes 2D en escala de grises y proporciona herramientas
    para su análisis y procesamiento médico: ajuste de contraste, inversión,
    ecualización, detección de bordes, selección de regiones de interés
    y visualización de clusters de intensidad.

    Atributos
        ---------
        -tipo_estudio : str
            Tipo de estudio radiográfico (ej: "tórax", "abdomen", "columna").
            Se almacena en self.info["tipo_estudio"].
        -brillo : int
            Valor de brillo para ajustar la visualización (0-255).
            Se almacena en self.info["brillo"].
        -region_interes : tuple o None
            Coordenadas de la región de interés: (x_min, y_min, x_max, y_max).
            None si no se definió ninguna región.
    """

    def __init__(self, data: np.ndarray, tipo_estudio: str = "", brillo: int = 0, info: Info = None):

        # Validamos que sea un array 2D antes de llamar a Imagen
        if isinstance(data, np.ndarray) and data.ndim != 2:
            raise ValueError("ImagenRadiografia requiere un array 2D (escala de grises).")

        # Si la imagen viene en float, convertimos ANTES de llamar al padre
        if isinstance(data, np.ndarray) and np.issubdtype(data.dtype, np.floating):
            if data.max() <= 1.0: # Si el valor máximo es menor o igual a 1,
                #asumimos que la imagen está normalizada entre 0 y 1.
                data = (data * 255).astype(np.uint8) # Convertimos los valores al rango típico de imágenes
                                                     # de 8 bits (0-255)

        super().__init__(data, info) # Llamamos al constructor de la clase Imagen para inicializar data e info



        # Guardamos el tipo de estudio dentro de los metadatos
        self.info.datos["tipo_estudio"] = tipo_estudio 
        self.info.datos["brillo"] = int(brillo)
        
        self._region_interes = None # Inicialmente no hay ninguna región de interés definida.

    
    #Propiedades para acceder a atributos de Info
    @property
    def tipo_estudio(self):
        """Retorna el tipo de estudio radiográfico almacenado en Info."""
        return self.info["tipo_estudio"]

    @property
    def brillo(self):
        """Retorna el valor de brillo almacenado en Info."""
        return self.info["brillo"]
    
    @property
    def region_interes(self):
        """Retorna la región de interés actual o None si no fue definida."""
        return self.region_interes

    #Sobreescribimos el método heredado de Imagen para poder ajustar la visualización segun el brillo definido
    #def visualizar(self):
    #    """
    #    Visualiza la radiografía aplicando el brillo definido en Info.

#        El brillo se suma a cada píxel antes de mostrar la imagen.
#        Valores positivos aclaran la imagen, negativos la oscurecen.
#        Hereda la estructura de visualizar() de Imagen y agrega el ajuste de brillo.
#        """
#        #Visualizacion de la imagen usando matplotlib (igual que lo hace Imagen)
#        fig, ax = plt.subplots(figsize=(8, 8)) #plt.subplots() crea la ventana y un conjunto de ejes (area donde va la imagen)
                                                    #figsize - define el tamaño de la ventana
                                                    #fig - representa toda la ventanta
                                                    #ax - representa el area donde va la imagen

        # Aplicamos el brillo: sumamos el valor a cada píxel y acotamos a 0-255
        # Convertimos a int32 para evitar errores al sumar el brillo sobre una imagen uint8.
        # Esto es porque si por ejemplo un pixel vale 255 y le queremos sumar un brillo de 20 eso sería 275 y se iria del rango de uint8
#        img_con_brillo = np.clip(self.data.astype(np.int32) + self.brillo, 0, 255).astype(np.uint8) # Luego sumamos el valor de brillo a todos los píxeles.
                                                                                                    # np.clip limita los valores para que permanezcan dentro del rango válido
                                                                                                    # de una imagen de 8 bits (0 a 255).
                                                                                                    # Finalmente volvemos a convertir la imagen a uint8 para visualizarla.

        # Mostramos la imagen utilizando escala de grises.
#        ax.imshow(img_con_brillo, cmap="gray", interpolation="none") # Interpolation="none" evita que matplotlib suavice los píxeles.
#        ax.set_title(f"Radiografía — {self.tipo_estudio if self.tipo_estudio else 'sin tipo'}") # Mostramos en el título el tipo de estudio.
                                                                                                # Si no se definió ninguno, se muestra "sin tipo".
#       ax.axis("off") # ocultamos los ejes
#        plt.tight_layout()
#        plt.show() # Mostramos


    def mejorar_contraste(self, factor: float = 1.5):
        """
         Ajusta la diferencia entre intensidades para resaltar estructuras.
        Devuelve una nueva instancia de ImagenRadiografia con el contraste mejorado.
         Un factor mayor a 1 hace que las zonas claras sean más claras y las oscuras más oscuras.

        Parámetros
        ----------
        factor : float
            Multiplicador de contraste. > 1 aumenta el contraste, < 1 lo reduce.
            Por defecto 1.5.
        """

        # Convierto la imagen a float para poder hacer operaciones matemáticas

        #Tomamos el gris medio (128) como referencia.
        #Primero restamos 128 para centrar los valores alrededor de 0, luego multiplicamos por el factor de contraste y finalmente
        #volvemos a sumar 128 para regresar al rango normal.
        matriz_contrastada = (self.data - 128.0) * factor + 128.0

        self.data = Imagen.normalizar(matriz_contrastada)

        self.titulo_actual = f"Imagen RX con mejora de contraste con factor: {factor} "

        # Registramos en el historial
        self.historial.modificar_historial(f"Contraste mejorado: factor {factor}")
    
    def invertir_intensidades(self):
        """
        Invierte las intensidades de la radiografía.

        Cada píxel se transforma según:
            nuevo_valor = 255 - valor_original

        Esto produce un negativo de la imagen:
        - las zonas claras pasan a oscuras
        - las zonas oscuras pasan a claras
        """
        # Invertimos los niveles de gris
        resultado = 255 - self.data

        # Registramos la transformación en el historial
        self.historial.modificar_historial("Intensidades invertidas")

        self.titulo = f"Imagen RX con las intensidades invertidas"

        # Retornamos una nueva imagen radiográfica
        return resultado

    def ecualizar_intensidades(self):
        """
        Redistribuye los píxeles para que usen todo el rango 0-255 de forma más uniforme, logrando más contraste.
        Ecualiza las intensidades de la radiografía mediante ecualización de histograma.
        """

        # Calculamos el histograma (256 niveles de gris)
        histograma, _ = np.histogram(self.data.flatten(),bins=256,range=(0, 256)) #devuelve histograma (grafico de cuantas veces aparece una intensidad en la imagen)
        
        #np.histogram devuelve histograma, bordes. Como no nos interesan los bordes→ ponemos _ 
        # porque no necesitamos ese valor

        #flatten pone las columnas continuas para tener todos los valores en la misma "linea" o lista
        #  para que sea mas facil contar apariciones de intensidades
        
        ecual = np.zeros_like(histograma) #creamos array del mismo tamaño que el histograma

        acumulado = 0 # variable para sumar las frecuencias

        for i in range(len(histograma)): #recorremos cada posición del histograma
            acumulado += histograma[i] #sumamos la aparicion actual a la variable acumulada
            
            ecual[i] = acumulado #guardamos el valor de frecuencias en la misma posicion del array ecual

        # Tomamos el valor mínimo del ecual.
        # Corresponde a la menor cantidad acumulada de píxeles.
        ecual_min = ecual.min()

        # Tomamos el valor máximo del array ecual.
        # Coincide con la cantidad total de píxeles de la imagen.
        ecual_max = ecual.max()

        # Aplicamos la fórmula de normalización para redistribuir los valores del array entre 0 y 255.
        ecual_normalizada = Imagen.normalizar(ecual)
        

        resultado = ecual_normalizada[self.data] #usa cada valor de self.data como un indice para ecual_normalizada
                                                 #el resultado es una matriz con los valores escualizados para cada uno de los indices

        # Registramos la transformación realizada en el historial asociado a la imagen.
        self.historial.modificar_historial("Intensidades ecualizadas")

        # Retornamos una nueva instancia de ImagenRadiografia con la imagen ecualizada y conservando los metadatos originales.
        return resultado

    def detectar_bordes(self):
        """
        Detecta los bordes anatómicos de la radiografía.
        """
        filtro_h = Filtro(nombre="sobelhorizontalx7")
        filtro_v = Filtro(nombre="sobelverticalx7")

        try:
            # 2. Obtenemos los gradientes individuales
            g_x = filtro_h.aplicar(self)
            g_y = filtro_v.aplicar(self)

            # Combinamos ambos gradientes
            img_filtrada = np.sqrt(g_x**2 + g_y**2)

            # Guardamos el resultado final en 'self.data'
            self.data = Imagen.normalizar(img_filtrada)

            self.titulo_actual = f"Imagen RX con filtro de deteccion de bordes"
            
            # Registramos el cambio en el historial.
            self.historial.modificar_historial("Se realizó Detección de Bordes con operador Sobel")

        except Exception as e:
            raise RuntimeError(f"Error al ejecutar la detección de bordes por Sobel: {e}") 
        

    def seleccionar_region_interes(self, y_min: int, y_max: int, x_min: int, x_max: int):
        """
        Recorta una región de interés específica dentro de la imagen radiográfica.
        Modifica la imagen actual (in-place) reduciendo su tamaño a la submatriz seleccionada.

        Parámetros:
            - y_min (int): Coordenada vertical superior (inicio de fila).
            - y_max (int): Coordenada vertical inferior (fin de fila).
            - x_min (int): Coordenada horizontal izquierda (inicio de columna).
            - x_max (int): Coordenada horizontal derecha (fin de columna).

        Raises:
            ValueError: Si las coordenadas son negativas, inconsistentes (mínimo mayor al máximo) 
                        o si desbordan las dimensiones de la imagen original.
        """
        #Obtenemos las dimensiones reales (alto = filas, ancho = columnas)
        alto, ancho = self.data.shape[:2]

        # Validamos que las coordenadas no sean negativas
        if y_min < 0 or y_max < 0 or x_min < 0 or x_max < 0:
            raise ValueError("Error de rango: Las coordenadas no pueden ser valores negativos.")

        # Validamos que los límites mínimos no superen o igualen a los límites máximos
        if y_min >= y_max or x_min >= x_max:
            raise ValueError(f"Error de rango: Los valores mínimos [Y: {y_min}, X: {x_min}] "
                             f"deben ser menores que los máximos [Y: {y_max}, X: {x_max}].")
        
        # Validamos que ninguna coordenada desborde el tamaño real de la matriz
        if y_max > alto or x_max > ancho:
            raise ValueError(f"Error de rango: Las coordenadas exceden los límites de la radiografía "
                             f"(Tamaño actual de la matriz: {ancho}x{alto}).")
        
        # Modificamos in place, extraemos la submatriz y pisamos directamente self.data
        # En NumPy el orden de indexación siempre es [filas(Y), columnas(X)]
        self.data = self.data[y_min:y_max, x_min:x_max]

        # Asignamos el nuevo título detallando el área del recorte al objeto actual
        self.titulo_actual = f"Recorte [X: {x_min}-{x_max}, Y: {y_min}-{y_max}]"

        # Registramos la acción de recorte en el historial de este mismo objeto
        self.historial.modificar_historial(f"Se recortó la imagen a la región de interés.")

    def visualizar_cluster(self):
        pass