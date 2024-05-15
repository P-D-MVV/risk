import streamlit as st
import os
import matplotlib.pyplot as plt
import numpy as np
import pprint

from algorithms.functions import *

st.set_page_config(page_title="MINE Risk", layout="wide")

st.title("MINE Risk")

dados_disponiveis = os.listdir("data")

if not dados_disponiveis:
    st.write("""
             Nenhum dado disponível. 
             Por favor, insira os dados na página Integração de Dados""")
elif dados_disponiveis:
    dado_escolhido = st.selectbox(label="Selecionar dado", options=dados_disponiveis)
    dados = pd.read_csv(f"data/{dado_escolhido}")
    dados = dados.sort_values(by="Data")
    dados_data = dados[dados.columns.values[1]]
    nome_dado = dado_escolhido.split(".")[0]
    dados = dados[nome_dado]

    fig2 = plt.figure(figsize=(12, 6))

    media, mediana, desvio = calcular_stats(dados)
    lsc = media + 3*desvio
    lic = media - 3*desvio

    plt.axhline(lsc, color="red", linestyle="--", label=f"{lsc:.2f} LSC")
    plt.axhline(lic, color="red", linestyle="--", label=f"{lic:.2f} LIC")
    plt.axhline(media, color="orange", linestyle="--", label=f"{media:.2f} Média")
    plt.plot(dados_data, dados, color="blue", linestyle="-", zorder=1)
    plt.xticks(rotation=90)
    plt.title(f"Carta de Controle da produção total ({nome_dado})")
    plt.legend()

    for dado, data in zip(dados, dados_data):
        if(dado>lsc or dado<lic):
            plt.scatter(x=data, y=dado, color="red", s=40)
        else:
            plt.scatter(x=data, y=dado, color="blue", s=20)

    indices_7p_acima_media = identificar_pontos_abaixo(dados, media)

    for index in indices_7p_acima_media:
        plt.scatter(x=dados_data[index], y=dados[index], color="red", s=40)

    st.pyplot(fig2)
