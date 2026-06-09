from bioimagenes.core.imagen import Imagen
from bioimagenes.core.info import Info
import matplotlib.pyplot as plt
import numpy as np
import cv2

class ImagenTermografica(Imagen):
    """
    Representar y procesar imágenes térmicas.

    Es una clase que hereda todos los atributos y metodos de la clase base del sistema.
    """
    def __init__(self, data: np.ndarray, info: Info = None):
        """
        Parámetros:
            -data (np.ndarray): Matriz numérica con las intensidades o temperaturas de la imagen.
            -info (objeto): Conjunto de metadatos asociados a la imagen.
        """
        super().__init__(data, info)


    def convertir_a_temperatura(self, temp_min: float, temp_max: float):
        """
        Convierte los píxeles de intensidad (0 a 255) a valores de temperatura reales
        en grados Celsius basándose en un rango mínimo y máximo.
        """
        # Validamos el rango
        if temp_min >= temp_max:
            raise ValueError(f"Error: La temperatura mínima ({temp_min}) debe ser menor que la máxima ({temp_max}).")

        # Convertimos self.data a float32 para poder almacenar decimales de temperatura
        # y evitar que se trunquen los valores en las operaciones matemáticas
        intensidades_float = self.data.astype(np.float32)

        # Aplicamos la fórmula de escalado lineal:
        # (self.data / 255.0) da un porcentaje entre 0.0 y 1.0.
        # Luego lo multiplicamos por el tamaño del rango térmico y le sumamos el piso (temp_min).
        matriz_temperaturas = (intensidades_float / 255.0) * (temp_max - temp_min) + temp_min

        # Modificamos in place, guardamos la matriz de temperaturas reales en el objeto
        self.data = matriz_temperaturas

        # Asignamos un titulo
        self.titulo_actual = f"Matriz Térmica Calibrada ({temp_min}°C a {temp_max}°C)"

        # Registramos en el historial
        self.historial.modificar_historial(f"Conversión a temperatura: rango [{temp_min}, {temp_max}] °C")


    def mapa_calor(self):
        """
        Genera un mapa de calor.
        Registrar el procesamiento en el historial de cambios.

        Returns:
            imagen_termografica: Nueva instancia con la matriz convertida en un mapa de calor.
        """
        # Obtenemos los valores térmicos mínimos y máximos de la matriz de datos
        data_min = self.data.min()
        data_max = self.data.max()

        #Normalizamos la imagen
        matriz_normalizada = Imagen.normalizar(self.data)

        # Llevamos temporalmente al rango 0.0 - 1.0 para que Matplotlib pueda aplicar el mapa de color
        data_para_cmap = matriz_normalizada / 255.0

        # Mapeamos a color RGB con la paleta "jet"
        cmap_termico = plt.get_cmap("jet")
        
        # Convertimos en una estructura RGB descartando el canal alfa 
        matriz_rgb_float = cmap_termico(data_para_cmap)[:, :, :3]

        # Transformamos los valores flotantes al formato estándar de 8 bits (0-255)
        self.data = (matriz_rgb_float * 255.0).astype(np.uint8)

        # Agregamos un titulo
        self.titulo_actual = f"Mapa de Calor Térmico (Rango: {data_min:.1f}°C a {data_max:.1f}°C)"

        # Registramos el cambio en el historial
        self.historial.modificar_historial("Imagen Radiográfica convertida a mapa de calor térmico")

    def segmentar_por_rangos(self,rango_min:int|float,rango_max:int|float):
        """
        Método que segmenta la imagen termografica según un rango de interés,
        pintando la zona seleccionada de rojo directamente sobre la imagen actual.
        Registra la operación en el historial de cambios.

        Parámetros:
            -rango_min (int | float): Valor térmico mínimo para iniciar el corte del rango.
            -rango_max (int | float): Valor térmico máximo para finalizar el corte del rango.
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
        
        # Pisamos la matriz del objeto actual con el resultado a color
        self.data = img_segmentada_a_color

        # Ponemos un titulo, modificando el objeto actual
        self.titulo_actual = f"Segmentación ({rango_min} a {rango_max})"


        #Añadimos el cambio de la segmentación en el historial del objeto original.
        self.historial.modificar_historial(f"Se aisló rango [{rango_min}, {rango_max}]")


    def detectar_puntos_calientes(self, temperatura: int | float, tolerancia: int|float = 1.0):
        """
        Detecta los puntos calientes o críticos con un valor de temperatura específico,
        pintándolos de rojo directamente sobre la imagen actual.
        Registra el cambio en el historial de modificaciones.

        Parámetros:
            temperatura (int|float): Valor térmico objetivo en grados Celsius.
            tolerancia (int|float): Margen de desvío permitido arriba y abajo del objetivo. Por defecto 0.5.
        """
        #Calculamos el límite térmico inferior y superior
        limite_inferior = temperatura - tolerancia
        limite_superior = temperatura + tolerancia

        #Generamos la máscara aislando únicamente los píxeles que caen dentro del rango
        puntos_calientes = cv2.inRange(self.data, limite_inferior, limite_superior)

        #Convertimos la matriz de escala de grises a formato RGB para habilitar el uso de colores
        img_puntos_calientes = cv2.cvtColor(self.data, cv2.COLOR_GRAY2RGB)
        
        #Asignamos color rojo puro (RGB: 255, 0, 0) a todos los píxeles validados por la máscara
        img_puntos_calientes[puntos_calientes > 0] = [255, 0, 0]

        # Modificacion in place, guardamos la matriz RGB directamente en el objeto actual
        self.data = img_puntos_calientes
    
        # Ponemos un titulo 
        self.titulo_actual = f"Puntos Térmicos Críticos ({temperatura}°C)"

        #Registramos el cambio en el historial de la imagen original
        self.historial.modificar_historial(f"Se aislaron los puntos con temperatura de {temperatura}°C (Tolerancia: +-{tolerancia})")