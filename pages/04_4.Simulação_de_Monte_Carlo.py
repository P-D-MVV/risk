import streamlit as st
import os 
import pandas as pd
import numpy as np
import streamlit_vertical_slider as svs
import matplotlib.pyplot as plt
import seaborn as sns
import io
from db.connection import incrementar_simulador
from pyxlsb import open_workbook as open_xlsb
import plotly.graph_objects as go

from datetime import datetime
from io import BytesIO
from PIL import Image

from functions import *

if "valor_agrupamento_dados" not in st.session_state:
    st.session_state.valor_agrupamento_dados = 15
if "melhor_distribuicao" not in st.session_state:
    st.session_state.melhor_distribuicao = None
if "melhor_parametro" not in st.session_state:
    st.session_state.melhor_parametro = None
if "simulacao_salva" not in st.session_state:
    st.session_state.simulacao_salva = None

st.set_page_config(page_title="Simulação de Monte Carlo", layout="wide", page_icon=":bar_chart:")

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

st.title("Simulação de Monte Carlo")

# dado_selecionado = st.selectbox(label="Selecionar o dado", options=os.listdir("data"), placeholder="Selecionar o dado")
if "df" in st.session_state:
    dado_selecionado = st.session_state.df


    # dados = pd.read_csv(f"data/{dado_selecionado}")
    nome_dado = dado_selecionado.columns[1]
    dados=dado_selecionado
    print(dados)
    menor_data, maior_data = min(dados["Data"]), max(dados["Data"])
    menor_data, maior_data = pd.to_datetime(menor_data), pd.to_datetime(maior_data)
    data_ini = st.date_input(label="Escolha a data início", value=menor_data, min_value=menor_data, max_value=maior_data)
    data_fim = st.date_input(label="Escolha a data fim", value=maior_data, min_value=menor_data, max_value=maior_data)

    dados_filtrados = dados.copy()
    dados_filtrados = dados_filtrados.sort_values(by="Data")

    filtragem = (str(data_ini) <= dados_filtrados["Data"]) & (dados_filtrados["Data"] <= str(data_fim))
    dados_filtrados = dados_filtrados[filtragem]
    dados_data = dados_filtrados["Data"]
    dados = dados_filtrados[nome_dado]

    with st.expander("Estatísticas dos dados"):
        media, mediana = np.mean(dados), np.median(dados)
        menor, maior = min(dados), max(dados)
        desvio, var = np.std(dados), np.var(dados)

        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.metric("Média", f"{media:.2f}")
            with st.container(border=True):
                st.metric("Menor valor", f"{menor:.2f}", f"-{media-menor:.2f}")
        with col2:
            with st.container(border=True):
                st.metric("Mediana", f"{mediana:.2f}")
            with st.container(border=True):
                st.metric("Maior valor", f"{maior:.2f}", f"{maior-media:.2f}")
        with col3:
            with st.container(border=True):
                st.metric("Desvio Padrão", f"{desvio:.2f}")
            with st.container(border=True):
                st.metric("Variância", f"{var:.2f}", "0", delta_color="off")

        col4, col5 = st.columns([7, 1])

        with col5:
            valor_agrupamento = svs.vertical_slider(key="slider", 
                            default_value=15, 
                            step=1, 
                            min_value=1, 
                            max_value=100,
                            slider_color= 'blue', #optional
                            track_color='lightgray', #optional
                            thumb_color = 'darkblue' #optional
                            )
            st.session_state.valor_agrupamento_dados = valor_agrupamento

        with col4:
            # fig = plt.figure(figsize=(16, 8))
            # fig_dados = plt.hist(dados, bins = st.session_state.valor_agrupamento_dados, density=False, alpha=.6, color="blue", label="Histograma dos dados importados")
            # plt.title(f"Histograma dos dados importados ({nome_dado})")
            # st.pyplot(fig)
            fig = go.Figure(data=[go.Histogram(x=dados, nbinsx=st.session_state.valor_agrupamento_dados, marker_color='blue', opacity=0.6, name='Histograma dos dados importados')])
            fig.update_layout(title=f'Histograma dos dados importados ({nome_dado})')
            st.plotly_chart(fig, use_container_width=True)

    with st.expander("Formulário de simulação", expanded=True):
        tipo_de_importacao = st.selectbox(label="Escolha o tipo de importação", options=["Preencher parâmetros", "Importar"])
        if tipo_de_importacao=="Preencher parâmetros":
            melhor_dist, melhor_param, todas_dist, todos_param = definir_melhor_distribuicao(dados)

            meta = st.number_input(label="Meta", value=10000.0, placeholder="Meta")
            n_sim = st.number_input(label="Quantidade de simulações", value=1000, placeholder="Número de simulações")
            n_dias = st.number_input(label="Quantidade de dias", value=7.0, placeholder="Número de dias", step=.25) 
            tipo_calculo = st.selectbox(label="Selecione a forma de calcular", options=["Soma", "Média"])
            distribution = st.selectbox(label="Seleciona a distribuição escolhida", options=[definir_nome_distribuicao(dist) for dist in todas_dist])
            # submit = st.button("Simular")
            print(dados.shape)
        if tipo_de_importacao=="Importar":
            dados_pre = st.file_uploader(label="Insira os dados")
            stats_pre = st.file_uploader(label="Insira as estatísticas")

            if dados_pre and stats_pre:
                dados = pd.DataFrame(pd.read_csv(dados_pre))
                dados = dados[dados.columns[2]]
                estatisticas = pd.DataFrame(pd.read_csv(stats_pre))
                melhor_dist, melhor_param, todas_dist, todos_param = definir_melhor_distribuicao(dados)
                print(todas_dist)

                meta = estatisticas["Meta"][0]
                n_sim = estatisticas["Numero de Simulacoes"][0]
                n_dias = estatisticas["Numero de Dias"][0]
                tipo_calculo = estatisticas["Tipo de Calculo"][0]
                distribution = estatisticas["Distribuicao"][0]

                print(distribution)

        submit = st.button("Simular")

        if submit:
            incrementar_simulador()
            st.session_state.melhor_distribuicao = melhor_dist
            st.session_state.melhor_parametro = melhor_param

            # media_sim, mediana_sim, desvio_sim, p80_inf_sim, p80_sup_sim, prob_meta_sim, resultados_sim = simular_monte_carlo(gerar_dados_amostrais(st.session_state.melhor_distribuicao, st.session_state.melhor_parametro), meta, n_sim, n_dias, tipo_calculo)
            media_sim, mediana_sim, desvio_sim, p80_inf_sim, p80_sup_sim, prob_meta_sim, resultados_sim = simular_monte_carlo(gerar_dados_amostrais(retornar_distribuição(distribution), todos_param[todas_dist.index(retornar_distribuição(distribution))]), meta, n_sim, n_dias, tipo_calculo)
            # fig = plt.figure(figsize=(12, 6))
            # plt.hist(resultados_sim, bins=15, density=True, alpha=.6, color='green', label="Dados da simulação")
            # # plt.hist(dados, bins=15, density=True, alpha=.7, color="blue", label="Dados históricos")
            # plt.axvline(x=meta, color='red', linestyle='--', label=f'Target - {meta:.2f}')
            # plt.axvline(x=p80_inf_sim, color='blue', linestyle='--', label=f'C20 - {p80_inf_sim:.2f}')
            # plt.axvline(x=p80_sup_sim, color='blue', linestyle='--', label=f'C80 - {p80_sup_sim:.2f}')
            # plt.xlabel('Produção Total')
            # plt.ylabel('Densidade de Probabilidade')
            # plt.title(f'''Distribuição da Produção Total\nDado: {nome_dado}\nDistribuição: {definir_nome_distribuicao(retornar_distribuição(distribution))}''')
            # plt.legend()

            fig = go.Figure()
            fig.add_trace(
                go.Histogram(x=resultados_sim, marker_color="green", name=f"Dados de {nome_dado}")
            )
            fig.update_layout(
                title=f"""
                    Distribuição de Produção Total\n
                    Dado: {nome_dado}\n
                    Distribuição: {definir_nome_distribuicao(retornar_distribuição(distribution))} 
                        """,
                xaxis_title="Produção Total",
                yaxis_title="Densidade",
                autosize=True, width=1000
                )
            fig.add_vline(x=meta, line_color="red", name="meta")
            fig.add_vline(x=p80_inf_sim, line_color="blue")
            fig.add_vline(x=p80_sup_sim, line_color="blue")
    

            # fig.add_trace(
            #     go.Scatter(x=[meta], y=[50], mode="lines", name="Meta")
            # )


            st.subheader("Estatísticas da simulação")
            col6, col7, col8 = st.columns(3)

            with col6:
                with st.container(border=True):
                    st.metric("Média", f"{media_sim:.2f}")
                with st.container(border=True):
                    st.metric("C20", f"{p80_inf_sim:.2f}")
            with col7:
                with st.container(border=True):
                    st.metric("Mediana", f"{mediana_sim:.2f}")
                with st.container(border=True):
                    st.metric("C80", f"{p80_sup_sim:.2f}")
            with col8:
                with st.container(border=True):
                    st.metric("Desvio Padrão", f"{desvio_sim:.2f}")
                with st.container(border=True):
                    st.metric("Prob. de atingir a meta", f"{prob_meta_sim:.2%}")

            # st.pyplot(fig)
            st.plotly_chart(fig, use_container_width=True)

            # Curva de probs
            resultados_ord = np.sort(resultados_sim)

            prob_acumulada = np.arange(1, len(resultados_ord) + 1) / len(resultados_ord)

            passo = int(len(resultados_ord) / 100)
            resultados_exibicao = resultados_ord[::passo]
            prob_acumulada_exibicao = prob_acumulada[::passo]

            granularidade_y = 100  # Ajuste conforme necessário
            prob_acumulada_exibicao = np.linspace(0, 1, granularidade_y)

            # Plotar a distribuição de probabilidade acumulada com plotly
            fig2 = go.Figure(data=go.Scatter(x=resultados_exibicao, y=prob_acumulada_exibicao, mode='markers', marker=dict(symbol='circle', size=3.5)))
            fig2.update_layout(title='Distribuição de Probabilidade Acumulada',
                                        xaxis_title='Valores',
                            yaxis_title='Probabilidade Acumulada')
            
            st.plotly_chart(fig2, use_container_width=True)

            # ===================

            df = pd.DataFrame({
                "Meta": meta,
                "Numero de Simulacoes": n_sim,
                "Numero de Dias": n_dias,
                "Tipo de Calculo": tipo_calculo,
                "Distribuicao": distribution,
                "Data": [datetime.now()],
                "Media": [media_sim],
                "Mediana": [mediana_sim],
                "C20": [p80_inf_sim],
                "C80": [p80_sup_sim],
                "Desvio Padrao": [desvio_sim],
                "Probabilidade de atingir a meta": [prob_meta_sim*100]
            })

            # buffer = io.BytesIO()
            # with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            #     df.to_excel(writer, sheet_name='Estatisticas')
            #     writer.save()

            dados_salvar = pd.DataFrame(dados_filtrados)

            baixar_stats = st.download_button("Baixar estatísticas", data=df.to_csv(header=True).encode("utf-8"), file_name="Estatisticas da Simulacao.csv")
            baixar_dados = st.download_button("Baixar dados", data=dados_salvar.to_csv(header=True).encode("utf-8"), file_name="Dados.csv")
                # st.download_button("Salvar simulação", data=writer, file_name="Resultado Monte Carlo.csv")


