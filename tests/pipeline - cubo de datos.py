from scripts.lecturas_datos import *
from scripts.auxiliares_procesamiento import *
from scripts.graficas import *
from scripts.estadisticos import *
import os

print("=" * 70)
print('PIPELINE DE EJEMPLO PARA LA EXTRACCIÓN DE DATOS DEL CUBO')
print("=" * 70)

#Metadatos de ejemplo
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ruta = 'G:/Mi unidad/IDEAM/Archivos_cubo_de_datos'
rutaGuardado = os.path.join(BASE_DIR, 'tests', 'results_tests')

print('Rutas:')
print(f'Ruta archivo: {ruta}')
print(f'Ruta guardado: {rutaGuardado} \n')

variable = 'prcp'
coordenadas = [5.7491,-73.328] #lat, lon

#Uso de la función
data = extraccion_cubo_datos(ruta,variable,coordenadas)
# data[data['Valor'] > 80] = np.nan
data = eliminar_atipicos_diarios(data,n_boot= 5000,percentil=97,tamano_muestra=48)
data['Valor'] = data['Valor'].fillna(data[['Valor']].median())

print('DATOS EXTRAÍDOS CORRECTAMENTE')

#Se grafican los datos diarios
labels = {
    'titulo' : f'Serie diaria de precipitación x = {coordenadas[1]}, y = {coordenadas[0]}',
    'ylabel' : 'Precipitación [mm]',
    'xlabel' : 'Fecha',
}
ylims = {
    'y_bajo' : 0,
    'y_alto' : 100
}

rutaGuardadoGraficas = os.path.join(rutaGuardado, 'Precipitación diaria Cubo.png')

graficar_serie_temporal(data,
                        labels = [labels['titulo'], labels['xlabel'], labels['ylabel']],
                        ylims = [ylims['y_bajo'], ylims['y_alto']],
                        color = '#AB0303',
                        ruta_guardado = rutaGuardadoGraficas)

print('GRÁFICAS ELABORADA CORRECTAMENTE')

#Agregación de datos
dataMensual = agregados_ideam(data, num_datos_minimo = 0.8*30, frecuencia = 'ME', estadistico = 'sum')
dataAnual = agregados_ideam(data, num_datos_minimo = 0.8*365, frecuencia = 'YE', estadistico = 'sum')

print('AGREGACIÓN DE DATOS A NIVEL ANUAL Y MENSUAL ELABORADAS CORRECTAMENTE')

#Estadistícos descriptivos
tablaEstDescMen = estadisticos_desc_mensuales(dataMensual)
tablaEstDescAnual = dataAnual.describe()
tablaEstDescMen.to_excel(os.path.join(rutaGuardado, 'Estadisticos mensuales CDD.xlsx'))
tablaEstDescAnual.to_excel(os.path.join(rutaGuardado, 'Estadisticos anuales CDD.xlsx'))

print('ESTADISTICOS DESCRIPTIVOS  A NIVEL ANUAL Y MENSUAL ELABORADOS CORRECTAMENTE')





