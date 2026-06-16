
import streamlit as st
import pandas as pd

st.title("👥 Clientes")

df = pd.DataFrame({
"Cliente":["João","Maria","Pedro","Ana","Lucas"],
"Telefone":["9999-1111","9999-2222","9999-3333","9999-4444","9999-5555"],
"Status":["Em atraso","Pago","Negociando","Pago","Pago"],
"Valor":["150","500","230","900","120"]
})

st.dataframe(df,use_container_width=True)
st.button("Novo Cliente")
