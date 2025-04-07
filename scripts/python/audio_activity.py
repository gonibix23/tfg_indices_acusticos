import sqlite3
import pandas as pd
import numpy as np
import librosa
import os
import logging

# Configurar el logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- 1. Conexión a la base de datos y creación de la tabla si no existe ---
db_path = "../../db/audio_metadata.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Crear la tabla "audio_activity" si no existe, con las columnas:
# recorder, datetime, filepath, activity, duration
create_table_query = """
CREATE TABLE IF NOT EXISTS audio_activity (
    recorder TEXT,
    datetime DATETIME,
    filepath TEXT,
    activity FLOAT,
    duration FLOAT
);
"""
cur.execute(create_table_query)
conn.commit()

# --- 2. Cargar la metadata y determinar los audios pendientes ---
df_metadata = pd.read_sql_query("SELECT * FROM audio_metadata", conn)

try:
    df_activity = pd.read_sql_query("SELECT filepath FROM audio_activity", conn)
    processed_filepaths = set(df_activity["filepath"].tolist())
except Exception as e:
    logging.info("La tabla 'audio_activity' no existe, se usará un conjunto vacío de procesados.")
    processed_filepaths = set()

conn.close()

logging.info(f"Total de audios en metadata: {len(df_metadata)}")
logging.info(f"Audios ya procesados: {len(processed_filepaths)}")

# --- 3. Procesamiento individual y actualización incremental ---
conn = sqlite3.connect(db_path)
cur = conn.cursor()

for idx, row in df_metadata.iterrows():
    file_path = row["filepath"]

    # Si el audio ya fue procesado, se omite
    if file_path in processed_filepaths:
        continue

    if not os.path.exists(file_path):
        logging.warning(f"Archivo no encontrado: {file_path}")
        continue

    try:
        y, sr = librosa.load(file_path, sr=None)
        rms = librosa.feature.rms(y=y)
        avg_rms = float(np.mean(rms))
        # Calcular la duración en segundos
        duration = float(librosa.get_duration(y=y, sr=sr))

        recorder = row.get("recorder", None)
        dt = row.get("datetime", None)
        if pd.notnull(dt):
            dt = pd.to_datetime(dt).strftime("%Y-%m-%d %H:%M:%S")
        else:
            dt = None

        insert_query = """
            INSERT INTO audio_activity (recorder, datetime, filepath, activity, duration)
            VALUES (?, ?, ?, ?, ?)
        """
        cur.execute(insert_query, (recorder, dt, file_path, avg_rms, duration))
        conn.commit()
        logging.info(f"Procesado: {file_path} -> actividad: {avg_rms:.4f}, duración: {duration:.2f} s")
    except Exception as e:
        logging.error(f"Error procesando {file_path}: {e}")

cur.execute("CREATE INDEX IF NOT EXISTS idx_activity_filepath ON audio_activity (filepath);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_activity_recorder ON audio_activity (recorder);")
conn.commit()
conn.close()

logging.info("Proceso completado. La tabla 'audio_activity' se ha actualizado incrementalmente.")


