import streamlit as st
import pandas as pd 
st.set_page_config(page_title="Integração de Dados", layout="wide", page_icon=":newspaper:")

st.title("Integração de Dados do MINE Risk")

uploaded = st.file_uploader("Faça upload dos dados", accept_multiple_files=False)

if uploaded:
    if ".xlsx" in uploaded.name:
        dados = pd.read_excel(uploaded, None)
        planilha_selecionada = st.selectbox(label="Selecionar planilha", options=[s for s, content in dados.items()])
        dados = pd.read_excel(uploaded, sheet_name=planilha_selecionada)

    colunas = dados.columns.values

    coluna_selecionada = st.selectbox(label="Selecionar coluna", options=colunas)
    coluna_data = st.selectbox(label="Selecionar coluna da data", options=colunas)
    
    salvar = st.button(label="Salvar dado")
    if salvar:
        try:
            dados = dados.loc[:, [coluna_data, coluna_selecionada]]

            dados[coluna_selecionada] = pd.to_numeric(dados[coluna_selecionada], errors="coerce")
            dados = dados.dropna()
            dados = dados.sort_values(by="Data")

            dados.to_csv(f"data/{coluna_selecionada}.csv", header=True)
            st.success("Dados salvos")
        except:
            st.error("Não foi possível salvar os dados ")
