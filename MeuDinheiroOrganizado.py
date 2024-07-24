import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from datetime import datetime
from PIL import Image

class MeuDinheiroOrganizadoApp:
    def __init__(self):
        # Inicializar o estado da sessão para diferentes categorias de dados
        self.init_session_state()

    def init_session_state(self):
        if 'monthly_transactions' not in st.session_state:
            st.session_state['monthly_transactions'] = {}
        if 'fixed_expenses' not in st.session_state:
            st.session_state['fixed_expenses'] = pd.DataFrame(columns=['Descrição', 'Valor'])
        if 'variable_expenses' not in st.session_state:
            st.session_state['variable_expenses'] = pd.DataFrame(columns=['Descrição', 'Valor'])
        if 'credit_card_bills' not in st.session_state:
            st.session_state['credit_card_bills'] = pd.DataFrame(columns=['Cartão', 'Data de Vencimento', 'Valor'])
        if 'debts' not in st.session_state:
            st.session_state['debts'] = pd.DataFrame(columns=['Descrição', 'Valor'])
        if 'investments' not in st.session_state:
            st.session_state['investments'] = pd.DataFrame(columns=['Descrição', 'Valor'])
        if 'spending_limits' not in st.session_state:
            st.session_state['spending_limits'] = pd.DataFrame(columns=['Categoria', 'Limite'])
        if 'credit_cards' not in st.session_state:
            st.session_state['credit_cards'] = pd.DataFrame(columns=['Cartão', 'Limite', 'Data de Vencimento', 'Imagem'])
        if 'wishlist' not in st.session_state:
            st.session_state['wishlist'] = pd.DataFrame(columns=['Descrição', 'Categoria', 'Decisão'])
        if 'financial_goals' not in st.session_state:
            st.session_state['financial_goals'] = pd.DataFrame(columns=['Descrição', 'Valor Necessário', 'Data', 'Imagem'])
    
    def run(self):
        # Navegação por abas
        st.sidebar.title("Menu")
        menu = st.sidebar.radio("Selecione uma opção", ["Transações Mensais", "Despesas Fixas", "Despesas Variáveis", 
                                                       "Faturas de Cartões de Crédito", "Dívidas", "Investimentos", 
                                                       "Limite de Gastos por Categorias", "Cartões de Crédito", 
                                                       "Lista de Desejos", "Metas Financeiras", "Mural dos Sonhos"])
        
        if menu == "Transações Mensais":
            self.transacoes_mensais()
        elif menu == "Despesas Fixas":
            self.despesas_fixas()
        elif menu == "Despesas Variáveis":
            self.despesas_variaveis()
        elif menu == "Faturas de Cartões de Crédito":
            self.faturas_cartoes()
        elif menu == "Dívidas":
            self.dividas()
        elif menu == "Investimentos":
            self.investimentos()
        elif menu == "Limite de Gastos por Categorias":
            self.limite_gastos()
        elif menu == "Cartões de Crédito":
            self.cartoes_credito()
        elif menu == "Lista de Desejos":
            self.lista_desejos()
        elif menu == "Metas Financeiras":
            self.metas_financeiras()
        elif menu == "Mural dos Sonhos":
            self.mural_sonhos()

    def transacoes_mensais(self):
        st.title("Transações Mensais")
        # Lógica para adicionar e visualizar transações mensais
        # ... (código existente)
        
    def despesas_fixas(self):
        st.title("Despesas Fixas")
        # Lógica para adicionar e visualizar despesas fixas
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        if st.button("Adicionar Despesa Fixa"):
            new_expense = pd.DataFrame({'Descrição': [descricao], 'Valor': [valor]})
            st.session_state['fixed_expenses'] = pd.concat([st.session_state['fixed_expenses'], new_expense], ignore_index=True)
            st.success("Despesa Fixa adicionada!")
        st.dataframe(st.session_state['fixed_expenses'])
        
    def despesas_variaveis(self):
        st.title("Despesas Variáveis")
        # Lógica para adicionar e visualizar despesas variáveis
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        if st.button("Adicionar Despesa Variável"):
            new_expense = pd.DataFrame({'Descrição': [descricao], 'Valor': [valor]})
            st.session_state['variable_expenses'] = pd.concat([st.session_state['variable_expenses'], new_expense], ignore_index=True)
            st.success("Despesa Variável adicionada!")
        st.dataframe(st.session_state['variable_expenses'])
        
    def faturas_cartoes(self):
        st.title("Faturas de Cartões de Crédito")
        # Lógica para adicionar e visualizar faturas de cartões de crédito
        cartao = st.text_input("Cartão")
        data_vencimento = st.date_input("Data de Vencimento")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        if st.button("Adicionar Fatura"):
            new_bill = pd.DataFrame({'Cartão': [cartao], 'Data de Vencimento': [data_vencimento], 'Valor': [valor]})
            st.session_state['credit_card_bills'] = pd.concat([st.session_state['credit_card_bills'], new_bill], ignore_index=True)
            st.success("Fatura adicionada!")
        st.dataframe(st.session_state['credit_card_bills'])
        
    def dividas(self):
        st.title("Minhas Dívidas")
        # Lógica para adicionar e visualizar dívidas
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        if st.button("Adicionar Dívida"):
            new_debt = pd.DataFrame({'Descrição': [descricao], 'Valor': [valor]})
            st.session_state['debts'] = pd.concat([st.session_state['debts'], new_debt], ignore_index=True)
            st.success("Dívida adicionada!")
        st.dataframe(st.session_state['debts'])
        
    def investimentos(self):
        st.title("Investimentos")
        # Lógica para adicionar e visualizar investimentos
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        if st.button("Adicionar Investimento"):
            new_investment = pd.DataFrame({'Descrição': [descricao], 'Valor': [valor]})
            st.session_state['investments'] = pd.concat([st.session_state['investments'], new_investment], ignore_index=True)
            st.success("Investimento adicionado!")
        st.dataframe(st.session_state['investments'])
        
    def limite_gastos(self):
        st.title("Limite de Gastos por Categorias")
        # Lógica para adicionar e visualizar limites de gastos
        categoria = st.text_input("Categoria")
        limite = st.number_input("Limite", min_value=0.0, format="%.2f")
        if st.button("Adicionar Limite"):
            new_limit = pd.DataFrame({'Categoria': [categoria], 'Limite': [limite]})
            st.session_state['spending_limits'] = pd.concat([st.session_state['spending_limits'], new_limit], ignore_index=True)
            st.success("Limite de Gasto adicionado!")
        st.dataframe(st.session_state['spending_limits'])
        
    def cartoes_credito(self):
        st.title("Meus Cartões de Crédito")
        # Lógica para adicionar e visualizar cartões de crédito
        cartao = st.text_input("Cartão")
        limite = st.number_input("Limite", min_value=0.0, format="%.2f")
        data_vencimento = st.date_input("Data de Vencimento")
        imagem = st.file_uploader("Imagem do Cartão", type=["png", "jpg", "jpeg"])
        if st.button("Adicionar Cartão"):
            if imagem is not None:
                image_path = f"images/{cartao}.png"
                with open(image_path, "wb") as f:
                    f.write(imagem.getbuffer())
                new_card = pd.DataFrame({'Cartão': [cartao], 'Limite': [limite], 'Data de Vencimento': [data_vencimento], 'Imagem': [image_path]})
                st.session_state['credit_cards'] = pd.concat([st.session_state['credit_cards'], new_card], ignore_index=True)
                st.success("Cartão adicionado!")
        st.dataframe(st.session_state['credit_cards'])
        # Exibir imagens dos cartões
        for index, row in st.session_state['credit_cards'].iterrows():
            st.image(row['Imagem'], caption=row['Cartão'])

    def lista_desejos(self):
        st.title("Lista de Desejos")
        # Lógica para adicionar e visualizar lista de desejos
        descricao = st.text_input("Descrição")
        categoria = st.selectbox("Categoria", ['Roupas', 'Presentes', 'Show', 'Festivais', 'Eventos', 'Tecnologia', 'Cuidados Pessoais', 'Itens para Casa', 'Conhecimento', 'Estudos'])
        decisao = st.radio("Decisão de Compra", ['😍 Eu preciso mesmo desse item?', '💵 Esse item cabe no meu orçamento hoje?', '⌛ Se eu esperar até amanhã, ainda vou lembrar que queria esse item?'])
        if st.button("Adicionar à Lista de Desejos"):
            new_wish = pd.DataFrame({'Descrição': [descricao], 'Categoria': [categoria], 'Decisão': [decisao]})
            st.session_state['wishlist'] = pd.concat([st.session_state['wishlist'], new_wish], ignore_index=True)
            st.success("Item adicionado à lista de desejos!")
        st.dataframe(st.session_state['wishlist'])

    def metas_financeiras(self):
        st.title("Metas Financeiras")
        descricao = st.text_input("Descrição da Meta")
        valor_necessario = st.number_input("Valor Necessário", min_value=0.0, format="%.2f")
        data_meta = st.date_input("Data para atingir a Meta")
        if st.button("Adicionar Meta Financeira"):
            new_goal = pd.DataFrame({'Descrição': [descricao], 'Valor Necessário': [valor_necessario], 'Data': [data_meta]})
            st.session_state['financial_goals'] = pd.concat([st.session_state['financial_goals'], new_goal], ignore_index=True)
            st.success("Meta financeira adicionada!")
        st.dataframe(st.session_state['financial_goals'])

    def mural_sonhos(self):
        st.title("Mural dos Sonhos")
        descricao = st.text_input("Descrição do Sonho")
        valor_necessario = st.number_input("Valor Necessário", min_value=0.0, format="%.2f")
        data_meta = st.date_input("Data para atingir o Sonho")
        imagem = st.file_uploader("Upload de imagem para o Sonho", type=["png", "jpg", "jpeg"])
        if st.button("Adicionar ao Mural dos Sonhos"):
            if imagem is not None:
                image_path = f"images/{descricao.replace(' ', '_')}.png"
                with open(image_path, "wb") as f:
                    f.write(imagem.getbuffer())
                new_dream = pd.DataFrame({'Descrição': [descricao], 'Valor Necessário': [valor_necessario], 'Data': [data_meta], 'Imagem': [image_path]})
                st.session_state['mural_sonhos'] = pd.concat([st.session_state['mural_sonhos'], new_dream], ignore_index=True)
                st.success("Sonho adicionado ao mural!")
        # Exibir sonhos com imagens
        for index, row in st.session_state['mural_sonhos'].iterrows():
            st.image(row['Imagem'], caption=f"{row['Descrição']} - {row['Data']}")

if __name__ == "__main__":
    app = MeuDinheiroOrganizadoApp()
    app.run()
