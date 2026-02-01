# Funciones para realizar la importación de datos
import pandas as pd
import numpy as np
import xarray as xr
from datetime import datetime
from typing import Tuple


def abrir_archivo_aqts_web(ruta_archivo: str, sep: str = ',') -> pd.DataFrame:
    '''
    Abre y procesa archivos CSV descargados desde AQTS Web.

    Args:
        ruta_archivo: Ruta completa del archivo CSV
        sep: Separador del archivo CSV (por defecto coma)

    Returns:
        DataFrame con índice de fechas y columna 'Valor'
    '''
    # Leer archivo y seleccionar columnas relevantes
    data = pd.read_csv(ruta_archivo, sep = sep, header = 0)[['Fecha', 'Valor']]

    # Convertir valores: reemplazar comas por puntos y convertir a float
    data['Valor'] = data['Valor'].astype(str).str.replace(',', '.', regex=False).astype(float)

    # Establecer índice de fechas
    data.set_index('Fecha', inplace=True)
    data.index = pd.to_datetime(data.index)

    return data

def abrir_archivos_aqts(ruta_archivo: str, sep: str = ',') -> pd.DataFrame:
    '''
    Abre y procesa archivos CSV exportados desde AQTS.

    Args:
        ruta_archivo: Ruta completa del archivo CSV
        sep: Separador del archivo CSV (por defecto coma)

    Returns:
        DataFrame con índice de fechas y columna 'Valor'
    '''
    # Leer archivo omitiendo las primeras 14 líneas de encabezado
    datos = pd.read_csv(ruta_archivo, header=14, sep = sep)[['Timestamp (UTC-05:00)', 'Value']]
    datos.columns = ['Fecha', 'Valor']

    # Establecer índice de fechas
    datos.set_index('Fecha', inplace=True)
    datos.index = pd.to_datetime(datos.index)

    return datos

def abrir_archivos_nasa(ruta_archivo: str, sep: str = ',', formato_fechas: list = None) -> pd.DataFrame:
    '''
    Abre y procesa archivos de datos de NASA POWER DATA con formato de año juliano.

    Args:
        ruta_archivo: Ruta completa del archivo CSV
        formato_fechas: Lista con nombres de columnas [año, día_juliano]

    Returns:
        DataFrame con índice de fechas y variables climáticas
    '''
    if formato_fechas is None:
        formato_fechas = ['YEAR', 'DOY']

    def _fecha_desde_anio_y_dia(anio: int, dia_del_anio: int) -> datetime.date:
        '''Convierte año y día juliano a fecha'''
        return datetime.strptime(f'{anio} {dia_del_anio}', '%Y %j').date()

    # Determinar número de líneas de encabezado
    header = pd.read_csv(ruta_archivo, on_bad_lines='skip').values.shape[0] + 1
    datos = pd.read_csv(ruta_archivo, header=header, sep = sep)

    # Crear columna de fechas a partir de año y día juliano
    datos['Fecha'] = datos.apply(
        lambda row: _fecha_desde_anio_y_dia(int(row[formato_fechas[0]]), int(row[formato_fechas[1]])),
        axis=1
    )
    datos.set_index('Fecha', inplace=True)

    # Reemplazar valores faltantes (-999 es el código de NASA para datos faltantes)
    datos = datos.replace(-999, np.nan)

    # Convertir índice a datetime
    datos.index = pd.to_datetime(datos.index)

    # Eliminar columnas de año y día juliano (ya no son necesarias)
    datos = datos.drop(columns=formato_fechas)

    return datos

def abrir_archivos_giovanni(ruta_archivo: str, sep: str = ',') -> pd.DataFrame:
    """
    Abre y procesa archivos CSV del sistema Giovanni.

    Args:
        ruta_archivo: Ruta completa del archivo CSV a procesar

    Returns:
        DataFrame con índice de fechas y valores procesados
    """
    # Leer archivo CSV omitiendo las primeras 8 líneas de metadata/encabezado
    # que son características de los archivos exportados de Giovanni
    datos = pd.read_csv(ruta_archivo, header=8, sep = sep)

    # Renombrar columnas para tener nombres descriptivos y consistentes
    datos.columns = ['Fecha', 'Valor']

    # Convertir la columna 'Fecha' en el índice del DataFrame
    datos.set_index('Fecha', inplace=True)

    # Convertir el índice de tipo string a objetos datetime para
    datos.index = pd.to_datetime(datos.index)

    # Reemplazar el valor centinela -9999 (dato faltante) con NaN
    datos = datos.replace(-9999, np.nan)

    return datos

def abrir_archivos_automaticas(ruta_archivo: str, sep: str = ',') -> pd.DataFrame:
    """
    Abre y procesa archivos CSV de estaciones automáticas.

    Args:
        ruta_archivo: Ruta completa del archivo CSV a procesar
        sep: Separador de columnas (por defecto coma ',')

    Returns:
        DataFrame con índice de fechas y valores procesados
    """
    # Leer archivo CSV desde la primera línea (header=0)
    datos = pd.read_csv(ruta_archivo, header=0, sep=sep)

    # Renombrar columnas para tener nombres descriptivos y consistentes
    datos.columns = ['Fecha', 'Valor']

    # Convertir la columna 'Fecha' en el índice del DataFrame
    datos.set_index('Fecha', inplace=True)

    # Convertir el índice de tipo string a objetos datetime para
    datos.index = pd.to_datetime(datos.index)

    return datos

def extraccion_cubo_datos(ruta: str, variable: str, coordenadas: Tuple[float, float]) -> pd.DataFrame:
    '''
    Extrae series temporales de archivos NetCDF para una coordenada específica.

    Args:
        ruta: Directorio donde se encuentran los archivos NetCDF
        variable: Nombre de la variable a extraer
        coordenadas: Tupla (latitud, longitud) del punto a extraer

    Returns:
        DataFrame con serie temporal completa 1991-2020
    '''
    dataframes = []

    # Procesar datos en bloques de 10 años (1991-2000, 2001-2010, 2011-2020)
    for decada in range(3):
        # Calcular fechas del período
        anio_inicio = 1991 + (decada * 10)
        anio_fin = 2000 + (decada * 10)
        fecha_inicial = f'{anio_inicio}-01-01'
        fecha_final = f'{anio_fin}-12-31'

        # Abrir archivo NetCDF correspondiente
        archivo_nc = f'{ruta}/{variable}_dia_{anio_inicio}_{anio_fin}.nc'
        data = xr.open_dataset(archivo_nc)

        # Extraer variable para la coordenada más cercana
        nombre_variable = list(data.data_vars)[0]
        data_coordenada = data[nombre_variable].sel(
            lat=coordenadas[0],
            lon=coordenadas[1],
            method='nearest'
        ).sel(time=slice(fecha_inicial, fecha_final)).values

        # Crear DataFrame para este período
        rango_fechas = pd.date_range(start=fecha_inicial, end=fecha_final)
        df_periodo = pd.DataFrame(data_coordenada, index=rango_fechas, columns=['Valor'])
        dataframes.append(df_periodo)

    # Concatenar todos los períodos
    df_completo = pd.concat(dataframes)
    df_completo.index.name = 'Fecha'

    return df_completo

def abrir_archivos_dhime(ruta: str, sep: str = ',') -> pd.DataFrame:
    """
    Abre y procesa archivos CSV del sistema DHIME.

    Args:
        ruta: Ruta completa del archivo CSV a procesar
        sep: Separador de columnas (por defecto coma ',')

    Returns:
        DataFrame con índice de fechas y valores procesados
    """
    # Leer archivo CSV
    datos = pd.read_csv(ruta, header=0, sep=sep)[['Fecha','Valor']]

    # Renombrar columnas para tener nombres descriptivos y consistentes
    datos.columns = ['Fecha', 'Valor']

    # Convertir la columna 'Fecha' en el índice del DataFrame
    datos.set_index('Fecha', inplace=True)

    # Convertir el índice de tipo string a objetos datetime para
    datos.index = pd.to_datetime(datos.index, format = 'mixed')

    return datos