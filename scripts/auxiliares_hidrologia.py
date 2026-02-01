import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

def parametros_IDF(prec_max_TR):
    """""
    Esta función permite calcular los parámetros k, m y n de la ecuación I=k(T**m)/(d**n), empleando la metodología de
    Dyck y Peschke para duraciones menores a 24 horas, en función de las precitaciones máximas asociadas a las distribu-
    ciones de probabilidad previamente calculadas.
    Los resultados calculados son k,m,n y los estadísticos de la regresión
    """""
    minutos=np.arange(1,1441,1)
    horas=[round(minutos[i]/60,2) for i in range(0,len(minutos))]
    pdis=[]
    for i in range(0,prec_max_TR.shape[0]):
        a=list(prec_max_TR[prec_max_TR.columns[1]])[i]
        b=[]
        for j in range(0,len(minutos)):
            c=a*((minutos[j]/1440)**0.25)/horas[j]
            b.append(c)
        pdis.append(b)

    int_dis = pd.DataFrame()
    int_dis['min']=minutos
    int_dis['Hr']= [round(minutos[i]/60,2) for i in range(0,len(minutos))]

    for i in range(0,prec_max_TR.shape[0]):
        #Se extraen los valores obtenidos con cad TR
        a=list(prec_max_TR[prec_max_TR.columns[0]])[i]
        #Se crean columnas con los valores obtenidos de cada TR
        int_dis[str(a)] = np.array(pdis)[i]

    #Se crea una variable con los TR
    T=list(int_dis.columns[2:])

    #Lista concatenada de intensidades
    for i in range(2,int_dis.shape[1]):
        if i == 2:
            I = list(int_dis[int_dis.columns[i]]) #Se crea una variable I con los valores de cada TR
        else:
            I = I + list(int_dis[int_dis.columns[i]])  # Se anexan las intensidades de cada TR en una lista

    #Lista concatenada de duraciones
    for i in range(0,prec_max_TR.shape[0]):
        if i == 0:
            d = list(int_dis[int_dis.columns[0]])
            a = [T[i] for j in range(0, len(minutos))]
        else:
            d = d + list(int_dis[int_dis.columns[0]])
            a = a + [T[i] for j in range(0, len(minutos))]

    df_DTI=pd.DataFrame()
    df_DTI['d']=d
    df_DTI['T']=a
    df_DTI['I']=I
    df_DTI['Log (T) x1']=[np.log10(float(a[i])) for i in range(0,len(a))]
    df_DTI['Log (d) x2']=[np.log10(float(d[i])) for i in range(0,len(a))]
    df_DTI['Log (I) y']=[np.log10(float(I[i])) for i in range(0,len(a))]
    df_DTI = df_DTI.apply(pd.to_numeric)

    #Se obtienen los parámetros de la regresión lineal mpultiple con la libreria sm
    y = df_DTI['Log (I) y']
    X = df_DTI[['Log (T) x1', 'Log (d) x2']]
    X = sm.add_constant(X)
    regresion = sm.OLS(y, X).fit()
    est_regr=regresion.summary() #Si se quisieran revisar todos los estadísticos de la regresión
    k,m,n=10**regresion.params[0],regresion.params[1],-regresion.params[2] #Parametros de la curva IDF
    parametros=[k,m,n]

    return parametros,est_regr
def resultados_IDF(k, m, n, TR, do):
    def Intensidad(T, d, k, m, n):
        return (k * (T ** m)) / (d ** n)

    IDF = []
    for i in range(0, len(TR)):
        c = []
        for j in range(0, len(do)):
            b = Intensidad(float(TR[i]), float(do[j]), k, m, n)
            c.append(b)
        IDF.append(c)

    IDF_df = pd.DataFrame(np.array(IDF).T)
    IDF_df.columns = TR
    IDF_df.index = do

    return IDF_df
def graficar_IDF(IDF_df,ruta_guardado):

    markers = ['o', 's', '^', 'v', '>', '<', 'd']
    blues = [(0, 0, i) for i in np.linspace(1, 0.2, 6)]
    tipo_linea = ['-', '--', '-.', ':']
    plt.figure(figsize=(15,6))
    for columna in range(0,IDF_df.shape[1]):
        plt.plot(IDF_df.index,IDF_df[IDF_df.columns[columna]],color = blues[columna],
                 marker = markers[columna], linestyle = '--',
                 markersize = 5,linewidth = 0.5,
                 label= f'TR: {IDF_df.columns[columna]} Años')
        plt.xlim(IDF_df.index[0],IDF_df.index[len(IDF_df.index)-1])
        plt.ylim(0,350)
        plt.ylabel('Intensidad [mm/h]',fontsize=14,fontweight='bold')
        plt.xlabel('Duración [min]', fontsize=14, fontweight='bold')

        plt.minorticks_on()
        plt.grid(which='major', linestyle='-', linewidth='0.5')
        plt.grid(which='minor', linestyle=':', linewidth='0.5')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=IDF_df.shape[1], frameon=True)

    plt.savefig(ruta_guardado + '/Curva_IDF.png', bbox_inches="tight")
    plt.show()
def BloquesALternos(k, m, n, TR, duracion, intervalo, ruta_guardado):
    from datetime import datetime, timedelta
    def calculoIntensidad(k, m, n, t, TR):
        I = (k * (TR ** m)) / (t ** n)
        return I

    def organizar_vector(vector):
        pares = []
        impares = []

        for i, elemento in enumerate(vector):
            if i % 2 == 0:
                pares.append(elemento)
            else:
                impares.append(elemento)

        vector_reorganizado = impares[::-1] + pares

        return vector_reorganizado

    def crear_vector_fechas(duracion_horas, intervalo_minutos, hora_inicio=7):
        fecha_actual = datetime.now()

        año = fecha_actual.year
        mes = fecha_actual.month
        dia = fecha_actual.day

        hora_actual = datetime(año, mes, dia, hora_inicio, 0)
        fechas = []

        # Calcular el timedelta para el intervalo en minutos
        intervalo = timedelta(minutes=intervalo_minutos)

        while duracion_horas > 0:
            fechas.append(hora_actual)
            hora_actual += intervalo
            duracion_horas -= intervalo_minutos / 60

        vector_fechas = []
        for fecha in fechas:
            vector_fechas.append(fecha.strftime('%H:%M'))

        return vector_fechas

    Duracion = np.arange(intervalo, duracion + intervalo, intervalo)
    I = []
    for dur in range(0, len(Duracion)):
        int = calculoIntensidad(k, m, n, Duracion[dur], TR)
        I.append(int)

    ProfAcum = [Duracion[i] * I[i] / 60 for i in range(0, len(I))]
    ProfInc = np.diff(np.array(ProfAcum), prepend=0)
    Prec = organizar_vector(ProfInc)
    ints = crear_vector_fechas(duracion / 60, intervalo)
    bloquesAlternos = pd.DataFrame([ints, Duracion, I, ProfAcum, ProfInc, Prec]).transpose()
    bloquesAlternos.columns = ['Intervalos', 'Duración', 'Intesidad', 'Profundidad acumulada',
                               'Profundidad incremental', 'Precipitación']
    bloquesAlternos.Intervalos = pd.to_datetime(bloquesAlternos.Intervalos)
    bloquesAlternos['Intervalos'] = bloquesAlternos['Intervalos'].dt.strftime('%H:%M')

    bloquesAlternos.to_excel(ruta_guardado + f'/Lluvia de diseño {TR} años.xlsx', index=False)

    plt.figure(figsize=(15, 6))
    x = bloquesAlternos['Intervalos']
    y = bloquesAlternos['Precipitación']
    plt.bar(x, y, zorder=2, color='#000FC5',label = f'Periodo de retorno: {TR} años')
    plt.xticks(size='large', color='k', rotation=45)
    plt.yticks(size='large', color='k', rotation=0)
    plt.ylabel('Precipitation [mm]', fontweight='bold')
    plt.xlim(x[0], x[len(x) - 1])
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth='0.5', zorder=0)
    plt.grid(which='minor', linestyle=':', linewidth='0.5', zorder=0)
    plt.legend()
    plt.savefig(ruta_guardado + f'/Hietograma {TR} años.png', bbox_inches='tight')
    plt.show()

    return bloquesAlternos

def graficarHidrogramasRAS(ruta_datos,hidrogramas,label,ruta_guardado):
    Q = pd.read_excel(ruta_datos)
    Q = Q.iloc[6:]
    Q = Q.drop(Q.columns[0], axis = 1)
    Q.columns = ['Fecha'] + ['TR ' + str(item) for item in hidrogramas]
    Q['Fecha'] = pd.to_datetime(Q['Fecha'], format='%Y-%m-%d %H:%M:%S')
    Q['Fecha'] = Q['Fecha'].dt.strftime('%H:%M')
    Q.set_index('Fecha',inplace= True)

    time = Q.index

    for columna in Q.columns:
        Q[columna] = pd.to_numeric(Q[columna], errors='coerce')

    plt.figure(figsize=(15, 6))
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FFA500', '#800080', '#008000', '#800000']
    for i in range(len(hidrogramas)):
        # print(Q[Q.columns[i]])
        plt.plot(time, Q[Q.columns[i]].values*1000, color = colors[i], label = f'{label} : {hidrogramas[i]}')

    plt.ylim(0)
    plt.xlim(time[0], time[len(time) - 1])
    plt.xticks(rotation=45, size='medium')

    plt.ylabel('Caudal [l/s]',fontsize = 12,fontweight = 'bold')
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth='0.5')
    plt.grid(which='minor', linestyle=':', linewidth='0.5')
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.legend()
    plt.savefig(ruta_guardado + '/Hidrogramas.png', bbox_inches="tight")
    plt.show()