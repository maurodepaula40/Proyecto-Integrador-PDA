from bioimagenes.core.historial import Historial

def test_basico():
    h = Historial()   #creo historial vacío
    assert len(h) == 0  #verifico que no tenga nada, assert sirve para hacer el test
                        # si pasa el test dice passed, si no falla

# ==========================================================
#   TESTS DE HISTORIAL
# ==========================================================

def test_agregar_un_cambio():
    """Verifica que al agregar un cambio se guarde la estructura de diccionario."""
    h = Historial()
    h.modificar_historial("Filtro aplicado")
    
    # Comprobamos que el cambio se guardó en la lista interna
    assert len(h.lista_cambios) == 1
    # Accedemos a la clave 'operacion' del diccionario guardado
    assert h.lista_cambios[0]['operacion'] == "Filtro aplicado"


def test_ultimo_cambio():
    """Asegura que devuelva el último diccionario de operación registrado."""
    h = Historial()
    h.modificar_historial("Operación A")
    h.modificar_historial("Operación B")
    
    ultimo = h.ultimo_cambio
    # Evaluamos que devuelva el diccionario o el texto según tu método real
    assert ultimo['operacion'] == "Operación B"


def test_str():
    """Verifica la correcta conversión del reporte del historial a texto sin romper índices."""
    cambios_iniciales = [
        {"fecha": "2026-06-17 10:00:00", "operacion": "Carga inicial"},
        {"fecha": "2026-06-17 10:15:00", "operacion": "Filtro Gaussiano"}
    ]
    
    h = Historial(cambios_iniciales)
    texto = str(h)
    
    # Verificamos que el reporte impreso contenga las cabeceras e información estructural
    assert "HISTORIAL CLÍNICO DE LA IMAGEN" in texto
    assert "Carga inicial" in texto
    assert "Filtro Gaussiano" in texto