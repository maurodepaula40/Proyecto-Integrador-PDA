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
            Ejemplo: {"dimensiones": (100, 100), "brillo": 120}
        historial : Historial
            Instancia de la clase Historial asociada a la imagen.
            Si no se proporciona, se crea una nueva.

        Retorna
        -------
        None
            """
        # Si nos pasan un historial lo usamos, si no, creamos uno nuevo vacío
        self.historial:Historial = historial if historial is not None else Historial()

        # Si nos pasan un diccionario lo usamos, si no, creamos uno con valores por defecto
        if datos is not None:
            self._datos = {
                "dimensiones": datos.get("dimensiones", (0, 0, 1)),
                "brillo": int(datos.get("brillo", 0)),  #forzar a que sean 8 bits (entero) porque float usa 64 por defecto
                "cortada": datos.get("cortada", False),
                "tipo_estudio": datos.get("tipo_estudio", ""),
            }

        else:
            self._datos = {
                "dimensiones":  (0, 0, 1),
                "brillo":       0,
                "cortada":      False,
                "tipo_estudio": "",
            }

     def __contains__(self, key: str):
        """
        Permite verificar si una clave existe en los metadatos.
        Se activa con el operador 'in'.

        Ejemplo: "brillo" in info  →  True

        Parámetros
        ----------
        key : str
            Nombre del metadato a verificar.

        Retorna
        -------
        bool
        """

        return key in self._datos
     
     def __getitem__(self, key: str):
        """
        Permite acceder a valores como info["brillo"].
        Se activa con el operador [].

        Parámetros
        ----------
        key : str
            Nombre del metadato a obtener.

        Retorna
        -------
        El valor del metadato solicitado.

        Lanza
        -----
        KeyError si la clave no existe.
        """

        if key not in self._datos:  #si la clave no existe → error
            raise KeyError(f"'{key}' no es un metadato válido de Info.")
        
        return self._datos[key] #si existe retorna el dato solicitado
     
     def tamaño_voxel(self):
        """
        Calcula el tamaño total de la imagen en cantidad de voxels.
        Equivale a ancho x alto x canales.
        Solo válido para imágenes 3D.

        Retorna
        -------
        int : cantidad total de voxels en la imagen.

        Lanza
        -----
        ValueError si las dimensiones no son una tupla de exactamente 3 elementos.
        """
        dimensiones = self._datos["dimensiones"]

        if len(dimensiones) != 3:
            raise ValueError(
                f"tamaño_voxel() requiere dimensiones 3D (ancho, alto, canales), "
                f"pero se recibió: {dimensiones}"
            )

        ancho, alto, canales = dimensiones
        return ancho * alto * canales