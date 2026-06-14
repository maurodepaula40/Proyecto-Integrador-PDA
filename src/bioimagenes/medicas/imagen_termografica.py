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
        # Guardamos temp_min y temp_max
        self.temp_min = temp_min
        self.temp_max = temp_max
        
        # Validamos el rango
        if temp_min >= temp_max:
            raise ValueError(f"Error: La temperatura mínima ({temp_min}) debe ser menor que la máxima ({temp_max}).")

        self.data = temp_min + (self.data.astype(np.float32) / 255.0) * (temp_max - temp_min)

        # Asignamos un titulo
        self.titulo_actual = f"Imagen Termográfica ({temp_min}°C a {temp_max}°C)"

        # Registramos en el historial
        self.historial.modificar_historial(f"Conversión a temperatura: rango [{temp_min}, {temp_max}] °C")

        return self

    def mapa_calor(self):
        """
        Aplica un mapa de color sobre la imagen tormográfica.
        """
        # Reutilizamos el método estático de la clase base para obtener la imagen entre 0 y 255 en np.uint8
        grises_visuales = Imagen.normalizar(self.data)
        
        # Aplicamos la paleta de colores sobre los grises
        img_color = cv2.applyColorMap(grises_visuales, cv2.COLORMAP_JET)
        
        # Convertimos de BGR a RGB y pisamos self.data
        self.data = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
        
        # Actualizamos el titulo
        self.titulo_actual = "Mapa de Calor"
        self.historial.modificar_historial("Se aplicó mapa de calor")
        return self

    def segmentar_por_rangos(self, min_temp: float, max_temp: float):
        """
        Aísla las zonas que se encuentren dentro del rango térmico 
        en grados Celsius especificado y las pinta de rojo.
        """

        # Creamos la máscara lógica usando las temperaturas Celsius reales
        mascara = (self.data >= min_temp) & (self.data <= max_temp)

        # Normalizamos la matriz original a formato visual uint8 (0-255) para el fondo
        v_min, v_max = self.data.min(), self.data.max()
        if v_max - v_min == 0:
            fondo_gris = np.zeros(self.data.shape, dtype=np.uint8)
        else:
            fondo_gris = (((self.data - v_min) / (v_max - v_min)) * 255).astype(np.uint8)

        # 4. Construimos la imagen de salida en 3 canales (RGB)
        imagen_rgb = cv2.cvtColor(fondo_gris, cv2.COLOR_GRAY2RGB)

        # 5. Pintamos de ROJO PURO [255, 0, 0] donde la máscara lógica sea verdadera
        imagen_rgb[mascara] = [255, 0, 0]

        # Guardamos el estado final y registramos la operación
        self.data = imagen_rgb
        # Actualizamos el titulo
        self.titulo_actual = f"Segmentación ({min_temp:.1f}°C a {max_temp:.1f}°C)"
        # Guardamos el cambio en el historial
        self.historial.modificar_historial(f"Segmentación por rangos térmicos: {min_temp} - {max_temp}")


    def detectar_puntos_calientes(self, temperatura: float, tolerancia: float = 1.0):
        """
        Detecta focos térmicos críticos basándose en un umbral Celsius y su tolerancia,
        destacándolos en color rojo.
        """
        # Calculamos los límites de la ventana térmica objetivo
        limite_inferior = temperatura - tolerancia
        limite_superior = temperatura + tolerancia

        # Evaluamos la máscara directamente sobre las temperaturas 
        mascara = (self.data >= limite_inferior) & (self.data <= limite_superior)

        # Normalizamos la matriz original a formato visual de grises (0-255)
        v_min, v_max = self.data.min(), self.data.max()
        if v_max - v_min == 0:
            fondo_gris = np.zeros(self.data.shape, dtype=np.uint8)
        else:
            fondo_gris = (((self.data - v_min) / (v_max - v_min)) * 255).astype(np.uint8)

        # Pasamos a 3 canales (RGB)
        imagen_rgb = cv2.cvtColor(fondo_gris, cv2.COLOR_GRAY2RGB)

        # Destacamos los puntos calientes en ROJO PURO [255, 0, 0]
        imagen_rgb[mascara] = [255, 0, 0]

        #Actualizamos el estado de self.data
        self.data = imagen_rgb
        #Actualizamos el titulo
        self.titulo_actual = f"Puntos Críticos ({temperatura:.1f}°C)"
        self.historial.modificar_historial(f"Detección de puntos calientes en: {temperatura} (+/-{tolerancia})")