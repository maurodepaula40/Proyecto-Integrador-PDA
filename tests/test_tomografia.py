import numpy as np

from bioimagenes.medicas.imagen_tomografia import ImagenTomografica


def test_creacion_imagen_tomografica():
    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    assert img.corte_actual == 0
    assert isinstance(img.ventana_actual, tuple)


def test_obtener_corte():
    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    corte = img.obtener_corte(2)

    assert corte.shape == (20, 20)


def test_seleccionar_corte():
    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    img.seleccionar_corte(3)

    assert img.corte_actual == 3


def test_ajustar_ventana():
    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    img.ajustar_ventana(-100, 200)

    assert img.ventana_actual == (-100, 200)


def test_aplicar_preset():
    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    img.aplicar_preset("cerebro")

    assert img.ventana_actual == (0.0, 80.0)


def test_visualizar_corte():
    data = np.array([
        [[-1000], [-700]],
        [[50], [500]]
    ])

    img = ImagenTomografica(data)

    resultado = img.visualizar_corte()

    assert resultado.shape == (2, 2, 3)


def test_historial_seleccionar_corte():
    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    cantidad_inicial = len(img.info.historial)

    img.seleccionar_corte(1)

    assert len(img.info.historial) == cantidad_inicial + 1


def test_historial_ajustar_ventana():
    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    cantidad_inicial = len(img.info.historial)

    img.ajustar_ventana(-200, 200)

    assert len(img.info.historial) == cantidad_inicial + 1


def test_obtener_corte_fuera_de_rango():
    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    try:
        img.obtener_corte(100)
        assert False
    except IndexError:
        assert True


def test_aplicar_preset_invalido():
    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    try:
        img.aplicar_preset("corazon")
        assert False
    except ValueError:
        assert True


if __name__ == "__main__":

    tests = [
        test_creacion_imagen_tomografica,
        test_obtener_corte,
        test_seleccionar_corte,
        test_ajustar_ventana,
        test_aplicar_preset,
        test_visualizar_corte,
        test_historial_seleccionar_corte,
        test_historial_ajustar_ventana,
        test_obtener_corte_fuera_de_rango,
        test_aplicar_preset_invalido,
    ]

    print("\n=== EJECUCIÓN DE TESTS DE IMAGEN TOMOGRÁFICA ===\n")

    aprobados = 0

    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            aprobados += 1

        except AssertionError:
            print(f"✗ {test.__name__}")

        except Exception as e:
            print(f"✗ {test.__name__} -> ERROR: {e}")

    print(f"\nResultado: {aprobados}/{len(tests)} tests aprobados")