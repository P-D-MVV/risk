import streamlit as st
import pandas as pd 
import os 
import pprint

from functions import *

st.set_page_config(page_title="Testes de Distribuição", layout="wide", page_icon=":mountain:")

st.title("Testes de distribuição")

dado_selecionado = st.selectbox(label="Selecionar o dado", options=os.listdir("data"), placeholder="Selecionar o dado")

simular = st.button(label="Simular")

if simular:
    dados = pd.read_csv(f"data/{dado_selecionado}")
    coluna_especifica = dado_selecionado.split(".")[0]
    dados = dados[coluna_especifica]
    melhor_dist, melhor_param, todas_dist, todos_param = definir_melhor_distribuicao(dados)
    st.session_state.melhor_distribuicao = melhor_dist
    st.session_state.melhor_parametro = melhor_param
    for dist, param in zip(todas_dist, todos_param):
        modelo = definir_nome_distribuicao(dist)
        if dist.name == melhor_dist.name:
            modelo += " (Recomendado)"

        with st.expander(modelo):
            dados_amostrais = gerar_dados_amostrais(dist, param)
            media_amostral, mediana_amostral, desvio_amostral = calcular_stats(dados_amostrais)

            col1, col2, col3 = st.columns(3)

            with col1:
                with st.container(border=True):
                    st.metric("Média amostral", f"{media_amostral:.2f}")
            with col2:
                with st.container(border=True):    
                    st.metric("Mediana amostral", f"{mediana_amostral:.2f}")
            with col3:
                with st.container(border=True):    
                    st.metric("Desvio padrão amostral", f"{desvio_amostral:.2f}")

            fig = plt.figure(figsize=(12, 6))
            fig_amostra = plt.hist(dados_amostrais, bins = 15, density=False, alpha=.6, color="green", label="Dados gerados pela distribuição")
            fig_dados = plt.hist(dados, bins = 15, density=False, alpha=.6, color="blue", label="Dados importados")
            plt.title(f"Comparação: dados importados X dados gerados pela distribuição ({coluna_especifica})")
            plt.legend()
            st.pyplot(fig)
