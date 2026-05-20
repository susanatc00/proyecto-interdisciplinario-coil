# Proyecto Interdisciplinario COIL — Arquitectura Big Data en AWS

## Descripción

Este proyecto implementa una arquitectura Big Data distribuida sobre AWS para el procesamiento batch de órdenes médicas. La solución permite almacenar, procesar, catalogar, consultar y visualizar información médica utilizando servicios cloud y procesamiento paralelo.

El sistema recibe datasets CSV con órdenes médicas, aplica reglas de cobertura mediante workers distribuidos y genera datasets curados listos para análisis analítico y visualización.

---

# Arquitectura

```text
Datasets CSV
      ↓
Amazon S3 (RAW)
      ↓
EC2 Ubuntu
      ↓
Docker Workers Distribuidos
      ↓
Amazon S3 (CURATED)
      ↓
AWS Glue Catalog
      ↓
Amazon Athena
      ↓
Dashboard Streamlit
