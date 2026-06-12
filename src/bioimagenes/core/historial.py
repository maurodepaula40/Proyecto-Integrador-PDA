from datetime import datetime

class Historial():
    """
    Clase para registrar y gestionar la trazabilidad de las operaciones
    realizadas sobre una imagen.

    Guarda los cambios en una lista y permite:
    - Agregar nuevos cambios
    - Consultar el último cambio
    - Contar cuántos cambios hay
    - Recorrerlos
    - Mostrar un resumen
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
            self.__lista_cambios = []  # Lista vacía por defecto
        else:
            self.__lista_cambios = lista_cambios  # Usa la lista dada
    
    @property
    def lista_cambios(self):
        return self.__lista_cambios

    def modificar_historial(self, cambio:str):
        """
        Agrega un nuevo cambio al historial.

        Parámetros:
            -cambio : str
                Descripción del cambio realizado (ej: "Filtro aplicado")
        
        - Toma el cambio recibido
        - Lo agrega al final de la lista
        """
        # datetime.now() saca la hora exacta de la computadora en este segundo.
        fecha_y_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Guardamos esa fecha en un diccionario
        registro = {
            "fecha": fecha_y_hora,  # Ej: "2026-06-09 21:51:00"
            "operacion": cambio
        }
        self.lista_cambios.append(registro)
    
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
            return "Historial vacío: No se han registrado cambios."
        
        texto = f"""==================================================
            HISTORIAL CLÍNICO DE LA IMAGEN
==================================================
 FECHA Y HORA        | OPERACIÓN REALIZADA
--------------------------------------------------"""
        for cambio in self.lista_cambios:
            texto += f"\n {cambio['fecha']} | {cambio['operacion']}"
        
        texto += f"""\n==================================================
 Total operaciones: {len(self.lista_cambios)} | Último: {self.ultimo_cambio}
=================================================="""

        return texto