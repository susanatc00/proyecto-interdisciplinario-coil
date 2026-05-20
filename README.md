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
Tecnologías utilizadas
Amazon S3
Amazon EC2
AWS Glue Data Catalog
Amazon Athena
Docker
Docker Compose
Python
Pandas
Boto3
Streamlit
Componentes implementados
1. Data Lake en Amazon S3

Estructura implementada:

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
2. Procesamiento distribuido

La solución utiliza Docker Compose para ejecutar múltiples workers en paralelo.

Cada worker:

Procesa un subconjunto de archivos CSV
Aplica reglas de cobertura médica
Genera datasets curados
Produce reportes de trazabilidad
3. Glue Data Catalog

AWS Glue se utiliza para:

Inferir automáticamente el esquema
Catalogar datasets curados
Integrar los datos con Athena

Base de datos:

coil_medical_db

Tabla generada:

decisiones_cobertura
4. Athena

Athena permite realizar consultas SQL serverless sobre los datos curados almacenados en S3.

Ejemplos de consultas:

Cobertura total
SELECT decision_cobertura, COUNT(*) AS total
FROM decisiones_cobertura
GROUP BY decision_cobertura;
Valor reconocido
SELECT SUM(valor_reconocido)
FROM decisiones_cobertura;
Top medicamentos
SELECT medicamento, COUNT(*) AS total
FROM decisiones_cobertura
GROUP BY medicamento
ORDER BY total DESC
LIMIT 10;
5. Dashboard Streamlit

El dashboard permite visualizar:

Total de órdenes procesadas
Valor solicitado
Valor reconocido
Promedio de cobertura
Distribución de cobertura
Workers utilizados
Vista previa de datos
Resultados obtenidos
Corrida	Workers	Tiempo
run_2	2	7.369 s
run_3	3	7.031 s
Métricas principales
Total procesado: 30.000 órdenes médicas
Valor solicitado: $45,589,646,412
Valor reconocido: $18,660,755,577
Cobertura promedio: 41.02%
Ejecución del proyecto
1. Clonar repositorio
git clone https://github.com/susanatc00/proyecto-interdisciplinario-coil.git
cd proyecto-interdisciplinario-coil
2. Configurar entorno
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Ejecutar procesamiento distribuido
2 workers
time docker compose -f docker-compose-2.yml up --build
3 workers
time docker compose -f docker-compose-3.yml up --build
4. Ejecutar dashboard
cd dashboard
source ../venv/bin/activate

streamlit run app.py \
  --server.port 8501 \
  --server.address 0.0.0.0
Trazabilidad

Cada worker genera reportes JSON en:

reports/

Ejemplo:

run_3_worker_a_summary.json

Incluyendo:

archivos procesados
filas procesadas
tiempo total
timestamps
worker_id
run_id
Escalabilidad

La arquitectura implementa procesamiento horizontal utilizando múltiples workers Docker sobre EC2.

Esto permite:

Reducir tiempos de procesamiento
Distribuir carga
Mejorar escalabilidad
Mantener trazabilidad por worker
Dashboard

Dashboard desplegado en:

http://98.80.166.145:8501
