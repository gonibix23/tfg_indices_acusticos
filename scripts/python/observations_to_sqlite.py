import pandas as pd
import sqlite3
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Ruta del CSV de observaciones
csv_path = "../../csv/observations.csv"  # Ajusta según corresponda

# Leer el CSV en un DataFrame
df = pd.read_csv(csv_path)
logging.info("Archivo CSV cargado. Número de registros: %d", len(df))

# Limpiar los nombres de las columnas
df.columns = df.columns.str.strip()

# Renombrar las columnas deseadas: "Grabadora" -> "recorder", "Especie" -> "bird"
df.rename(columns={"Grabadora": "recorder", "Especie": "bird"}, inplace=True)

# Crear columna datetime combinando "Fecha" y "Hora_fin"
df["datetime"] = pd.to_datetime(df["Fecha"] + " " + df["Hora_fin"], dayfirst=True)

# Seleccionar únicamente las columnas requeridas: se omite la columna original "Fecha" y "Hora_fin"
df = df[["recorder", "datetime", "bird"]]

# Convertir la columna 'bird' a mayúsculas
df["bird"] = df["bird"].str.upper()

# Anteponer "AM" a la columna "recorder"
df["recorder"] = "AM" + df["recorder"].astype(str)

# Conectar (o crear) la base de datos SQLite
conn = sqlite3.connect("../../db/audio_metadata.db")

# Escribir el DataFrame en una tabla SQLite llamada "observations"
# Forzamos que la columna 'datetime' tenga tipo DATETIME en SQLite.
df.to_sql("observations", conn, if_exists="replace", index=False, dtype={"datetime": "DATETIME"})

# Crear índices (opcional)
with conn:
    conn.execute("CREATE INDEX IF NOT EXISTS idx_observations_recorder ON observations (recorder);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_observations_datetime ON observations (datetime);")

conn.close()

logging.info("La base de datos SQLite 'audio_metadata.db' ha sido actualizada con la tabla 'observations' exitosamente.")
