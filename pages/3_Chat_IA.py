import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="CobraAI - Chatbot", page_icon="🤖", layout="wide")

if st.button("🏠 Voltar para a Home"):
    st.switch_page("app.py")

# Captura a chave colocada na barra lateral
api_key = st.sidebar.text_input("Chave API Gemini", type="password", key="gemini_api_key")

st.title("🤖 Chatbot de Negociação")

df = st.session_state.get("df_cobrancas")

# Escolha do cliente para o contexto da conversa
lista_clientes = df["Cliente"].tolist()
cliente_ativo = st.selectbox("Selecione o cliente para simular o atendimento:", lista_clientes)

dados_cliente = df[df["Cliente"] == cliente_ativo].iloc[0]
nome_cli = dados_cliente["Cliente"]
valor_cli = dados_cliente["Valor"]

st.info(f"Contexto Ativo: **{nome_cli}** | Valor do Débito: **R$ {valor_cli:,.2f}**")

# Cria uma chave de histórico separada para cada cliente para evitar misturar conversas
historico_key = f"chat_{nome_cli}"
if historico_key not in st.session_state:
    st.session_state[historico_key] = [
        {"role": "model", "parts": f"Olá, {nome_cli}. Verificamos em nosso sistema uma pendência no valor de R$ {valor_cli:,.2f}. Como podemos te ajudar a organizar esse pagamento hoje?"}
    ]

# Renderiza as mensagens trocadas
for msg in st.session_state[historico_key]:
    with st.chat_message("assistant" if msg["role"] == "model" else "user"):
        st.write(msg["parts"])

# Caixa de digitação
prompt_usuario = st.chat_input("Digite a resposta simulada do cliente...")

if prompt_usuario:
    # Adiciona a fala do usuário na tela e no histórico
    with st.chat_message("user"):
        st.write(prompt_usuario)
    st.session_state[historico_key].append({"role": "user", "parts": prompt_usuario})
    
    # Valida se a API Key existe na barra lateral
    if api_key:
        try:
            genai.configure(api_key=api_key)
            
            # Instancia o modelo instruindo-o sobre o papel dele e dados do cliente
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=(
                    f"Você é a CobraAI, um agente virtual especializado em negociação de dívidas de forma humana e amigável. "
                    f"Você está conversando com o cliente chamado '{nome_cli}', que deve o valor exato de R$ {valor_cli:,.2f}. "
                    f"Seja gentil, não ameace o cliente e ofereça opções como parcelamentos ou facilitação de pagamentos se solicitado."
                )
            )
            
            # Envia todo o histórico estruturado para a API responder com contexto completo
            resposta = model.generate_content(st.session_state[historico_key])
            texto_ia = resposta.text
            
        except Exception as e:
            texto_ia = f"⚠️ Erro na API do Gemini: {str(e)}. Verifique sua chave de acesso."
    else:
        # Resposta de Demonstração caso esteja sem chave
        texto_ia = f"👋 (Modo Demonstração) Entendi seu ponto. Insira a sua 'Chave API Gemini' na barra lateral para receber propostas reais calculadas pela IA da CobraAI."

    # Adiciona a resposta da IA na tela e no histórico
    with st.chat_message("assistant"):
        st.write(texto_ia)
    st.session_state[historico_key].append({"role": "model", "parts": texto_ia})
