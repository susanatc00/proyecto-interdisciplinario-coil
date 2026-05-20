# Proyecto Interdisciplinario COIL — Arquitectura Big Data en AWS

## Descripción

Este proyecto implementa una arquitectura Big Data distribuida sobre AWS para el procesamiento batch de órdenes médicas. La solución permite almacenar, procesar, catalogar, consultar y visualizar información médica utilizando servicios cloud y procesamiento paralelo.

El sistema recibe datasets CSV con órdenes médicas, aplica reglas de cobertura mediante workers distribuidos y genera datasets curados listos para análisis analítico y visualización.

---

## Arquitectura

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
AWS Glue Data Catalog
      ↓
Amazon Athena
      ↓
Dashboard Streamlit
```

---

## Tecnologías utilizadas

| Categoría | Tecnología |
|-----------|------------|
| Almacenamiento | Amazon S3 |
| Cómputo | Amazon EC2 |
| Catálogo | AWS Glue Data Catalog |
| Consultas | Amazon Athena |
| Contenedores | Docker, Docker Compose |
| Procesamiento | Python, Pandas, Boto3 |
| Visualización | Streamlit |

---

## Componentes implementados

### 1. Data Lake en Amazon S3
s3://proyecto-interdisciplinario-coil-grupo07/
│
├── raw/
│   └── ordenes_medicas/
│
├── curated/
│   └── decisiones_cobertura/
│       ├── run_2/
│       └── run_3/
│
├── reports/
│
└── athena-results/

### 2. Procesamiento distribuido

La solución utiliza Docker Compose para ejecutar múltiples workers en paralelo. Cada worker:

- Procesa un subconjunto de archivos CSV
- Aplica reglas de cobertura médica
- Genera datasets curados
- Produce reportes de trazabilidad

### 3. AWS Glue Data Catalog

AWS Glue se utiliza para inferir automáticamente el esquema, catalogar datasets curados e integrarlos con Athena.

- **Base de datos:** `coil_medical_db`
- **Tabla generada:** `decisiones_cobertura`

### 4. Amazon Athena

Athena permite realizar consultas SQL serverless sobre los datos curados almacenados en S3.

**Cobertura total**
```sql
SELECT decision_cobertura, COUNT(*) AS total
FROM decisiones_cobertura
GROUP BY decision_cobertura;
```

**Valor reconocido**
```sql
SELECT SUM(valor_reconocido)
FROM decisiones_cobertura;
```

**Top medicamentos**
```sql
SELECT medicamento, COUNT(*) AS total
FROM decisiones_cobertura
GROUP BY medicamento
ORDER BY total DESC
LIMIT 10;
```

### 5. Dashboard Streamlit

El dashboard visualiza:

- Total de órdenes procesadas
- Valor solicitado y valor reconocido
- Promedio de cobertura
- Distribución de cobertura por decisión
- Workers utilizados
- Vista previa de datos

---

## Resultados obtenidos

### Tiempos de ejecución

| Corrida | Workers | Tiempo |
|---------|---------|--------|
| run_2   | 2       | 7.369 s |
| run_3   | 3       | 7.031 s |

### Métricas principales

| Métrica | Valor |
|---------|-------|
| Total órdenes procesadas | 30.000 |
| Valor solicitado | $45.589.646.412 |
| Valor reconocido | $18.660.755.577 |
| Cobertura promedio | 41.02% |

---

## Ejecución del proyecto

### 1. Clonar repositorio

```bash
git clone https://github.com/susanatc00/proyecto-interdisciplinario-coil.git
cd proyecto-interdisciplinario-coil
```

### 2. Configurar entorno

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Ejecutar procesamiento distribuido

**2 workers**
```bash
time docker compose -f docker-compose-2.yml up --build
```

**3 workers**
```bash
time docker compose -f docker-compose-3.yml up --build
```

### 4. Ejecutar dashboard

```bash
cd dashboard
source ../venv/bin/activate
streamlit run app.py \
  --server.port 8501 \
  --server.address 0.0.0.0
```

---

## Trazabilidad

Cada worker genera reportes JSON en `reports/`. Ejemplo: `run_3_worker_a_summary.json`

Cada reporte incluye:

- `worker_id` y `run_id`
- Archivos y filas procesadas
- Tiempo total de ejecución
- Timestamps de inicio y fin

---

## Escalabilidad

La arquitectura implementa procesamiento horizontal con múltiples workers Docker sobre EC2, lo que permite:

- Reducir tiempos de procesamiento
- Distribuir la carga de trabajo
- Mantener trazabilidad por worker
- Escalar horizontalmente según demanda

---

## Dashboard

El dashboard está desplegado en: [http://98.80.166.145:8501](http://98.80.166.145:8501)
