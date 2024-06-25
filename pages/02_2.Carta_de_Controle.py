import streamlit as st
import os
import matplotlib.pyplot as plt
import numpy as np
import pprint
from PIL import Image
import random

import plotly.express as px 
import plotly.graph_objects as go

from functions import *

st.set_page_config(page_title="MINE Risk", layout="wide", page_icon=":chart_with_downwards_trend:")

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

st.title("MINE Risk")

if "data_inicial" not in st.session_state:
    st.session_state.data_inicial = None
if "data_final" not in st.session_state:
    st.session_state.data_final = None
if "df" not in st.session_state:
    st.write("Insira dados para prosseguir")
if "df" in st.session_state:
    dados_disponiveis = st.session_state.df
    # print(dados_disponiveis)
    # dado_escolhido = st.selectbox(label="Selecionar dado", options=dados_disponiveis)
    dados = dados_disponiveis
    menor_data, maior_data = min(dados["Data"]), max(dados["Data"])
    menor_data, maior_data = pd.to_datetime(menor_data), pd.to_datetime(maior_data)
    data_ini = st.date_input(label="Escolha a data inicial", value=menor_data, min_value=menor_data, max_value=maior_data)
    data_fim = st.date_input(label="Escolha a data fim", value=maior_data, min_value=menor_data, max_value=maior_data)
    st.session_state.data_inicial = data_ini
    st.session_state.data_final = data_fim
    dados = dados.sort_values(by="Data")
    filtragem = (str(data_ini) <= dados["Data"]) & (dados["Data"] <= str(data_fim))
    dados_s_filtro = dados.copy()
    dados = dados[filtragem]
    # dados_data = dados[dados.columns.values[1]]
    nome_dado = dados.columns[1]
    # dados = dados[nome_dado]

    fig2 = plt.figure(figsize=(12, 6))

    media, mediana, desvio = calcular_stats(dados[nome_dado])
    lsc = media + 3*desvio
    lic = media - 3*desvio
    
    if st.session_state.data_inicial and st.session_state.data_final:
        # print("r")
        layout = go.Layout(
            autosize=True,
            width=1000
        )

        fig = go.Figure(layout=layout)
        # fig.update_layout(width=1000, autosize=True)

        pontos_atencao=identificar_pontos(dados, lic, lsc, media)
        filtered_data = dados

        fig.add_trace(
            go.Scatter(x=filtered_data["Data"], y=filtered_data[nome_dado], mode="lines+markers", name="Dados")
        )

        fig.add_trace(
            go.Scatter(x=filtered_data["Data"], y=[lsc] * len(filtered_data["Data"]), mode="lines", line=dict(color="rgb(255, 0, 0)"), name="Limite Superior")
        )

        fig.add_trace(
            go.Scatter(x=filtered_data["Data"], y=[lic] * len(filtered_data["Data"]), mode="lines", line=dict(color="rgb(255, 0, 0)"), name="Limite Inferior")
        )

        fig.add_trace(
            go.Scatter(
                x=filtered_data["Data"], y=[media] * len(filtered_data["Data"]), mode="lines", name="Média global", line=dict(color="rgb(255, 255, 0)")
            )
        )

        fig.add_trace(
            go.Scatter(
                x=pontos_atencao["Data"], y=pontos_atencao[nome_dado], mode="markers", name="Causas especiais", marker=dict(color="rgb(255, 0, 0)")
            )
        )

        periodos = st.checkbox("Mostrar períodos (recurso experimental)")
        if periodos:
            import ruptures as rpt
            n_samples, dim, sigma = len(dados_s_filtro[nome_dado]), 2, 4
            n_bkps = 4  # number of breakpoints
            signal, bkps = rpt.pw_constant(n_samples, dim, n_bkps, noise_std=sigma)

            # detection
            algo = rpt.Pelt(model="rbf").fit(dados_s_filtro[nome_dado].values.reshape(-1, 1))
            result = algo.predict(pen=10)

            for bkp in bkps:
                try:
                    fig.add_vline(x=filtered_data["Data"][bkp], line_width=1.2, line_color="brown")
                except: 
                    pass

            bkps.insert(0, 0)

            # for i in range(len(bkps)):
            #     if i > 3:
            #         bkps[i] = bkps[i]-1

            for i in range(len(bkps)-1):
                i0 = bkps[i]
                i1 = bkps[i+1] - 1  # Ajuste para usar corretamente o índice final
                if i > 1:
                    i1 -= 2
                if i > 2:
                    i0 -= 2
                if i> 3:
                    i1 -= 1
                media_per = np.mean(filtered_data[nome_dado][i0:i1+1])  # Calcular a média corretamente
                fig.add_trace(
                    go.Scatter(x=filtered_data["Data"][i0:i1+2], y=[media_per] * len(filtered_data["Data"][i0:i1+2]), mode="lines", name=f"Média do período {i+1}", marker=dict(color="rgb(0, 0, 153)"))
                )

        st.plotly_chart(fig, use_container_width=True)
