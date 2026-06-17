import streamlit as st

st.title("🤖 Negociação IA")

if "df_cobrancas" not in st.session_state:
    st.warning("Acesse a página inicial primeiro para carregar o sistema.")
else:
    df = st.session_state["df_cobrancas"]
    
    # 1. SELEÇÃO DINÂMICA DO CLIENTE PARA A CONVERSA
    lista_clientes = df["Cliente"].tolist()
    cliente_ativo = st.selectbox("Selecione o cliente para simular a conversa de cobrança:", lista_clientes)
    
    # Busca os dados em tempo real daquele cliente específico
    dados_cliente = df[df["Cliente"] == cliente_ativo].iloc[0]
    nome_cli = dados_cliente["Cliente"]
    valor_cli = dados_cliente["Valor"]
    
    # Caixa visual mostrando os dados que serão enviados como contexto para a IA
    st.info(f"**Contexto Atualizado no Chat:** Enviando cobrança para **{nome_cli}** | Valor da pendência: **R$ {valor_cli:,.2f}**")
    
    # Inicializa o histórico da conversa se não existir
    if "historico_conversas" not in st.session_state:
        st.session_state["historico_conversas"] = []

    # Mensagem de saudação automática estruturada com os dados REAIS do cliente
    saudacao_inicial = f"Olá, {nome_cli}. Notamos uma pendência no valor de R$ {valor_cli:,.2f} no nosso sistema. Como podemos te ajudar a regularizar essa situação hoje?"
    st.chat_message("assistant").write(saudacao_inicial)

    # Exibe as mensagens trocadas na sessão atual
    for papel, texto in st.session_state["historico_conversas"]:
        st.chat_message(papel).write(texto)

    # Captura a resposta enviada pelo usuário
    resposta_usuario = st.chat_input("Digite a resposta simulada do cliente...")
    
    if resposta_usuario:
        # Exibe e guarda a mensagem do usuário
        st.chat_message("user").write(resposta_usuario)
        st.session_state["historico_conversas"].append(("user", resposta_usuario))
        
        # ----------------------------------------------------------------------
        # PONTO DE INTEGRAÇÃO DA SUA API DE IA:
        # Aqui você fará a chamada da API (ex: OpenAI, Google Gemini, Anthropic).
        # Você deve passar as variáveis 'nome_cli', 'valor_cli' e 'resposta_usuario'
        # dentro do prompt do sistema para que a IA gere a resposta correta.
        # ----------------------------------------------------------------------
        
        # Resposta fictícia estruturada simulando o comportamento da futura API
        resposta_ia = f"Entendido, {nome_cli}. Como você mencionou que '{resposta_usuario}', posso gerar um link de parcelamento para este valor de R$ {valor_cli:,.2f}?"
        
        # Exibe e guarda a resposta gerada pela IA
        st.chat_message("assistant").write(resposta_ia)
        st.session_state["historico_conversas"].append(("assistant", resposta_ia))
