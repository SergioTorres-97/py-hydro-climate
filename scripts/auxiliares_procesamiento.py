# Funciones auxiliares para el procesamiento de los datos
import pandas as pd
import numpy as np


def filtrar_datos(datos: pd.DataFrame, anio_inicial: str, anio_final: str) -> pd.DataFrame:
    '''
    Filtra un DataFrame por un rango de años específico.

    Args:
        datos: DataFrame con índice de fechas
        anio_inicial: Año inicial del filtro (formato 'YYYY-MM-DD' o 'YYYY')
        anio_final: Año final del filtro (formato 'YYYY-MM-DD' o 'YYYY')

    Returns:
        DataFrame filtrado por el rango de años especificado
    '''
    return datos.loc[anio_inicial:anio_final]


def identificar_nan(datos: pd.DataFrame) -> pd.DataFrame:
    '''
    Identifica y completa datos faltantes a escala diaria.

    Crea un rango completo de fechas diarias entre el inicio y fin de los datos,
    e inserta NaN donde falten registros.

    Args:
        datos: DataFrame con índice de fechas (puede tener días faltantes)

    Returns:
        DataFrame con todas las fechas diarias completadas (NaN donde faltaban datos)
    '''
    # Asegurar que el índice sea datetime
    datos.index = pd.to_datetime(datos.index)

    # Obtener primera y última fecha
    fecha_inicio = datos.index[0]
    fecha_fin = datos.index[-1]

    # Crear rango completo de fechas diarias
    rango_fechas = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='D')
    df_completo = pd.DataFrame(index=rango_fechas)
    df_completo.index.name = 'Fecha'

    # Unir con datos originales (insertar NaN donde falten datos)
    df_final = df_completo.join(datos)

    return df_final


def identificar_nan_horario(datos: pd.DataFrame, horas: list = None) -> pd.DataFrame:
    '''
    Identifica y completa datos faltantes a escala horaria para horas específicas.

    Función diseñada para datos de evaporación tomados a horas específicas del día.
    Maneja el caso especial de las 18:00 y 19:00 (conserva solo una si ambas existen).

    Args:
        datos: DataFrame con índice de fechas y hora
        horas: Lista de horas del día a considerar (por defecto [7, 13, 18, 19])

    Returns:
        DataFrame con registros horarios completos, resolviendo duplicados 18:00/19:00
    '''
    if horas is None:
        horas = [7, 13, 18, 19]

    # Crear rango de fechas diarias
    fechas = pd.date_range(start=datos.index[0], end=datos.index[-1], freq='D')

    # Generar todas las combinaciones de fecha + hora
    fechas_horas = [
        f'{fecha.date()} {hora}:00:00'
        for fecha in fechas
        for hora in horas
    ]
    horas_vector = pd.to_datetime(fechas_horas)

    # Crear DataFrame con todas las horas esperadas
    df_completo = pd.DataFrame(index=horas_vector)
    df_completo.index.name = 'Fecha'

    # Unir con datos originales
    datos_completos = df_completo.join(datos)

    # Resolver conflicto entre 18:00 y 19:00 (conservar solo uno si ambos existen)
    horas_18_19 = datos_completos.between_time('18:00', '19:00')

    # Identificar registros de 19:00 donde 18:00 tiene datos
    to_drop_19 = horas_18_19[
        (horas_18_19.index.hour == 19) &
        (horas_18_19.shift(1)['Valor'].notna())
        ].index

    # Identificar registros de 18:00 donde 19:00 tiene datos
    to_drop_18 = horas_18_19[
        (horas_18_19.index.hour == 18) &
        (horas_18_19.shift(-1)['Valor'].notna())
        ].index

    # Eliminar duplicados
    indices_eliminar = to_drop_19.union(to_drop_18)
    df_sin_duplicados = datos_completos.drop(indices_eliminar)

    # Estandarizar hora 18:00 a 19:00
    df_copia = df_sin_duplicados.copy()
    df_18 = df_copia[df_copia.index.hour == 18]
    df_18.index = df_18.index + pd.DateOffset(hours=1)

    # Combinar datos de 19:00 con el resto de horas
    df_final = pd.concat([
        df_copia[df_copia.index.hour != 18],
        df_18
    ]).sort_index()

    return df_final


def eliminar_atipicos_diarios(datos: pd.DataFrame, n_boot: int = 5000,
                              percentil: int = 97, tamano_muestra: int = 48) -> pd.DataFrame:
    '''
    Elimina valores atípicos diarios usando bootstrap sobre máximos mensuales.

    Aplica técnica de bootstrap para estimar el umbral de valores atípicos
    basándose en los máximos mensuales de la serie.

    Args:
        datos: DataFrame con columna 'Valor'
        n_boot: Número de remuestreos bootstrap (por defecto 5000)
        percentil: Percentil a evaluar (por defecto 97)
        tamano_muestra: Tamaño de muestra para bootstrap, equivalente a años*12 (por defecto 48 = 4 años)

    Returns:
        DataFrame con valores atípicos reemplazados por NaN
    '''
    # Calcular máximos mensuales
    maximos_mensuales = datos.resample('M').max()['Valor'].dropna().values

    # Aplicar bootstrap para estimar umbral
    estadisticos_boot = []

    for _ in range(n_boot):
        # Remuestreo con reemplazo
        muestra = np.random.choice(maximos_mensuales, size=tamano_muestra, replace=True)
        estadisticos_boot.append(np.percentile(muestra, percentil))

    estadisticos_boot = np.array(estadisticos_boot)

    # Calcular umbral como percentil de los estadísticos bootstrap
    umbral = np.percentile(estadisticos_boot, percentil)

    # Identificar valores atípicos
    outliers = maximos_mensuales[maximos_mensuales >= umbral]

    # Reemplazar valores atípicos por NaN
    datos_limpios = datos.copy()
    datos_limpios[datos_limpios[datos_limpios.columns[0]] >= outliers.min()] = np.nan

    return datos_limpios