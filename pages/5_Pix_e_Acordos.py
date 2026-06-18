import streamlit as st

st.set_page_config(page_title="CobraAI - Pix", page_icon="⚡", layout="wide")

if st.button("🏠 Voltar para a Home"): 
    st.switch_page("app.py")

st.sidebar.title("🐍 CobrAI")
st.sidebar.text_input("Chave API Gemini", type="password", key="gemini_api_key")

st.title("⚡ Pix e Acordos Automáticos")

st.info("Espaço reservado para integrações futuras de APIs de Gateway de Pagamentos (Geração de Pix Copia e Cola e PDFs de Acordos).")
