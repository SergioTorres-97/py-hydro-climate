import pandas as pd
import numpy as np

#Función para promedios mensuales en función de número de datos
def PromediosIDEAM(datos, numDatos, agregado, estadistico):
    columna = datos.columns[0]
    datos = datos.resample(agregado).agg([estadistico, 'count'])
    datos[estadistico] = np.where(datos[columna]['count'] > numDatos, datos[columna][estadistico], np.nan)
    datos = datos[[estadistico]]
    datos.columns = [columna]
    return datos