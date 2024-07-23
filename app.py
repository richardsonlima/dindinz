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

# # Menu lateral para seleção das aplicações
# st.sidebar.title("Menu")
# app_choice = st.sidebar.radio("Selecione a Aplicação", ("Verificador de Fatura", "Simulação de Investidor"))

# # Carregar a aplicação selecionada
# if app_choice == "Verificador de Fatura":
#     load_verificador_de_fatura()
# elif app_choice == "Simulação de Investidor":
#     load_simulacao_investidor()


# Menu lateral
menu = st.sidebar.selectbox("Menu", ["Home", "Verificador de Fatura", "Simulação de Investidor"])

st.write(f"Debug: Menu selecionado: {menu}")

# if menu == "Home":
#     st.title("Bem-vindo ao aplicativo financeiro!")
# elif menu == "Verificador de Fatura":
#     st.write("Debug: Chamando a função load_verificador_de_fatura.")
#     load_verificador_de_fatura()
# elif menu == "Simulação de Investidor":
#     st.write("Debug: Chamando a função load_simulacao_investidor.")
#     load_simulacao_investidor()

if menu == "Home":
    st.title("Bem-vindo ao aplicativo financeiro!")
elif menu == "Verificador de Fatura":
    from VerificadorDeFatura import main
    load_verificador_de_fatura()
elif menu == "Simulação de Investidor":
    from SimulacaoInvestidor import SimulacaoInvestidorApp
    load_simulacao_investidor()
