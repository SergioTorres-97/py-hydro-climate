#Funciones auxiliares para el procesamiento de los datos
import pandas as pd
import numpy as np

#Función para el filtrado de datos
def filtrarDatos(datos,año_inicial,año_final):
    datos = datos.loc[año_inicial:año_final]
    return datos

#Función para la identificación de datos faltantes a escala diaria
def identificarNAN(datos):
    datos.index = pd.to_datetime(datos.index)
    fecha_inicio = datos.index[0]
    fecha_fin = datos.index[datos.shape[0]-1]
    rango_fechas = pd.date_range(start=fecha_inicio, end=fecha_fin)
    df = pd.DataFrame(rango_fechas, columns=['Fecha'])
    df.set_index('Fecha',inplace = True)

    df_fin = df.join(datos)
    return df_fin

#Función para la identificación de datos faltantes a escala horaria
def IdentificarNAN3h(datos, horas = [7, 13, 18, 19]):
    fechas = pd.date_range(start=datos.index[0], end=datos.index[-1], freq='D')

    horas_vector = pd.to_datetime([f"{fecha.date()} {hora}:00:00" for fecha in fechas for hora in horas])

    dfFechas = pd.DataFrame(horas_vector, columns=['Fecha'])
    dfFechas.set_index('Fecha', inplace=True)

    datos_new = dfFechas.join(datos)

    hours_18_19 = datos_new.between_time('18:00', '19:00')

    to_drop_19 = hours_18_19[(hours_18_19.index.hour == 19) &
                             (hours_18_19.shift(1)['Valor'].notna())].index

    to_drop_18 = hours_18_19[(hours_18_19.index.hour == 18) &
                             (hours_18_19.shift(-1)['Valor'].notna())].index

    to_drop = to_drop_19.append(to_drop_18)
    df = datos_new.drop(to_drop)

    df_copy = df.copy()
    df_18 = df_copy[df_copy.index.hour == 18]
    df_18.index = df_18.index + pd.DateOffset(hours=1)
    df_combined = pd.concat([df_copy[df_copy.index.hour != 18], df_18])
    df_combined = df_combined.sort_index()
    df = df_combined
    return df

def EliminarAtipicosDiarios(datos):
    MaximosMensuales = datos.resample('M').max()['Valor'].dropna().values

    n_boot = 5000               # número de remuestreos
    stat_func = np.percentile   # estadístico a evaluar
    p = 97                      # percentil que queremos analizar

    boot_stats = []
    n = 48 #Muestra de 3 años
    for i in range(n_boot):
        muestra = np.random.choice(MaximosMensuales, size=n, replace=True)
        boot_stats.append(stat_func(muestra, p))

    boot_stats = np.array(boot_stats)

    umbral = np.percentile(boot_stats, p)

    outliers = MaximosMensuales[MaximosMensuales >= umbral]

    datos[datos[datos.columns[0]] >= outliers.min()] = np.nan

    return datos

