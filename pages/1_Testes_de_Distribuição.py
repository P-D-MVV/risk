import streamlit as st
import pandas as pd 
import os 
import pprint

from functions import *

st.set_page_config(page_title="Testes de Distribuição", layout="wide")

st.title("Testes de distribuição")

dado_selecionado = st.selectbox(label="Selecionar o dado", options=os.listdir("data"))

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

    with st.expander("Mais informações (Passo a passo)"):
        dists = [definir_nome_distribuicao(dist) for dist in todas_dist]
             
        st.markdown(f'<div style="text-align: justify;"> Este módulo serve para indicar qual a distribuição mais parecida com os dados selecionados. São testadas as seguintes distribuições:<br><br>{dists}<br><br>Para cada distribuição, é calculado o erro quadrático médio (SSE) para determinar qual a distribuição mais parecida com os dados selecionados. A distribuição que obtiver o menor SSE, será indicado pelo algoritmo como a distribuição recomendada. Após esse processo, a distribuição recomendada será utilizada para gerar dados amostrais semelhantes aos dados selecionados. No final, o resultado deste processo é exibido na tela, permitindo a comparação entre os dados gerados pela distribuição recomendada com os dados selecionados. Esta distribuição será utilizada na Simulação de Monte Carlo para geração de dados com base nos parâmetros determinados pelo usuário. </div>', unsafe_allow_html=True)
        
