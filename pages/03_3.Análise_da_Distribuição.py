import streamlit as st
import pandas as pd 
import os 
import pprint
from PIL import Image

from functions import *

st.set_page_config(page_title="Testes de Distribuição", layout="wide", page_icon=":mountain:")

col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    image = Image.open("assets/Imagem3.png")
    new_image = image.resize((125, 50))
    st.image(new_image)
with col2:
    image = Image.open("assets/Imagem1 1.jpg")
    new_image = image.resize((150, 50))
    st.image(new_image)
with col3:
    image = Image.open("assets/Imagem2.png")
    new_image = image.resize((125, 50))
    st.image(new_image)
with col4:
    image = Image.open("assets/Imagem4.png")
    new_image = image.resize((125, 50))
    st.image(new_image)

st.title("Testes de distribuição")

# dado_selecionado = st.selectbox(label="Selecionar o dado", options=os.listdir("data"), placeholder="Selecionar o dado")
if "df" in st.session_state:
    dado_selecionado = st.session_state.df

simular = st.button(label="Simular")

if simular:
    dados = dado_selecionado[dado_selecionado.columns[1]]
    # coluna_especifica = dado_selecionado.split(".")[0]
    # dados = dados[coluna_especifica]
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
            import plotly.graph_objects as go

            fig = go.Figure()
            fig.add_trace(go.Histogram(x=dados_amostrais, nbinsx=15, marker_color='green', opacity=0.6, name='Dados gerados pela distribuição'))
            fig.add_trace(go.Histogram(x=dados, nbinsx=15, marker_color='blue', opacity=0.6, name='Dados importados'))
            fig.update_layout(title='Comparação: dados importados X dados gerados pela distribuição', barmode='overlay')
            fig.update_traces(opacity=0.6)
            st.plotly_chart(fig, use_container_width=True)
            # fig = plt.figure(figsize=(12, 6))
            # fig_amostra = plt.hist(dados_amostrais, bins = 15, density=False, alpha=.6, color="green", label="Dados gerados pela distribuição")
            # fig_dados = plt.hist(dados, bins = 15, density=False, alpha=.6, color="blue", label="Dados importados")
            # plt.title(f"Comparação: dados importados X dados gerados pela distribuição")
            # plt.legend()
            # st.pyplot(fig)
