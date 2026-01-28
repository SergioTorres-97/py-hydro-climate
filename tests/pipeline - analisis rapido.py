from scripts.lecturas_datos import *
from scripts.auxiliares_procesamiento import *
from scripts.graficas import *
from scripts.estadisticos import *
import os

print("=" * 70)
print('PIPELINE DE EJEMPLO PARA EL ANÁLISIS DE DATOS')
print("=" * 70)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
rutaData = os.path.join(BASE_DIR, 'tests', 'data', 'TSSM_MEDIA_D_CAL.csv')
rutaGuardado = os.path.join(BASE_DIR, 'tests', 'results_tests')

print('Rutas:')
print(f'Ruta archivo: {rutaData}')
print(f'Ruta guardado: {rutaGuardado} \n')


#anio_inicio, anio_fin
anio_inicio, anio_fin = '1991', '2020'

print('Anios seleccionados:')
print(f'Anio inicio: {anio_inicio} Anio final: {anio_fin} \n')

#Se abre el archivo con AbrirArchivosAQTS, ya que proviene de esta fuente
data = abrir_archivos_aqts(rutaData)
#Se filtran los archivos
data = filtrar_datos(data,anio_inicio, anio_fin )
#Se revisan los nan
data = identificar_nan(data)

print('DATOS LEÍDOS CORRECTAMENTE \n')

#Se grafican los datos diarios
labels = {
    'titulo' : 'Serie diaria de temperatura',
    'ylabel' : 'Temperatura [°C]',
    'xlabel' : 'Fecha',
}
ylims = {
    'y_bajo' : 10,
    'y_alto' : 30
}

rutaGuardadoGraficas = os.path.join(rutaGuardado, 'Temperatura diaria.png')
graficar_serie_temporal(data,
                        labels = [labels['titulo'], labels['xlabel'], labels['ylabel']],
                        ylims = [ylims['y_bajo'], ylims['y_alto']],
                        color = '#AB0303',
                        ruta_guardado = rutaGuardadoGraficas)

print('GRÁFICAS ELABORADA CORRECTAMENTE')

#Agregación de datos
dataMensual = agregados_ideam(data, num_datos_minimo = 0.6*30, frecuencia = 'ME', estadistico = 'mean')
dataAnual = agregados_ideam(data, num_datos_minimo = 0.6*365, frecuencia = 'YE', estadistico = 'mean')
dataMaxAnual = agregados_ideam(data, num_datos_minimo = 0.6*365, frecuencia = 'YE', estadistico = 'max')

print('AGREGACIÓN DE DATOS A NIVEL ANUAL Y MENSUAL ELABORADAS CORRECTAMENTE')

#Se grafican los datos mensuales
labels = {
    'titulo' : 'Serie mensual de temperatura',
    'ylabel' : 'Temperatura [°C]',
    'xlabel' : 'Fecha',
}
ylims = {
    'y_bajo' : 10,
    'y_alto' : 30
}

rutaGuardadoGraficas = os.path.join(rutaGuardado, 'Temperatura mensual.png')
graficar_serie_temporal(dataMensual,
                        labels = [labels['titulo'], labels['xlabel'], labels['ylabel']],
                        ylims = [ylims['y_bajo'], ylims['y_alto']],
                        color = '#AB0303',
                        ruta_guardado = rutaGuardadoGraficas)

print('GRÁFICAS ELABORADA CORRECTAMENTE')

#Se grafican los datos anuales
labels = {
    'titulo' : 'Serie anual de temperatura',
    'ylabel' : 'Temperatura [°C]',
    'xlabel' : 'Fecha',
}
ylims = {
    'y_bajo' : 10,
    'y_alto' : 30
}

rutaGuardadoGraficas = os.path.join(rutaGuardado, 'Temperatura mensual.png')
graficar_serie_temporal(dataAnual,
                        labels = [labels['titulo'], labels['xlabel'], labels['ylabel']],
                        ylims = [ylims['y_bajo'], ylims['y_alto']],
                        color = '#AB0303',
                        ruta_guardado = rutaGuardadoGraficas)

print('GRÁFICAS ELABORADA CORRECTAMENTE')

#Se grafican los datos máximos anuales
labels = {
    'titulo' : 'Serie máxima anual de temperatura',
    'ylabel' : 'Temperatura [°C]',
    'xlabel' : 'Fecha',
}
ylims = {
    'y_bajo' : 10,
    'y_alto' : 30
}

rutaGuardadoGraficas = os.path.join(rutaGuardado, 'Temperatura mensual.png')
graficar_serie_temporal(dataMaxAnual,
                        labels = [labels['titulo'], labels['xlabel'], labels['ylabel']],
                        ylims = [ylims['y_bajo'], ylims['y_alto']],
                        color = '#AB0303',
                        ruta_guardado = rutaGuardadoGraficas)

print('GRÁFICAS ELABORADA CORRECTAMENTE')

#Estadistícos descriptivos
tablaEstDescMen = estadisticos_desc_mensuales(dataMensual)
tablaEstDescAnual = dataAnual.describe()
tablaEstDescMen.to_excel(os.path.join(rutaGuardado, 'Estadisticos mensuales.xlsx'))
tablaEstDescAnual.to_excel(os.path.join(rutaGuardado, 'Estadisticos anuales.xlsx'))

print('ESTADISTICOS DESCRIPTIVOS  A NIVEL ANUAL Y MENSUAL ELABORADOS CORRECTAMENTE')
