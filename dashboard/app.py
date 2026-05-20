import boto3
import pandas as pd
import streamlit as st
from io import BytesIO

BUCKET = "proyecto-interdisciplinario-coil-grupo07"
PREFIX = "curated/decisiones_cobertura/run_3/"

s3 = boto3.client("s3")

@st.cache_data
def load_data():
    objects = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX).get("Contents", [])
    dfs = []

    for obj in objects:
        key = obj["Key"]

        if key.endswith(".csv"):
            body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
            dfs.append(pd.read_csv(BytesIO(body)))

    return pd.concat(dfs, ignore_index=True)

df = load_data()

st.title("COIL - Dashboard Órdenes Médicas")

st.metric("Total órdenes", len(df))
st.metric("Valor solicitado", f"${df['valor_procedimiento'].sum():,.0f}")
st.metric("Valor reconocido", f"${df['valor_reconocido'].sum():,.0f}")
st.metric("Promedio cobertura", f"{df['porcentaje_cubierto'].mean():.2f}%")

st.subheader("Cobertura")
st.bar_chart(df["decision_cobertura"].value_counts())

st.subheader("Porcentaje cubierto")
st.bar_chart(df["porcentaje_cubierto"].value_counts())

st.subheader("Órdenes por worker")
st.bar_chart(df["worker_id"].value_counts())

st.subheader("Vista previa")
st.dataframe(df.head(100))
