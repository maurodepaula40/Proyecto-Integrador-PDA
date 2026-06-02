import numpy as np
import matplotlib.pyplot as plt
from bioimagenes.core.imagen import Imagen
from bioimagenes.core.info import Info

class ImagenRadiografia(Imagen):
    """
    Clase heredada de Imagen especializada en radiografías digitales.

    Trabaja con imágenes 2D en escala de grises y proporciona herramientas
    para su análisis y procesamiento médico: ajuste de contraste, inversión,
    ecualización, detección de bordes, selección de regiones de interés
    y visualización de clusters de intensidad.
    """

    def _init_(self, data: np.ndarray, tipo_estudio: str = "", brillo: int = 0, info: Info = None):
        """
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

        # Llamamos al constructor de Imagen
        super()._init_(data, info)

        # Guardamos tipo_estudio y brillo en Info
        self.info.datos["tipo_estudio"] = tipo_estudio
        self.info.datos["brillo"] = int(brillo)
        
        # Región de interés: ninguna por defecto
        self._region_interes = None