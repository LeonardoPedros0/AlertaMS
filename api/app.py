from flask import Flask, render_template,request
import geradordefiguras as gdf
import os
import pandas as pd
from datetime import datetime, timedelta

diretorio_atual = os.getcwd()
diretorio_script = os.path.dirname(os.path.abspath(__file__))

# Muda o diretório de trabalho para o diretório do script
os.chdir(diretorio_script)

app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    print("\n\n\nDiretório atual:", diretorio_script)
    return render_template('index.html')

@app.route('/AMSPrevisao',methods=['GET'])
def AMSprev():
    data_atual = datetime.now()
    if data_atual.hour in [0,1,2,3]:
        data_atual -= timedelta(hours=data_atual.hour+1)
    pasta_hoje='previsao_'+data_atual.date().strftime("%Y-%m-%d")

    cidade = request.args.get('capital')
    modelos = request.args.getlist('model')
    fig_cidade =1
    limiar_min =1
    limiar_max =1
    if cidade and modelos:
        try: # caso online
            previsoes = gdf.get_raw_file_data(repo_url='https://github.com/AlertaMS/Previsao',pasta=pasta_hoje)
            
            estacoes = gdf.get_raw_file_data(repo_url='https://github.com/AlertaMS/Previsao',pasta='Estacoes',formato='.txt')
            nome_arq = [i for i in estacoes if i.startswith(cidade) and i.endswith('.txt')][0]
            estacoes = pd.read_table(estacoes[nome_arq],sep='\t')
            
            cidades_fig = gdf.get_raw_file_data(repo_url='https://github.com/AlertaMS/Previsao',pasta='Estacoes',formato='.png')
            cidade_fig = [i for i in cidades_fig if i.startswith(cidade) and i.endswith('.png')][0]
            fig_cidade=cidades_fig[cidade_fig]
        except Exception as e: # caso off-online
            print('\n\n','deu erro',e,'\n\n')
            previsoes = [arq for arq in os.listdir(fr'C:\Users\HP\Desktop\AlertaMS\Saida\Previsao\{pasta_hoje}') if arq.endswith('.csv')]
            previsoes = {mod:fr'C:\Users\HP\Desktop\AlertaMS\Saida\Previsao\{pasta_hoje}\{mod}' for mod in previsoes}
            
            estacoes = [arq for arq in os.listdir(fr'C:\Users\HP\Desktop\AlertaMS\Site\api\Estacoes') if arq.endswith('.txt')]
            nome_arq = [i for i in estacoes if i.startswith(cidade) and i.endswith('.txt')][0]
            estacoes = pd.read_table(fr'C:\Users\HP\Desktop\AlertaMS\Site\api\Estacoes\{nome_arq}',sep='\t')
            
            cidades_fig = [arq for arq in os.listdir(r'C:\Users\HP\Desktop\AlertaMS\Site\api\static\img') if arq.endswith('.png')]
            fig_cidade = [f'img/{i}' for i in cidades_fig if i.startswith(cidade) and i.endswith('.png')][0]
            
        limiar_min, limiar_max = gdf.plot_graf_temp(estacoes,previsoes,cidade, modelos)
        
    return render_template('AMSprev.html',cidade=cidade,
                           modelos=modelos,
                           fig_cidade=fig_cidade,
                           limiar_min=limiar_min,
                           limiar_max=limiar_max)

if __name__ == '__main__':
    app.run(debug=True,port=80)
