import streamlit as st
import pandas as pd

df = pd.read_csv("dados_2018_2022.csv")

ano = st.selectbox("Escolha o ano", sorted(df["ano_campeonato"].unique()))
time = st.selectbox("Escolha o time mandante", sorted(df["time_mandante"].unique()))

df_filtrado = df[(df["ano_campeonato"] == ano) & (df["time_mandante"] == time)]
st.write(df_filtrado)