import streamlit as st
from importlib import import_module

# Configuração da página deve ser a primeira chamada
st.set_page_config(page_title="Guru dos Dinheirinhos", page_icon="💰", layout="wide")

# Funções para carregar as aplicações
def load_verificador_de_fatura():
    try:
        module = import_module("VerificadorDeFatura")
        app = module.VerificadorDeFaturaApp()
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

# Menu lateral para seleção das aplicações
st.sidebar.title("Menu")
app_choice = st.sidebar.radio("Selecione a Aplicação", ("Verificador de Fatura", "Simulação de Investidor"))

# Carregar a aplicação selecionada
if app_choice == "Verificador de Fatura":
    load_verificador_de_fatura()
elif app_choice == "Simulação de Investidor":
    load_simulacao_investidor()
