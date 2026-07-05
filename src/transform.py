import json
from pathlib import Path

import pandas as pd


BRONZE_PATH = Path("data/bronze")
SILVER_PATH = Path("data/silver")


NOMBRES_INDICADORES = {
    "PN01206PM": "Tipo de cambio promedio mensual",
    "PN01271PM": "Inflación mensual",
    "PN01273PM": "Inflación anual",
    "PN01728AM": "PBI variación interanual",
    "PD04722MM": "Tasa de referencia",
}


MESES_ES = {
    "Ene": 1,
    "Feb": 2,
    "Mar": 3,
    "Abr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Ago": 8,
    "Sep": 9,
    "Set": 9,
    "Oct": 10,
    "Nov": 11,
    "Dic": 12,
}


def obtener_ultimo_json_bronze() -> Path:
    """
    Busca el último archivo JSON descargado en la capa bronze.
    """
    archivos_json = list(BRONZE_PATH.glob("*.json"))

    if not archivos_json:
        raise FileNotFoundError(
            "No se encontraron archivos JSON en data/bronze. "
            "Primero ejecuta python src/extract.py"
        )

    ultimo_archivo = max(archivos_json, key=lambda archivo: archivo.stat().st_mtime)
    return ultimo_archivo


def leer_json(ruta_archivo: Path) -> dict:
    """
    Lee un archivo JSON crudo descargado desde la API del BCRP.
    """
    with open(ruta_archivo, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def convertir_periodo_a_fecha(periodo: str) -> pd.Timestamp:
    """
    Convierte periodos del BCRP a fecha.

    Ejemplos posibles:
    Ene.2020
    Feb.2021
    Mar.2022
    """
    periodo = periodo.replace(".", " ").strip()
    partes = periodo.split()

    if len(partes) != 2:
        raise ValueError(f"No se pudo interpretar el periodo: {periodo}")

    mes_texto = partes[0]
    anio = int(partes[1])

    mes = MESES_ES.get(mes_texto)

    if mes is None:
        raise ValueError(f"Mes no reconocido en el periodo: {periodo}")

    return pd.Timestamp(year=anio, month=mes, day=1)


def convertir_valor(valor):
    """
    Convierte valores del BCRP a número decimal.
    Maneja valores vacíos o no disponibles.
    """
    if valor is None:
        return None

    valor = str(valor).strip()

    if valor in ["", "n.d.", "ND", "N.D.", "-"]:
        return None

    try:
        return float(valor.replace(",", ""))
    except ValueError:
        return None


def transformar_json_a_dataframe(data: dict) -> pd.DataFrame:
    """
    Transforma el JSON del BCRP en una tabla limpia.
    """
    series = data.get("config", {}).get("series", [])
    periods = data.get("periods", [])

    if not series:
        raise ValueError("El JSON no contiene información de series.")

    if not periods:
        raise ValueError("El JSON no contiene periodos.")

    codigos_series = [serie["name"] for serie in series]

    registros = []

    for periodo in periods:
        fecha = convertir_periodo_a_fecha(periodo["name"])
        valores = periodo.get("values", [])

        for codigo, valor in zip(codigos_series, valores):
            registros.append(
                {
                    "fecha": fecha,
                    "anio": fecha.year,
                    "mes": fecha.month,
                    "trimestre": f"T{fecha.quarter}",
                    "codigo_indicador": codigo,
                    "nombre_indicador": NOMBRES_INDICADORES.get(codigo, codigo),
                    "valor": convertir_valor(valor),
                    "frecuencia": "Mensual",
                    "fuente": "BCRP",
                }
            )

    df = pd.DataFrame(registros)

    df = df.sort_values(
        by=["codigo_indicador", "fecha"]
    ).reset_index(drop=True)

    return df


def guardar_csv(df: pd.DataFrame, nombre_archivo: str) -> Path:
    """
    Guarda el DataFrame limpio en la capa silver.
    """
    SILVER_PATH.mkdir(parents=True, exist_ok=True)

    ruta_salida = SILVER_PATH / nombre_archivo
    df.to_csv(ruta_salida, index=False, encoding="utf-8-sig")

    return ruta_salida


def main():
    print("Iniciando transformación de datos BCRP...")

    archivo_bronze = obtener_ultimo_json_bronze()
    print(f"Archivo bronze utilizado: {archivo_bronze}")

    data = leer_json(archivo_bronze)

    df_limpio = transformar_json_a_dataframe(data)

    ruta_salida = guardar_csv(
        df_limpio,
        "bcrp_indicadores_mensuales_clean.csv"
    )

    print("Transformación completada correctamente.")
    print(f"Archivo guardado en: {ruta_salida}")
    print(f"Filas generadas: {len(df_limpio)}")
    print(f"Indicadores procesados: {df_limpio['codigo_indicador'].nunique()}")

    print("\nVista previa:")
    print(df_limpio.head(10))


if __name__ == "__main__":
    main()