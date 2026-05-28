from bioimagenes.core.imagen import Imagen
from bioimagenes.core.info import Info
import matplotlib.pyplot as plt
import numpy as np
import cv2

class imagen_termografica(Imagen):
    """
    Representar y procesar imágenes térmicas.

    Es una clase que hereda todos los atributos y metodos de la clase base del sistema.
    """
    def __init__(self, data: np.ndarray, info: Info = None):
        """
        Parámetros:
            -data (np.ndarray): Matriz numérica con las intensidades o temperaturas del examen.
            -info (objeto): Conjunto de metadatos asociados a la imagen.
        """
        super().__init__(data, info)


    def convertir_a_temperatura(self):
        pass


    def mapa_calor(self):
        """
        Generar un mapa de calor.
        Registrar el procesamiento en el historial de cambios.

        Returns:
            imagen_termografica: Nueva instancia con la matriz convertida en un mapa de calor.
        """
        # Obtenemos los valores térmicos mínimos y máximos de la matriz de datos
        data_min = self.data.min()
        data_max = self.data.max()

        #Normalizamos la imagen entre un rango de 0 y 1
        data_normalizada = (self.data - data_min) / (data_max - data_min)

        # Mapeamos a color RGB con la paleta "jet"
        cmap_termico = plt.get_cmap("jet")
        
        # Convertimos los datos normalizados en una estructura RGB descartando el canal alfa de transparencia
        matriz_rgb_float = cmap_termico(data_normalizada)[:,:, :3]

        # Transformamos los valores flotantes al formato estándar de 8 bits con enteros sin signo
        matriz_termica_rgb = (matriz_rgb_float * 255).astype(np.uint8)

        # Instanciamos un nuevo objeto con la nueva matriz a color y los metadatos
        nueva_imagen = imagen_termografica(matriz_termica_rgb, self.info)

        # Asignamos un título al nuevo objeto detallando el rango de temperaturas analizadas
        nueva_imagen.titulo_actual = f"Mapa de Calor Térmico (Rango: {data_min:.1f}°C a {data_max:.1f}°C)"

        # Registramos el cambio en el historial de la imagen original
        self.historial.modificar_historial("Se generó una nueva instancia con mapa de calor térmico")

        # Retornamos el nuevo objeto de imagen termográfica
        return nueva_imagen

    def segmentar_por_rangos(self,rango_min:int|float,rango_max:int|float):
        """
        Metodo que segmenta la imagen térmica según un rango de interés.
        Registra la operación en el historial de la imagen de origen.

        Parámetros:
            -rango_min (int | float): Valor térmico mínimo para iniciar el corte del rango.
            -rango_max (int | float): Valor térmico máximo para finalizar el corte del rango.

        Retorna:
            - una nueva instancia de imagen_termografica con la zona de interes en color rojo.
        """
        #Validamos que el límite mínimo no supere o iguale al límite máximo establecido
        if rango_min >= rango_max:
            raise ValueError(f"Error en los parámetros: El rango mínimo ({rango_min}) debe ser menor al máximo ({rango_max}).")

        #Obtenemos los extremos térmicos presentes en la matriz
        absoluto_min = self.data.min()
        absoluto_max = self.data.max()

        #Validamos que los valores que se pasaron como parametro no queden fuera de rango de la imagen
        if rango_min < absoluto_min or rango_max > absoluto_max:
            raise ValueError(
                f"Error de desbordamiento: El rango [{rango_min}, {rango_max}] excede los límites reales de la imagen "
                f"[{absoluto_min:.2f}, {absoluto_max:.2f}]."
            )

        #Generamos una máscara binaria donde los píxeles dentro del rango toman valor 255 y el resto 0
        mascara = cv2.inRange(self.data, rango_min, rango_max)

        #Convertimos la matriz de escala de grises a formato RGB para habilitar el uso de colores
        img_segmentada_a_color = cv2.cvtColor(self.data, cv2.COLOR_GRAY2RGB)
        
        #Asignamos color rojo puro (RGB: 255, 0, 0) a todos los píxeles validados por la máscara
        img_segmentada_a_color[mascara > 0] = [255, 0, 0]
        
        #Creamos una nueva instancia de la clase para almacenar la imagen segmentada a color
        img_segmentada = imagen_termografica(img_segmentada_a_color, self.info)

        #Formateamos el título de la nueva imagen reflejando los límites térmicos
        img_segmentada.titulo_actual = f"Segmentación ({rango_min} a {rango_max})"

        #Añadimos el cambio de la segmentación en el historial del objeto original.
        self.historial.modificar_historial(f"Se aisló rango [{rango_min}, {rango_max}]")

        #Devolvemos el nuevo objeto
        return img_segmentada

    def detectar_puntos_calientes(self, temperatura: int | float, tolerancia: int|float = 0.5):
        """Detecta los puntos calientes o criticos con un valor de temperatura específico.

        Registrar el cambio en el historial de la imagen de origen y retornar una nueva instancia 
        independiente con los puntos térmicos aislados.

        Parámetros:
            temperatura (int|float): Valor térmico objetivo en grados Celsius.
            tolerancia (int|float): Margen de desvío permitido arriba y abajo del objetivo. Por defecto 0.5.

        Retorna:
            imagen_termografica: Nueva instancia con la máscara de los puntos detectados.
        """
        #Calculamos el límite térmico inferior
        limite_inferior = temperatura - tolerancia
        
        #Calculamos el límite térmico superior
        limite_superior = temperatura + tolerancia

        #Generamos la máscara aislando únicamente los píxeles que caen dentro del rango
        puntos_calientes = cv2.inRange(self.data, limite_inferior, limite_superior)

        #Convertimos la matriz de escala de grises a formato RGB para habilitar el uso de colores
        img_puntos_calientes = cv2.cvtColor(self.data, cv2.COLOR_GRAY2RGB)
        
        #Asignamos color rojo puro (RGB: 255, 0, 0) a todos los píxeles validados por la máscara
        img_puntos_calientes[puntos_calientes > 0] = [255, 0, 0]
        
        #Creamos la nueva instancia de la clase pasando la matriz
        img_segmentada = imagen_termografica(img_puntos_calientes, self.info)

        #Asignamos el título de la imagen
        img_segmentada.titulo_actual = f"Puntos Térmicos Criticos ({temperatura}°C)"

        #Registramos el cambio en el historial de la imagen original
        self.historial.modificar_historial(f"Se aislaron los puntos con temperatura de {temperatura}°C (Tolerancia: +-{tolerancia})")

        #Retornamos una objeto nuevo
        return img_segmentada