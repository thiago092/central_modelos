import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from tabs import data_preparation, regression_models, classification_models, recommendation_system, clustering_models

# Função para carregar dashboards salvos
def load_dashboards():
    if os.path.exists("saved_dashboards.json"):
        with open("saved_dashboards.json", "r") as f:
            return json.load(f)
    else:
        return {}

# Função para salvar um novo dashboard
def save_dashboard(dashboard_name, config, figures):
    dashboards = load_dashboards()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dashboards[dashboard_name] = {
        "timestamp": timestamp,
        "config": config,
        "figures": figures
    }
    with open("saved_dashboards.json", "w") as f:
        json.dump(dashboards, f)

# Carregar dashboards existentes
dashboards = load_dashboards()

# Título principal do App
st.title("Plataforma de Análise e Modelagem de Dados")

# Definindo o menu horizontal superior com abas
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Início", 
    "1. Preparação de Dados", 
    "2. Modelos de Regressão", 
    "3. Modelos de Classificação", 
    "4. Sistema de Recomendação",
    "5. Modelos de Clustering",
    "6. Dashboard Personalizado"
])

# Tela de boas-vindas
with tab1:
    st.write("### Bem-vindo à Plataforma de Análise e Modelagem de Dados!")
    st.write("""
        Esta plataforma permite realizar análises e modelagens de dados completas, 
        com preparação de dados, regressão, classificação, sistemas de recomendação e clustering.
        
        Use o menu acima para navegar entre as seções.
    """)

# Seção de Preparação de Dados
with tab2:
    st.subheader("1. Preparação de Dados")
    data = data_preparation.run()  # Executa a preparação e armazenamento dos dados
    if data is not None:
        st.session_state["data"] = data  # Salva os dados carregados para todas as outras abas

# Seção de Modelos de Regressão
with tab3:
    st.subheader("2. Modelos de Regressão")
    data = st.session_state.get("data")
    if data is not None:
        regression_models.run(data)
    else:
        st.warning("Carregue os dados na seção 'Preparação de Dados' antes de usar esta seção.")

# Seção de Modelos de Classificação
with tab4:
    st.subheader("3. Modelos de Classificação")
    data = st.session_state.get("data")
    if data is not None:
        classification_models.run(data)
    else:
        st.warning("Carregue os dados na seção 'Preparação de Dados' antes de usar esta seção.")

# Seção de Sistema de Recomendação
with tab5:
    st.subheader("4. Sistema de Recomendação")
    data = st.session_state.get("data")
    if data is not None:
        recommendation_system.run(data)
    else:
        st.warning("Carregue os dados na seção 'Preparação de Dados' antes de usar esta seção.")

# Seção de Modelos de Clustering
with tab6:
    st.subheader("5. Modelos de Clustering")
    data = st.session_state.get("data")
    if data is not None:
        clustering_models.run(data)
    else:
        st.warning("Carregue os dados na seção 'Preparação de Dados' antes de usar esta seção.")

# Seção de Dashboard Personalizado
with tab7:
    st.subheader("6. Dashboard Personalizado")

    # Verifica se os dados foram carregados na preparação de dados
    data = st.session_state.get("data")
    if data is not None:
        st.write("Visualização dos Dados Carregados:")
        st.dataframe(data)

        # Configuração do gráfico personalizado
        st.subheader("Configuração de Gráficos Personalizados")

        # Configuração do gráfico
        chart_type = st.selectbox("Escolha o tipo de gráfico", ["Linha", "Dispersão", "Barras", "Histograma"])
        x_column = st.selectbox("Selecione a coluna para o eixo X", data.columns)
        y_column = st.selectbox("Selecione a coluna para o eixo Y", data.columns)

        # Visualização do gráfico personalizado
        fig, ax = plt.subplots()
        if chart_type == "Linha":
            sns.lineplot(x=data[x_column], y=data[y_column], ax=ax)
        elif chart_type == "Dispersão":
            sns.scatterplot(x=data[x_column], y=data[y_column], ax=ax)
        elif chart_type == "Barras":
            sns.barplot(x=data[x_column], y=data[y_column], ax=ax)
        elif chart_type == "Histograma":
            sns.histplot(data[y_column], kde=True, ax=ax)

        st.pyplot(fig)

        # Configuração do dashboard para salvamento
        st.subheader("Salvar Dashboard")
        dashboard_name = st.text_input("Nome para o Dashboard")

        if st.button("Salvar Dashboard") and dashboard_name:
            # Salvando configuração do gráfico e parâmetros
            config = {
                "chart_type": chart_type,
                "x_column": x_column,
                "y_column": y_column
            }
            save_dashboard(dashboard_name, config, {"fig": fig})
            st.success(f"Dashboard '{dashboard_name}' salvo com sucesso!")
    else:
        st.warning("Carregue os dados na aba 'Preparação de Dados' para usar o Dashboard Personalizado.")

    # Exibir dashboards salvos
    st.subheader("Dashboards Salvos")
    if dashboards:
        for name, dashboard in dashboards.items():
            st.write(f"**Dashboard**: {name}")
            st.write(f"Data de Criação: {dashboard['timestamp']}")

            # Exibir configuração e recriar gráficos
            config = dashboard["config"]
            st.write(f"Tipo de Gráfico: {config['chart_type']}")
            st.write(f"Eixo X: {config['x_column']}")
            st.write(f"Eixo Y: {config['y_column']}")

            # Recriar o gráfico salvo
            fig, ax = plt.subplots()
            if config["chart_type"] == "Linha":
                sns.lineplot(x=data[config["x_column"]], y=data[config["y_column"]], ax=ax)
            elif config["chart_type"] == "Dispersão":
                sns.scatterplot(x=data[config["x_column"]], y=data[config["y_column"]], ax=ax)
            elif config["chart_type"] == "Barras":
                sns.barplot(x=data[config["x_column"]], y=data[config["y_column"]], ax=ax)
            elif config["chart_type"] == "Histograma":
                sns.histplot(data[config["y_column"]], kde=True, ax=ax)

            st.pyplot(fig)
            st.write("---")
    else:
        st.info("Nenhum dashboard salvo encontrado.")
