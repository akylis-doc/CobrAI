import streamlit as st
import pandas as pd

st.set_page_config(page_title="CobraAI - Home", page_icon="💰", layout="wide")

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

st.sidebar.title("🐍 CobrAI")
st.sidebar.text_input("Chave API Gemini", type="password", key="gemini_api_key", help="Cole sua chave aqui para ativar a IA em todas as páginas.")

st.title("🐍 CobrAI — Sistema de Gestão Financeira")
st.subheader("Selecione um painel abaixo para gerenciar sua operação:")
st.write("---")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📊 Dashboard Executivo", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

with col2:
    if st.button("💸 Cobranças & Cadastros", use_container_width=True):
        st.switch_page("pages/2_Cobrancas.py")

with col3:
    if st.button("🤖 Chatbot de Negociação", use_container_width=True):
        st.switch_page("pages/3_Chat_IA.py")

with col4:
    if st.button("📈 Relatórios de Inadimplência", use_container_width=True):
        st.switch_page("pages/4_Relatorios.py")

with col5:
    if st.button("⚡ Pix e Acordos", use_container_width=True):
        st.switch_page("pages/5_Pix_e_Acordos.py")
