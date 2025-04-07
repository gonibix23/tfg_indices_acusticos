import pandas as pd
import sqlite3

# Ruta del CSV de recorders (con separador ';')
csv_path = "../../csv/recorders.csv"

# Leer el CSV en un DataFrame, especificando el separador
df = pd.read_csv(csv_path, sep=";")

# Conectar (o crear) la base de datos SQLite (se creará el archivo si no existe)
conn = sqlite3.connect("../../db/audio_metadata.db")

# Escribir el DataFrame en una tabla de SQLite llamada "recorders"
# Forzamos que las columnas 'lat' y 'lon' tengan tipo REAL.
df.to_sql("recorders", conn, if_exists="replace", index=False, dtype={"lat": "REAL", "lon": "REAL"})

# (Opcional) Crear un índice en la columna "recorder" para mejorar el rendimiento en consultas
with conn:
    conn.execute("CREATE INDEX IF NOT EXISTS idx_recorder_recorders ON recorders (recorder);")

# Cerrar la conexión
conn.close()

print("La base de datos SQLite 'audio_metadata.db' ha sido actualizada con la tabla 'recorders' exitosamente.")
