# Dashboard Económico del Perú - API BCRP

## Descripción

Este proyecto presenta un análisis de los principales indicadores económicos del Perú utilizando datos obtenidos desde la API pública del Banco Central de Reserva del Perú (BCRP).

El proyecto desarrolla un flujo completo de análisis de datos que incluye extracción desde una API, limpieza y transformación con Python, generación de un modelo analítico, almacenamiento en SQLite y visualización mediante un dashboard interactivo en Power BI.

Este repositorio fue desarrollado como proyecto de portafolio para demostrar habilidades en análisis de datos, manejo de APIs, procesamiento de series de tiempo, modelado de datos, Power BI y DAX.

---

## Objetivo del proyecto

Analizar la evolución económica del Perú mediante indicadores macroeconómicos como tipo de cambio, inflación, PBI y tasa de referencia, construyendo un dashboard que permita visualizar tendencias, comparar indicadores y revisar KPIs económicos relevantes.

---

## Fuente de datos

Los datos fueron obtenidos desde la API pública del BCRP.

URL base de la API:

```text
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/
```

Ejemplo de consulta utilizada:

```text
https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01206PM-PN01271PM-PN01273PM-PN01728AM-PD04722MM/json/2020-1/2026-6/esp
```

---

## Indicadores utilizados

| Indicador | Código BCRP | Frecuencia | Unidad |
|---|---|---|---|
| Tipo de cambio promedio mensual | PN01206PM | Mensual | Soles por dólar |
| Inflación mensual | PN01271PM | Mensual | Porcentaje |
| Inflación anual | PN01273PM | Mensual | Porcentaje |
| PBI variación interanual | PN01728AM | Mensual | Porcentaje |
| Tasa de referencia | PD04722MM | Mensual | Porcentaje |

---

## Tecnologías utilizadas

- Python
- Requests
- Pandas
- SQLAlchemy
- SQLite
- Power BI
- DAX
- Git
- GitHub

---

## Arquitectura del proyecto

El proyecto sigue una arquitectura por capas:

```text
API BCRP
   ↓
Extracción con Python Requests
   ↓
Bronze: datos crudos en formato JSON
   ↓
Silver: datos limpios y transformados
   ↓
Gold: modelo analítico para Power BI
   ↓
Dashboard en Power BI
```

---

## Estructura del repositorio

```text
dashboard-economico-peru-bcrp/
│
├── data/
│   ├── bronze/          # Datos crudos extraídos desde la API del BCRP
│   ├── silver/          # Datos limpios y transformados
│   └── gold/            # Datos finales para Power BI y SQLite
│
├── images/              # Capturas del dashboard
├── powerbi/             # Archivo .pbix del dashboard
├── src/                 # Scripts Python del proceso ETL
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Proceso ETL

### 1. Extracción

El script `src/extract.py` se conecta a la API del BCRP y descarga las series económicas en formato JSON.

En esta etapa se realiza:

- Construcción de la URL de consulta.
- Conexión a la API del BCRP.
- Descarga de indicadores económicos.
- Validación básica de la respuesta.
- Almacenamiento del JSON crudo.

Los datos crudos se guardan en:

```text
data/bronze/
```

---

### 2. Transformación

El script `src/transform.py` limpia y transforma la información descargada desde la API.

En esta etapa se realiza:

- Conversión de periodos a fechas.
- Conversión de valores a formato numérico.
- Corrección de formatos decimales.
- Estandarización de códigos de indicadores.
- Asignación de nombres descriptivos.
- Creación de columnas de año, mes y trimestre.
- Generación de una tabla limpia para análisis.

Los datos procesados se guardan en:

```text
data/silver/
```

---

### 3. Carga

El script `src/load.py` genera el modelo analítico final.

En esta etapa se crean las siguientes tablas:

- `dim_fecha.csv`
- `dim_indicador.csv`
- `fact_indicadores.csv`
- `bcrp_economia_peru.db`

Los datos finales se guardan en:

```text
data/gold/
```

---

## Modelo de datos

El modelo utilizado en Power BI sigue una estructura tipo estrella:

```text
dim_fecha  ───<  fact_indicadores  >───  dim_indicador
```

### Tabla `dim_fecha`

Contiene la información temporal del modelo.

Columnas principales:

- `fecha_id`
- `fecha`
- `anio`
- `mes`
- `nombre_mes`
- `trimestre`
- `anio_mes`

---

### Tabla `dim_indicador`

Contiene la información descriptiva de cada indicador económico.

Columnas principales:

- `indicador_id`
- `codigo_indicador`
- `nombre_indicador`
- `categoria`
- `unidad`
- `frecuencia`
- `fuente`

---

### Tabla `fact_indicadores`

Contiene los valores mensuales de los indicadores económicos.

Columnas principales:

- `fecha_id`
- `indicador_id`
- `codigo_indicador`
- `fecha`
- `anio`
- `mes`
- `trimestre`
- `valor`

---

## Dashboard en Power BI

El dashboard está dividido en cuatro páginas principales.

---

### 1. Resumen económico

Esta página presenta una vista general de los principales indicadores económicos del Perú.

Incluye:

- KPI de tipo de cambio promedio mensual.
- KPI de inflación mensual.
- KPI de inflación anual.
- KPI de PBI en variación interanual.
- KPI de tasa de referencia.
- Gráfico de evolución mensual de indicadores.
- Segmentadores por año e indicador.

![Resumen económico](images/dashboard_resumen.png)

---

### 2. Inflación

Esta página analiza la evolución de la inflación mensual y anual.

Incluye:

- Última inflación mensual disponible.
- Última inflación anual disponible.
- Evolución mensual de la inflación.
- Comparación entre inflación mensual e inflación anual.
- Promedios anuales.

![Inflación](images/dashboard_inflacion.png)

---

### 3. Tipo de cambio y tasa de referencia

Esta página muestra la evolución del tipo de cambio promedio mensual y de la tasa de referencia.

Incluye:

- Último tipo de cambio disponible.
- Última tasa de referencia disponible.
- Evolución del tipo de cambio.
- Evolución de la tasa de referencia.
- Comparación entre tipo de cambio y política monetaria.

![Tipo de cambio y tasa de referencia](images/dashboard_tipo_cambio.png)

---

### 4. PBI y actividad económica

Esta página analiza la evolución del PBI en variación interanual.

Incluye:

- Última variación del PBI disponible.
- Evolución mensual del PBI.
- Promedio anual de variación del PBI.
- Comparación entre PBI y tasa de referencia.
- Tabla de detalle mensual.

![PBI y actividad económica](images/dashboard_pbi.png)

---

## Medidas DAX principales

El dashboard utiliza medidas DAX para calcular KPIs, valores dinámicos y gráficos de tendencia.

### Medida base

```DAX
Valor Indicador =
AVERAGE(fact_indicadores[valor])
```

---

### Valores por indicador

```DAX
Valor Tipo de Cambio =
CALCULATE(
    [Valor Indicador];
    dim_indicador[codigo_indicador] = "PN01206PM"
)
```

```DAX
Valor Inflación Mensual =
CALCULATE(
    [Valor Indicador];
    dim_indicador[codigo_indicador] = "PN01271PM"
)
```

```DAX
Valor Inflación Anual =
CALCULATE(
    [Valor Indicador];
    dim_indicador[codigo_indicador] = "PN01273PM"
)
```

```DAX
Valor PBI =
CALCULATE(
    [Valor Indicador];
    dim_indicador[codigo_indicador] = "PN01728AM"
)
```

```DAX
Valor Tasa de Referencia =
CALCULATE(
    [Valor Indicador];
    dim_indicador[codigo_indicador] = "PD04722MM"
)
```

---

### KPIs de último valor disponible

```DAX
Último Tipo de Cambio =
VAR UltimaFecha =
    CALCULATE(
        MAX(fact_indicadores[fecha]);
        dim_indicador[codigo_indicador] = "PN01206PM";
        NOT(ISBLANK(fact_indicadores[valor]))
    )
RETURN
    CALCULATE(
        [Valor Tipo de Cambio];
        fact_indicadores[fecha] = UltimaFecha
    )
```

```DAX
Última Inflación Mensual =
VAR UltimaFecha =
    CALCULATE(
        MAX(fact_indicadores[fecha]);
        dim_indicador[codigo_indicador] = "PN01271PM";
        NOT(ISBLANK(fact_indicadores[valor]))
    )
RETURN
    CALCULATE(
        [Valor Inflación Mensual];
        fact_indicadores[fecha] = UltimaFecha
    )
```

```DAX
Última Inflación Anual =
VAR UltimaFecha =
    CALCULATE(
        MAX(fact_indicadores[fecha]);
        dim_indicador[codigo_indicador] = "PN01273PM";
        NOT(ISBLANK(fact_indicadores[valor]))
    )
RETURN
    CALCULATE(
        [Valor Inflación Anual];
        fact_indicadores[fecha] = UltimaFecha
    )
```

```DAX
Último PBI =
VAR UltimaFecha =
    CALCULATE(
        MAX(fact_indicadores[fecha]);
        dim_indicador[codigo_indicador] = "PN01728AM";
        NOT(ISBLANK(fact_indicadores[valor]))
    )
RETURN
    CALCULATE(
        [Valor PBI];
        fact_indicadores[fecha] = UltimaFecha
    )
```

```DAX
Última Tasa de Referencia =
VAR UltimaFecha =
    CALCULATE(
        MAX(fact_indicadores[fecha]);
        dim_indicador[codigo_indicador] = "PD04722MM";
        NOT(ISBLANK(fact_indicadores[valor]))
    )
RETURN
    CALCULATE(
        [Valor Tasa de Referencia];
        fact_indicadores[fecha] = UltimaFecha
    )
```

---

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/enleam/dashboard-economico-peru-bcrp.git
cd dashboard-economico-peru-bcrp
```

---

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

---

### 3. Activar entorno virtual

En Windows PowerShell:

```bash
.\.venv\Scripts\activate
```

---

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 5. Ejecutar el flujo ETL

```bash
python src/extract.py
python src/transform.py
python src/load.py
```

---

### 6. Abrir el dashboard

Abrir el archivo de Power BI ubicado en:

```text
powerbi/dashboard_economico_peru.pbix
```

---

## Resultados esperados

El proyecto permite analizar la evolución mensual de indicadores económicos del Perú, identificar tendencias de inflación, observar cambios en el tipo de cambio, analizar la variación del PBI y revisar la evolución de la tasa de referencia.

El dashboard facilita la comparación de indicadores macroeconómicos mediante KPIs, gráficos de líneas, gráficos de columnas, segmentadores y medidas DAX.

---

## Conclusiones

Este proyecto demuestra la construcción de un flujo completo de análisis de datos, desde la extracción de información económica real mediante una API pública hasta la creación de un dashboard interactivo en Power BI.

Además, permite aplicar conceptos importantes para un perfil de analista de datos, como limpieza de datos, modelado analítico, series de tiempo, visualización de información y creación de medidas DAX.

---

## Futuras mejoras

- Agregar más indicadores económicos del BCRP.
- Incorporar reservas internacionales.
- Agregar indicadores laborales.
- Automatizar la actualización de datos.
- Crear un notebook de análisis exploratorio.
- Publicar el dashboard en Power BI Service.
- Agregar validaciones de calidad de datos.
- Incorporar análisis comparativo por periodos económicos.

---

## Autor

**Flavio Enrique Huapaya Bohorquez**

Estudiante de Ingeniería de Sistemas  
Universidad Nacional Mayor de San Marcos

---

## Licencia

Este proyecto se desarrolla con fines educativos y de portafolio.

Los datos pertenecen a sus respectivas fuentes oficiales.