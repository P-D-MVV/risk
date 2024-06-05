import streamlit as st
import os
import matplotlib.pyplot as plt
import numpy as np
import pprint

import plotly.express as px 
import plotly.graph_objects as go

from functions import *

st.set_page_config(page_title="MINE Risk", layout="wide", page_icon=":chart_with_downwards_trend:")

st.title("MINE Risk")

if "data_inicial" not in st.session_state:
    st.session_state.data_inicial = None
if "data_final" not in st.session_state:
    st.session_state.data_final = None

dados_disponiveis = os.listdir("data")

if not dados_disponiveis:
    st.write("""
             Nenhum dado disponível. 
             Por favor, insira os dados na página Integração de Dados""")
elif dados_disponiveis:
    dado_escolhido = st.selectbox(label="Selecionar dado", options=dados_disponiveis)
    dados = pd.read_csv(f"data/{dado_escolhido}")
    menor_data, maior_data = min(dados["Data"]), max(dados["Data"])
    menor_data, maior_data = pd.to_datetime(menor_data), pd.to_datetime(maior_data)
    data_ini = st.date_input(label="Escolha a data inicial", value=menor_data, min_value=menor_data, max_value=maior_data)
    data_fim = st.date_input(label="Escolha a data fim", value=maior_data, min_value=menor_data, max_value=maior_data)
    st.session_state.data_inicial = data_ini
    st.session_state.data_final = data_fim
    dados = dados.sort_values(by="Data")
    filtragem = (str(data_ini) <= dados["Data"]) & (dados["Data"] <= str(data_fim))
    dados = dados[filtragem]
    # dados_data = dados[dados.columns.values[1]]
    nome_dado = dado_escolhido.split(".")[0]
    # dados = dados[nome_dado]

    fig2 = plt.figure(figsize=(12, 6))

    media, mediana, desvio = calcular_stats(dados[nome_dado])
    lsc = media + 3*desvio
    lic = media - 3*desvio
    
    if st.session_state.data_inicial and st.session_state.data_final:
        print("r")
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
                x=filtered_data["Data"], y=[media] * len(filtered_data["Data"]), mode="lines", name="Média", line=dict(color="rgb(255, 255, 0)")
            )
        )

        fig.add_trace(
            go.Scatter(
                x=pontos_atencao["Data"], y=pontos_atencao[nome_dado], mode="markers", name="Causas especiais", marker=dict(color="rgb(255, 0, 0)")
            )
        )

        st.plotly_chart(fig, use_container_width=True)