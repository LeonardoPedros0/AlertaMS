
# 🌤️ Alerta Meteorológico de Saúde

Este projeto é uma aplicação web que utiliza previsões meteorológicas e análise de dados climáticos para alertar sobre condições que possam impactar a saúde. Ele apresenta informações organizadas e visualizações interativas para facilitar o entendimento de alertas de temperatura e condições climáticas em diferentes regiões do Brasil.

---

## 🚀 Tecnologias Utilizadas

- **HTML**: Estrutura da interface web.
- **CSS**: Estilização da interface para um design amigável e responsivo.
- **Python (Flask)**: Framework web usado para desenvolver a aplicação.
- **Plotly**: Para criar gráficos interativos e visualizações de dados.
- **Pandas**: Para manipulação e análise de dados meteorológicos.
- **Gerador de Figuras**: Um módulo personalizado para gerar visualizações.
- **Data Sources**: Modelos meteorológicos como ECMWF, GFS, JMA e DWD.

---

## 📋 Funcionalidades

1. **Página Inicial**: Apresenta os dados meteorológicos e alertas.
2. **Modelos Meteorológicos**:
   - ECMWF CF
   - ECMWF FC
   - GFS
   - JMA
   - DWD
3. **Alertas de Temperatura**:
   - Baseado em limites regionais definidos:
     - **Frio extremo** e **calor extremo**.
     - Exemplos:
       - São Paulo, SP: Frio abaixo de 13.1°C | Calor acima de 26.2°C.
       - Recife, PE: Frio abaixo de 23.45°C | Calor acima de 28.4°C.
4. **Gráficos Interativos**:
   - Zoom, panorâmica e ferramentas avançadas de análise.
   - Comparação de dados climáticos.

---

## 🛠️ Configuração do Ambiente

### **Pré-requisitos**
- Python 3.8 ou superior.
- Virtualenv (opcional, mas recomendado).

### **Passo a Passo**
1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/seurepositorio.git
   cd seurepositorio


2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```bash
   python app.py
   ```

5. Acesse no navegador:
   - URL: `http://127.0.0.1:5000`

---

## 📊 Dados e Visualizações

### Modelos Meteorológicos
Os modelos meteorológicos utilizados incluem:
- **ECMWF (CF e FC)**
- **GFS**
- **JMA**
- **DWD**

### Limiares de Temperatura
Os limites de temperatura para cada cidade foram definidos como:
- Exemplo: `{'Manaus_AM': (24.20, 30.50)}`

### Ferramentas de Gráficos
O projeto utiliza botões interativos do Plotly para:
- Zoom 2D, panorâmica, seleção com laço.
- Comparação de dados em gráficos interativos.

---

## 📁 Estrutura do Projeto

```
.
├── app.py                  # Arquivo principal da aplicação Flask
├── static/
│   ├── css/
│   │   └── styles.css      # Arquivo de estilos CSS
├── templates/
│   ├── base.html           # Template principal da aplicação
│   └── index.html          # Página inicial
├── geradordefiguras.py     # Módulo personalizado para visualizações
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação do projeto
```

---
