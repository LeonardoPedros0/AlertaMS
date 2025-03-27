import requests
import pandas as pd
import plotly.graph_objects as go


def get_raw_file_data(repo_url, pasta='',formato = '.csv', token=None):
    # Obtém a URL do repositório
    if not repo_url.endswith('/'):
        repo_url += '/'
    api_url = repo_url.replace('github.com', 'api.github.com/repos') + 'contents/' + pasta

    # Prepara os cabeçalhos com o token de acesso pessoal para autenticação
    headers = {'Authorization': f'token {token}'} if token else {}

    # Envia uma solicitação GET para a API do GitHub para obter os conteúdos do repositório
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        print("Erro ao acessar o repositório:", response.status_code)
        return {}

    # Analisa a resposta JSON
    contents = response.json()

    # Extrai os dados brutos dos arquivos
    raw_file_data = {}
    for item in contents:
        if item['type'] == 'file' and item['name'].endswith(formato):  # Adapte para o formato do seu arquivo
            file_url = item['download_url']
            file_name = item['name']
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                raw_file_data[file_name] = file_url  # Supondo que seja um arquivo de texto
            else:
                print(f"Erro ao obter o arquivo '{file_name}':", file_response.status_code)

    return raw_file_data

dict_modelos = {
    "ecmwf_cf": "ECMWF CF",
    "ecmwf_fc": "ECMWF FC",
    "GFS_thredds": "GFS",
    "rjtd_cf": "JMA",
    "dwd_fc": "DWD"
}
dic_temp = {'temp_max':'Máx.','temp_min':'Min.'}
plotly_buttons = [
    "zoom2d",                   # Ferramenta de zoom para gráficos 2D
    "pan2d",                    # Ferramenta de panorâmica para gráficos 2D
    "lasso2d",                  # Ferramenta de seleção laço para gráficos 2D
    "zoomIn2d",                 # Ferramenta de zoom in para gráficos 2D
    "zoomOut2d",                # Ferramenta de zoom out para gráficos 2D
    "autoScale2d",              # Reajustar automaticamente o gráfico 2D
    "hoverClosestCartesian",    # Mostrar o ponto mais próximo no gráfico cartesiano
    "hoverCompareCartesian",    # Mostrar a comparação dos valores no gráfico cartesiano
    "hoverClosestGl2d",         # Mostrar o ponto mais próximo no gráfico WebGL 2D
    "hoverClosestPie",          # Mostrar o ponto mais próximo no gráfico de pizza
    "toggleHover",              # Alternar a exibição das etiquetas de hover
    "resetViewMapbox"           # Redefinir a vista do gráfico Mapbox
]     
limiares_temp = {        #Frio  #Quente
      'Manaus_AM'      : (24.20, 30.50),
      'Natal_RN'       : ( 9.95, 27.50),
      'Porto Alegre_RS': (10.00, 27.45),
      'Recife_PE'      : (23.45, 28.40),
      'Salvador_BA'    : (23.30, 28.10),
      'Sao Luis_MA'    : (24.90, 28.50),
      'Sao Paulo_SP'   : (13.10, 26.20),
      'Teresina_PI'    : (24.85, 30.80)
    } 

def plot_graf_temp(estacoes,previsoes,cidade, modelos):
    estacoes = estacoes['Estacao']
    estacoes = estacoes.astype(str)
    fig = go.Figure()
    for modelo in modelos:
        df = pd.read_table(previsoes[[i for i in previsoes if i.startswith(modelo)][0]],sep='\t')
        df['Cod_estacao'] = df['Cod_estacao'].astype(str)
        for estacao in estacoes:
            for temp in ['temp_max','temp_min']:
                df_ = df[df['Cod_estacao'] == estacao]
                fig.add_trace(go.Scatter(
                    x=df_['date_time'],
                    y=df_[temp],
                    mode='markers+lines',  # Adiciona linhas entre os marcadores
                    name=dic_temp[temp]+' ('+str(estacao)+'-'+str(dict_modelos[modelo])+')',
                    line=dict(dash='dot')  # Define o estilo da linha como pontilhada
                ))
        fig.update_layout(
            xaxis_title="Data e Hora (UTC)",
            yaxis_title="Temperatura (°C)",
            # legend_title="Modelos",
            legend=dict(
                orientation="h",    # Define a orientação da legenda para horizontal (em cima)
                yanchor="top",      # Define o ponto de ancoragem da legenda como o topo
                y=1.8 if len(modelos)>=3 else 1.15,             # Define a posição vertical da legenda
                xanchor="left",     # Define o ponto de ancoragem horizontal da legenda como a direita
                x=-0.015            # Define a posição horizontal da legenda
                ),
            margin=dict(l=2, r=1, t=130, b=2),
            height=500,
            showlegend=True,  # Mantém a legenda visível
            )
    for limiar, cor, nome in zip(limiares_temp[cidade], ['Red', 'Blue'], ['limiar superior', 'limiar inferior']):
        # Adiciona a linha horizontal no eixo y com um valor fixo
        fig.add_shape(
            type='line',
            x0=df['date_time'].min(),  # Início no eixo x (mínimo da data)
            x1=df['date_time'].max(),  # Fim no eixo x (máximo da data)
            y0=limiar,  # Valor fixo no eixo y
            y1=limiar,  # Mesmo valor fixo no eixo y
            line=dict(
                color=cor,   # Cor da linha
                width=2,     # Espessura da linha
                dash='dashdot'  # Estilo da linha (opcional: 'solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot')
            ),
            name=nome  # Nome para a linha na legenda
        )
    fig.write_html(f"./templates/grafico.html",config={'modeBarButtonsToRemove': plotly_buttons,'displaylogo': False})
    return limiares_temp[cidade]