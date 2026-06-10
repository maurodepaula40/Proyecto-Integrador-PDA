from bioimagenes.medicas.imagen_termografica import ImagenTermografica
from bioimagenes.medicas.imagen_radiografia import ImagenRadiografica

ruta = "tests/imagenes_test/termografias/N11104.jpg"

ruta2 = "tests/imagenes_test/radiografias/216840111366964013829543166512013358092118761_02-089-145.png"

termografia = ImagenTermografica.cargar(ruta=ruta)
termografia.convertir_a_temperatura(32,40)
termografia.mapa_calor()
termografia.visualizar()
print(termografia.historial)

radiografia = ImagenRadiografica.cargar(ruta2)
radiografia.visualizar()
radiografia.detectar_bordes()
radiografia.visualizar()
print(radiografia.historial)

