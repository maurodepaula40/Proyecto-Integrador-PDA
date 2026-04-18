from bioimagenes.core.historial import Historial

def test_basico():
    h = Historial()   #creo historial vacío
    assert len(h) == 0  #verifico que no tenga nada, assert sirve para hacer el test
                        # si pasa el test dice passed, si no falla

def test_agregar_un_cambio():
    h = Historial()  #creo historial vacío
    h.modificar_historial("Filtro aplicado")  #Agrego un cambio al Historial

    assert len(h) == 1
    assert h.ultimo_cambio == "Filtro aplicado" #Verificación del utlimo cambio cuando hay 1 solo

def test_ultimo_cambio():
    h = Historial()

    h.modificar_historial("A")   #Agrego cosas al historial
    h.modificar_historial("B")
    h.modificar_historial("C")

    assert h.ultimo_cambio == "C"   #verifico si el ultimo cambio es en realidad C, si no falla el test

def test_str():
    h = Historial(["A", "B"])     # Creo un historial con dos cambios iniciales

    texto = str(h)     # Convierto el objeto a string usando __str__

    assert "Total de cambios: 2" in texto  # Verifico que aparezca la cantidad correcta de cambios
    assert "Último cambio: B" in texto   # Verifico que el último cambio sea el correcto
