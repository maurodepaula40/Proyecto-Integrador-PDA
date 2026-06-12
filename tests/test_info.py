from bioimagenes.core.info import Info
from bioimagenes.core.historial import Historial
from bioimagenes.core.imagen import Imagen
from bioimagenes.medicas.imagen_radiografia import ImagenRadiografia


RUTA_IMAGEN_REAL = "tests/imagenes_test/radiografias/216840111366964013200840352202011315131143616_01-032-099.png"


# ==========================================================
# TESTS UNITARIOS - INFO
# ==========================================================

def test_info_por_defecto():
    """
    Verifica que Info se cree correctamente con valores por defecto.
    """

    info = Info()

    assert info["dimensiones"] == (0, 0, 1)
    assert info["brillo"] == 0
    assert info["cortada"] == False
    assert info["tipo_estudio"] == ""
    assert info["tamano_voxel"] == (1.0, 1.0, 1.0)


def test_contiene_clave():
    """
    Verifica que el operador 'in' funcione con claves válidas.
    """

    info = Info()

    assert "brillo" in info
    assert "dimensiones" in info
    assert "tipo_estudio" in info


def test_contiene_clave_invalida():
    """
    Verifica que una clave inexistente no esté en Info.
    """

    info = Info()

    assert "contraste" not in info
    assert "paciente" not in info


def test_contiene_clave_tipo_invalido():
    """
    Debe lanzar TypeError si la clave no es string.
    """

    info = Info()

    try:
        123 in info

        assert False

    except TypeError:
        assert True


def test_getitem():
    """
    Verifica que se pueda acceder a un metadato con corchetes.
    """

    info = Info({"brillo": 120})

    assert info["brillo"] == 120


def test_getitem_clave_invalida():
    """
    Debe lanzar KeyError si se intenta acceder a una clave inexistente.
    """

    info = Info()

    try:
        info["contraste"]

        assert False

    except KeyError:
        assert True


def test_info_con_datos_personalizados():
    """
    Verifica que Info almacene correctamente un diccionario de datos.
    """

    datos = {
        "dimensiones": (100, 200, 3),
        "brillo": 80,
        "cortada": True,
        "tipo_estudio": "radiografia",
        "tamano_voxel": (0.5, 0.5, 1.0)
    }

    info = Info(datos)

    assert info["dimensiones"] == (100, 200, 3)
    assert info["brillo"] == 80
    assert info["cortada"] == True
    assert info["tipo_estudio"] == "radiografia"
    assert info["tamano_voxel"] == (0.5, 0.5, 1.0)


def test_info_datos_no_diccionario():
    """
    Debe lanzar TypeError si datos no es un diccionario.
    """

    try:
        Info(datos="no soy un diccionario")

        assert False

    except TypeError:
        assert True


def test_cantidad_voxel():
    """
    Verifica el cálculo de cantidad total de voxels.
    """

    info = Info({"dimensiones": (100, 200, 3)})

    assert info.cantidad_voxel() == 60000


def test_cantidad_voxel_dimension_invalida():
    """
    Debe lanzar ValueError si dimensiones no tiene 3 valores.
    """

    info = Info({"dimensiones": (100, 200)})

    try:
        info.cantidad_voxel()

        assert False

    except ValueError:
        assert True


def test_tamano_voxel():
    """
    Verifica que se pueda obtener el tamaño de voxel.
    """

    info = Info({"tamano_voxel": (0.5, 0.5, 1.0)})

    assert info.tamano_voxel() == (0.5, 0.5, 1.0)


def test_historial_asociado():
    """
    Verifica que Info pueda recibir un Historial externo.
    """

    h = Historial(["Cambio 1"])

    info = Info(historial=h)

    assert len(info.historial) == 1
    assert info.historial.ultimo_cambio == "Cambio 1"


def test_historial_tipo_invalido():
    """
    Debe lanzar TypeError si historial no es una instancia de Historial.
    """

    try:
        Info(historial="no soy historial")

        assert False

    except TypeError:
        assert True


def test_modificar_datos_info():
    """
    Verifica que se puedan modificar los datos internos de Info.
    """

    info = Info()

    info.datos["brillo"] = 150
    info.datos["tipo_estudio"] = "torax"
    info.datos["cortada"] = True

    assert info["brillo"] == 150
    assert info["tipo_estudio"] == "torax"
    assert info["cortada"] == True


# ==========================================================
# TESTS CON IMAGEN REAL
# ==========================================================

def test_crear_info_desde_imagen_real():
    """
    Verifica que se pueda crear Info usando las dimensiones
    de una imagen real cargada.
    """

    imagen = Imagen.cargar(RUTA_IMAGEN_REAL)

    dimensiones = imagen.data.shape

    info = Info({
        "dimensiones": dimensiones,
        "brillo": 0,
        "cortada": False,
        "tipo_estudio": "imagen real"
    })

    assert info["dimensiones"] == dimensiones
    assert info["brillo"] == 0
    assert info["cortada"] == False
    assert info["tipo_estudio"] == "imagen real"


def test_info_con_radiografia_real():
    """
    Verifica que una ImagenRadiografia real almacene correctamente
    los metadatos en Info.
    """

    imagen = Imagen.cargar(RUTA_IMAGEN_REAL)

    rx = ImagenRadiografia(
        imagen.data,
        tipo_estudio="radiografia orginal",
        brillo=20
    )

    assert rx.info["tipo_estudio"] == "radiografia original"
    assert rx.info["brillo"] == 20
    assert rx.data.ndim == 2


def test_info_dimensiones_radiografia_real():
    """
    Verifica que se puedan guardar las dimensiones reales
    de una radiografía en Info.
    """

    imagen = Imagen.cargar(RUTA_IMAGEN_REAL)

    rx = ImagenRadiografia(
        imagen.data,
        tipo_estudio="radiografia original",
        brillo=0
    )

    alto, ancho = rx.data.shape

    rx.info.datos["dimensiones"] = (ancho, alto, 1)

    assert rx.info["dimensiones"] == (ancho, alto, 1)
    assert rx.info.cantidad_voxel() == ancho * alto * 1


def test_info_historial_con_imagen_real():
    """
    Verifica que los cambios realizados sobre una radiografía real
    se registren en el historial de Info.
    """

    imagen = Imagen.cargar(RUTA_IMAGEN_REAL)

    rx = ImagenRadiografia(
        imagen.data,
        tipo_estudio="radiografia original",
        brillo=0
    )

    cantidad_inicial = len(rx.info.historial)

    rx.mejorar_contraste(1.5)

    assert len(rx.info.historial) == cantidad_inicial + 1


def test_info_brillo_con_imagen_real():
    """
    Verifica que al ajustar el brillo de una radiografía real,
    el valor quede registrado en Info.
    """

    imagen = Imagen.cargar(RUTA_IMAGEN_REAL)

    rx = ImagenRadiografia(
        imagen.data,
        tipo_estudio="radiografia original",
        brillo=0
    )

    rx.ajustar_brillo(50)

    assert rx.info["brillo"] == 50


# ==========================================================
# EJECUCIÓN MANUAL
# ==========================================================

if __name__ == "__main__":

    tests = [
        test_info_por_defecto,
        test_contiene_clave,
        test_contiene_clave_invalida,
        test_contiene_clave_tipo_invalido,
        test_getitem,
        test_getitem_clave_invalida,
        test_info_con_datos_personalizados,
        test_info_datos_no_diccionario,
        test_cantidad_voxel,
        test_cantidad_voxel_dimension_invalida,
        test_tamano_voxel,
        test_historial_asociado,
        test_historial_tipo_invalido,
        test_modificar_datos_info,
    ]

    tests_reales = [
        test_crear_info_desde_imagen_real,
        test_info_con_radiografia_real,
        test_info_dimensiones_radiografia_real,
        test_info_historial_con_imagen_real,
        test_info_brillo_con_imagen_real,
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

    print(f"\nResultado tests unitarios: {aprobados}/{len(tests)} tests aprobados")

    print("\n=== EJECUCIÓN DE TESTS DE INFO CON IMAGEN REAL ===\n")
    print("Recordá cambiar RUTA_IMAGEN_REAL antes de ejecutar estos tests.\n")

    aprobados_reales = 0

    for test in tests_reales:

        try:
            test()

            print(f"✓ {test.__name__}")

            aprobados_reales += 1

        except AssertionError:

            print(f"✗ {test.__name__}")

        except Exception as e:

            print(f"✗ {test.__name__} -> ERROR: {e}")

    print(f"\nResultado tests reales: {aprobados_reales}/{len(tests_reales)} tests aprobados")


# ==========================================================
# PRUEBA MANUAL CON IMAGEN REAL
# ==========================================================

# Para usar esta sección:
# 1. Cambiar RUTA_IMAGEN_REAL por la ruta real de la imagen.
# 2. Descomentar las líneas.
# 3. Ejecutar el archivo.

imagen = Imagen.cargar(RUTA_IMAGEN_REAL)

rx = ImagenRadiografia(
    imagen.data,
    tipo_estudio="radiografia original",
    brillo=0)

print("\nMetadatos iniciales:")
print(rx.info.datos)

rx.info.datos["dimensiones"] = (rx.data.shape[1], rx.data.shape[0], 1)

print("\nMetadatos actualizados:")
print(rx.info.datos)

rx.ajustar_brillo(40)

print("\nMetadatos luego de ajustar brillo:")
print(rx.info.datos)

print("\nHistorial de Info:")
for cambio in rx.info.historial:
    print(cambio)

rx.visualizar()