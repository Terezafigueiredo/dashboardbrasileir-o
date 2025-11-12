import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAÇÃO GERAL DO DASHBOARD
st.set_page_config(
    page_title="Dashboard Brasileirão – Vitórias, Aproveitamento e Gols (2018–2022)",
    page_icon="⚽",
    layout="wide"
)

st.title("🏆 Dashboard Brasileirão – Vitórias, Aproveitamento e Gols (2018–2022)")
st.markdown("Análise interativa de vitórias, aproveitamento e desempenho entre 2018 e 2022.")

# LEITURA DOS DADOS
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados_2018_2022.csv")

    # Normaliza nomes das colunas
    df.columns = [c.strip().lower() for c in df.columns]

    # Verifica se tem coluna de ano, se não cria
    if "ano_campeonato" not in df.columns:
        st.warning("❗ Coluna 'ano_campeonato' não encontrada — será criada com base em 2020–2024.")
        df["ano_campeonato"] = 2020  # valor fixo se não existir

    # Garante que gols são numéricos
    df["gols_mandante"] = pd.to_numeric(df["gols_mandante"], errors="coerce").fillna(0).astype(int)
    df["gols_visitante"] = pd.to_numeric(df["gols_visitante"], errors="coerce").fillna(0).astype(int)

    return df

df = carregar_dados()

# FILTROS LATERAIS
st.sidebar.header("⚙️ Filtros")

anos_disponiveis = sorted(df["ano_campeonato"].unique())
ano = st.sidebar.selectbox("Escolha o ano", anos_disponiveis)
times = sorted(pd.unique(df[['time_mandante', 'time_visitante']].values.ravel('K')))
time = st.sidebar.selectbox("Escolha o time", ["Todos"] + times)

# Filtra por ano e time
df_filtrado = df[df["ano_campeonato"] == ano]
if time != "Todos":
    df_filtrado = df_filtrado[
        (df_filtrado["time_mandante"] == time) | (df_filtrado["time_visitante"] == time)
    ]

# CÁLCULOS PRINCIPAIS
def calcular_estatisticas(df):
    df = df.copy()
    df["vencedor"] = df.apply(
        lambda row: row["time_mandante"]
        if row["gols_mandante"] > row["gols_visitante"]
        else (row["time_visitante"] if row["gols_visitante"] > row["gols_mandante"] else "Empate"),
        axis=1
    )
    return df

df_calc = calcular_estatisticas(df_filtrado)

# TOP 10 MANDANTES / VISITANTES
vitorias_mand = (
    df_calc[df_calc["vencedor"] == df_calc["time_mandante"]]
    .groupby("time_mandante")
    .size()
    .reset_index(name="vitórias")
    .sort_values(by="vitórias", ascending=False)
    .head(10)
)

vitorias_vis = (
    df_calc[df_calc["vencedor"] == df_calc["time_visitante"]]
    .groupby("time_visitante")
    .size()
    .reset_index(name="vitórias")
    .sort_values(by="vitórias", ascending=False)
    .head(10)
)

# APROVEITAMENTO POR TIME
def calcular_aproveitamento(df):
    times = pd.unique(df[["time_mandante", "time_visitante"]].values.ravel("K"))
    stats = []
    for t in times:
        jogos = df[(df["time_mandante"] == t) | (df["time_visitante"] == t)]
        vitorias = jogos[
            ((jogos["time_mandante"] == t) & (jogos["gols_mandante"] > jogos["gols_visitante"])) |
            ((jogos["time_visitante"] == t) & (jogos["gols_visitante"] > jogos["gols_mandante"]))
        ]
        aproveitamento = (len(vitorias) / len(jogos)) * 100 if len(jogos) > 0 else 0
        stats.append({"time": t, "jogos": len(jogos), "vitórias": len(vitorias), "aproveitamento_%": round(aproveitamento, 2)})
    return pd.DataFrame(stats).sort_values(by="aproveitamento_%", ascending=False)

df_aproveitamento = calcular_aproveitamento(df_calc)

# EVOLUÇÃO DE VITÓRIAS POR ANO
df_evolucao = df.copy()
df_evolucao["vencedor"] = df_evolucao.apply(
    lambda row: row["time_mandante"]
    if row["gols_mandante"] > row["gols_visitante"]
    else (row["time_visitante"] if row["gols_visitante"] > row["gols_mandante"] else "Empate"),
    axis=1
)
df_evolucao = df_evolucao[df_evolucao["vencedor"] != "Empate"]
df_evolucao = (
    df_evolucao.groupby(["ano_campeonato", "vencedor"])
    .size()
    .reset_index(name="vitórias")
)

# GRÁFICO DE GOLS DOS MANDANTES
gols_mand = (
    df.groupby("time_mandante")["gols_mandante"]
    .sum()
    .reset_index()
    .sort_values(by="gols_mandante", ascending=False)
    .head(10)
)

# VISUALIZAÇÕES
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏠 Top 10 – Vitórias como Mandante")
    if not vitorias_mand.empty:
        fig_mand = px.bar(vitorias_mand, x="vitórias", y="time_mandante", orientation="h", color="vitórias",
                          color_continuous_scale="Blues", title=f"Top 10 Mandantes ({ano})")
        st.plotly_chart(fig_mand, use_container_width=True)
    else:
        st.info("Sem dados de mandantes para esse ano.")

with col2:
    st.subheader("🛫 Top 10 – Vitórias como Visitante")
    if not vitorias_vis.empty:
        fig_vis = px.bar(vitorias_vis, x="vitórias", y="time_visitante", orientation="h", color="vitórias",
                         color_continuous_scale="Reds", title=f"Top 10 Visitantes ({ano})")
        st.plotly_chart(fig_vis, use_container_width=True)
    else:
        st.info("Sem dados de visitantes para esse ano.")

# EVOLUÇÃO DE VITÓRIAS (LINHA)
st.subheader("📈 Evolução de Vitórias por Ano")
if not df_evolucao.empty:
    fig_evol = px.line(df_evolucao, x="ano_campeonato", y="vitórias", color="vencedor",
                       title="Evolução de Vitórias por Time (2018–2022)")
    st.plotly_chart(fig_evol, use_container_width=True)
else:
    st.info("Sem dados de evolução disponíveis.")

# GRÁFICO DE GOLS DOS MANDANTES
st.subheader("⚽ Gols Marcados por Times Mandantes (Top 10)")
if not gols_mand.empty:
    fig_gols = px.bar(gols_mand, x="gols_mandante", y="time_mandante", orientation="h", color="gols_mandante",
                      color_continuous_scale="Viridis", title="Top 10 Mandantes em Gols Marcados")
    st.plotly_chart(fig_gols, use_container_width=True)
else:
    st.info("Sem dados de gols para exibir.")

# TABELA DE APROVEITAMENTO
st.subheader("📊 Aproveitamento por Time")
st.dataframe(df_aproveitamento)

# RODAPÉ
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Desenvolvido para análise do Brasileirão (2018–2022) • por Tereza Figueiredo, Pyetro Araujo e Ivan Aguiar ⚽</p>",
    unsafe_allow_html=True
)
