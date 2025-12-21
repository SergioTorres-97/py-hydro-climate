#Funciones para realizar la importación de datos
import pandas as pd
import numpy as np
import xarray as xr
from datetime import datetime
from typing import Tuple

def AbrirArchivoAqtsWeb(ruta_folder: str, sep = ',') -> pd.DataFrame:
    data = pd.read_csv(ruta_folder)[['Sello de tiempo (UTC-05:00)','Valor (Millimetres)']]
    data.columns = ['Fecha','Valor']
    data['Valor'] = data['Valor'].astype(str).str.replace(",", ".", regex=False)
    data['Valor'] = data['Valor'].astype(float)
    data.set_index('Fecha',inplace = True)
    return data

def AbrirArchivosAQTS(rutaArchivo: str, sep = ',') -> pd.DataFrame:
    datos = pd.read_csv(rutaArchivo, header=14)[['Timestamp (UTC-05:00)', 'Value']]
    datos.columns = ['Fecha', 'Valor']
    datos.set_index('Fecha', inplace=True)
    return datos

def AbrirArchivosNASA(rutaArchivo, formatoFechas = ['YEAR','DOY']):
    def fecha_desde_anio_y_dia(anio, dia_del_anio):
      return datetime.strptime(f"{anio} {dia_del_anio}", "%Y %j").date()

    header = pd.read_csv(rutaArchivo, on_bad_lines='skip').values.shape[0] + 1
    datos = pd.read_csv(rutaArchivo,header = header)
    fecha = []
    for i in range(0, datos.shape[0]):
        fec = fecha_desde_anio_y_dia(datos[formatoFechas[0]].values[i], int(datos[formatoFechas[1]].values[i]))
        fecha.append(fec)

    datos['Fecha'] = fecha
    datos.set_index('Fecha', inplace=True)

    datos = datos.replace(-999, np.nan)

    datos.index = pd.to_datetime(datos.index)

    columnas = list(datos.columns)
    columnas.remove(formatoFechas[0])
    columnas.remove(formatoFechas[1])
    datos = datos[columnas]
    return datos

def ExtraccionCuboDatos(ruta: str, variable: str, coordenadas: Tuple[float, float]) -> pd.DataFrame:

    for iter in range(0, 3):
        if iter == 0:
            fecha_inicial, fecha_final = '1991-01-01', '2000-12-31'
        else:
            fecha_inicial = f'{int(fecha_inicial[0:4]) + 10}-01-01'
            fecha_final = f'{int(fecha_final[0:4]) + 10}-12-31'

        # Abrir el archivo de datos
        data = xr.open_dataset(f'{ruta}/{variable}_dia_{fecha_inicial[0:4]}_{int(fecha_final[0:4])}.nc')

        # Extraer la variable principal y seleccionar la coordenada más cercana
        data_coor = data[list(data.data_vars)[0]].sel(
            lat=coordenadas[0], lon=coordenadas[1], method='nearest'
        ).sel(time=slice(fecha_inicial, fecha_final)).values

        # Crear un rango de fechas diarias
        df_fechas = pd.date_range(start=fecha_inicial, end=fecha_final)

        # Armar el DataFrame
        if iter == 0:
            df = pd.DataFrame(data_coor, index=df_fechas, columns=['Valor'])
        else:
            df_aux = pd.DataFrame(data_coor, index=df_fechas, columns=['Valor'])
            df = pd.concat([df, df_aux])

    # Cambiar nombre del índice
    df.index.name = 'Fecha'

    return df


