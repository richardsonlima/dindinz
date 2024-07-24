import streamlit as st
from importlib import import_module
from streamlit_lottie import st_lottie
import json

# Configuração da página deve ser a primeira chamada
st.set_page_config(page_title="Guru dos Dinheirinhos", page_icon="💰", layout="wide")

# Função para carregar animações Lottie
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {filepath}")
    except json.JSONDecodeError:
        st.error("Erro ao decodificar o arquivo JSON")
    except Exception as e:
        st.error(f"Erro inesperado: {e}")

# Carregar animações Lottie
lottie_invest = load_lottiefile("Animation-FinanceGuru-1721707438111.json")
if lottie_invest:
    st_lottie(lottie_invest, height=200, key="invest")

# Função para carregar um módulo e executar a aplicação
def load_app(module_name, class_name=None):
    try:
        module = import_module(module_name)
        if class_name:
            app = getattr(module, class_name)()
        else:
            app = module.main()
        app.run()
    except ImportError:
        st.error(f"Módulo {module_name} não encontrado")
    except AttributeError:
        st.error(f"Classe ou função não encontrada no módulo {module_name}")
    except Exception as e:
        st.error(f"Erro ao carregar {module_name}: {e}")

# Menu com ícones
menu_options = {
    "Home": "🏠",
    "Verificador de Fatura": "📄",
    "Simulação de Investidor": "💹",
    "Meu Dinheiro Organizado": "💼"
}

st.sidebar.title("Menu")
selection = st.sidebar.radio("Navegação", list(menu_options.keys()), format_func=lambda x: f"{menu_options[x]} {x}")

if selection == "Home":
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
elif selection == "Verificador de Fatura":
    load_app("VerificadorDeFatura")
elif selection == "Simulação de Investidor":
    load_app("SimulacaoInvestidor", "SimulacaoInvestidorApp")
elif selection == "Meu Dinheiro Organizado":
    load_app("MeuDinheiroOrganizado", "MeuDinheiroOrganizadoApp")
