import streamlit as st
from openai import OpenAI

st.title("🤖 Negociação IA")

api_key = st.session_state.get("gemini_api_key")

historico = [
    ("assistant", "Olá João. Identificamos uma pendência de R$150."),
    ("user", "Consigo pagar apenas semana que vem."),
    ("assistant", "Posso parcelar em 2x sem juros.")
]

for role, msg in historico:
    st.chat_message(role).write(msg)

msg = st.chat_input("Digite uma resposta")
if msg:
    st.chat_message("user").write(msg)
    
    if api_key:
        try:
            client = OpenAI(api_key=api_key.strip(), base_url="https://api.deepseek.com/v1")
            
            mensagens_api = [
                {"role": "system", "content": "Você é a CobraAI, um assistente de negociação amigável de cobranças."},
                {"role": "assistant", "content": "Olá João. Identificamos uma pendência de R$150."},
                {"role": "user", "content": "Consigo pagar apenas semana que vem."},
                {"role": "assistant", "content": "Posso parcelar em 2x sem juros."},
                {"role": "user", "content": msg} # A mensagem nova que o usuário acabou de digitar
            ]
            
            resposta = client.chat.completions.create(
                model="deepseek-chat",
                messages=mensagens_api,
                temperature=0.7
            )
            
            resposta_ia = resposta.choices[0].message.content
            st.chat_message("assistant").write(resposta_ia)
            
        except Exception as e:
            st.chat_message("assistant").write(f"Erro ao conectar ao DeepSeek: {e}")
    else:
        st.chat_message("assistant").write("Obrigado. Esta é uma resposta simulada da CobraAI (Insira a API Key para resposta real).")
