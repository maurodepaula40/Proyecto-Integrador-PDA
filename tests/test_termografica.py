from bioimagenes.medicas.imagen_termografica import ImagenTermografica

ruta = "tests/imagenes_test/termografias/N11104.jpg"

termografia = ImagenTermografica.cargar(ruta=ruta)
termografia.convertir_a_temperatura(32,40)
termografia.visualizar()
