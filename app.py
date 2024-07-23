import streamlit as st
from importlib import import_module
from streamlit_lottie import st_lottie
import json
from VerificadorDeFatura import main
from SimulacaoInvestidor import SimulacaoInvestidorApp

# Configuração da página deve ser a primeira chamada
st.set_page_config(page_title="Guru dos Dinheirinhos", page_icon="💰", layout="wide")

# Função para carregar animações Lottie
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
# Carregar animações Lottie
lottie_invest = load_lottiefile("Animation-FinanceGuru-1721707438111.json")
st_lottie(lottie_invest, height=200, key="invest")
#lottie_invest = load_lottiefile("Lottie/Animation-FinanceGuru-1721707438111.json")

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

# Menu lateral
menu = st.sidebar.selectbox("Menu", ["Home", "Verificador de Fatura", "Simulação de Investidor"])

st.write(f"Menu selecionado: {menu}")

if menu == "Home":
    st.title("Bem-vindo ao Guru dos Dinheirinhos!")
    st.write("""
    O **Guru dos Dinheirinhos** é a sua plataforma completa para gerenciar suas finanças pessoais e planejar seus investimentos de forma inteligente. Temos duas aplicações poderosas para ajudá-lo a atingir seus objetivos financeiros:
    
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
    
    ---
    
    Sinta-se à vontade para explorar cada aplicação através do menu lateral. Estamos aqui para ajudar você a alcançar a liberdade financeira e a tomar decisões mais informadas sobre suas finanças pessoais.
    
    Se tiver alguma dúvida ou precisar de assistência, não hesite em nos contatar. Aproveite ao máximo o Guru dos Dinheirinhos!
    """)
elif menu == "Verificador de Fatura":
    from VerificadorDeFatura import main
    load_verificador_de_fatura()
elif menu == "Simulação de Investidor":
    from SimulacaoInvestidor import SimulacaoInvestidorApp
    load_simulacao_investidor()
