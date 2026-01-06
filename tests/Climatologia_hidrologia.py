import pandas as pd
from scripts.lecturas_datos import *
from scripts.auxiliares_procesamiento import *
from scripts.graficas import *
from scripts.estadisticos import *
from scripts.auxiliares_generales import *
import os

print("=" * 70)
print('PIPELINE DE EJEMPLO PARA COMPLETAR DATOS DIARIOS MEDIANTE EL CUBO DE DATOS')
print("=" * 70)

#Metadatos de ejemplo
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
rutaCubo = 'G:/Mi unidad/IDEAM/Archivos_cubo_de_datos'
rutaDatos = 'C:/Users/sergi/Desktop/Pruebas_leidy'
rutaGuardado = 'C:/Users/sergi/Desktop/Pruebas_leidy/RESULTADOS'

coordenadas_arc = pd.read_excel(os.path.join(rutaDatos, 'coordenadas.xlsx'))
archivos = [f for f in os.listdir(rutaDatos) if f.endswith('.csv')]

estadisticos = []
labelEstaciones = []
for arc in range(0,len(archivos)):
    #Se crea la carpeta por estación con resultados
    estacion = os.path.splitext(archivos[arc])[0]

    rutaGuardadoEstacion = os.path.join(rutaGuardado, estacion)
    #Se importan los datos de la estaciones del IDEAM
    try:
        datosIDEAM = identificar_nan(abrir_archivos_dhime(os.path.join(rutaDatos,estacion + '.csv'), sep = ','))
    except:
        datosIDEAM = identificar_nan(abrir_archivos_dhime(os.path.join(rutaDatos,estacion + '.csv'), sep = ';'))

    #Se extraen los datos del cubo de datos
    variable = 'prcp'
    coord = list(coordenadas_arc[coordenadas_arc['CODIGO'] == 24030570][['Y','X']].values[0])
    coordenadas = [coord[0], coord[1]] #lat, lon

    #Uso de la función
    dataCubo = extraccion_cubo_datos(rutaCubo,variable,coordenadas)
    dataCubo = eliminar_atipicos_diarios(dataCubo,n_boot= 5000,percentil=97,tamano_muestra=48)
    dataCubo['Valor'] = dataCubo['Valor'].fillna(dataCubo[['Valor']].median())

    #Se hace el reemplazo de los nan de los datos del IDEAM por los datos del cubo de datos
    datosIDEAM['Valor'] = datosIDEAM['Valor'].fillna(dataCubo['Valor'])

    #Se hace el agregado a nivel mensual y se exportan estadísticos
    datosIDEAMMensual = agregados_ideam(datosIDEAM, num_datos_minimo = 0.6*30, frecuencia = 'ME', estadistico = 'sum')

    #Estadistícos descriptivos
    tablaEstDescMen = estadisticos_desc_mensuales(datosIDEAMMensual)[['Mediana']]
    indices = [1,2,3,4,5,6,7,8,9,10,11,12,'Suma']
    valores = tablaEstDescMen[tablaEstDescMen.index.isin(indices)].T.values[0]

    estadisticos.append(valores)
    labelEstaciones.append(estacion)

    print(f'Estación {estacion} completada correctamente')

columnas = [1,2,3,4,5,6,7,8,9,10,11,12,'Suma']
dfEstadisticos = pd.DataFrame(estadisticos, index = labelEstaciones, columns=columnas)
dfEstadisticos.to_csv(os.path.join(rutaGuardado, 'Resultados globales' + '.csv'))

print('PIPELINE COMPLETADO CON EXITO')








