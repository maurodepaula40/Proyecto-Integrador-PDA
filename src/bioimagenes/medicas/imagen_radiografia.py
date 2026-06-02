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

    def _init_(self, data: np.ndarray, tipo_estudio: str = "", brillo: int = 0, info: Info = None):
        """Ver documentación de la clase"""

        # Llamamos al constructor de Imagen
        super().__init__(data, info)

        # Guardamos tipo_estudio y brillo en Info
        self._info._datos["tipo_estudio"] = tipo_estudio
        self._info._datos["brillo"] = int(brillo)

        # Región de interés: ninguna por defecto
        self._region_interes = None
    
    #Propiedades para acceder a atributos de Info
    @property
    def tipo_estudio(self):
        """Retorna el tipo de estudio radiográfico almacenado en Info."""
        return self._info["tipo_estudio"]

    @property
    def brillo(self):
        """Retorna el valor de brillo almacenado en Info."""
        return self._info["brillo"]
    
    @property
    def region_interes(self):
        """Retorna la región de interés actual o None si no fue definida."""
        return self._region_interes

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
        resultado = np.clip((datos - 128) * factor + 128, 0, 255).astype(np.uint8)

        # Registramos en el historial
        self.historial.modificar_historial(f"Contraste mejorado: factor {factor}")

        #Retorna una imagen (instancia de la clase, no la original) con el contraste modificado
        return ImagenRadiografia(resultado, self.tipo_estudio, self.brillo)
    

