import streamlit as st
from db.connection import consultar_contador

st.set_page_config(page_title="Mais Informações", layout="wide", page_icon=":information_source:")

acessos, simulador = consultar_contador()

col1, col2 = st.columns([1, 1])

with col1:
    with st.container(border=True):
        st.metric("Acessos aos Mine RISK", acessos)
with col2:
    with st.container(border=True):
        st.metric("Simulações no Mine RISK", simulador)

with st.expander("Análise de Distribuição"):
    dists = ['Normal', 'Logarítmica normal', 'Exponencial', 'Gamma', 'Weibull mínimo', 'Weibull máximo', 'Pareto', 'Beta', 'Triangular']
            
    st.markdown(f'<div style="text-align: justify;"> Este módulo serve para indicar qual a distribuição mais parecida com os dados selecionados. São testadas as seguintes distribuições:<br><br>{dists}<br><br>Para cada distribuição, é calculado o erro quadrático médio (SSE) para determinar qual a distribuição mais parecida com os dados selecionados. A distribuição que obtiver o menor SSE, será indicado pelo algoritmo como a distribuição recomendada. Após esse processo, a distribuição recomendada será utilizada para gerar dados amostrais semelhantes aos dados selecionados. No final, o resultado deste processo é exibido na tela, permitindo a comparação entre os dados gerados pela distribuição recomendada com os dados selecionados. Esta distribuição será utilizada na Simulação de Monte Carlo para geração de dados com base nos parâmetros determinados pelo usuário. </div>', unsafe_allow_html=True)
    
