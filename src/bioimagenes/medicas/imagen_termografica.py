from bioimagenes.core.imagen import Imagen
import matplotlib.pyplot as plt
import numpy as np

class imagen_termografica(Imagen):
    """
    Clase especializada para el manejo y análisis de imágenes termográficas.
    Hereda de la clase base Imagen.
    """
    def __init__(self,data,info):
        """
        Documentacion
        """
        super().__init__(data, info)
        #self.temp_min = rango_temperatura[0]
        #self.temp_max = rango_temperatura[1]
        pass


    def convertir_a_temperatura(self):
        pass


    def mapa_calor(self):
        """
        Muestra la imagen termografica utilizando un mapa de color
        """
        #Normalización Min-Max
        data_min = self.data.min()
        data_max = self.data.max()
        data_normalizada = (self.data - data_min) / (data_max - data_min)

        #Mapeo a color RGB (0 a 255)
        cmap_termico = plt.get_cmap("jet")
        matriz_rgb_float = cmap_termico(data_normalizada)[:,:, :3]
        matriz_termica_rgb = (matriz_rgb_float * 255).astype(np.uint8)

        nueva_imagen = imagen_termografica(matriz_termica_rgb, self.info)
        nueva_imagen.titulo_actual = f"Mapa de Calor Térmico (Rango Real: {data_min:.1f}°C a {data_max:.1f}°C)"

        # 5. MODIFICACIÓN DE HISTORIAL (EN LA ORIGINAL): 
        # Usamos 'self' para que el cambio quede guardado para siempre en el objeto original.
        self.historial.modificar_historial("Se generó una nueva instancia con mapa de calor térmico")

        # 6. Retornamos el nuevo objeto empaquetado y listo
        return nueva_imagen

    def detectar_puntos_calientes(self):
        pass