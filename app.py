import streamlit as st
from importlib import import_module
from streamlit_lottie import st_lottie
import json

# Configuração da página deve ser a primeira chamada
st.set_page_config(page_title="Guru dos Dinheirinhos", page_icon="💰", layout="wide")

# Função para carregar animações Lottie
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Carregar animações Lottie
lottie_invest = load_lottiefile("Animation-FinanceGuru-1721707438111.json")
st_lottie(lottie_invest, height=200, key="invest")

# Funções para carregar as aplicações
def load_verificador_de_fatura():
    try:
        module = import_module("VerificadorDeFatura")
        app = module.main()
        app.run()
    except Exception as e:
        st.error(f"Erro ao carregar Verificador de Fatura: {e}")

def load_simulacao_investidor():
    try:
        module = import_module("SimulacaoInvestidor")
        app = module.SimulacaoInvestidorApp()
        app.run()
    except Exception as e:
        st.error(f"Erro ao carregar Simulação de Investidor: {e}")

def load_meu_dinheiro_organizado():
    try:
        module = import_module("MeuDinheiroOrganizado")
        app = module.MeuDinheiroOrganizadoApp()
        app.run()
    except Exception as e:
        st.error(f"Erro ao carregar Meu Dinheiro Organizado: {e}")

# Menu lateral
menu = st.sidebar.selectbox("Menu", ["Home", "Verificador de Fatura", "Simulação de Investidor", "Meu Dinheiro Organizado"])

if menu == "Home":
    st.title("Bem-vindo ao Guru dos Dinheirinhos!")
    st.write("""
    O **Guru dos Dinheirinhos** é a sua plataforma completa para gerenciar suas finanças pessoais e planejar seus investimentos de forma inteligente. Temos três aplicações poderosas para ajudá-lo a atingir seus objetivos financeiros:
    
    #### 1. Verificador de Fatura
    **Verificador de Fatura** é uma ferramenta essencial para controlar suas despesas com cartão de crédito. Com esta aplicação, você pode:
    - Analisar suas faturas de cartão de crédito.
    - Identificar padrões de gastos e possíveis economias.
    - Manter-se informado sobre seu consumo mensal para evitar surpresas desagradáveis.
    
    #### 2. Simulação de Investidor
    **Simulação de Investidor** é a aplicação ideal para quem deseja planejar seus investimentos a longo prazo. Com esta ferramenta, você pode:
    - Simular diferentes cenários de investimento.
    - Comparar opções de rentabilidade, como Poupança, CDI e uma carteira diversificada de ações.
    - Visualizar seu crescimento financeiro ao longo dos anos e planejar sua jornada rumo ao primeiro milhão de reais.

    #### 3. Meu Dinheiro Organizado
    A aplicação **Meu Dinheiro Organizado** é um rastreador financeiro pessoal desenvolvido com Streamlit. Ela permite que os usuários registrem 
    suas transações financeiras, visualizem um histórico dessas transações, obtenham estatísticas resumidas e explorem gráficos interativos para 
    análise de despesas.
    - O usuário pode adicionar novas transações especificando a data, categoria (Receita, Mercado, Aluguel, Utilidades, Lazer, Outros) e valor.
    - A entrada de dados é feita através de uma barra lateral na interface do usuário.
    - A aplicação exibe uma tabela com todas as transações registradas, mostrando data, categoria e valor.
    - A aplicação calcula e exibe um resumo das despesas totais agrupadas por categoria.
    - **Gráfico de Barras (Altair)**: Mostra a distribuição das despesas por categoria.
    - **Gráfico de Pizza (Plotly)**: Representa a distribuição percentual das despesas por categoria.
    - **Gráfico de Série Temporal (Plotly)**: Mostra as despesas diárias ao longo do tempo.
    - O usuário pode salvar as transações em um arquivo CSV.
    - O usuário pode carregar as transações a partir de um arquivo CSV previamente salvo.

    ---
    
    Sinta-se à vontade para explorar cada aplicação através do menu lateral. Estamos aqui para ajudar você a alcançar a liberdade financeira e a tomar decisões mais informadas sobre suas finanças pessoais.
    
    Se tiver alguma dúvida ou precisar de assistência, não hesite em nos contatar. Aproveite ao máximo o Guru dos Dinheirinhos!
    """)
elif menu == "Verificador de Fatura":
    load_verificador_de_fatura()
elif menu == "Simulação de Investidor":
    load_simulacao_investidor()
elif menu == "Meu Dinheiro Organizado":
    load_meu_dinheiro_organizado()
