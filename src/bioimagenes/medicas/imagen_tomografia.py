from bioimagenes.core.imagen import Imagen
import numpy as np
from bioimagenes.core.info import Info

class ImagenTomografica(Imagen):
    """Clase heredada de Imagen especializada en imagenes tomograficas
    Clase hija de Imagen especializada en imágenes tomográficas (3D).

    Extiende Imagen para manejar volúmenes 3D (ej: NIfTI, DICOM),
    proporcionando herramientas para acceder a cortes individuales,
    ajustar ventanas de intensidad, aplicar presets de tejido,
    segmentar tejidos por color y reconstruir el volumen en 3D.

    Parámetros
    ----------
    - data : np.ndarray
        Matriz con los datos del volumen.
        - Debe ser np.ndarray de 2 o 3 dimensiones.
        - Si es 3D, shape debe ser (filas, columnas, cortes) con cortes >= 1.
        - Los valores pueden ser int o float.

    - info : Info o None
        Metadatos asociados a la imagen.
        - Debe ser instancia de Info o None.
        - Si es None → se crea una instancia por defecto.
        - Se le agrega automáticamente el atributo tamaño_voxel si no lo tiene.

    Atributos privados
    ------------------
    - __ventana_actual : tuple (min, max)
        Rango de intensidades visible en la visualización.
        - Ambos valores deben ser numéricos (int o float).
        - min debe ser estrictamente menor que max.
        - Se inicializa con (data.min(), data.max()).
        - Solo modificable mediante ajustar_ventana().

    - __corte_actual : int
        Índice del corte actualmente seleccionado.
        - Debe ser int en el rango [0, número_de_cortes - 1].
        - Se inicializa en 0.
        - Solo modificable mediante seleccionar_corte().
    """
    
    #Definimos los atributos de clase, estos se usarán para el método aplicar_preset() que ajusta la ventana seún el tipo de tejido
    #Los presets son siempre los mismos para todos los objetos por eso son atributos de clase

    _PRESETS_TEJIDO = {             
        "cerebro":   {"centro":  40,  "ancho":  80,  "color": "Purples"}, #colormaps de matplotlib para colorear imagenes
        "hueso":     {"centro": 400,  "ancho": 1800, "color": "bone"},
        "pulmon":    {"centro": -600, "ancho": 1500, "color": "Blues"},
        "higado":    {"centro":  60,  "ancho": 160,  "color": "YlOrBr"},
        "tejido":    {"centro":  50,  "ancho": 350,  "color": "RdYlGn"},
        "angio":     {"centro": 250,  "ancho": 500,  "color": "hot"},
    }

    
    def __init__(self, data: np.ndarray, info: Info = None):
        super().__init__(data, info)
        
        #definir atributos privados
        self.__ventana_actual = (float(data.min()), float(data.max()))
        self.__corte_actual = 0 #arranca en el primer slice
