import pandas as pd
import numpy as np


def agregados_ideam(datos: pd.DataFrame, num_datos_minimo: int,
                               frecuencia: str, estadistico: str = 'mean') -> pd.DataFrame:
    '''
    Calcula estadísticos por período temporal solo si hay suficientes datos válidos.

    Implementa la metodología del IDEAM que requiere un número mínimo de observaciones
    para calcular estadísticos válidos en cada período de agregación.

    Args:
        datos: DataFrame con índice temporal y una columna de valores
        num_datos_minimo: Número mínimo de datos requeridos para calcular el estadístico
        frecuencia: Frecuencia de agregación (ej: 'M' mensual, 'Y' anual, 'D' diario)
        estadistico: Estadístico a calcular: 'mean', 'sum', 'max', 'min', etc. (por defecto 'mean')

    Returns:
        DataFrame con estadísticos calculados (NaN donde no hay suficientes datos)

    Ejemplo:
        >>> # Promedios mensuales solo si hay al menos 25 días de datos
        >>> datos_mensuales = calcular_estadistico_ideam(datos, 25, 'M', 'mean')
        >>>
        >>> # Totales anuales solo si hay al menos 330 días de datos
        >>> datos_anuales = calcular_estadistico_ideam(datos, 330, 'Y', 'sum')
    '''
    # Obtener nombre de la columna original
    nombre_columna = datos.columns[0]

    # Agregar por período calculando el estadístico y el conteo de datos
    datos_agregados = datos.resample(frecuencia).agg([estadistico, 'count'])

    # Solo mantener estadístico si el conteo supera el mínimo requerido
    datos_agregados[estadistico] = np.where(
        datos_agregados[nombre_columna]['count'] > num_datos_minimo,
        datos_agregados[nombre_columna][estadistico],
        np.nan
    )

    # Seleccionar solo la columna del estadístico
    datos_finales = datos_agregados[[estadistico]]
    datos_finales.columns = [nombre_columna]

    return datos_finales

def estadisticos_desc_mensuales(datos):
    datos.columns = ['Valor']
    datos['Mes'] = datos.index.month
    datos['Año'] = datos.index.year

    tabla = pd.pivot(datos, index='Mes', columns='Año', values='Valor')
    est_filaMean, est_filaMed, est_filaMin, est_filaMax, est_filaSum, est_filaQ25, est_fila50, est_fila75 = tabla.mean(), tabla.median(), tabla.min(), tabla.max(),tabla.sum(),tabla.quantile(0.25), tabla.quantile(0.5), tabla.quantile(0.75)

    tabla.loc['Promedio'] = est_filaMean
    tabla.loc['Mediana'] = est_filaMed
    tabla.loc['Mínimo'] = est_filaMin
    tabla.loc['Máxima'] = est_filaMax
    tabla.loc['Suma'] = est_filaSum
    tabla.loc['Q25'] = est_filaQ25
    tabla.loc['Q50'] = est_fila50
    tabla.loc['Q75'] = est_fila75


    est_colMean,est_colMed, est_colMin, est_colMax, est_Q25,est_Q50,estQ75 = tabla.mean(axis = 1),tabla.median(axis = 1), tabla.min(axis = 1), tabla.max(axis = 1),tabla.quantile(0.25,axis = 1),tabla.quantile(0.5,axis = 1),tabla.quantile(0.75,axis = 1)

    tabla['Promedio'] = est_colMean
    tabla['Mediana'] = est_colMed
    tabla['Mínimo'] = est_colMin
    tabla['Máxima'] = est_colMax
    tabla['Q25'] = est_Q25
    tabla['Q50'] = est_Q50
    tabla['Q75'] = estQ75
    tabla = tabla.round(2)

    return tabla
