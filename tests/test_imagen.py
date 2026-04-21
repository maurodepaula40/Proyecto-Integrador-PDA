from src.bioimagenes.core.imagen import Imagen
import numpy as np
import matplotlib.pyplot as plt

#Prueba con imagen en escala de grises

#datovich = np.random.randint(0, 255, (100, 100)) 
#img = Imagen(data=datovich, info=None)
#img.visualizar()

#prueba con imagen RGB

#datovich = np.random.randint(0, 255, (100, 100,3)) 
#img = Imagen(data=datovich, info=None)
#img.visualizar()

#Prueba de tipo de dato
#data = [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]]

#image = Imagen(data=data, info=None)

#PRUEBA DE TIPO DE DIMENSIONES

data = np.random.randint(0,255,(100,100,5))
dimensiones = Imagen(data=data, info=None)
dimensiones.visualizar()
