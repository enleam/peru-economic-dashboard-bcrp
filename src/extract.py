import json
from datetime import datetime
from pathlib import Path

import requests


# URL base de la API del BCRP
BCRP_API_BASE = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"


# Configuración de las series económicas mensuales
SERIES_MENSUALES = {
    "PN01206PM": "Tipo de cambio - Interbancario venta promedio mensual",
    "PN01271PM": "Inflación mensual - IPC var% mensual",
    "PN01273PM": "Inflación anual - IPC var% 12 meses",
    "PN01728AM": "PBI - Variación porcentual interanual",
    "PD04722MM": "Tasa de referencia de política monetaria",
}


# Periodo de análisis
PERIODO_INICIAL = "2020-1"
PERIODO_FINAL = "2026-6"
IDIOMA = "esp"
FORMATO = "json"


# Carpeta donde se guardarán los datos crudos
BRONZE_PATH = Path("data/bronze")


def construir_url(series: dict, formato: str, periodo_inicial: str, periodo_final: str, idioma: str) -> str:
    """
    Construye la URL de consulta para la API del BCRP.
    """
    codigos_series = "-".join(series.keys())

    url = (
        f"{BCRP_API_BASE}/"
        f"{codigos_series}/"
        f"{formato}/"
        f"{periodo_inicial}/"
        f"{periodo_final}/"
        f"{idioma}"
    )

    return url


def extraer_datos_bcrp(url: str) -> dict:
    """
    Realiza la petición GET a la API del BCRP y devuelve los datos en formato JSON.
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        if "periods" not in data:
            raise ValueError("La respuesta de la API no contiene la clave 'periods'.")

        return data

    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Error al conectarse con la API del BCRP: {error}")

    except json.JSONDecodeError:
        raise RuntimeError("La respuesta de la API no tiene formato JSON válido.")


def guardar_json(data: dict, nombre_archivo: str) -> Path:
    """
    Guarda los datos crudos en la capa bronze.
    """
    BRONZE_PATH.mkdir(parents=True, exist_ok=True)

    ruta_salida = BRONZE_PATH / nombre_archivo

    with open(ruta_salida, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return ruta_salida


def main():
    print("Iniciando extracción de datos desde la API del BCRP...")

    url = construir_url(
        series=SERIES_MENSUALES,
        formato=FORMATO,
        periodo_inicial=PERIODO_INICIAL,
        periodo_final=PERIODO_FINAL,
        idioma=IDIOMA,
    )

    print("URL de consulta:")
    print(url)

    data = extraer_datos_bcrp(url)

    fecha_ejecucion = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"bcrp_indicadores_mensuales_raw_{fecha_ejecucion}.json"

    ruta_salida = guardar_json(data, nombre_archivo)

    print("Extracción completada correctamente.")
    print(f"Archivo guardado en: {ruta_salida}")
    print(f"Cantidad de periodos descargados: {len(data.get('periods', []))}")


if __name__ == "__main__":
    main()