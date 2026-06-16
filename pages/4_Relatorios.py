
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Relatórios")

df = pd.DataFrame({
"Motivo":["Esquecimento","Sem dinheiro","Banco","Outros"],
"Qtd":[35,28,22,15]
})

fig = px.pie(df,names="Motivo",values="Qtd",title="Motivos de Inadimplência")
st.plotly_chart(fig,use_container_width=True)
