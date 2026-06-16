
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CobraAI", page_icon="💰", layout="wide")

st.markdown('''
<style>
.metric-card{background:#fff;padding:15px;border-radius:12px;border:1px solid #eaeaea}
</style>
''', unsafe_allow_html=True)

st.sidebar.title("💰 CobraAI")
st.sidebar.success("Painel Principal")

st.title("Dashboard Executivo")

c1,c2,c3,c4 = st.columns(4)
c1.metric("Recuperado", "R$ 128.450", "+12%")
c2.metric("Cobranças", "1.284", "+89")
c3.metric("Inadimplentes", "143", "-17")
c4.metric("Conversão", "82%", "+4%")

dados = pd.DataFrame({
    "Mês":["Jan","Fev","Mar","Abr","Mai","Jun"],
    "Valor":[22000,28000,35000,42000,51000,65000]
})

col1,col2 = st.columns([2,1])

with col1:
    fig = px.bar(dados,x="Mês",y="Valor",title="Recuperação Financeira")
    st.plotly_chart(fig,use_container_width=True)

with col2:
    st.subheader("IA Analytics")
    st.info("35% esquecem o vencimento")
    st.info("28% alegam falta de caixa")
    st.info("22% problemas bancários")

st.subheader("Últimas cobranças")
st.dataframe(pd.DataFrame({
"Cliente":["João","Maria","Pedro","Ana","Lucas"],
"Valor":["150","500","230","900","120"],
"Status":["Pago","Negociando","Em atraso","Pago","Pago"]
}), use_container_width=True)
