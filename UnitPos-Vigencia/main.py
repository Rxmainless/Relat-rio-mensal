import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Configuração inicial do app
st.set_page_config(
    page_title="Dashboard SGCor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização com CSS
st.markdown(
    """
    <style>
    /* Fundo geral */
    .main {
        background-color: #F0F4F8;
    }
    /* Barra lateral */
    .sidebar .sidebar-content {
        background-color: #2E4053;
        color: white;
    }
    .sidebar h1, .sidebar h2, .sidebar h3 {
        color: #ffffff;
    }
    /* Cabeçalho */
    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
        color: #1F618D;
    }
    /* KPIs */
    .metric-container {
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
    }
    .metric-box {
        padding: 1.5rem;
        background-color: #ffffff;
        border-radius: 8px;
        text-align: center;
        flex: 1;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-box h3 {
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
        color: #34495E;
    }
    .metric-box p {
        margin: 0;
        font-size: 1.5rem;
        font-weight: bold;
        color: #2E86C1;
    }
    /* Ajuste para gráficos */
    .plotly-chart {
        padding: 2rem;
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Função para carregar e depurar os dados
@st.cache_data
def load_data(filepath):
    try:
        data1 = pd.read_csv(filepath, encoding='utf-8', sep=None, engine='python')
    except UnicodeDecodeError:
        try:
            data1 = pd.read_csv(filepath, encoding='latin1', sep=None, engine='python')
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {str(e)}")
            return None

    # Exibindo as primeiras linhas do arquivo para depuração
    st.write("Preview dos dados carregados:")
    st.write(data1.head())  # Exibe as primeiras 5 linhas do dataframe

    # Remove colunas vazias e indesejadas
    data_cleaned = data1.dropna(how='all', axis=1)
    data_cleaned = data_cleaned.loc[:, ~data_cleaned.columns.str.contains('^Unnamed')]

    # Tratamento de datas
    date_columns = [col for col in data_cleaned.columns if "Data" in col]
    for col in date_columns:
        data_cleaned[col] = pd.to_datetime(data_cleaned[col], errors='coerce', format='%d/%m/%Y')

    return data_cleaned


# Função para garantir que as colunas estão no tipo numérico
def convert_to_numeric(data2, columns):
    for column in columns:
        data2[column] = pd.to_numeric(data2[column],
                                      errors='coerce')  # Converte para numérico e coloca NaN em valores não numéricos
    return data2


# Título principal
st.title("📊 Dashboard SGCor")

# Barra lateral para navegação
st.sidebar.title("Navegação")
app_mode = st.sidebar.radio("Escolha uma opção", (
"Visão Geral", "Análises Detalhadas", "KPIs", "Gráficos Comparativos", "Análise por Companhia"))

# Upload do arquivo
uploaded_file = st.file_uploader("Faça o upload do arquivo CSV", type="csv")

if uploaded_file is not None:
    with open("temp.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    data = load_data("temp.csv")
    os.remove("temp.csv")

    if data is not None and not data.empty:
        # Garantir que as colunas relevantes estão no tipo numérico
        data = convert_to_numeric(data, [
            "Prêmio Líquido", "Comissão", "% Comissão", "% Agenciamento", "Parcelas", "Pgto."
        ])

        # Filtros na barra lateral
        st.sidebar.header("Filtros")
        if "Convenção Negociada" in data.columns:
            convencoes = data["Convenção Negociada"].dropna().unique()
            filtro_convencao = st.sidebar.multiselect("Selecione Convenções", convencoes, default=convencoes)
            data = data[data["Convenção Negociada"].isin(filtro_convencao)]

        # Agrupamento mensal baseado na 'Data Vigência Inicial'
        data['Ano-Mês'] = data['Data Vigência Inicial'].dt.to_period('M').astype(str)  # Corrigido aqui

        # Resumo Mensal
        resumo_mensal = data.groupby('Ano-Mês').agg(
            total_premio_liquido=('Prêmio Líquido', 'sum'),
            total_comissao=('Comissão', 'sum'),
            total_pagamento=('Pgto.', 'sum'),
            total_apolices=('Id Produção', 'count'),
            media_comissao=('Comissão', 'mean'),
            media_percentual_comissao=('% Comissão', 'mean'),
            total_cancelamentos=('Status', lambda x: (x == 'Cancelada').sum())
        ).reset_index()

        # Cálculo de Índices de Crescimento
        resumo_mensal['crescimento_premio_liquido'] = resumo_mensal['total_premio_liquido'].pct_change() * 100
        resumo_mensal['crescimento_comissao'] = resumo_mensal['total_comissao'].pct_change() * 100
        resumo_mensal['taxa_conversao'] = (resumo_mensal['total_apolices'] / resumo_mensal['total_apolices'].shift(
            1)) * 100
        resumo_mensal['comissao_por_apolice'] = resumo_mensal['total_comissao'] / resumo_mensal['total_apolices']
        resumo_mensal['premio_liquido_por_faturamento'] = resumo_mensal['total_premio_liquido'] / resumo_mensal[
            'total_pagamento']

        # Navegação
        if app_mode == "Visão Geral":
            st.header("📅 Resumo Geral Mensal")
            st.dataframe(resumo_mensal)

        elif app_mode == "Análises Detalhadas":
            st.header("📊 Análises Detalhadas")
            fig = px.line(resumo_mensal, x='Ano-Mês', y=['total_premio_liquido', 'total_comissao', 'total_pagamento'],
                          labels={'value': 'Valor (R$)', 'Ano-Mês': 'Mês/Ano'},
                          title="Resumo Mensal de Prêmios, Comissões e Pagamentos")
            st.plotly_chart(fig, use_container_width=True)

            fig_growth = px.line(resumo_mensal, x='Ano-Mês', y=['crescimento_premio_liquido', 'crescimento_comissao'],
                                 labels={'value': 'Crescimento (%)', 'Ano-Mês': 'Mês/Ano'},
                                 title="Crescimento de Prêmio Líquido e Comissão")
            st.plotly_chart(fig_growth, use_container_width=True)

        elif app_mode == "KPIs":
            st.header("📊 KPIs - Indicadores Principais")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Prêmio Líquido", f"R$ {resumo_mensal['total_premio_liquido'].sum():,.2f}")
            col2.metric("Total Comissão", f"R$ {resumo_mensal['total_comissao'].sum():,.2f}")
            col3.metric("Total Pagamento", f"R$ {resumo_mensal['total_pagamento'].sum():,.2f}")

        elif app_mode == "Gráficos Comparativos":
            st.header("📊 Gráficos Comparativos")
            fig_comissao_apolice = px.bar(resumo_mensal, x='Ano-Mês', y='comissao_por_apolice',
                                          labels={'value': 'Comissão por Apólice (R$)', 'Ano-Mês': 'Mês/Ano'},
                                          title="Comissão por Apólice")
            st.plotly_chart(fig_comissao_apolice, use_container_width=True)

            fig_premio_faturamento = px.scatter(resumo_mensal, x='total_premio_liquido', y='total_pagamento',
                                                size='total_apolices', color='Ano-Mês',
                                                title="Relação entre Prêmio Líquido e Faturamento")
            st.plotly_chart(fig_premio_faturamento, use_container_width=True)

        elif app_mode == "Análise por Companhia":
            st.header("📊 Análise de Cadastros por Companhia")
            if "Companhia" in data.columns:
                # Agrupando os dados por companhia
                cadastros_companhia = data.groupby('Companhia').size().reset_index(name='Total Cadastros')

                # Exibindo o gráfico
                fig_cadastros = px.bar(cadastros_companhia, x='Companhia', y='Total Cadastros',
                                       title="Total de Cadastros por Companhia", labels={'Total Cadastros': 'Número de Cadastros'})
                st.plotly_chart(fig_cadastros, use_container_width=True)
            else:
                st.error("A coluna 'Companhia' não foi encontrada nos dados.")

