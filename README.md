# Dashboard SGCor

**Dashboard SGCor** é uma aplicação interativa construída com Streamlit para visualização e análise de dados financeiros. A aplicação permite que os usuários carreguem arquivos CSV com informações de prêmios, comissões, pagamentos e cadastros por companhia, oferecendo gráficos interativos e métricas detalhadas.

---

## Requisitos

### Python 3.8+

### Bibliotecas:
- `streamlit`
- `pandas`
- `plotly`

### Para instalar as dependências, execute o comando:

```bash
pip install streamlit pandas plotly
Como Usar
1. Carregar o Arquivo CSV
Faça o upload do seu arquivo CSV clicando no botão "Faça o upload do arquivo CSV" na interface do aplicativo.

2. Aplicar Filtros
Utilize os filtros na barra lateral para selecionar convenções e outros parâmetros. Isso atualizará os gráficos e métricas.

3. Visualizar Gráficos e Métricas
O dashboard exibirá as métricas principais, como total de prêmios, comissões e pagamentos, e gráficos interativos, como:

Gráfico de barras de cadastros por companhia.
Gráfico de linha de comissões ao longo do tempo.
4. Interagir com os Gráficos
Todos os gráficos são interativos, permitindo zoom, hover e a visualização de detalhes.

Como Executar
Clone este repositório:
bash
Copiar código
git clone https://github.com/seu_usuario/sgcor-dashboard.git
Navegue até o diretório do projeto:
bash
Copiar código
cd sgcor-dashboard
Execute o aplicativo com o comando:
bash
Copiar código
streamlit run app.py
O aplicativo será aberto no seu navegador padrão, geralmente na URL http://localhost:8501.

Funcionalidades
Carregamento de Arquivo CSV: Permite que o usuário carregue um arquivo CSV com dados financeiros.
Filtros Interativos: Permite selecionar convenções e outras opções para filtrar os dados.
Visualização de Gráficos: Gráficos de barras e linha para análise de dados, como prêmios, comissões e cadastros por companhia.
Exibição de Métricas: Métricas financeiras principais são exibidas de forma destacada.
Estrutura do Código
1. Carregamento e Processamento de Dados
O arquivo CSV carregado é processado com Pandas para limpar dados vazios e converter colunas para tipos adequados.

2. Filtros Interativos
Filtros permitem a seleção de convenções e outras opções para filtrar os dados antes de gerar os gráficos.

3. Gráficos Interativos
Utilizando Plotly, o aplicativo gera gráficos interativos, como:

Gráfico de Barras: Para cadastros por companhia.
Gráfico de Linha: Para comissões ao longo do tempo.
4. Métricas e KPIs
Métricas financeiras, como total de prêmios, comissões e pagamentos, são calculadas e exibidas como indicadores.

Licença
Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para mais detalhes.

css
Copiar código

Este formato de **Markdown** está completo, com todas as seções organizadas em cabeçalhos, l
