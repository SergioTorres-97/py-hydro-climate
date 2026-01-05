from scripts.lecturas_datos import *
from scripts.auxiliares_procesamiento import *
from scripts.auxiliares_generales import *
from scripts.graficas import *
from scripts.estadisticos import *
import os

rutaBase = r'' #Ruta donde se almacenan los datos crudos
rutaGuardar = r'' #Ruta de resultados

print("=" * 70)
print('CLIMATOLOGÍA MODELO DE CALIDAD - RÍO CHICAMOCHA')
print("=" * 70)

print('TRAMO 1 - CHICAMOCHA')
print("=" * 70)

savefile = 'T1_CHICAMOCHA' #Se modifica
rutaGuardado = os.path.join(rutaGuardar, savefile)
crear_carpeta(rutaGuardado, True)

print('TEMPERATURA MEDIA')
folder = 'ESTACIONES TEMPERATURA MEDIA' #se modifica folder donde esta almacenada la informacion
filename = '' #se modifica - nombre del archivo
ruta = os.path.join(rutaBase, folder, filename)

datos = identificar_nan(filtrar_datos(abrir_archivo_aqts_web(ruta, sep = ','),'2015','2024'))

#Se grafican los datos diarios
labels = {
    'titulo' : 'Serie diaria de temperatura', #Se cambia
    'ylabel' : 'Temperatura [°C]', #Se cambia
    'xlabel' : 'Fecha', #Se cambia
}
ylims = {
    'y_bajo' : 10, #Se cambia
    'y_alto' : 30 #Se cambia
}

color = '#993F2B' #se modifica - https://htmlcolorcodes.com/

rutaGuardadoGraficas = os.path.join(rutaGuardado, 'Temperatura media.png') #Se puede cambiar

graficar_serie_temporal(datos,
                        labels = [labels['titulo'], labels['xlabel'], labels['ylabel']],
                        ylims = [ylims['y_bajo'], ylims['y_alto']],
                        color = color,
                        ruta_guardado = rutaGuardadoGraficas)

dataMensual = agregados_ideam(datos, num_datos_minimo = 0.6*30, frecuencia = 'ME', estadistico = 'mean')
#Estadistícos descriptivos
tablaEstDescMen = estadisticos_desc_mensuales(dataMensual)
tablaEstDescMen.to_excel(os.path.join(rutaGuardado, 'Estadisticos_Tmed.xlsx')) #Se puede cambiar

print('TEMPERATURA PUNTO DE ROCIO')

folder = 'ESTACIONES PUNTO ROCIO' #se modifica folder donde esta almacenada la informacion
filename = '' #se modifica - nombre del archivo
ruta = os.path.join(rutaBase, folder, filename)

datos = identificar_nan(filtrar_datos(abrir_archivo_aqts_web(ruta, sep = ','),'2015','2024'))

#Se grafican los datos diarios
labels = {
    'titulo' : 'Serie diaria de temperatura', #Se cambia
    'ylabel' : 'Temperatura de rocío [°C]', #Se cambia
    'xlabel' : 'Fecha', #Se cambia
}
ylims = {
    'y_bajo' : 10, #Se cambia
    'y_alto' : 30 #Se cambia
}

color = '#993F2B' #se modifica - https://htmlcolorcodes.com/

rutaGuardadoGraficas = os.path.join(rutaGuardado, 'Punto rocio.png') #Se puede cambiar

graficar_serie_temporal(datos,
                        labels = [labels['titulo'], labels['xlabel'], labels['ylabel']],
                        ylims = [ylims['y_bajo'], ylims['y_alto']],
                        color = color,
                        ruta_guardado = rutaGuardadoGraficas)

dataMensual = agregados_ideam(datos, num_datos_minimo = 0.6*30, frecuencia = 'ME', estadistico = 'mean')
#Estadistícos descriptivos
tablaEstDescMen = estadisticos_desc_mensuales(dataMensual)
tablaEstDescMen.to_excel(os.path.join(rutaGuardado, 'Estadisticos_Punto_rocio.xlsx')) #Se puede cambiar

print('VELOCIDAD DEL VIENTO')

folder = 'ESTACIONES VELOCIDAD DEL VIENTO' #se modifica folder donde esta almacenada la informacion
filename = '' #se modifica - nombre del archivo
ruta = os.path.join(rutaBase, folder, filename)

datos = identificar_nan(filtrar_datos(abrir_archivos_nasa(ruta, sep = ','),'2015','2024'))

#Se grafican los datos diarios
labels = {
    'titulo' : 'Serie diaria de temperatura', #Se cambia
    'ylabel' : 'Temperatura de rocío [°C]', #Se cambia
    'xlabel' : 'Fecha', #Se cambia
}
ylims = {
    'y_bajo' : 0, #Se cambia
    'y_alto' : 15 #Se cambia
}

color = '#993F2B' #se modifica - https://htmlcolorcodes.com/

rutaGuardadoGraficas = os.path.join(rutaGuardado, 'Punto rocio.png') #Se puede cambiar

graficar_serie_temporal(datos,
                        labels = [labels['titulo'], labels['xlabel'], labels['ylabel']],
                        ylims = [ylims['y_bajo'], ylims['y_alto']],
                        color = color,
                        ruta_guardado = rutaGuardadoGraficas)

dataMensual = agregados_ideam(datos, num_datos_minimo = 0.6*30, frecuencia = 'ME', estadistico = 'mean')
#Estadistícos descriptivos
tablaEstDescMen = estadisticos_desc_mensuales(dataMensual)
tablaEstDescMen.to_excel(os.path.join(rutaGuardado, 'Estadisticos_Punto_rocio.xlsx')) #Se puede cambiar

print('NUBOSIDAD')

folder = 'ESTACIONES NOBOSIDAD' #se modifica folder donde esta almacenada la informacion
filename = '' #se modifica - nombre del archivo
ruta = os.path.join(rutaBase, folder, filename)

datos = identificar_nan(filtrar_datos(abrir_archivos_giovanni(ruta, sep = ','),'2015','2024'))

#Se grafican los datos diarios
labels = {
    'titulo' : 'Serie diaria de temperatura', #Se cambia
    'ylabel' : 'Nubosidad [-]', #Se cambia
    'xlabel' : 'Fecha', #Se cambia
}
ylims = {
    'y_bajo' : 0, #Se cambia
    'y_alto' : 1 #Se cambia
}

color = '#993F2B' #se modifica - https://htmlcolorcodes.com/

rutaGuardadoGraficas = os.path.join(rutaGuardado, 'Punto rocio.png') #Se puede cambiar

graficar_serie_temporal(datos,
                        labels = [labels['titulo'], labels['xlabel'], labels['ylabel']],
                        ylims = [ylims['y_bajo'], ylims['y_alto']],
                        color = color,
                        ruta_guardado = rutaGuardadoGraficas)

dataMensual = agregados_ideam(datos, num_datos_minimo = 0.6*30, frecuencia = 'ME', estadistico = 'mean')
#Estadistícos descriptivos
tablaEstDescMen = estadisticos_desc_mensuales(dataMensual)
tablaEstDescMen.to_excel(os.path.join(rutaGuardado, 'Estadisticos_Punto_rocio.xlsx')) #Se puede cambiar

print("=" * 70)
print('TRAMO 2 - CHICAMOCHA')
print("=" * 70)

savefile = 'T2_CHICAMOCHA'
rutaGuardado = os.path.join(rutaGuardar, savefile)
crear_carpeta(rutaGuardado, True)

print('TEMPERATURA MEDIA')
folder = 'ESTACIONES TEMPERATURA MEDIA' #se modifica folder donde esta almacenada la informacion
filename = '' #se modifica - nombre del archivo
ruta = os.path.join(rutaBase, folder, filename)

datos = identificar_nan(filtrar_datos(abrir_archivo_aqts_web(ruta, sep = ','),'2015','2024'))

#Se grafican los datos diarios
labels = {
    'titulo' : 'Serie diaria de temperatura', #Se cambia
    'ylabel' : 'Temperatura [°C]', #Se cambia
    'xlabel' : 'Fecha', #Se cambia
}
ylims = {
    'y_bajo' : 10, #Se cambia
    'y_alto' : 30 #Se cambia
}

color = '#993F2B' #se modifica - https://htmlcolorcodes.com/

rutaGuardadoGraficas = os.path.join(rutaGuardado, 'Temperatura media.png') #Se puede cambiar

graficar_serie_temporal(datos,
                        labels = [labels['titulo'], labels['xlabel'], labels['ylabel']],
                        ylims = [ylims['y_bajo'], ylims['y_alto']],
                        color = color,
                        ruta_guardado = rutaGuardadoGraficas)

dataMensual = agregados_ideam(datos, num_datos_minimo = 0.6*30, frecuencia = 'ME', estadistico = 'mean')
#Estadistícos descriptivos
tablaEstDescMen = estadisticos_desc_mensuales(dataMensual)
tablaEstDescMen.to_excel(os.path.join(rutaGuardado, 'Estadisticos_Tmed.xlsx')) #Se puede cambiar

print('TEMPERATURA PUNTO DE ROCIO')


print('VELOCIDAD DEL VIENTO')


print('NUBOSIDAD')

print("=" * 70)
print('TRAMO 3 - CHICAMOCHA')
print("=" * 70)

savefile = 'T3_CHICAMOCHA'
rutaGuardado = os.path.join(rutaGuardar, savefile)
crear_carpeta(rutaGuardado, True)

print('TEMPERATURA MEDIA')

print('TEMPERATURA PUNTO DE ROCIO')


print('VELOCIDAD DEL VIENTO')


print('NUBOSIDAD')

print("=" * 70)
print('TRAMO 4 - CHICAMOCHA')
print("=" * 70)

savefile = 'T4_CHICAMOCHA'
rutaGuardado = os.path.join(rutaGuardar, savefile)
crear_carpeta(rutaGuardado, True)

print('TEMPERATURA MEDIA')

print('TEMPERATURA PUNTO DE ROCIO')


print('VELOCIDAD DEL VIENTO')


print('NUBOSIDAD')

print("=" * 70)
print('TRAMO 5 - CHICAMOCHA')
print("=" * 70)

savefile = 'T5_CHICAMOCHA'
rutaGuardado = os.path.join(rutaGuardar, savefile)
crear_carpeta(rutaGuardado, True)

print('TEMPERATURA MEDIA')

print('TEMPERATURA PUNTO DE ROCIO')


print('VELOCIDAD DEL VIENTO')


print('NUBOSIDAD')

print("=" * 70)
print('TRAMO 6 - CHICAMOCHA')
print("=" * 70)

savefile = 'T6_CHICAMOCHA'
rutaGuardado = os.path.join(rutaGuardar, savefile)
crear_carpeta(rutaGuardado, True)

print('TEMPERATURA MEDIA')

print('TEMPERATURA PUNTO DE ROCIO')


print('VELOCIDAD DEL VIENTO')


print('NUBOSIDAD')

print("=" * 70)
print('TRAMO - CANAL VARGAS')
print("=" * 70)

savefile = 'T_VARGAS'
rutaGuardado = os.path.join(rutaGuardar, savefile)
crear_carpeta(rutaGuardado, True)

print('TEMPERATURA MEDIA')

print('TEMPERATURA PUNTO DE ROCIO')


print('VELOCIDAD DEL VIENTO')


print('NUBOSIDAD')

print("=" * 70)
print('TRAMO - RIO PESCA')
print("=" * 70)

savefile = 'T_PESCA'
rutaGuardado = os.path.join(rutaGuardar, savefile)
crear_carpeta(rutaGuardado, True)

print('TEMPERATURA MEDIA')

print('TEMPERATURA PUNTO DE ROCIO')


print('VELOCIDAD DEL VIENTO')


print('NUBOSIDAD')

print("=" * 70)
print('TRAMO - RIO TOTA')
print("=" * 70)

savefile = 'T_TOTA'
rutaGuardado = os.path.join(rutaGuardar, savefile)
crear_carpeta(rutaGuardado, True)

print('TEMPERATURA MEDIA')

print('TEMPERATURA PUNTO DE ROCIO')


print('VELOCIDAD DEL VIENTO')


print('NUBOSIDAD')

print("=" * 70)
print('TRAMO - RIO CHIQUITO')
print("=" * 70)

savefile = 'T_CHIQUITO'
rutaGuardado = os.path.join(rutaGuardar, savefile)
crear_carpeta(rutaGuardado, True)

print('TEMPERATURA MEDIA')

print('TEMPERATURA PUNTO DE ROCIO')


print('VELOCIDAD DEL VIENTO')


print('NUBOSIDAD')

print("=" * 70)
print('PROCESAMIENTO FINALIZADO CON ÉXITO')
print("=" * 70)