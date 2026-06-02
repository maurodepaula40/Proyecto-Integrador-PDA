import numpy as np
import matplotlib.pyplot as plt
from bioimagenes.medicas.imagen_radiografia import ImagenRadiografia

RUTA_radio1 = "docs/216840111366964013451228379692012257110540618_02-006-005.png"
RUTA_radio2 = "docs\216840111366964013451228379692012269104148390_01-054-004.png"
RUTA_radio3 = ""
RUTA_radio4 = ""


# # 1. Cargar
radio = ImagenRadiografia(RUTA_radio2, "Tórax", 30)

radio.visualizar()