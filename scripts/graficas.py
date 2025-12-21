import pandas as pd
import numpy as np
import seaborn as sbn
import matplotlib
matplotlib.use('qtagg')
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional


def graficar_serie_temporal(data: pd.DataFrame, labels: List[str], ylims: Tuple[float, float],
                            color: str, ruta_guardado: Optional[str] = None) -> None:
    '''
    Genera un gráfico de serie temporal con formato personalizado.

    Args:
        data: DataFrame con índice temporal y una columna de valores
        labels: Lista con [título, etiqueta_x, etiqueta_y]
        ylims: Tupla con límites del eje Y (min, max)
        color: Color de la línea de la serie
        ruta_guardado: Ruta donde guardar la figura (opcional, None para no guardar)

    Returns:
        None (muestra el gráfico)

    Ejemplo:
        >>> labels = ['Precipitación Mensual', 'Fecha', 'Precipitación (mm)']
        >>> graficar_serie_temporal(datos, labels, (0, 500), 'blue', './grafico.png')
    '''
    # Crear figura
    plt.figure(figsize=(15, 6))

    # Graficar serie temporal
    plt.plot(data.index, data[data.columns[0]], color)

    # Configurar límites de ejes
    plt.ylim(ylims[0], ylims[1])
    plt.xlim(data.index[0], data.index[-1])

    # Configurar etiquetas
    plt.title(labels[0], fontsize=12, fontweight='bold')
    plt.xlabel(labels[1], fontsize=10, fontweight='bold')
    plt.ylabel(labels[2], fontsize=10, fontweight='bold')

    # Configurar grillas (mayores y menores)
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth='0.5', zorder=0)
    plt.grid(which='minor', linestyle=':', linewidth='0.5', zorder=0)

    # Guardar figura si se especifica ruta
    if ruta_guardado:
        plt.savefig(ruta_guardado)

    plt.show()


def boxplot_mensual(datos_mensuales: pd.DataFrame, ylabel: str, titulo: str) -> None:
    '''
    Genera un boxplot comparativo por mes con medias superpuestas.

    Crea un gráfico de cajas que muestra la distribución de valores por mes,
    incluyendo puntos que representan la media mensual.

    Args:
        datos_mensuales: DataFrame con índice temporal mensual y una columna de valores
        ylabel: Etiqueta del eje Y
        titulo: Título del gráfico

    Returns:
        None (muestra el gráfico)

    Ejemplo:
        >>> boxplot_mensual(datos, 'Precipitación (mm)', 'Distribución Mensual de Lluvia')
    '''
    # Crear copia y extraer mes
    data_boxplot = datos_mensuales.copy()
    columna = data_boxplot.columns[0]
    data_boxplot['Mes'] = data_boxplot.index.month

    # Nombres de los meses
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    # Crear figura
    plt.figure(figsize=(15, 6))

    # Paleta de colores degradado azul-verde
    palette = sbn.color_palette('YlGnBu', 12)

    # Crear boxplot principal
    sbn.boxplot(
        x='Mes',
        y=columna,
        data=data_boxplot,
        palette=palette,
        width=0.6,
        fliersize=3,
        linewidth=1,
        zorder=2,
        boxprops={'alpha': 0.9}
    )

    # Superponer puntos de la media mensual
    medias = data_boxplot.groupby('Mes')[columna].mean()
    plt.scatter(range(12), medias, color='darkred', s=40, zorder=3, label='Media')

    # Configurar ejes y etiquetas
    plt.xticks(range(12), meses, rotation=30, fontsize=10)
    plt.ylim(0, None)
    plt.xlabel('Mes', fontsize=12, fontweight='bold', color='#00334d')
    plt.ylabel(ylabel, fontsize=12, fontweight='bold', color='#00334d')
    plt.title(titulo, fontsize=14, fontweight='bold', color='#00334d', pad=15)

    # Configurar cuadrículas
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth=0.5, alpha=0.5, zorder=0)
    plt.grid(which='minor', linestyle=':', linewidth=0.5, alpha=0.3, zorder=0)

    # Agregar leyenda
    plt.legend(frameon=False, fontsize=10, loc='upper right')

    plt.tight_layout()
    plt.show()


def histogramas_mensuales(datos_mensuales: pd.DataFrame, titulo: str) -> None:
    '''
    Genera un panel de 12 histogramas (uno por cada mes) con KDE.

    Crea una grilla de 4x3 con histogramas que muestran la distribución
    de valores para cada mes, incluyendo líneas de media y mediana.

    Args:
        datos_mensuales: DataFrame con índice temporal mensual y una columna de valores
        titulo: Título principal del panel de histogramas

    Returns:
        None (muestra el gráfico)

    Ejemplo:
        >>> histogramas_mensuales(datos, 'Distribución Mensual de Temperatura 1990-2020')
    '''
    # Crear copia y extraer mes
    data_hist = datos_mensuales.copy()
    columna = data_hist.columns[0]
    data_hist['Mes'] = data_hist.index.month

    # Nombres de los meses
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    # Crear figura con grilla 4x3
    plt.figure(figsize=(16, 10))

    # Paleta de colores degradado azul-verde
    palette = sbn.color_palette('YlGnBu', 12)

    # Generar histograma para cada mes
    for i, mes in enumerate(range(1, 13), start=1):
        # Filtrar datos del mes
        data_mes = data_hist[data_hist['Mes'] == mes]

        # Calcular estadísticos
        media = np.nanmean(data_mes[columna])
        mediana = np.nanmedian(data_mes[columna])

        # Crear subplot
        ax = plt.subplot(4, 3, i)

        # Generar histograma con KDE
        sbn.histplot(
            data_mes[columna],
            color=palette[i - 1],
            kde=True,
            bins=15,
            edgecolor='white',
            alpha=0.8
        )

        # Agregar líneas verticales de media y mediana
        plt.axvline(media, color='darkred', linestyle='--', linewidth=1.5, label='Media')
        plt.axvline(mediana, color='darkgreen', linestyle='--', linewidth=1.5, label='Mediana')

        # Configurar título y etiquetas del subplot
        plt.title(meses[i - 1], fontsize=11, fontweight='bold', color='#004b6d')
        plt.xlabel('')
        plt.ylabel('Frecuencia', fontsize=9)

        # Agregar leyenda y grilla
        plt.legend(fontsize=8, loc='upper right', frameon=False)
        plt.grid(alpha=0.3)

    # Título principal
    plt.suptitle(titulo, fontsize=15, fontweight='bold', color='#00334d', y=1.02)

    plt.tight_layout()
    plt.show()