# 🐦📊 Caracterización de Diversidad Acústica en Doñana

**Trabajo de Fin de Grado - Grado en Matemática Computacional**  
**Autor:** Gonzalo de Antonio Sierra  
**Tutora:** Mar Angulo Martínez  
**Co-Tutora:** Irene Mendoza Sagrera  
**Convocatoria:** Ordinaria Abril 2025

---

## 🌱 Descripción

Este repositorio contiene el código, análisis y documentación correspondiente al Trabajo de Fin de Grado titulado **"Caracterización de Diversidad Acústica en Doñana y Comparación con la Diversidad Aviar"**, cuyo objetivo principal es evaluar la utilidad de la **ecoacústica** como herramienta para el monitoreo de la biodiversidad, con especial foco en la diversidad de aves.

A través del procesamiento de más de 300.000 audios recogidos mediante grabadoras automáticas instaladas en el Parque Nacional de Doñana, se calculan múltiples **índices acústicos** y se comparan con censos visuales de aves realizados por expertos.

---

## 🎯 Objetivos

- Analizar la **variabilidad espacio-temporal** de índices acústicos (ACI, ADI, AEI, BIO, NDSI, H y AR).
- Determinar si existe una **firma sonora distintiva** en cada hábitat (marisma, matorral, vera, laguna).
- Contrastar los resultados acústicos con censos ornitológicos tradicionales.

---

## 📂 Estructura del repositorio
```bash
📁 csv/                                           # CSV con datos adicionales
📁 db/                                            # Base de datos SQLite y audios procesados (comprimido a zip para poder subirlo)
📁 metabase/                                      # Entorno de BI (pesa demasiado no puedo cargarlo)
📁 notebooks/                                     # Notebooks en Python usados para análisis y visualización
📁 plots/                                         # Figuras y visualizaciones generadas
📁 scripts/                                       # Scripts tanto de R como Python
📄 TFG_MACO_Memoria_Gonzalo_de_Antonio.pdf        # Documento completo del TFG
📄 README.md                                      # Este archivo
```

---

## 🧪 Tecnologías y herramientas

- **Lenguajes:** R (4.3.2), Python (3.10)
- **Bases de datos:** SQLite (3.42.0)
- **Análisis estadístico y visualización:**
  - R: soundecology, seewave, tuneR, dplyr, DBI, RSQLite
  - Python: pandas, numpy, matplotlib, seaborn, scipy, statsmodels, sqlite3
- **Business Intelligence:** Metabase (0.48.6)

---

## 📈 Índices Acústicos Calculados

- ACI – Acoustic Complexity Index
- ADI – Acoustic Diversity Index
- AEI – Acoustic Evenness Index
- BIO – Bioacoustic Index
- NDSI – Normalized Difference Soundscape Index
- H – Acoustic Entropy Index
- AR – Acoustic Richness Index

---

## 📬 Contacto

¿Dudas o sugerencias? Puedes escribirme a [gonzalo@deantoniosierra.es]
