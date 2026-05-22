from bioimagenes.core.historial import Historial
class Info:
     """
    Clase para almacenar y gestionar los metadatos asociados a una imagen.
    Funciona de manera similar a un diccionario, permitiendo acceder, modificar
    y consultar información relevante como dimensiones, brillo, contraste y estado
    de la imagen. 
    
    Además, se integra con la clase Historial para mantener coherencia
    entre los datos y las transformaciones aplicadas.

    Parámetros
    ----------
    - datos : dict o None
        Diccionario con los metadatos iniciales de la imagen.
        Si no se proporciona, se inicializa con valores por defecto.

        Claves reconocidas:
            - "dimensiones" : tuple de 2 o 3 ints positivos.
                              Formato: (ancho, alto) o (ancho, alto, canales).
                              Por defecto: (0, 0, 1)
            - "brillo"      : int entre 0 y 255.
                              Por defecto: 0
            - "cortada"     : bool.
                              Por defecto: False
            - "tipo_estudio": str.
                              Por defecto: ""

    - historial : Historial o None
        Instancia de Historial asociada a la imagen.
        Si no se proporciona, se crea una nueva instancia vacía.
    """
     
    # Conjunto con los nombres de metadatos permitidos.
    # Lo usamos para validar que nadie acceda a una clave que no existe en Info.
     METADATOS_VALIDOS = {"dimensiones", "brillo", "historial", "cortada", "tipo_estudio"}


     def __init__(self, datos:dict = None, historial: Historial= None): 
        """Ver documentación de la clase."""
        
        if datos is not None and not isinstance(datos, dict): # si nos pasan algo que no es un diccionario → error 
            raise TypeError(f"'datos' debe ser un diccionario, se recibió {type(datos).__name__}.")
        
        if historial is not None and not isinstance(historial, Historial): #si el dato pasado no es una instancia de Historial → error
            raise TypeError(f"'historial' debe ser una instancia de Historial, se recibió {type(historial).__name__}.")
        
        # Si nos pasan un historial lo usamos, si no, creamos uno nuevo vacío
        self.historial:Historial = historial if historial is not None else Historial()

        # Si nos pasan un diccionario lo usamos, si no, creamos uno con valores por defecto
        if datos is not None:
            self._datos = {
                "dimensiones": datos.get("dimensiones", (0, 0, 1)),
                "brillo": int(datos.get("brillo", 0)),  #forzar a que sean 8 bits (entero) porque float usa 64 por defecto (recomendación del docente)
                "cortada": datos.get("cortada", False),
                "tipo_estudio": datos.get("tipo_estudio", ""),
                "tamano_voxel": datos.get("tamano_voxel", (1.0, 1.0, 1.0)),
            }

        else:
            self._datos = {
                "dimensiones":  (0, 0, 1),
                "brillo":       0,
                "cortada":      False,
                "tipo_estudio": "",
                "tamano_voxel": (1.0, 1.0, 1.0),
            }

     def __contains__(self, key: str) -> bool:
        """
        Permite verificar si una clave existe en los metadatos.
        Se activa con el operador 'in'.

        Ejemplo: "brillo" in info  →  True

        Parámetros
        ----------
        key : str
            Nombre del metadato a verificar.
            Debe ser un string NO vacío

        Retorna
        -------
        - True si la clave existe en los metadatos, False en caso contrario.
        - No modifica el estado del objeto.
        """
        if not isinstance(key, str): #si la key no es un string → error
            raise TypeError(f"La clave debe ser un string, se recibió {type(key).__name__}.")
        return key in self._datos
     
     def __getitem__(self, key: str):
        """
        Permite acceder a valores como info["brillo"].
        Se activa con el operador [].

        Parámetros
        ----------
        key : str
            Nombre del metadato a obtener
            Debe existir en los metadatos
            Debe ser un string NO vacío

        Retorna
        -------
        El valor asociado a la clave sin modificar el estado del objeto
        """

        if key not in self._datos:  #si la clave no existe → error
            raise KeyError(f"'{key}' no es un metadato válido de Info.")
        
        return self._datos[key] #si existe retorna el dato solicitado
     
     def cantidad_voxel(self):
        """
        Calcula el tamaño total de la imagen en cantidad de voxels.
        Equivale a ancho x alto x canales.
        Solo válido para imágenes 3D.

        Las dimensiones deben ser una tupla de exactamente 3 enteros positivos con formato (ancho, alto, canales).
        
        Retorna
        -------
        int : cantidad total de voxels en la imagen (ancho x alto x canales)
        No modifica el estado del objeto

        """
        dimensiones = self._datos["dimensiones"]

        if len(dimensiones) != 3:
            raise ValueError(
                f"tamaño_voxel() requiere dimensiones 3D (ancho, alto, canales), "
                f"pero se recibió: {dimensiones}"
            )

        ancho, alto, canales = dimensiones
        return ancho * alto * canales
     
     def tamano_voxel(self):
        """
        Retorna las dimensiones físicas de cada vóxel en milímetros.
        Solo válido para imágenes 3D.

        Retorna
        -------
        tuple : (vx, vy, vz) donde cada valor representa el tamaño
                en mm de cada dimensión del vóxel.
                Por defecto (1.0, 1.0, 1.0).
        """
        return self._datos["tamano_voxel"]