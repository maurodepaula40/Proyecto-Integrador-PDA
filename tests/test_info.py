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
    info = Info({"brillo": 120})

    assert info["brillo"] == 120

def test_cantidad_voxel():
    info = Info({"dimensiones": (100, 200, 3)})

    assert info.cantidad_voxel() == 60000

def test_tamano_voxel():
    info = Info({"tamano_voxel": (0.5, 0.5, 1.0)})

    assert info.tamano_voxel() == (0.5, 0.5, 1.0)

def test_historial_asociado():
    h = Historial(["Cambio 1"])
    info = Info(historial=h)

    assert len(info.historial) == 1
    assert info.historial.ultimo_cambio == "Cambio 1"


if __name__ == "__main__":
    tests = [
        test_info_por_defecto,
        test_contiene_clave,
        test_getitem,
        test_cantidad_voxel,
        test_tamano_voxel,
        test_historial_asociado,
    ]

    print("\n=== EJECUCIÓN DE TESTS DE INFO ===\n")

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