import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="CobraAI - Cobranças", page_icon="💸", layout="wide")

if st.button("🏠 Voltar para a Home"):
    st.switch_page("app.py")

st.sidebar.title("🐍 CobrAI")
st.sidebar.text_input("Chave API Gemini", type="password", key="gemini_api_key")

st.title("💸 Gestão de Cobranças")

df = st.session_state.get("df_cobrancas")

st.subheader("🔍 Localizar Registro")
termo_busca = st.text_input("Pesquise digitando o Nome do cliente ou o Número de Telefone:")

if termo_busca:
    # Filtra se bater parte do nome OU parte do telefone
    df_filtrado = df[
        df["Cliente"].astype(str).str.contains(termo_busca, case=False, na=False) |
        df["Telefone"].astype(str).str.contains(termo_busca, case=False, na=False)
    ]
else:
    df_filtrado = df

st.dataframe(df_filtrado[["Cliente", "Telefone", "Valor", "Data_Cobranca", "Status"]], use_container_width=True)

with st.expander("➕ Cadastrar Nova Cobrança", expanded=False):
    with st.form("cadastro_cliente", clear_on_submit=True):
        nome = st.text_input("Nome Completo *")
        telefone = st.text_input("Número de Telefone / WhatsApp *")
        valor = st.number_input("Valor da Cobrança (R$) *", min_value=0.0, step=10.0, format="%.2f")
        data_cobranca = st.date_input("Data de Vencimento / Cobrança", value=datetime.now())
        motivo = st.selectbox("Classificação de Inadimplência", ["Esquecimento", "Sem dinheiro", "Banco", "Outros"])
        
        submetido = st.form_submit_button("Confirmar e Salvar")
        
        if submetido:
            if not nome or not telefone or valor <= 0:
                st.error("Preencha todos os campos marcados com asterisco (*) informando valores válidos.")
            else:
                meses_abrev = {1:"Jan", 2:"Fev", 3:"Mar", 4:"Abr", 5:"Mai", 6:"Jun", 
                               7:"Jul", 8:"Ago", 9:"Set", 10:"Out", 11:"Nov", 12:"Dez"}
                mes_nome = meses_abrev[data_cobranca.month]

                nova_linha = {
                    "Cliente": nome,
                    "Telefone": telefone,
                    "Status": "Em atraso",
                    "Valor": valor,
                    "Data_Cobranca": data_cobranca.strftime("%d/%m/%Y"),
                    "Mês": mes_nome,
                    "Motivo": motivo
                }
                
                # Alimenta o banco de dados global
                st.session_state["df_cobrancas"] = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
                st.success(f"Cobrança para '{nome}' inserida com sucesso!")
                st.rerun()
