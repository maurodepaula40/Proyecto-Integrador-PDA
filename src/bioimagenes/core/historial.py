class Historial():
    """
    Clase para registrar y gestionar la trazabilidad de las operaciones
    realizadas sobre una imagen.

    Guarda los cambios en una lista y permite:
    - agregar nuevos cambios
    - consultar el último cambio
    - contar cuántos cambios hay
    - recorrerlos
    - mostrar un resumen
    """

    def __init__(self, lista_cambios:list = None):
        """
        Inicializa una instancia de la clase Historial.

        Parámetros
        lista_cambios : list
            Lista inicial de cambios realizados sobre la imagen.
            Cada cambio puede ser un string o un diccionario.

        - Si no se pasa nada → crea lista vacía
        - Si se pasa una lista → la usa como historial inicial
        """
        if lista_cambios is None:
            self.lista_cambios = []  # Lista vacía por defecto
        else:
            self.lista_cambios = lista_cambios  # Usa la lista dada

    def modificar_historial(self, cambio):
        """
        Agrega un nuevo cambio al historial.

        Parámetros:
        cambio : str
        Descripción del cambio realizado (ej: "Filtro aplicado")
        
        - Toma el cambio recibido
        - Lo agrega al final de la lista
        """

        self.lista_cambios.append(cambio)
    
    @property
    def ultimo_cambio(self):
        if len(self.lista_cambios) > 0:    # si la lista tiene algún elemento
            return self.lista_cambios[-1]  # devuelve el último cambio
        return None
    
    def __len__(self):
        """
        Método nativo
        Retorna la cantidad total de cambios registrados.
        """

        return len(self.lista_cambios)
    
    def __iter__(self):
        """
        Método nativo
        Permite iterar sobre los cambios del historial
        """
        return iter(self.lista_cambios)

    def __str__(self):
        """
        Método nativo
        Muestra un resumen del historial y el último cambio realizado
        """
        if len(self.lista_cambios) == 0:
            return "Historial vacío"

        return f"Total de cambios: {len(self.lista_cambios)} | Último cambio: {self.ultimo_cambio}"