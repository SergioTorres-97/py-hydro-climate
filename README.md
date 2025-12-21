<div align="center">

```
    ╔════════════════════════════════════════════════════════╗
    ║                                                        ║
    ║          ██████╗ ██╗   ██╗      ██╗  ██╗              ║
    ║          ██╔══██╗╚██╗ ██╔╝      ██║  ██║              ║
    ║          ██████╔╝ ╚████╔╝ █████╗███████║              ║
    ║          ██╔═══╝   ╚██╔╝  ╚════╝██╔══██║              ║
    ║          ██║        ██║         ██║  ██║              ║
    ║          ╚═╝        ╚═╝         ╚═╝  ╚═╝              ║
    ║                                                        ║
    ║              ~ hydro · climate ~                       ║
    ║                                                        ║
    ║         🌧️  💧  ☁️  📊  🌡️  📈                          ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
```

# py-hydro.climate

**Herramientas Python para análisis hidrometeorológico y climático**

*Transforma datos climáticos multifuente en insights visuales*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📋 Descripción del Proyecto

**py-hydro.climate** es un conjunto de herramientas de **pre-procesamiento, análisis estadístico y visualización** de datos hidrometeorológicos y climáticos provenientes de **múltiples fuentes**. El objetivo es facilitar el análisis de series temporales climáticas mediante funciones modulares y reutilizables.

### ¿Qué puedes hacer con este proyecto?

- **Leer y procesar** datos de múltiples fuentes (AQTS, NASA, NetCDF)
- **Realizar análisis estadísticos** sobre series temporales climáticas
- **Generar visualizaciones** profesionales (boxplots, histogramas mensuales)
- **Automatizar** flujos de trabajo de análisis climático

---

## ✨ Características Principales

### 📁 Lectura de Datos Multifuente

El módulo `lecturas_datos.py` soporta:

- **AQTS Web** - Datos de estaciones hidrometeorológicas
- **AQTS Local** - Archivos CSV con formato AQTS
- **NASA POWER** - Datos satelitales y reanálisis
- **NetCDF** - Cubos de datos climáticos multidimensionales

### 📊 Análisis Estadístico

El módulo `estadisticos.py` incluye:

- Cálculo de **promedios mensuales** con filtrado por cantidad de datos
- **Agregaciones temporales** personalizables (diario, mensual, anual)
- Manejo inteligente de **datos faltantes**

### 📈 Visualizaciones Interactivas

El módulo `graficas.py` genera:

- **Boxplots mensuales** con medias destacadas
- **Histogramas mensuales** con distribuciones y estadísticas
- Paletas de colores profesionales (YlGnBu)
- Cuadrículas y leyendas configurables

---

## 📦 Estructura del Proyecto

```
Climatologia/
│
├── scripts/
│   ├── lecturas_datos.py              # Funciones de lectura de datos
│   ├── estadisticos.py                 # Análisis estadístico
│   ├── graficas.py                     # Visualizaciones
│   ├── auxiliares_procesamiento.py    # Utilidades de procesamiento
│   └── auxiliares_generales.py        # Funciones auxiliares
│
├── tests/                              # Tests unitarios (en desarrollo)
│
└── README.md                           # Este archivo
```

---

## 🚀 Instalación Rápida

### Requisitos Previos

- Python 3.8+
- pip

### Instalación

1. **Clona el repositorio**

```bash
git clone <url-del-repositorio>
cd Climatologia
```

2. **Crea un entorno virtual**

```bash
python -m venv .venv
```

3. **Activa el entorno virtual**

- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```

- **Linux/Mac:**
  ```bash
  source .venv/bin/activate
  ```

4. **Instala las dependencias**

```bash
pip install pandas numpy matplotlib seaborn xarray openpyxl
```

---

## 💻 Guía de Uso Rápida

### Ejemplo 1: Leer datos de AQTS Web

```python
from scripts.lecturas_datos import AbrirArchivoAqtsWeb

# Cargar datos de precipitación
datos = AbrirArchivoAqtsWeb('ruta/a/tu/archivo.csv')
print(datos.head())
```

### Ejemplo 2: Análisis estadístico mensual

```python
from scripts.estadisticos import PromediosIDEAM

# Calcular promedios mensuales (requiere mínimo 20 datos por mes)
promedios = PromediosIDEAM(datos, numDatos=20, agregado='ME', estadistico='mean')
```

### Ejemplo 3: Generar boxplot mensual

```python
from scripts.graficas import BoxplotMensual

# Visualizar distribución mensual
BoxplotMensual(
    promedios,
    ylabel='Precipitación (mm)',
    titulo='Distribución Mensual de Precipitación'
)
```

### Ejemplo 4: Extraer datos de NetCDF

```python
from scripts.lecturas_datos import ExtraccionCuboDatos

# Extraer serie temporal de una coordenada específica
datos_nc = ExtraccionCuboDatos(
    ruta='path/to/netcdf/folder',
    variable='precipitacion',
    coordenadas=(4.6097, -74.0817)  # Bogotá, Colombia
)
```

---

## 🎨 Ejemplos Visuales

### Boxplot Mensual
Visualiza la distribución de datos climáticos por mes, incluyendo:
- Cuartiles y valores atípicos
- Media mensual (puntos rojos)
- Paleta de colores YlGnBu

### Histogramas Mensuales
Genera una matriz de 12 histogramas (uno por mes) mostrando:
- Distribución de frecuencias
- Curva de densidad (KDE)
- Media y mediana

---

## 🤝 Contribuir

**¡Tus contribuciones son bienvenidas!**

Si tienes ideas para mejorar este proyecto:

1. **Reporta bugs** abriendo un issue
2. **Propón nuevas funcionalidades** en la sección de issues
3. **Envía pull requests** con mejoras o correcciones
4. **Comparte tu feedback** sobre cómo usas el proyecto

### ¿Cómo contribuir?

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva funcionalidad'`)
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 🗺️ Roadmap

- [ ] Agregar tests unitarios completos
- [ ] Implementar lectura de más formatos (GeoTIFF, HDF5)
- [ ] Crear notebooks de ejemplo con casos de uso reales
- [ ] Documentación API completa
- [ ] Integración con APIs climáticas (OpenWeather, NOAA)
- [ ] Dashboard interactivo con Streamlit/Dash

---

## 💬 Feedback y Soporte

**¿Necesitas ayuda o tienes sugerencias?**

- Abre un **Issue** en este repositorio
- Envía tus comentarios sobre qué te gustaría ver implementado
- Comparte ejemplos de uso interesantes

---

## 🛠️ Tecnologías Utilizadas

- **pandas** - Manipulación de datos tabulares
- **numpy** - Operaciones numéricas
- **matplotlib** - Visualización base
- **seaborn** - Visualizaciones estadísticas elegantes
- **xarray** - Manejo de datos multidimensionales (NetCDF)
- **openpyxl** - Exportación a Excel

---

## 👨‍💻 Autor

**Sergio Torres**
- Email: [sertorrespira@gmail.com](mailto:sertorrespira@gmail.com)

---

## 📄 Licencia

Este proyecto está disponible bajo la licencia MIT.

---

<div align="center">

**¿Listo para explorar tus datos climáticos?**

Clona el repo y empieza a analizar.

**¡Gracias por tu interés en este proyecto!**

Si te resultó útil, considera darle una ⭐ al repositorio

</div>
