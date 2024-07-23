# Guru dos Dinheirinhos 💰

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
- **Locale**: Formatação de valores monetários.
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
- `Lottie/`: Pasta contendo animações Lottie.
- `requirements.txt`: Lista de dependências do projeto.

## Dependências
Coloque esse conteúdo em um arquivo chamado requirements.txt no diretório raiz do seu projeto. Isso garantirá que todas as dependências necessárias sejam 
instaladas ao configurar o ambiente.

streamlit
pandas
numpy
yfinance
requests
openai
streamlit-lottie

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

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Contato

Richardson Edson de Lima - [LinkedIn](www.linkedin.com/in/richardsonlima) - [Email](mailto: contatorichardsonlima at gmail dot com)
