import os
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import cv2
from bioimagenes.core.imagen import Imagen
from bioimagenes.core.info import Info
from bioimagenes.filtros.filtro import Filtro
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class ImagenRadiografia(Imagen):
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
        return self._region_interes

    def ajustar_brillo(self, brillo: int):
        """
        Ajusta el brillo de la radiografía modificando la imagen actual.

        Primero normaliza la imagen original al rango 0-255 y luego suma el brillo.
        Esto evita que la imagen quede completamente blanca si los datos originales
        están en otro rango, por ejemplo 0-4095 o 0-65535.

        Parámetros
        ----------
        brillo : int
            Valor de brillo a sumar. Puede ser positivo o negativo.
        """

        brillo = int(brillo)

        # Guardamos el brillo en los metadatos
        self.info.datos["brillo"] = brillo

        # Usamos siempre la imagen original para que el brillo no se acumule
        img = self.original.astype(np.float64)

        # Normalizamos la imagen al rango 0-255
        minimo = img.min()
        maximo = img.max()

        if maximo == minimo:
            img_normalizada = np.zeros_like(img)
        else:
            img_normalizada = (img - minimo) * 255 / (maximo - minimo)

        # Aplicamos el brillo
        img_con_brillo = img_normalizada + brillo

        # Limitamos al rango válido 0-255
        img_con_brillo = np.clip(img_con_brillo, 0, 255).astype(np.uint8)

        # Modificamos la imagen actual
        self.data = img_con_brillo

        # Actualizamos el título
        self.titulo_actual = f"Radiografía — brillo {brillo}"

        # Registramos en historial
        self.historial.modificar_historial(f"Brillo ajustado: {brillo}")

        return self


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
        datos = self.data.astype(np.float64)

        #Tomamos el gris medio (128) como referencia.
        #Primero restamos 128 para centrar los valores alrededor de 0, luego multiplicamos por el factor de contraste y finalmente
        #volvemos a sumar 128 para regresar al rango normal.
        rx_contraste = np.clip((datos - 128) * factor + 128, 0, 255).astype(np.uint8)
        
        self.data = rx_contraste

        # Actualizamos el título
        self.titulo_actual = f"RX con contraste ajustado ({factor})"

        # Registramos en el historial
        self.info.historial.modificar_historial(f"Contraste mejorado: factor {factor}")
        
        #Retorna una imagen (instancia de la clase, no la original) con el contraste modificado
        return self
    
    def invertir_intensidades(self):
        """
        Invierte las intensidades de la radiografía.

        Cada píxel se transforma según:
            nuevo_valor = 255 - valor_original

        Esto produce un negativo de la imagen:
        - las zonas claras pasan a oscuras
        - las zonas oscuras pasan a claras

        Retorna
        -------
        self : ImagenRadiografia
            Retorna la misma instancia con las intensidades invertidas.
        """

        # Invertimos los niveles de gris
        resultado = 255 - self.data

        # Modificamos la imagen actual
        self.data = resultado.astype(np.uint8)

        # Actualizamos el título
        self.titulo_actual = "RX con intensidades invertidas"

        # Registramos la transformación en el historial
        self.info.historial.modificar_historial("Intensidades invertidas")

        return self

    def ecualizar_intensidades(self):
        """
        Redistribuye los píxeles para que usen todo el rango 0-255 de forma más uniforme,
        logrando más contraste.

        Ecualiza las intensidades de la radiografía mediante ecualización de histograma.

        Modifica self.data y retorna self.
        """

        # Primero normalizamos la imagen al rango 0-255.
        # Esto evita errores si la radiografía real viene en uint16 o con valores mayores a 255.
        datos = self.data.astype(np.float64)

        minimo = datos.min()
        maximo = datos.max()

        if maximo == minimo:
            datos_normalizados = np.zeros_like(datos, dtype=np.uint8)
        else:
            datos_normalizados = ((datos - minimo) * 255 / (maximo - minimo)).astype(np.uint8)

        # Calculamos el histograma sobre la imagen ya normalizada
        histograma, _ = np.histogram(datos_normalizados.flatten(),bins=256,range=(0, 256))

        ecual = np.zeros_like(histograma, dtype=np.float64)

        acumulado = 0

        for i in range(len(histograma)):
            acumulado += histograma[i]
            ecual[i] = acumulado

        ecual_min = ecual[ecual > 0].min()
        ecual_max = ecual.max()

        if ecual_max == ecual_min:
            resultado = datos_normalizados
        else:
            ecual_normalizada = ((ecual - ecual_min) * 255) / (ecual_max - ecual_min)
            ecual_normalizada = np.clip(ecual_normalizada, 0, 255).astype(np.uint8)

            resultado = ecual_normalizada[datos_normalizados]

        # Guardamos la imagen ecualizada
        self.data = resultado.astype(np.uint8)

        # Actualizamos el título
        self.titulo_actual = "RX con intensidades ecualizadas"

        # Registramos la transformación realizada en el historial
        self.historial.modificar_historial("Intensidades ecualizadas")

        return self

    def detectar_bordes(self):
        """
        Detecta los bordes anatómicos de la radiografía.
        Utilizando un operador sobel de 7x7
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
            self.data = np.clip(img_filtrada, 0, 255).astype(np.uint8)
            
            # Actualizamos el titulo 
            self.titulo_actual = "RX con detección de bordes"

            # Registramos el cambio en el historial.
            self.historial.modificar_historial("Se realizó Detección de Bordes con operador Sobel")

            return self 
        
        except Exception as e:
            raise RuntimeError(f"Error al ejecutar la detección de bordes por Sobel: {e}") 

    def seleccionar_region_interes(self, y_min:int, y_max:int, x_min:int, x_max:int):
        """
        Recorta una región de interés específica dentro de la imagen radiográfica.

        Parámetros:
            -y_min (int): Fila inicial de la región.
            -y_max (int): Fila final de la región.
            -x_min (int): Columna inicial de la región.
            -x_max (int): Columna final de la región.

        Retorna:
            imagen_radiografia: Nueva instancia que almacena la submatriz recortada.

        Raises:
            ValueError: Si las coordenadas son negativas, inconsistentes (mínimo mayor al máximo) 
                o si desbordan las dimensiones de la imagen original.
        """
        # Obtenemos las dimensiones reales (alto y ancho) de la matriz de la radiografía
        alto_real, ancho_real = self.data.shape[:2]

        
        # Validamos que los límites mínimos no superen o igualen a los límites máximos
        if x_min >= x_max or y_min >= y_max:
            raise ValueError(f"Error de rango: Los valores mínimos [{x_min}, {y_min}] "
                            f"deben ser menores que los máximos [{x_max}, {y_max}].")
        
        # Validamos que las coordenadas no sean negativas
        if x_min < 0 or y_min < 0:
            raise ValueError("Error de rango: Las coordenadas no pueden ser negativas.") 
        
        # Validamos que ninguna coordenada este fuera de rango del tamaño de la matriz
        if x_max > ancho_real or y_max > alto_real:
            raise ValueError(f"Error de rango: Las coordenadas exceden los límites de la radiografía "
                            f"(Tamaño actual: {ancho_real}x{alto_real}).")
        
        # Guardamos la región seleccionada en el objeto original
        self._region_interes = (x_min, y_min, x_max, y_max)

        # Extraer la submatriz utilizando slicing
        matriz_recortada = self.data[y_min:y_max, x_min:x_max]
        
        # Creamos una copia independiente de la información
        info_nueva = Info(self.info.datos.copy())

        # Marcamos que la nueva imagen fue cortada
        info_nueva.datos["cortada"] = True

        # Instanciamos el nuevo objeto radiográfico pasando la submatriz y los metadatos
        img_recortada = ImagenRadiografia(matriz_recortada, info=info_nueva)
        
        # Guardamos la región en la imagen recortada
        img_recortada._region_interes = (x_min, y_min, x_max, y_max)

        # Asignamos un nuevo titulo al nuevo objeto detallando el área del recorte
        img_recortada.titulo_actual = f"Recorte [{x_min}:{x_max}, {y_min}:{y_max}]"

        # Registramos la acción de recorte en el historial de la imagen original
        self.historial.modificar_historial(f"Se recortó la imagen.")

        # Retornamos la nueva instancia de imagen radiografica
        return img_recortada

    def _cargar_y_vectorizar_imagenes(self,carpeta, tamano=(128, 128)):
        """Lee todas las radiografías, las redimensiona y las convierte en vectores lineales."""
        vectores = []
        imagenes_originales = []
        nombres = []
        
        # os.listdir ya devuelve una lista con todos los nombres de los archivos
        archivos = os.listdir(carpeta)
        
        for archivo in archivos:
            ruta = os.path.join(carpeta, archivo)
            objeto_img = Imagen.cargar(ruta=ruta)
            if objeto_img is not None:
                # Guardamos una versión legible para el "hover"
                imagenes_originales.append(objeto_img)
                nombres.append(archivo)
                
                # Redimensionar para que todas tengan la misma cantidad de píxeles
                img_redimensionada = cv2.resize(objeto_img.data, tamano)
                # Aplanar la imagen completa a un vector de 1 fila
                vectores.append(img_redimensionada.flatten())
                
        return np.array(vectores), imagenes_originales, nombres


    def _reducir_dimensiones(self,vectores_imagenes):
        """Reduce los píxeles a solo 2 coordenadas (X, Y) usando PCA."""
        pca = PCA(n_components=2, random_state=42)
        puntos_2d = pca.fit_transform(vectores_imagenes)
        return puntos_2d


    # Metodo auxiliar que 
    def _agrupar_con_kmeans(self,puntos_2d, k=3):
        """Aplica K-means sobre los puntos bidimensionales."""
        kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
        etiquetas = kmeans.fit_predict(puntos_2d)
        return etiquetas

    # Método  
    def visualizar_cluster(self,carpeta_radiografias, k=3):
        """
        Método principal que agrupa las radiografías completas en un plano 2D
        y genera la gráfica interactiva con ventana emergente al pasar el cursor.
        """
        # Procesamos el set de datos completo
        vectores, imagenes_reales, nombres = self.cargar_y_vectorizar_imagenes(carpeta_radiografias)
        
        if len(vectores) == 0:
            print("No se encontraron imágenes válidas.")
            return
            
        # Obtenemos coordenadas X (Feature 1) e Y (Feature 2)
        puntos_2d = self.reducir_dimensiones(vectores)
        
        # Clasificamos a qué grupo pertenece a cada radiografía
        etiquetas = self.agrupar_con_kmeans(puntos_2d, k=k)
        
        # Creamos la gráfica interactiva de Matplotlib
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.set_title("Image Clusters (Radiografías)", fontsize=14, fontweight='bold')
        ax.set_xlabel("Feature 1")
        ax.set_ylabel("Feature 2")
        
        # Dibujamos los puntos del scatter plot usando colores según su clúster
        colores_mapa = ["red", "blue", "green", "purple", "orange"]
        colores_puntos = [colores_mapa[e % len(colores_mapa)] for e in etiquetas]
        
        scatter = ax.scatter(puntos_2d[:, 0], puntos_2d[:, 1], c=colores_puntos, s=100, edgecolors='black', alpha=0.8)
        
        # Creamos la ventana oculta por defecto para la radiografía
        imagen_vacia = np.zeros((50, 50), dtype=np.uint8) # Cuadro negro temporal
        imagen_flotante = OffsetImage(imagen_vacia, zoom=0.5, cmap='gray')
        caja_anotacion = AnnotationBbox(imagen_flotante, (0, 0), xybox=(30, 30),
                                        xycoords='data', boxcoords="offset points",
                                        arrowprops=dict(arrowstyle="->"), bboxprops=dict(boxstyle="round", fc="w"))
        caja_anotacion.set_visible(False)
        ax.add_artist(caja_anotacion)
        
        # --- EVENTO HOVER (Detectar el movimiento del cursor) ---
        def hover(event):
            vis = caja_anotacion.get_visible()
            if event.inaxes == ax:
                # Comprobar si el cursor está sobre algún punto del scatter plot
                cont, ind = scatter.contains(event)
                if cont:
                    # Obtener el índice de la radiografía seleccionada
                    idx = ind["ind"][0]
                    pos = puntos_2d[idx]
                    
                    # Actualizar la posición de la ventana flotante
                    caja_anotacion.xy = pos
                    
                    # Cambiar la imagen del cuadro por la radiografía real correspondiente
                    # Redimensionamos un poco la ventana emergente para que no tape todo el gráfico
                    img_popup = cv2.resize(imagenes_reales[idx].data, (150, 150))
                    imagen_flotante.set_data(img_popup)
                    
                    caja_anotacion.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    if vis:
                        caja_anotacion.set_visible(False)
                        fig.canvas.draw_idle()

        # Conectar la función hover a la ventana de Matplotlib
        fig.canvas.mpl_connect("motion_notify_event", hover)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()

        # Guardamos en el historial el cambio realizado
        self.historial.modificar_historial(f"Se visualizó el cluster de radiografías con k={k}.")

