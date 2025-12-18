import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn


def BoxplotMensual(datosMensuales, ylabel, titulo):
    dataBoxplotMensual = datosMensuales.copy()
    columna = dataBoxplotMensual.columns[0]
    dataBoxplotMensual['Mes'] = dataBoxplotMensual.index.month

    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
             'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

    plt.figure(figsize=(15,6))

    palette = sbn.color_palette("YlGnBu", 12)

    # Boxplot principal
    sbn.boxplot(
        x='Mes',
        y=columna,
        data=dataBoxplotMensual,
        palette=palette,
        width=0.6,
        fliersize=3,
        linewidth=1,
        zorder=2,
        boxprops={'alpha':0.9}
    )

    # Puntos de la media mensual (promedios sobre cada caja)
    medias = dataBoxplotMensual.groupby('Mes')[columna].mean()
    plt.scatter(range(12), medias, color='darkred', s=40, zorder=3, label='Media')

    # Ejes y etiquetas
    plt.xticks(range(12), meses, rotation=30, fontsize=10)
    plt.ylim(0, None)
    plt.xlabel('Mes', fontsize=12, fontweight='bold', color='#00334d')
    plt.ylabel(ylabel, fontsize=12, fontweight='bold', color='#00334d')
    plt.title(titulo, fontsize=14, fontweight='bold', color='#00334d', pad=15)

    # Cuadrículas limpias
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth=0.5, alpha=0.5, zorder=0)
    plt.grid(which='minor', linestyle=':', linewidth=0.5, alpha=0.3, zorder=0)

    # Leyenda
    plt.legend(frameon=False, fontsize=10, loc='upper right')

    plt.tight_layout()
    plt.show()

def HistogramasMensuales(datosMensuales, titulo):
    dataHistMensual = datosMensuales.copy()
    columna = dataHistMensual.columns[0]
    dataHistMensual['Mes'] = dataHistMensual.index.month

    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    plt.figure(figsize=(16,10))

    palette = sbn.color_palette("YlGnBu", 12)

    for i, mes in enumerate(range(1,13), start=1):
        dataMes = dataHistMensual[dataHistMensual['Mes'] == mes]
        media = np.nanmean(dataMes[columna])
        mediana = np.nanmedian(dataMes[columna])

        ax = plt.subplot(4,3,i)
        sbn.histplot(dataMes[columna],
                     color=palette[i-1],
                     kde=True,
                     bins=15,
                     edgecolor='white',
                     alpha=0.8)


        plt.axvline(media, color='darkred', linestyle='--', linewidth=1.5, label='Media')
        plt.axvline(mediana, color='darkgreen', linestyle='--', linewidth=1.5, label='Mediana')

        plt.title(meses[i-1], fontsize=11, fontweight='bold', color='#004b6d')

        plt.xlabel('')
        plt.ylabel('Frecuencia', fontsize=9)
        plt.legend(fontsize=8, loc='upper right', frameon=False)
        plt.grid(alpha=0.3)


    plt.suptitle(titulo,fontsize=15, fontweight='bold', color='#00334d', y=1.02)

    plt.tight_layout()