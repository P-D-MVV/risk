import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd 

def calcular_stats(dados):
    media           = np.mean(dados)
    mediana         = np.median(dados)
    desvio_padrao   = np.std(dados)

    return media, mediana, desvio_padrao

def calcular_p80(dados):
    p80_inf = np.percentile(dados, 10)
    p80_sup = np.percentile(dados, 90)

    return p80_inf, p80_sup

def simular_monte_carlo(dados, meta, n_simulacoes, n_dias, tipo_calculo):
    resultados = []
    
    for _ in range(n_simulacoes):
        producao_simulada = np.random.choice(dados, int(n_dias), replace=True)
        decimal = n_dias - int(n_dias)
        if(decimal > 0):
            producao_dia_decimal = np.random.choice(dados, 1, replace=True)
            producao_dia_decimal = producao_dia_decimal * decimal
            producao_simulada = producao_simulada.tolist() + producao_dia_decimal.tolist()
        total = np.sum(producao_simulada)

        if tipo_calculo=="Média":
            total = total/n_dias

        resultados.append(total)

    media, mediana, desvio = calcular_stats(resultados)
    p80_inf, p80_sup = calcular_p80(resultados)

    prob_meta = sum(1 for resultado in resultados if resultado >= meta) / n_simulacoes

    # plt.hist(resultados, bins=15, density=True, alpha=0.7, color='blue')
    # plt.axvline(x=meta, color='red', linestyle='--', label='Target')
    # plt.axvline(x=p80_inf, color='green', linestyle='--', label='p80_lower')
    # plt.axvline(x=p80_sup, color='green', linestyle='--', label='p80_upper')
    # plt.xlabel('Produção Total')
    # plt.ylabel('Densidade de Probabilidade')
    # plt.title('Distribuição da Produção Total')
    # plt.legend()
    # plt.show()
 
    return media, mediana, desvio, p80_inf, p80_sup, prob_meta, resultados

def definir_melhor_distribuicao(dados):
    distributions = [        
        stats.norm, stats.lognorm, stats.expon, stats.gamma, stats.weibull_min,
        stats.weibull_max, stats.pareto, stats.beta, stats.triang
    ]
    
    best_distribution = None
    best_params = None
    best_sse = np.inf

    all_distributions = []
    all_params = []
    all_results_stats = []
    # mean_production = np.mean(results)
    # median_production = np.median(results)
    # std_deviation = np.std(results)
    
    # # Calcular o intervalo de confiança p80
    # p80_lower = np.percentile(results, 10)
    # p80_upper = np.percentile(results, 90)
    for distribution in distributions:
        # Tenta ajustar a distribuição aos dados
        try:
            params = distribution.fit(dados)
            arg = params[:-2]
            loc = params[-2]
            scale = params[-1]

            # Calcula o erro quadrático médio (SSE)
            sse = np.sum((distribution.pdf(dados, loc=loc, scale=scale, *arg) - dados) ** 2)

            # Salva a distribuição se for melhor
            all_distributions.append(distribution)
            all_params.append(params)

            if best_sse > sse > 0:
                best_distribution = distribution
                best_params = params
                best_sse = sse

        except Exception:
            pass

    return best_distribution, best_params, all_distributions, all_params

def gerar_dados_amostrais(dist, params):
    return dist.rvs(*params, size=1000) 

def identificar_indices_consecutivos_abaixo_media(dados, media, tamanho_conjunto=7):
    indices_conjuntos_consecutivos = []

    for i in range(len(dados) - tamanho_conjunto + 1):
        conjunto = dados[i:i+tamanho_conjunto]
        if all(valor < media for valor in conjunto):
            indices_conjuntos_consecutivos.append(i)

    return indices_conjuntos_consecutivos

def identificar_pontos_abaixo(dados, media):
    p_abaixo_media = []
    # print(dados)
    for i in range(dados.index[0], len(dados) - 6):
        if dados[i] < media:
            flag = True
            for dado in dados[i:i+7]:
                if dado>=media: flag=False
            if flag==True: 
                for j in range(i, len(dados)):
                    if dados[j]<media:
                        p_abaixo_media.append(j)
                    elif dados[j]>=media:
                        break


    return p_abaixo_media

def identificar_pontos_acima(dados, media):
    p_acima_media = []
    # print(dados)
    for i in range(dados.index[0], len(dados) - 6):
        if dados[i] > media:
            flag = True
            for dado in dados[i:i+7]:
                if dado<=media: flag=False
            if flag==True: 
                for j in range(i, len(dados)):
                    if dados[j]>media:
                        p_acima_media.append(j)
                    elif dados[j]<=media:
                        break


    return p_acima_media

def definir_nome_distribuicao(dist):
    match dist.name:
            case 'norm':
                modelo = "Normal"
            case 'lognorm':
                modelo = "Logarítmica normal"
            case 'expon':
                modelo = "Exponencial"
            case 'gamma':
                modelo = "Gamma"
            case 'weibull_min':
                modelo = "Weibull mínimo"
            case 'weibull_max':
                modelo = "Weibull máximo"
            case 'pareto':
                modelo = "Pareto"
            case 'beta':
                modelo = "Beta"
            case 'logistic':
                modelo = "Logistic"
            case 'triang':
                modelo = "Triangular"

    return modelo

def retornar_distribuição(nome):
    if nome == "Normal":
        return stats.norm
    if nome == "Logarítmica normal":
        return stats.lognorm
    if nome == "Exponencial":
        return stats.expon
    if nome == "Gamma":
        return stats.gamma
    if nome == "Weibull mínimo":
        return stats.weibull_min
    if nome == "Weibull máximo":
        return stats.weibull_max
    if nome == "Pareto":
        return stats.pareto
    if nome == "Beta":
        return stats.beta
    if nome == "Triangular":
        return stats.triang

def filtrar_acima_da_media(dados, media, coluna):
    dados["flag"] = False
    dados.reset_index(drop=True, inplace=True)
    for i in range(dados.index[0], dados.shape[0] - 6):
        if dados.iloc[i][coluna] > media:
            flag = True
            for dado in dados.iloc[i:i+7][coluna]:
                if dado<=media: flag=False
            if flag==True: 
                for j in range(i, dados.shape[0]):
                    if dados.iloc[j][coluna]>media:
                        dados.at[j, "flag"] = True
                        # dados.iloc[j][coluna] = 0
                        # print(dados.iloc[j][coluna])
                    elif dados.iloc[j][coluna]<=media:
                        break
    filtro = (dados["flag"] == True)
    dados = dados[filtro]

    return dados

def filtrar_abaixo_da_media(dados, media, coluna):
    dados["flag"] = False
    for i in range(dados.index[0], dados.shape[0] - 6):
        if dados.iloc[i][coluna] < media:
            flag = True
            for dado in dados.iloc[i:i+7][coluna]:
                if dado>=media: flag=False
            if flag==True: 
                for j in range(i, dados.shape[0]):
                    if dados.iloc[j][coluna]<media:
                        dados.at[j, "flag"] = True
                    elif dados.iloc[j][coluna]>=media:
                        break
    filtro = (dados["flag"] == True)
    dados = dados[filtro]

    return dados

def identificar_pontos(dados, p80inf, p80sup, media):
    coluna = dados.columns[2]
    # print(dados)

    # media, mediana, desvio_padrao = calcular_stats(dados[coluna])
    pontos_acima = dados[dados[coluna] > p80sup]
    pontos_abaixo = dados[dados[coluna] < p80inf]

    filtro = (dados[coluna] <= p80sup) & (dados[coluna] >= p80inf)
    dados_dentro_p80 = dados[filtro]

    consecutivos_acima = filtrar_acima_da_media(dados_dentro_p80, media, coluna)
    consecutivos_abaixo = filtrar_abaixo_da_media(dados_dentro_p80, media, coluna)
    # print(consecutivos_abaixo)

    pontos = pd.concat([pontos_acima, pontos_abaixo, consecutivos_abaixo, consecutivos_acima])
    print(pontos)
    return pontos