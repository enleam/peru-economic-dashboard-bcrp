from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


SILVER_PATH = Path("data/silver")
GOLD_PATH = Path("data/gold")

ARCHIVO_SILVER = SILVER_PATH / "bcrp_indicadores_mensuales_clean.csv"

ARCHIVO_FACT = GOLD_PATH / "fact_indicadores.csv"
ARCHIVO_DIM_FECHA = GOLD_PATH / "dim_fecha.csv"
ARCHIVO_DIM_INDICADOR = GOLD_PATH / "dim_indicador.csv"
ARCHIVO_SQLITE = GOLD_PATH / "bcrp_economia_peru.db"


def leer_datos_limpios() -> pd.DataFrame:
    """
    Lee el archivo limpio generado en la capa silver.
    """
    if not ARCHIVO_SILVER.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo {ARCHIVO_SILVER}. "
            "Primero ejecuta python src/transform.py"
        )

    df = pd.read_csv(ARCHIVO_SILVER)
    df["fecha"] = pd.to_datetime(df["fecha"])

    return df


def crear_dim_fecha(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea la dimensión de fechas para el modelo analítico.
    """
    fechas = (
        df[["fecha"]]
        .drop_duplicates()
        .sort_values("fecha")
        .reset_index(drop=True)
    )

    fechas["fecha_id"] = fechas["fecha"].dt.strftime("%Y%m%d").astype(int)
    fechas["anio"] = fechas["fecha"].dt.year
    fechas["mes"] = fechas["fecha"].dt.month

    nombres_meses = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre",
    }

    fechas["nombre_mes"] = fechas["mes"].map(nombres_meses)
    fechas["trimestre"] = "T" + fechas["fecha"].dt.quarter.astype(str)
    fechas["anio_mes"] = fechas["fecha"].dt.strftime("%Y-%m")

    fechas = fechas[
        [
            "fecha_id",
            "fecha",
            "anio",
            "mes",
            "nombre_mes",
            "trimestre",
            "anio_mes",
        ]
    ]

    return fechas


def clasificar_categoria(codigo_indicador: str) -> str:
    """
    Clasifica cada indicador económico en una categoría.
    """
    categorias = {
        "PN01206PM": "Tipo de cambio",
        "PN01271PM": "Inflación",
        "PN01273PM": "Inflación",
        "PN01728AM": "Actividad económica",
        "PD04722MM": "Política monetaria",
    }

    return categorias.get(codigo_indicador, "Otros")


def definir_unidad(codigo_indicador: str) -> str:
    """
    Define la unidad de medida de cada indicador.
    """
    unidades = {
        "PN01206PM": "Soles por dólar",
        "PN01271PM": "Porcentaje",
        "PN01273PM": "Porcentaje",
        "PN01728AM": "Porcentaje",
        "PD04722MM": "Porcentaje",
    }

    return unidades.get(codigo_indicador, "No definido")


def crear_dim_indicador(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea la dimensión de indicadores económicos.
    """
    indicadores = (
        df[["codigo_indicador", "nombre_indicador", "frecuencia", "fuente"]]
        .drop_duplicates()
        .sort_values("codigo_indicador")
        .reset_index(drop=True)
    )

    indicadores["indicador_id"] = range(1, len(indicadores) + 1)
    indicadores["categoria"] = indicadores["codigo_indicador"].apply(
        clasificar_categoria
    )
    indicadores["unidad"] = indicadores["codigo_indicador"].apply(
        definir_unidad
    )

    indicadores = indicadores[
        [
            "indicador_id",
            "codigo_indicador",
            "nombre_indicador",
            "categoria",
            "unidad",
            "frecuencia",
            "fuente",
        ]
    ]

    return indicadores


def crear_fact_indicadores(
    df: pd.DataFrame,
    dim_indicador: pd.DataFrame
) -> pd.DataFrame:
    """
    Crea la tabla de hechos de indicadores económicos.
    """
    fact = df.copy()

    fact["fecha_id"] = fact["fecha"].dt.strftime("%Y%m%d").astype(int)

    fact = fact.merge(
        dim_indicador[["indicador_id", "codigo_indicador"]],
        on="codigo_indicador",
        how="left"
    )

    fact = fact[
        [
            "fecha_id",
            "indicador_id",
            "codigo_indicador",
            "fecha",
            "anio",
            "mes",
            "trimestre",
            "valor",
        ]
    ]

    fact = fact.sort_values(
        by=["indicador_id", "fecha"]
    ).reset_index(drop=True)

    return fact


def guardar_csv(df: pd.DataFrame, ruta: Path) -> None:
    """
    Guarda un DataFrame como archivo CSV.
    """
    df.to_csv(ruta, index=False, encoding="utf-8-sig")


def guardar_sqlite(
    fact_indicadores: pd.DataFrame,
    dim_fecha: pd.DataFrame,
    dim_indicador: pd.DataFrame
) -> None:
    """
    Guarda las tablas finales en una base de datos SQLite.
    """
    engine = create_engine(f"sqlite:///{ARCHIVO_SQLITE}")

    dim_fecha.to_sql(
        "dim_fecha",
        engine,
        if_exists="replace",
        index=False
    )

    dim_indicador.to_sql(
        "dim_indicador",
        engine,
        if_exists="replace",
        index=False
    )

    fact_indicadores.to_sql(
        "fact_indicadores",
        engine,
        if_exists="replace",
        index=False
    )


def main():
    print("Iniciando creación del modelo analítico...")

    GOLD_PATH.mkdir(parents=True, exist_ok=True)

    df = leer_datos_limpios()

    dim_fecha = crear_dim_fecha(df)
    dim_indicador = crear_dim_indicador(df)
    fact_indicadores = crear_fact_indicadores(
        df,
        dim_indicador
    )

    guardar_csv(dim_fecha, ARCHIVO_DIM_FECHA)
    guardar_csv(dim_indicador, ARCHIVO_DIM_INDICADOR)
    guardar_csv(fact_indicadores, ARCHIVO_FACT)

    guardar_sqlite(
        fact_indicadores,
        dim_fecha,
        dim_indicador
    )

    print("Modelo analítico creado correctamente.")
    print(f"Archivo generado: {ARCHIVO_DIM_FECHA}")
    print(f"Archivo generado: {ARCHIVO_DIM_INDICADOR}")
    print(f"Archivo generado: {ARCHIVO_FACT}")
    print(f"Base SQLite generada: {ARCHIVO_SQLITE}")

    print("\nResumen:")
    print(f"Fechas: {len(dim_fecha)}")
    print(f"Indicadores: {len(dim_indicador)}")
    print(f"Registros en fact_indicadores: {len(fact_indicadores)}")


if __name__ == "__main__":
    main()