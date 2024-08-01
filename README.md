# DinDinz 💰





# Aplicativo 01: Simulador do Investidor

Este é um aplicativo desenvolvido em Streamlit que auxilia na jornada de investimentos, permitindo a simulação de aportes iniciais e mensais em diferentes tipos de investimentos, como Poupança, CDI, Tesouro Direto, LCI, LCA, Previdência Privada e Carteiras de Ações.

## Funcionalidades

- **Simulação de Investimentos**: Insira o valor de aporte inicial e mensal e visualize a projeção de crescimento ao longo de 30 anos.
- **Taxas de Rendimento**: Obtenha taxas de rendimento atualizadas de diversas fontes (Banco Central, YFinance) e permita ajustes manuais.
- **Comparação de Investimentos**: Compare o rendimento de diferentes tipos de investimentos e visualize os resultados em gráficos.
- **Carteiras de Ações**: Inclua carteiras de ações predefinidas (ex: Carteira Barsi) ou customizadas e veja a simulação de rendimento.
- **Animações Lottie**: Interface interativa e animada utilizando animações Lottie.

## Tecnologias Utilizadas

- **Streamlit**: Framework principal para criação da aplicação web.
- **Pandas**: Manipulação e análise de dados.
- **NumPy**: Suporte para operações matemáticas e cálculos.
- **YFinance**: Obtenção de dados financeiros de ações.
- **Requests**: Acesso a APIs externas.
- **OpenAI**: Integração com GPT-4 para geração de insights (comentado no código).
- **Streamlit-Lottie**: Animações Lottie para uma interface mais amigável.

## Configuração e Execução

### Pré-requisitos

- Python 3.7 ou superior
- Pip para gerenciamento de pacotes

### Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/nome-do-repositorio.git
    cd nome-do-repositorio
    ```

2. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

### Execução

1. Adicione sua chave da API OpenAI (opcional) no código:
    ```python
    openai.api_key = 'sua-chave-api'
    ```

2. Execute a aplicação:
    ```bash
    streamlit run app.py
    ```

## Arquitetura do Projeto

- `app.py`: Código principal da aplicação Streamlit.
- `Animation-FinanceGuru-1721707438111.json`: Arquivo Json contendo animações Lottie.
- `requirements.txt`: Lista de dependências do projeto.

## Dependências
Coloque esse conteúdo em um arquivo chamado requirements.txt no diretório raiz do seu projeto. Isso garantirá que todas as dependências necessárias sejam 
instaladas ao configurar o ambiente.

```bash
streamlit
pandas
numpy
yfinance
requests
openai
streamlit-lottie
```

## Estrutura do Código

- **Funções de Carregamento**:
  - `load_lottiefile(filepath: str)`: Carrega arquivos Lottie.
  - `obter_taxa_bacen(endpoint)`: Obtém taxa de rendimento da API do Banco Central.
  - `obter_rendimento_acoes(tickers)`: Calcula o rendimento anual médio das ações.
  - `obter_info_acoes(tickers)`: Obtém informações atualizadas dos tickers das ações.

- **Funções de Cálculo**:
  - `calcular_rendimento(valor_inicial, valor_mensal, taxa_anual, anos=30)`: Calcula o rendimento ao longo do tempo.
  - `obter_taxas()`: Obtém as taxas de rendimento de várias fontes.
  - `resumir_dados(df)`: Resume os dados de um DataFrame.

- **Funções de Exibição**:
  - `exibir_texto_longo(texto, max_length=1000)`: Exibe textos longos em múltiplos blocos.
  - `st_lottie`: Exibe animações Lottie na interface Streamlit.


# Aplicativo 02:  Análise de Faturas de Cartão de Crédito

Esta aplicação Streamlit permite a análise de faturas de cartão de crédito, extraindo e categorizando transações a partir de arquivos PDF. A aplicação utiliza a API do OpenAI para fornecer insights financeiros detalhados sobre os gastos do usuário.

## Funcionalidades

- **Upload de Arquivos PDF**: Carregue sua fatura de cartão de crédito em formato PDF.
- **Extração de Texto**: Extração automática de texto a partir do PDF.
- **Análise de Transações**: Identificação e categorização das transações.
- **Gráfico de Despesas**: Visualização gráfica das despesas por categoria.
- **Insights Financeiros**: Utilização da API do OpenAI para gerar insights financeiros detalhados.
- **Interação com o Usuário**: Permite ao usuário fazer perguntas específicas sobre seus gastos.

## Tecnologias Utilizadas

- **Streamlit**: Framework para criação de aplicações web interativas em Python.
- **pdfplumber**: Biblioteca para extração de texto de arquivos PDF.
- **OpenAI**: API do OpenAI para geração de insights financeiros.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **Matplotlib**: Biblioteca para criação de gráficos.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    .\venv\Scripts\activate  # Windows
    ```

3. Instale as dependências:

    ```bash
    streamlit
    pdfplumber
    openai
    matplotlib
    pandas
    ```

    ```bash
    pip install -r requirements.txt
    ```

4. Configure a chave da API do OpenAI:
    - Obtenha sua chave da API do OpenAI em [OpenAI API](https://beta.openai.com/signup/).
    - Substitua `'sk-xxxx'` no arquivo `app.py` pela sua chave da API.

## Uso

1. Execute a aplicação Streamlit:
    ```bash
    streamlit run app.py
    ```

2. No navegador, carregue sua fatura de cartão de crédito em formato PDF.

3. A aplicação irá extrair e mostrar o texto do PDF, categorizar as transações, gerar gráficos e fornecer insights financeiros.

## Configuração do Tema

Para garantir que a aplicação use sempre o tema claro, a configuração do tema está definida diretamente no código `app.py`:

```python
st.set_page_config(
    layout="wide",
    page_icon="💳",
    page_title="Análise de Faturas de Cartão de Crédito",
    initial_sidebar_state="expanded",
    theme={"base": "light"}
)
```


## Licença

Este projeto está licenciado sob a [Apache-2.0 license](https://github.com/richardsonlima/guru-dos-dinheirinhos/tree/main?tab=Apache-2.0-1-ov-file#readme).

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Contato

Richardson Edson de Lima - [LinkedIn](www.linkedin.com/in/richardsonlima) - [Email](mailto: contatorichardsonlima at gmail dot com)
