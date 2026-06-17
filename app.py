import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CobraAI", page_icon="💰", layout="wide")

# Injeta o estilo CSS personalizado
st.markdown('''
<style>
.metric-card{background:#fff;padding:15px;border-radius:12px;border:1px solid #eaeaea}
</style>
''', unsafe_allow_html=True)

# 1. INICIALIZAÇÃO DO BANCO DE DADOS GLOBAL
# Se o estado de sessão não existir, criamos os dados base com valores numéricos reais
if "df_cobrancas" not in st.session_state:
    st.session_state["df_cobrancas"] = pd.DataFrame({
        "Cliente": ["João", "Maria", "Pedro", "Ana", "Lucas"],
        "Telefone": ["9999-1111", "9999-2222", "9999-3333", "9999-4444", "9999-5555"],
        "Status": ["Em atraso", "Pago", "Negociando", "Pago", "Pago"],
        "Valor": [150.0, 500.0, 230.0, 900.0, 120.0],
        "Data_Cobranca": ["10/06/2026", "12/06/2026", "14/06/2026", "15/06/2026", "16/06/2026"],
        "Mês": ["Jun", "Jun", "Jun", "Jun", "Jun"],
        "Motivo": ["Esquecimento", "Sem dinheiro", "Banco", "Esquecimento", "Banco"]
    })

# Puxa os dados atualizados do estado de sessão
df = st.session_state["df_cobrancas"]

# --- BARRA LATERAL ---
st.sidebar.title("💰 CobraAI")
st.sidebar.success("Painel Principal")

st.title("Dashboard Executivo")

# 2. CÁLCULO DE MÉTRICAS DINÂMICAS
total_cobrancas = len(df)
df_pagos = df[df["Status"] == "Pago"]
df_inadimplentes = df[df["Status"] == "Em atraso"]

valor_recuperado = df_pagos["Valor"].sum()
qtd_inadimplentes = len(df_inadimplentes)
taxa_conversao = (len(df_pagos) / total_cobrancas * 100) if total_cobrancas > 0 else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Recuperado", f"R$ {valor_recuperado:,.2f}", "+12%")
c2.metric("Cobranças", f"{total_cobrancas}", f"+{total_cobrancas}")
c3.metric("Inadimplentes", f"{qtd_inadimplentes}", "-17")
c4.metric("Conversão", f"{taxa_conversao:.1f}%", "+4%")

# --- CORPO DO DASHBOARD ---
col1, col2 = st.columns([2, 1])

with col1:
    # O gráfico agora agrupa os valores reais por mês
    dados_grafico = df.groupby("Mês", as_index=False)["Valor"].sum()
    fig = px.bar(dados_grafico, x="Mês", y="Valor", title="Recuperação Financeira por Mês")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("IA Analytics")
    # Calcula a porcentagem real dos motivos com base nos dados
    if total_cobrancas > 0:
        contagem_motivos = df["Motivo"].value_counts(normalize=True) * 100
        for motivo, porcentagem in contagem_motivos.items():
            st.info(f"{porcentagem:.0f}% alegam {motivo.lower()}")
    else:
        st.info("Sem dados de motivos disponíveis.")

st.subheader("Últimas cobranças")
st.dataframe(df[["Cliente", "Valor", "Status", "Data_Cobranca"]], use_container_width=True)
