
import streamlit as st

st.title("🤖 Negociação IA")

historico = [
("assistant","Olá João. Identificamos uma pendência de R$150."),
("user","Consigo pagar apenas semana que vem."),
("assistant","Posso parcelar em 2x sem juros.")
]

for role,msg in historico:
    st.chat_message(role).write(msg)

msg = st.chat_input("Digite uma resposta")
if msg:
    st.chat_message("user").write(msg)
    st.chat_message("assistant").write("Obrigado. Esta é uma resposta simulada da CobraAI.")
