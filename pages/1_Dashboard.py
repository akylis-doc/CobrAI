import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CobraAI - Dashboard", page_icon="📊", layout="wide")

# Botão Home obrigatório
if st.button("🏠 Voltar para a Home"):
    st.switch_page("app.py")

st.sidebar.title("💰 CobraAI")
st.sidebar.text_input("Chave API Gemini", type="password", key="gemini_api_key")

st.title("Dashboard Executivo")

df = st.session_state.get("df_cobrancas")

# Cálculos dinâmicos
total_cobrancas = len(df)
df_pagos = df[df["Status"] == "Pago"]
valor_recuperado = df_pagos["Valor"].sum()
inadimplentes = len(df[df["Status"] == "Em atraso"])
taxa_conversao = (len(df_pagos) / total_cobrancas * 100) if total_cobrancas > 0 else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Recuperado", f"R$ {valor_recuperado:,.2f}")
c2.metric("Cobranças Ativas", f"{total_cobrancas}")
c3.metric("Inadimplentes", f"{inadimplentes}")
c4.metric("Conversão", f"{taxa_conversao:.1f}%")

col1, col2 = st.columns([2, 1])
with col1:
    dados_grafico = df.groupby("Mês", as_index=False)["Valor"].sum()
    fig = px.bar(dados_grafico, x="Mês", y="Valor", title="Recuperação Financeira")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("IA Analytics")
    contagem_motivos = df["Motivo"].value_counts(normalize=True) * 100
    for motivo, porcentagem in contagem_motivos.items():
        st.info(f"{porcentagem:.0f}% alegam {motivo.lower()}")
