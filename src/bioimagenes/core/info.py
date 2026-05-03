from bioimagenes.core.historial import Historial
class Info:
     """
    Clase para almacenar y gestionar los metadatos asociados a una imagen.
    Funciona de manera similar a un diccionario, permitiendo acceder, modificar
    y consultar información relevante como dimensiones, brillo, contraste y estado
    de la imagen.

    Además, se integra con la clase Historial para mantener coherencia
    entre los datos y las transformaciones aplicadas.
    """
     
    # Conjunto con los nombres de metadatos permitidos.
    # Lo usamos para validar que nadie acceda a una clave que no existe en Info.
     METADATOS_VALIDOS = {"dimensiones", "brillo", "historial", "cortada", "tipo_estudio"}


     def __init__(self, datos:dict = None, historial: Historial= None): 
        """
            Inicializa una instancia de la clase Info.

            Parámetros
            ----------
            datos : dict
                Diccionario con los metadatos iniciales de la imagen.
                Ejemplo: {"dimensiones": (100, 100, 3), "brillo": 120}
            historial : Historial
                Instancia de la clase Historial asociada a la imagen.
                Si no se proporciona, se crea una nueva.

            Retorna
            -------
            None
            """
        # Si nos pasan un historial lo usamos, si no, creamos uno nuevo vacío
        self.historial:Historial = historial if historial is not None else Historial()

        if datos is not None:
            # Buscamos "dimensiones" en el dict. Si no está, usamos (0, 0, 1) por defecto.
            # La tupla es (ancho, alto, canales). 1 canal = escala de grises.
            self.dimensiones = datos.get("dimensiones", (0, 0, 1))
        
        


     
    
    