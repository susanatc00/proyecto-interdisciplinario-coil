import os
import re
import io
import json
import time
from datetime import datetime, timezone

import boto3
import pandas as pd

BUCKET = os.getenv("BUCKET")
RUN_ID = os.getenv("RUN_ID", "run_2")
WORKER_ID = os.getenv("WORKER_ID", "worker")
MANIFEST_PATH = os.getenv("MANIFEST_PATH")
OUTPUT_PREFIX = os.getenv("OUTPUT_PREFIX", "curated/decisiones_cobertura")

s3 = boto3.client("s3")

def extract_age(glosa):
    match = re.search(r"edad\s+(\d+)", glosa.lower())
    return int(match.group(1)) if match else None

def extract_medication(glosa):
    match = re.search(r"medicamento\s+([^;]+)", glosa.lower())
    return match.group(1).strip() if match else "no_identificado"

def decide_coverage(edad, medicamento, valor):
    esenciales = ["insulina", "amoxicilina", "metformina"]
    parciales = ["acetaminofen", "ibuprofeno", "omeprazol", "atorvastatina"]

    if medicamento in esenciales and edad is not None and (edad < 18 or edad >= 60):
        return "CUBRE", 100, "Medicamento esencial y paciente priorizado"
    elif medicamento in esenciales:
        return "CUBRE", 50, "Medicamento esencial con cobertura parcial"
    elif medicamento in parciales:
        return "CUBRE", 25, "Medicamento de cobertura limitada"
    else:
        return "NO_CUBRE", 0, "Medicamento no incluido en reglas de cobertura"

def process_file(s3_key):
    start = time.perf_counter()

    obj = s3.get_object(Bucket=BUCKET, Key=s3_key)
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))

    rows = []

    for _, row in df.iterrows():
        glosa = str(row["glosa"])
        edad = extract_age(glosa)
        medicamento = extract_medication(glosa)
        valor = float(row["valor_procedimiento"])

        decision, porcentaje, motivo = decide_coverage(edad, medicamento, valor)
        valor_reconocido = valor * porcentaje / 100

        rows.append({
            "id_orden": row["id_orden"],
            "fecha": row["fecha"],
            "edad_paciente": edad,
            "medicamento": medicamento,
            "valor_procedimiento": valor,
            "entidad_emisora": row["entidad_emisora"],
            "medio_emisor": row["medio_emisor"],
            "decision_cobertura": decision,
            "porcentaje_cubierto": porcentaje,
            "valor_reconocido": valor_reconocido,
            "motivo_decision": motivo,
            "worker_id": WORKER_ID,
            "run_id": RUN_ID,
            "fecha_procesamiento": datetime.now(timezone.utc).isoformat()
        })

    out_df = pd.DataFrame(rows)
    csv_body = out_df.to_csv(index=False).encode("utf-8")

    base = os.path.basename(s3_key)
    output_key = f"{OUTPUT_PREFIX}/{RUN_ID}/{base}"

    s3.put_object(
        Bucket=BUCKET,
        Key=output_key,
        Body=csv_body,
        ContentType="text/csv"
    )

    elapsed = time.perf_counter() - start

    print(json.dumps({
        "event": "file_processed",
        "worker": WORKER_ID,
        "input": s3_key,
        "output": output_key,
        "rows": len(out_df),
        "seconds": round(elapsed, 4)
    }))

    return len(out_df), elapsed

def main():
    total_rows = 0
    total_seconds = 0

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        files = [line.strip() for line in f if line.strip()]

    for s3_key in files:
        rows, seconds = process_file(s3_key)
        total_rows += rows
        total_seconds += seconds

    summary = {
        "run_id": RUN_ID,
        "worker_id": WORKER_ID,
        "files_processed": len(files),
        "rows_processed": total_rows,
        "worker_processing_seconds": round(total_seconds, 4),
        "finished_at": datetime.now(timezone.utc).isoformat()
    }

    summary_key = f"reports/{RUN_ID}_{WORKER_ID}_summary.json"

    s3.put_object(
        Bucket=BUCKET,
        Key=summary_key,
        Body=json.dumps(summary, indent=2).encode("utf-8"),
        ContentType="application/json"
    )

    print(json.dumps(summary))

if __name__ == "__main__":
    main()
