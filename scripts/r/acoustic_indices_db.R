# Instalar y cargar las librerías necesarias
if (!requireNamespace("DBI", quietly = TRUE)) install.packages("DBI")
if (!requireNamespace("RSQLite", quietly = TRUE)) install.packages("RSQLite")
if (!requireNamespace("seewave", quietly = TRUE)) install.packages("seewave")
if (!requireNamespace("soundecology", quietly = TRUE)) install.packages("soundecology")
if (!requireNamespace("tuneR", quietly = TRUE)) install.packages("tuneR")
if (!requireNamespace("dplyr", quietly = TRUE)) install.packages("dplyr")

library(DBI)
library(RSQLite)
library(seewave)
library(soundecology)
library(tuneR)
library(dplyr)

# Conectar (o crear) la base de datos SQLite
db_file <- "db/audio_metadata.db"
con <- dbConnect(RSQLite::SQLite(), dbname = db_file)

# Suponemos que ya existe una tabla "audio_metadata" con la información proveniente del CSV.
# Si aún no existe, puedes crearla previamente (por ejemplo, cargando el CSV y escribiéndolo en SQLite).
# En este ejemplo se lee la tabla:
metadata <- dbReadTable(con, "audio_metadata")

# Si la columna "processed" no existe, se añaden las columnas de índices (con NA) y se crea "processed"
# Además, se añade una columna auxiliar "orig_index" para identificar cada fila de forma única.
if (!("processed" %in% names(metadata))) {
  metadata <- metadata %>%
    mutate(
      ACI = NA_real_,
      ADI = NA_real_,
      AEI = NA_real_,
      BIO = NA_real_,
      NDSI = NA_real_,
      H = NA_real_,
      AR = NA_real_,
      processed = FALSE,
      orig_index = row_number()
    )
  # Reemplazamos la tabla en la base de datos
  dbWriteTable(con, "audio_metadata", metadata, overwrite = TRUE)
} else if (!("orig_index" %in% names(metadata))) {
  metadata <- metadata %>% mutate(orig_index = row_number())
  dbWriteTable(con, "audio_metadata", metadata, overwrite = TRUE)
}

# Filtrar los registros pendientes y agregar una columna "day" (extraída de "datetime")
pending <- metadata %>%
  mutate(day = as.Date(datetime))

# Agrupar por grabadora y día y tomar una muestra aleatoria de 6 registros (o menos si no hay suficientes)
pending_sample <- pending %>%
  group_by(recorder, day) %>%
  slice_sample(n = 6) %>%
  ungroup()

# Obtener los índices originales de las filas a procesar
rows_to_process <- pending_sample$orig_index

cat("Número de archivos pendientes de procesamiento (muestreados por día y grabadora):",
    length(rows_to_process), "\n")

# Iterar sobre cada fila seleccionada
for (i in rows_to_process) {
  # Buscar la fila correspondiente según "orig_index"
  row_idx <- which(metadata$orig_index == i)
  file_path <- metadata$filepath[row_idx]
  cat("Procesando archivo:", file_path, i, "\n")

  # Verificar que el archivo existe
  if (!file.exists(file_path)) {
    warning("El archivo no existe: ", file_path)
    next
  }

  tryCatch({
    # Leer el archivo WAV
    wav <- readWave(file_path)

    # Calcular los índices acústicos
    aci_val <- acoustic_complexity(wav)$AciTotAll_left
    adi_val <- acoustic_diversity(wav)$adi_left
    aei_val <- acoustic_evenness(wav)$aei_left
    bio_val <- bioacoustic_index(wav)$left_area
    ndsi_val <- ndsi(wav)$ndsi_left
    h_val <- H(wav, f = wav@samp.rate)
    ar_val <- AR(wav)$Ht

    # Actualizar la variable local "metadata"
    metadata$ACI[row_idx] <- aci_val
    metadata$ADI[row_idx] <- adi_val
    metadata$AEI[row_idx] <- aei_val
    metadata$BIO[row_idx] <- bio_val
    metadata$NDSI[row_idx] <- ndsi_val
    metadata$H[row_idx] <- h_val
    metadata$AR[row_idx] <- ar_val
    metadata$processed[row_idx] <- TRUE

    cat("Archivo procesado correctamente.\n")

    # Actualizar el registro en la base de datos mediante una consulta UPDATE
    update_query <- "UPDATE audio_metadata
                     SET ACI = ?, ADI = ?, AEI = ?, BIO = ?, NDSI = ?, H = ?, AR = ?, processed = ?
                     WHERE orig_index = ?"
    dbExecute(con, update_query, params = list(aci_val, adi_val, aei_val, bio_val, ndsi_val, h_val, ar_val, TRUE, i))

    cat("Registro actualizado en SQLite.\n")

  }, error = function(e) {
    message("Error procesando el archivo ", file_path, ": ", e$message)
  })
}

cat("Procesamiento completado.\n")

# Cerrar la conexión a la base de datos
dbDisconnect(con)
