import streamlit as st
import pandas as pd
from datetime import datetime

st.title("👥 Gestão de Clientes")

# Verifica se a base de dados global existe
if "df_cobrancas" not in st.session_state:
    st.warning("Acesse a página inicial primeiro para carregar o sistema.")
else:
    df = st.session_state["df_cobrancas"]

    # Exibe a tabela com os clientes cadastrados atualmente
    st.dataframe(df[["Cliente", "Telefone", "Valor", "Data_Cobranca", "Status"]], use_container_width=True)

    # FORMULÁRIO DE CADASTRO EXPANSÍVEL
    with st.expander("➕ Adicionar Novo Cliente", expanded=False):
        with st.form("cadastro_cliente", clear_on_submit=True):
            nome = st.text_input("Nome do Cliente *")
            telefone = st.text_input("Telefone / WhatsApp")
            valor = st.number_input("Valor que deve (R$) *", min_value=0.0, step=10.0, format="%.2f")
            data_cobranca = st.date_input("Data de Cobrança", value=datetime.now())
            motivo = st.selectbox("Motivo provável do atraso", ["Esquecimento", "Sem dinheiro", "Banco", "Outros"])
            
            submetido = st.form_submit_button("Salvar Cliente")
            
            if submetido:
                if not nome or valor <= 0:
                    st.error("Por favor, preencha o Nome e um Valor maior que R$ 0.")
                else:
                    # Mapeia o mês abreviado para alimentar o gráfico da home
                    meses_abrev = {1:"Jan", 2:"Fev", 3:"Mar", 4:"Abr", 5:"Mai", 6:"Jun", 
                                   7:"Jul", 8:"Ago", 9:"Set", 10:"Out", 11:"Nov", 12:"Dez"}
                    mes_nome = meses_abrev[data_cobranca.month]

                    # Cria a nova linha de dados
                    novo_cliente = {
                        "Cliente": nome,
                        "Telefone": telefone if telefone else "Não informado",
                        "Status": "Em atraso",  # Entra como inadimplente por padrão
                        "Valor": valor,
                        "Data_Cobranca": data_cobranca.strftime("%d/%m/%Y"),
                        "Mês": mes_nome,
                        "Motivo": motivo
                    }
                    
                    # Atualiza o DataFrame global salvando no session_state
                    st.session_state["df_cobrancas"] = pd.concat([df, pd.DataFrame([novo_cliente])], ignore_index=True)
                    st.success(f"Cliente '{nome}' cadastrado com sucesso!")
                    st.rerun()  # Atualiza a tela para mostrar o novo cliente na tabela
