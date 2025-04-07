import pandas as pd
import sqlite3

# Ruta del CSV generado
csv_path = "../csv/audio_files_metadata_with_info.csv"

# Leer el CSV en un DataFrame y convertir la columna "datetime" a tipo datetime de Pandas
df = pd.read_csv(csv_path)
df["datetime"] = pd.to_datetime(df["datetime"])

# Conectar a (o crear) la base de datos SQLite (se creará el archivo si no existe)
conn = sqlite3.connect("../db/audio_metadata.db")

# Escribir el DataFrame en una tabla de SQLite llamada "audio_metadata"
# Forzamos que la columna "datetime" tenga tipo DATETIME en la base de datos.
df.to_sql("audio_metadata", conn, if_exists="replace", index=False, dtype={"datetime": "DATETIME"})

# (Opcional) Crear índices en columnas clave para mejorar el rendimiento en consultas
with conn:
    conn.execute("CREATE INDEX IF NOT EXISTS idx_recorder ON audio_metadata (recorder);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_datetime ON audio_metadata (datetime);")

# Cerrar la conexión
conn.close()

print("La base de datos SQLite 'audio_metadata.db' ha sido creada exitosamente.")
