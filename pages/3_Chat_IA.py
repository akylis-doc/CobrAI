import streamlit as st
import google.generativeai as genai
import pandas as pd

# Configuração da página
st.set_page_config(page_title="CobraAI - Chatbot", page_icon="🤖", layout="wide")

# Botão para voltar à home
if st.button("🏠 Voltar para a Home"):
    st.switch_page("app.py")

# Entrada da chave API na sidebar
api_key = st.sidebar.text_input("Chave API Gemini", type="password", key="gemini_api_key")

# Título principal
st.title("🤖 Chatbot de Negociação")

# ===== CARREGAR DADOS DE EXEMPLO =====
if "df_cobrancas" not in st.session_state:
    # Dados de exemplo
    dados_exemplo = {
        "Cliente": [
            "João Silva", 
            "Maria Santos", 
            "Pedro Oliveira", 
            "Ana Costa", 
            "Carlos Lima"
        ],
        "Valor": [
            1500.00, 
            2300.50, 
            850.75, 
            3200.00, 
            1750.30
        ],
        "Vencimento": [
            "2024-01-15", 
            "2024-02-20", 
            "2024-03-10", 
            "2024-01-25", 
            "2024-02-15"
        ],
        "Status": [
            "Vencido", 
            "Vencido", 
            "Parcial", 
            "Vencido", 
            "Parcial"
        ]
    }
    st.session_state.df_cobrancas = pd.DataFrame(dados_exemplo)
    st.success("✅ Dados de exemplo carregados com sucesso!")

df = st.session_state.get("df_cobrancas")

# Verifica se o dataframe existe
if df is None or df.empty:
    st.error("⚠️ Nenhum dado de cobrança encontrado. Por favor, carregue os dados primeiro.")
    st.stop()

# Seleção do cliente
lista_clientes = df["Cliente"].tolist()
cliente_ativo = st.selectbox("Selecione o cliente para simular o atendimento:", lista_clientes)

# Obtém dados do cliente selecionado
dados_cliente = df[df["Cliente"] == cliente_ativo].iloc[0]
nome_cli = dados_cliente["Cliente"]
valor_cli = dados_cliente["Valor"]

# Exibe informações do cliente
st.info(f"Contexto Ativo: **{nome_cli}** | Valor do Débito: **R$ {valor_cli:,.2f}**")

# Inicializa o histórico da conversa
historico_key = f"chat_{nome_cli}"
if historico_key not in st.session_state:
    st.session_state[historico_key] = [
        {"role": "model", "parts": f"Olá, {nome_cli}. Verificamos em nosso sistema uma pendência no valor de R$ {valor_cli:,.2f}. Como podemos te ajudar a organizar esse pagamento hoje?"}
    ]

# Exibe mensagens do histórico
for msg in st.session_state[historico_key]:
    with st.chat_message("assistant" if msg["role"] == "model" else "user"):
        st.write(msg["parts"])

# Input do usuário
prompt_usuario = st.chat_input("Digite a resposta simulada do cliente...")

if prompt_usuario:
    # Adiciona a mensagem do usuário
    with st.chat_message("user"):
        st.write(prompt_usuario)
    st.session_state[historico_key].append({"role": "user", "parts": prompt_usuario})
    
    # Verifica se a chave API foi fornecida
    if api_key:
        try:
            # Configura a API do Gemini
            genai.configure(api_key=api_key)
            
            # Cria o modelo com instrução do sistema
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=(
                    f"Você é a CobraAI, um agente virtual especializado em negociação de dívidas de forma humana e amigável. "
                    f"Você está conversando com o cliente chamado '{nome_cli}', que deve o valor exato de R$ {valor_cli:,.2f}. "
                    f"Seja gentil, não ameace o cliente e ofereça opções como parcelamentos ou facilitação de pagamentos se solicitado."
                )
            )
            
            # Formata o histórico para a API
            historico_formatado = []
            for msg in st.session_state[historico_key]:
                role = "user" if msg["role"] == "user" else "model"
                historico_formatado.append({"role": role, "parts": [{"text": msg["parts"]}]})
            
            # Gera a resposta
            response = model.generate_content(historico_formatado[-1]["parts"][0]["text"])
            texto_ia = response.text
            
        except Exception as e:
            texto_ia = f"⚠️ Erro na API do Gemini: {str(e)}. Verifique sua chave de acesso."
    else:
        texto_ia = "👋 (Modo Demonstração) Por favor, insira sua 'Chave API Gemini' na barra lateral para iniciar a negociação real."

    # Exibe e salva a resposta da IA
    with st.chat_message("assistant"):
        st.write(texto_ia)
    st.session_state[historico_key].append({"role": "model", "parts": texto_ia})
