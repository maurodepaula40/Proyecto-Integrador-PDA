import numpy as np
import matplotlib.pyplot as plt
from bioimagenes.medicas.imagen_tomografia import ImagenTomografica
import os
import pytest

RUTA_TOMOGRAFIA = "tests/imagenes_test/AC421363f.nii"

# ==========================================================
# TESTS UNITARIOS (arrays creados manualmente)
# ==========================================================

def test_creacion_imagen_tomografica():
    """
    Verifica que la imagen tomográfica se cree correctamente.
    """

    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    assert img.corte_actual == 0
    assert isinstance(img.ventana_actual, tuple)


def test_obtener_corte():
    """
    Verifica que se pueda obtener un corte válido.
    """

    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    corte = img.obtener_corte(2)

    assert corte.shape == (20, 20)


def test_obtener_corte_fuera_de_rango():
    """
    Debe lanzar IndexError cuando el corte no existe.
    """

    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    try:
        img.obtener_corte(100)

        assert False

    except IndexError:
        assert True


def test_seleccionar_corte():
    """
    Verifica que el atributo corte_actual se actualice.
    """

    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    img.seleccionar_corte(3)

    assert img.corte_actual == 3


def test_historial_seleccionar_corte():
    """
    Verifica que seleccionar un corte agregue un registro al historial.
    """

    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    cantidad_inicial = len(img.info.historial)

    img.seleccionar_corte(1)

    assert len(img.info.historial) == cantidad_inicial + 1


def test_ajustar_ventana():
    """
    Verifica que la ventana cambie correctamente.
    """

    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    img.ajustar_ventana(-100, 200)

    assert img.ventana_actual == (-100, 200)


def test_ajustar_ventana_invalida():
    """
    Debe lanzar ValueError si mínimo >= máximo.
    """

    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    try:
        img.ajustar_ventana(100, 100)

        assert False

    except ValueError:
        assert True


def test_aplicar_preset():
    """
    Verifica que el preset cerebro configure la ventana esperada.
    """

    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    img.aplicar_preset("cerebro")

    assert img.ventana_actual == (0.0, 80.0)


def test_aplicar_preset_invalido():
    """
    Debe lanzar ValueError para un tejido inexistente.
    """

    data = np.random.randint(-1000, 1000, (20, 20, 5))

    img = ImagenTomografica(data)

    try:
        img.aplicar_preset("corazon")

        assert False

    except ValueError:
        assert True


def test_visualizar_corte_coloreado():
    """
    Verifica que visualizar_corte retorne una imagen RGB.
    """

    data = np.array([
        [[-1000], [-700]],
        [[50], [500]]
    ])

    img = ImagenTomografica(data)

    resultado = img.visualizar_corte()

    assert resultado.shape == (2, 2, 3)

# ==========================================================
# TESTS CON TOMOGRAFÍA REAL
# ==========================================================

def verificar_imagen_real():
    """
    Omite los tests que requieren una tomografía real si el archivo
    no se encuentra en la ruta esperada.
    """
    if not os.path.exists(RUTA_TOMOGRAFIA):   #si no se encuentra la imagen, se omiten (skip) los tests que requieren una imagen real
        pytest.skip(
            "No se encontró la imagen AC421363f.nii en tests/imagenes_test/. "
            "Este test se omite porque requiere una imagen tomográfica real."
        )


def test_cargar_tomografia_real():
    """
    Verifica que pueda cargarse una tomografía .nii real.
    """
    verificar_imagen_real()

    img = ImagenTomografica.cargar(RUTA_TOMOGRAFIA)

    assert img.data is not None
    assert img.data.ndim == 3


def test_dimensiones_tomografia_real():
    """
    Verifica que las dimensiones del volumen sean válidas.
    """
    verificar_imagen_real()

    img = ImagenTomografica.cargar(RUTA_TOMOGRAFIA)

    filas, columnas, cortes = img.data.shape

    assert filas > 0
    assert columnas > 0
    assert cortes > 0


def test_obtener_corte_central():
    """
    Verifica que pueda obtenerse el corte central.
    """
    verificar_imagen_real()

    img = ImagenTomografica.cargar(RUTA_TOMOGRAFIA)

    indice = img.data.shape[2] // 2

    corte = img.obtener_corte(indice)

    assert corte.ndim == 2


def test_seleccionar_corte_central():
    """
    Verifica la selección del corte central.
    """
    verificar_imagen_real()

    img = ImagenTomografica.cargar(RUTA_TOMOGRAFIA)

    indice = img.data.shape[2] // 2

    img.seleccionar_corte(indice)

    assert img.corte_actual == indice


def test_valores_hounsfield():
    """
    Verifica que existan valores mínimos y máximos distintos.
    """
    verificar_imagen_real()

    img = ImagenTomografica.cargar(RUTA_TOMOGRAFIA)

    minimo = img.data.min()
    maximo = img.data.max()

    assert minimo < maximo


def test_aplicar_preset_sobre_tomografia_real():
    """
    Verifica el funcionamiento del preset hueso sobre una imagen real.
    """
    verificar_imagen_real()

    img = ImagenTomografica.cargar(RUTA_TOMOGRAFIA)

    img.aplicar_preset("hueso")

    assert img.ventana_actual == (-500.0, 1300.0)


# ==========================================================
# EJECUCIÓN MANUAL
# ==========================================================

if __name__ == "__main__":
    print("\n=== PRUEBA VISUAL DE IMAGEN TOMOGRÁFICA ===\n")

    if not os.path.exists(RUTA_TOMOGRAFIA):
        print("No se encontró la imagen tomográfica real.")
        print(f"Ruta esperada: {RUTA_TOMOGRAFIA}")
        print(
            "Para ejecutar esta prueba visual, colocá el archivo "
            "'AC421363f.nii' dentro de la carpeta 'tests/imagenes_test/'."
        )

    else:
        tomo = ImagenTomografica.cargar(RUTA_TOMOGRAFIA)

        tomo.seleccionar_corte(320)
        tomo.mostrar_corte()

        tomo.visualizar_corte()

        tomo.aplicar_preset("hueso")
        tomo.mostrar_corte()

        print(tomo.info.historial)

        tomo.reconstruir_3d(200, 300)