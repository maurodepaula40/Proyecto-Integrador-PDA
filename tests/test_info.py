from bioimagenes.core.info import Info
from bioimagenes.core.historial import Historial

def test_info_por_defecto():
    info = Info()

    assert info["dimensiones"] == (0, 0, 1)
    assert info["brillo"] == 0
    assert info["cortada"] == False
    assert info["tipo_estudio"] == ""
    assert info["tamano_voxel"] == (1.0, 1.0, 1.0)

def test_contiene_clave():
    info = Info()

    assert "brillo" in info
    assert "dimensiones" in info

def test_getitem():
    datos = {"brillo": 120}

    info = Info(datos)

    assert info["brillo"] == 120

def test_cantidad_voxel():
    datos = {"dimensiones": (100, 200, 3)}

    info = Info(datos)

    assert info.cantidad_voxel() == 60000

def test_tamano_voxel():
    datos = {
        "tamano_voxel": (0.5, 0.5, 1.0)
    }

    info = Info(datos)

    assert info.tamano_voxel() == (0.5, 0.5, 1.0)

def test_historial_asociado():
    h = Historial(["Cambio 1"])

    info = Info(historial=h)

    assert len(info.historial) == 1
    assert info.historial.ultimo_cambio == "Cambio 1"

import pytest
from bioimagenes.core.info import Info

def test_error_datos_no_diccionario():
    with pytest.raises(TypeError):
        Info(datos=123)

def test_error_historial_invalido():
    with pytest.raises(TypeError):
        Info(historial="hola")

def test_error_clave_inexistente():
    info = Info()

    with pytest.raises(KeyError):
        info["inexistente"]

def test_error_cantidad_voxel_2d():
    info = Info({"dimensiones": (100, 200)})

    with pytest.raises(ValueError):
        info.cantidad_voxel()