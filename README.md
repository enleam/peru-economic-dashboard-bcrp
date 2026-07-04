# Dashboard Económico del Perú - API BCRP

## Descripción del proyecto

Este proyecto tiene como objetivo analizar los principales indicadores económicos del Perú utilizando datos obtenidos desde la API pública del Banco Central de Reserva del Perú (BCRP).

El proyecto consiste en construir un flujo de trabajo de análisis de datos que incluye extracción, limpieza, transformación, modelado y visualización de series económicas mediante Python, Pandas, SQL y Power BI.

Este repositorio está pensado como un proyecto de portafolio para demostrar habilidades de análisis de datos, manejo de APIs, procesamiento de series de tiempo y creación de dashboards interactivos.

## Objetivo

Desarrollar un proyecto de análisis económico del Perú que permita consultar, procesar y visualizar indicadores macroeconómicos relevantes, como inflación, tipo de cambio, PBI y tasa de referencia.

## Fuente de datos

Los datos serán obtenidos desde la API pública del BCRP, la cual permite consultar series estadísticas económicas en diferentes formatos como JSON, CSV, XLS, XML y TXT.

## Indicadores económicos iniciales

En la primera versión del proyecto se trabajará con los siguientes indicadores:

* Tipo de cambio
* Inflación mensual
* Inflación anual
* Variación del PBI
* Tasa de referencia

## Tecnologías utilizadas

* Python
* Requests
* Pandas
* SQL / SQLite
* Power BI
* DAX
* Git
* GitHub

## Estructura del proyecto

```text
dashboard-economico-peru-bcrp/
│
├── data/
│   ├── bronze/          # Datos crudos extraídos desde la API del BCRP
│   ├── silver/          # Datos limpios y transformados
│   └── gold/            # Datos finales listos para Power BI
│
├── notebooks/           # Notebooks de exploración y análisis
├── src/                 # Scripts de Python para el proceso ETL
├── sql/                 # Scripts SQL
├── powerbi/             # Archivo del dashboard en Power BI
├── images/              # Capturas del dashboard
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Roadmap del proyecto

### Sprint 0: Configuración inicial del proyecto

* Crear la estructura de carpetas
* Crear el entorno virtual de Python
* Instalar dependencias iniciales
* Crear el archivo `requirements.txt`
* Crear el archivo `.gitignore`
* Crear el archivo `README.md`
* Inicializar el repositorio con Git
* Subir el repositorio a GitHub

### Sprint 1: Extracción de datos desde la API del BCRP

* Conectarse a la API del BCRP
* Consultar series económicas en formato JSON
* Descargar indicadores económicos iniciales
* Guardar los datos crudos en la capa `bronze`

### Sprint 2: Limpieza y transformación de datos

* Limpiar fechas
* Convertir valores a formato numérico
* Estandarizar nombres de indicadores
* Crear columnas de año, mes y trimestre
* Transformar el tipo de cambio diario a frecuencia mensual
* Guardar datos procesados en la capa `silver`

### Sprint 3: Modelo analítico

* Crear tabla de hechos de indicadores económicos
* Crear tabla de dimensión de fechas
* Crear tabla de dimensión de indicadores
* Preparar los archivos finales para Power BI
* Guardar los datos finales en la capa `gold`

### Sprint 4: Dashboard en Power BI

* Conectar Power BI con los datos finales
* Crear visualizaciones de series de tiempo
* Crear KPIs económicos
* Agregar segmentadores por año e indicador
* Diseñar páginas del dashboard

### Sprint 5: Medidas DAX y análisis económico

* Crear medidas DAX
* Calcular último valor disponible
* Calcular promedios anuales
* Calcular variaciones porcentuales
* Redactar principales hallazgos económicos

### Sprint 6: Documentación final

* Mejorar el README
* Agregar capturas del dashboard
* Explicar el flujo ETL
* Documentar las fuentes de datos
* Agregar instrucciones de ejecución
* Preparar el repositorio para portafolio

## Resultado esperado

El resultado final será un dashboard interactivo en Power BI que permita analizar la evolución económica del Perú a través de indicadores como inflación, tipo de cambio, PBI y tasa de referencia.

## Estado del proyecto

Proyecto en desarrollo.

Fase actual: Sprint 0 - Configuración inicial del proyecto.