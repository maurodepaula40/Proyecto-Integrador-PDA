from bioimagenes.core.historial import Historial


def test_basico():
    h = Historial()
    assert len(h) == 0

def test_agregar_un_cambio():
    h = Historial()
    h.modificar_historial("Filtro aplicado")

    assert len(h) == 1
    assert h.ultimo_cambio == "Filtro aplicado" #Verificación del utlimo cambio cuando hay 1 solo

def test_ultimo_cambio():
    h = Historial()

    h.modificar_historial("A")
    h.modificar_historial("B")
    h.modificar_historial("C")

    assert h.ultimo_cambio == "C"   #verifica si el ultimo cambio es en realidad C, si no falla el test

    def test_str():
        h = Historial(["A", "B"])

        texto = str(h)

        assert "Total de cambios: 2" in texto
        assert "Último cambio: B" in texto