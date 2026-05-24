from bioimagenes.core.imagen import Imagen
import numpy as np
from bioimagenes.core.info import Info
import matplotlib.pyplot as plt

class ImagenTomografica(Imagen):
    """Clase heredada de Imagen especializada en imagenes tomograficas

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

    Atributos
    - ventana_actual : tuple (min, max)
        Rango de intensidades visible en la visualización.
        - Ambos valores deben ser numéricos (int o float).
        - min debe ser estrictamente menor que max.
        - Se inicializa con (data.min(), data.max())

    - corte_actual : int
        Índice del corte actualmente seleccionado.
        - Debe ser int en el rango [0, número_de_cortes - 1].
        - Se inicializa en 0.
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
        self.ventana_actual = (float(data.min()), float(data.max()))
        self.corte_actual = 0 #arranca en el primer slice

        # si el usuario pasó un Info lo asignamos, si no ya lo creó super()
        if info is not None:
            self.info = info

    
    def obtener_corte(self, indice:int):
        """ Devuelve un corte (slice) específico del volumen.
        
        Retorna:  np.ndarray. Matriz 2D del corte solicitado."""
        # verificar que sea un volumen
        if self.data.ndim != 3:
            raise ValueError(
                "La imagen no es tomográfica (debe ser 3D)"
            )
         
         # cantidad total de cortes
        total_cortes = self.data.shape[2]

        # verificar rango
        if indice < 0 or indice >= total_cortes:
            raise IndexError(
                f"Corte fuera de rango. "
                f"Hay {total_cortes} cortes"
            )

        corte = self.data[:,:,indice]  #el tercer elemento corresponde a la cantidad de slices

        return corte
    
    def seleccionar_corte(self, indice:int):
        """Selecciona un corte del volumen y lo guarda como corte actual para trabajar sobre él"""
        
        # verificamos que el corte exista
        self.obtener_corte(indice)

        # guardamos el índice
        self.corte_actual = indice

        # registrar historial
        self.info.historial.modificar_historial(f"Corte {indice} seleccionado")

    def mostrar_corte(self):
        """Muestra el corte actualmente seleccionado aplicando la ventana médica."""

        # verificar si hay corte seleccionado
        if self.corte_actual is None:
            raise ValueError("No hay un corte seleccionado")

        # obtener corte actual
        corte = self.obtener_corte(self.corte_actual)

        # obtener limites de ventana
        minimo,maximo = self.ventana_actual

        # aplicar ventana
        corte = np.clip(corte,minimo,maximo)  
        #clip convierte los valores > maximo en en maximo y los valores < minimo en el minimo,
        # para acotar la ventana a los limites que queremos

        # normalizar para visualizar
        corte = (corte-minimo)/(maximo-minimo) #reestingimos los valores entre 0 y 1 para que plt.imshow funcione mejor

        # mostrar
        plt.imshow(corte,cmap="gray")

        plt.title(f"Corte {self.corte_actual}")

        plt.axis("off")

        plt.show()

  