import streamlit as st
import plotly.express as px

st.set_page_config(page_title="CobraAI - Relatórios", page_icon="📈", layout="wide")

if st.button("🏠 Voltar para a Home"): 
    st.switch_page("app.py")

st.sidebar.title("💰 CobraAI")
st.sidebar.text_input("Chave API Gemini", type="password", key="gemini_api_key")

st.title("📈 Relatórios Analytics")

df = st.session_state.get("df_cobrancas")

if df is not None and not df.empty:
    df_motivos = df["Motivo"].value_counts().reset_index()
    df_motivos.columns = ["Motivo", "Qtd"]
    
    fig = px.pie(df_motivos, names="Motivo", values="Qtd", title="Motivos Reais de Inadimplência")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum dado disponível para gerar o relatório.")
