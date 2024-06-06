import streamlit as st
import pandas as pd 
from db.connection import incrementar_acesso

st.set_page_config(page_title="Integração de Dados", layout="wide", page_icon=":newspaper:")

st.title("Integração de Dados do MINE Risk")

incrementar_acesso()

uploaded = st.file_uploader("Faça upload dos dados", accept_multiple_files=False)

if uploaded:
    if ".xlsx" in uploaded.name:
        dados = pd.read_excel(uploaded, None)
        planilha_selecionada = st.selectbox(label="Selecionar planilha", options=[s for s, content in dados.items()])
        dados = pd.read_excel(uploaded, sheet_name=planilha_selecionada)

    colunas = dados.columns.values

    coluna_data = st.selectbox(label="Selecionar coluna da data", options=colunas)
    coluna_selecionada = st.selectbox(label="Selecionar coluna", options=colunas)
    nome_arquivo = st.text_input(label="Digite um nome para salvar o arquivo")
    
    salvar = st.button(label="Salvar dado")
    if salvar:
        try:
            dados = dados.loc[:, [coluna_data, coluna_selecionada]]
            dados[coluna_selecionada] = dados[coluna_selecionada].replace('-', pd.NA)
            dados = dados.dropna(axis=0, how="any")
            dados[coluna_selecionada] = pd.to_numeric(dados[coluna_selecionada], errors="coerce")
            dados[nome_arquivo] = dados[coluna_selecionada]
            dados = dados.loc[:, ["Data", nome_arquivo]]
            dados = dados.sort_values(by="Data")
            print(f"data/{coluna_selecionada}")

            dados.to_csv(f"""data/{nome_arquivo}.csv""", header=True)
            st.success("Dados salvos")
        except:
            st.error("Não foi possível salvar os dados ")
