import pytest
from bioimagenes.core.info import Info
from bioimagenes.core.historial import Historial

# ==========================================================
# FIXTURES (Estructuras base para reutilizar en los tests)
# ==========================================================

@pytest.fixture
def datos_validos_2d():
    """Genera un diccionario válido de metadatos para una imagen 2D."""
    return {
        "dimensiones": (512, 512),
        "brillo": 120,
        "cortada": False,
        "tipo_estudio": "Radiografía de Tórax"
    }

@pytest.fixture
def datos_validos_3d():
    """Genera un diccionario válido de metadatos para un volumen 3D."""
    return {
        "dimensiones": (256, 256, 40), # ancho, alto, canales/cortes
        "brillo": 85,
        "cortada": True,
        "tipo_estudio": "Tomografía Computada",
        "tamano_voxel": (0.5, 0.5, 1.2)
    }

@pytest.fixture
def historial_valido():
    """Instancia real de Historial para las pruebas de asociación."""
    return Historial()


# ==========================================================
# 1. TESTS DEL CONSTRUCTOR Y VALORES POR DEFECTO
# ==========================================================

def test_inicializacion_por_defecto():
    """Verifica que si no se pasan parámetros, se apliquen los valores por defecto establecidos."""
    info = Info()
    
    # Comprobación de diccionario base e historial automático
    assert isinstance(info.historial, Historial)
    assert info.datos["dimensiones"] == (0, 0, 1)
    assert info.datos["brillo"] == 0
    assert info.datos["cortada"] is False
    assert info.datos["tipo_estudio"] == ""
    assert info.datos["tamano_voxel"] == (1.0, 1.0, 1.0)


def test_inicializacion_con_datos_y_historial(datos_validos_2d, historial_valido):
    """Prueba la construcción correcta inyectando datos y un historial propio."""
    info = Info(datos=datos_validos_2d, historial=historial_valido)
    
    assert info.historial == historial_valido
    assert info.datos["dimensiones"] == (512, 512)
    assert info.datos["brillo"] == 120
    assert info.datos["tipo_estudio"] == "Radiografía de Tórax"


def test_inicializacion_forzar_brillo_entero():
    """Asegura el cumplimiento de la recomendación docente: castear brillo float a int."""
    datos = {"brillo": 145.75}
    info = Info(datos=datos)
    assert isinstance(info.datos["brillo"], int)
    assert info.datos["brillo"] == 145


# ==========================================================
# 2. TESTS DE VALIDACIÓN DE TIPOS (ERRORES EN CONSTRUCTOR)
# ==========================================================

def test_error_constructor_datos_no_es_dict():
    """Valida que lance TypeError si 'datos' no es un diccionario."""
    with pytest.raises(TypeError, match="'datos' debe ser un diccionario"):
        Info(datos=["lista", "invalida"])


def test_error_constructor_historial_no_valido(datos_validos_2d):
    """Valida que lance TypeError si 'historial' no es una instancia de la clase Historial."""
    with pytest.raises(TypeError, match="'historial' debe ser una instancia de Historial"):
        Info(datos=datos_validos_2d, historial="HistorialFalsoEnString")


# ==========================================================
# 3. TESTS DE MÉTODOS MÁGICOS (__contains__ y __getitem__)
# ==========================================================

def test_metodo_contains_clave_existente(datos_validos_2d):
    """Prueba el operador 'in' para verificar la existencia de metadatos válidos."""
    info = Info(datos=datos_validos_2d)
    assert "brillo" in info
    assert "tipo_estudio" in info
    assert "dimensiones" in info


def test_metodo_contains_clave_inexistente():
    """Comprueba que 'in' devuelva False si la propiedad no existe en el diccionario interno."""
    info = Info()
    assert "nombre_paciente" not in info


def test_metodo_contains_error_tipo():
    """Asegura que lance un TypeError si se busca una clave que no sea un string."""
    info = Info()
    with pytest.raises(TypeError, match="La clave debe ser un string"):
        _ = 123 in info


def test_metodo_getitem_acceso_exitoso(datos_validos_2d):
    """Verifica el acceso indexado tradicional por corchetes info['clave']."""
    info = Info(datos=datos_validos_2d)
    assert info["brillo"] == 120
    assert info["tipo_estudio"] == "Radiografía de Tórax"


def test_metodo_getitem_error_clave_inexistente():
    """Valida que intenter leer una clave inválida dispare un KeyError protegido."""
    info = Info()
    with pytest.raises(KeyError, match="no es un metadato válido de Info"):
        _ = info["contraste_invalido"]


# ==========================================================
# 4. TESTS DE LÓGICA DE VÓXELS (MÉTODOS ESPECÍFICOS 3D)
# ==========================================================

def test_cantidad_voxel_exitoso_3d(datos_validos_3d):
    """Comprueba el cálculo matemático correcto del volumen en voxels (ancho * alto * canales)."""
    info = Info(datos=datos_validos_3d)
    # 256 * 256 * 40 = 2621440
    assert info.cantidad_voxel() == 2621440


def test_cantidad_voxel_error_en_imagen_2d(datos_validos_2d):
    """Valida que lance ValueError si se pide calcular voxels en un estudio puramente 2D."""
    info = Info(datos=datos_validos_2d)
    with pytest.raises(ValueError, match="requiere dimensiones 3D"):
        info.cantidad_voxel()


def test_tamano_voxel_retorno(datos_validos_3d):
    """Verifica que devuelva correctamente la tupla física de tamaño en milímetros."""
    info = Info(datos=datos_validos_3d)
    assert info.tamano_voxel() == (0.5, 0.5, 1.2)