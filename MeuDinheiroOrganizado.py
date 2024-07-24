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
        if 'mural_sonhos' not in st.session_state:
            st.session_state['mural_sonhos'] = pd.DataFrame(columns=['Descrição', 'Valor Necessário', 'Data', 'Imagem'])

    def run(self):
        # Navegação por abas
        st.sidebar.title("Menu")
        menu = st.sidebar.radio("Selecione uma opção", ["Transações Mensais", "Panorama Anual", "Despesas Fixas", "Despesas Variáveis", 
                                                       "Faturas de Cartões de Crédito", "Dívidas", "Investimentos", 
                                                       "Limite de Gastos por Categorias", "Cartões de Crédito", 
                                                       "Lista de Desejos", "Metas Financeiras", "Mural dos Sonhos"])

        if menu == "Transações Mensais":
            self.transacoes_mensais()
        elif menu == "Panorama Anual":
            self.panorama_anual()
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
        month_names = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        st.sidebar.header('Adicionar Transação')
        month = st.sidebar.selectbox('Mês', list(month_names.values()))
        date = st.sidebar.date_input('Data', datetime.today())
        category = st.sidebar.selectbox('Categoria', st.session_state.get('categories', ['Entrada', 'Mercado', 'Aluguel', 'Utilidades', 'Lazer', 'Outros']))
        amount = st.sidebar.number_input('Valor', min_value=0.0, format="%.2f")

        if st.sidebar.button('Adicionar'):
            month_num = list(month_names.keys())[list(month_names.values()).index(month)]
            new_transaction = pd.DataFrame({'Data': [date], 'Categoria': [category], 'Valor': [amount]})
            if month_num not in st.session_state['monthly_transactions']:
                st.session_state['monthly_transactions'][month_num] = new_transaction
            else:
                st.session_state['monthly_transactions'][month_num] = pd.concat([st.session_state['monthly_transactions'][month_num], new_transaction], ignore_index=True)
            st.sidebar.success('Transação adicionada!')

        st.sidebar.header('Upload de Arquivo CSV')
        uploaded_file = st.sidebar.file_uploader("Escolha um arquivo CSV", type="csv")
        if uploaded_file is not None:
            df_uploaded = pd.read_csv(uploaded_file)
            for _, row in df_uploaded.iterrows():
                month = pd.to_datetime(row['Data']).month
                new_transaction = pd.DataFrame({'Data': [row['Data']], 'Categoria': [row['Categoria']], 'Valor': [row['Valor']]})
                if month not in st.session_state['monthly_transactions']:
                    st.session_state['monthly_transactions'][month] = new_transaction
                else:
                    st.session_state['monthly_transactions'][month] = pd.concat([st.session_state['monthly_transactions'][month], new_transaction], ignore_index=True)
            st.sidebar.success('Arquivo carregado com sucesso!')

        selected_month = st.selectbox('Selecione o Mês', list(month_names.values()))
        selected_month_num = list(month_names.keys())[list(month_names.values()).index(selected_month)]
        if selected_month_num in st.session_state['monthly_transactions']:
            transactions = st.session_state['monthly_transactions'][selected_month_num]
            st.header('Histórico de Transações')
            st.dataframe(transactions)

            st.header('Estatísticas Resumidas')
            summary = transactions.groupby('Categoria')['Valor'].sum().reset_index()
            st.dataframe(summary)

            st.header('Despesas por Categoria (Altair)')
            alt_chart = alt.Chart(summary).mark_bar().encode(
                x='Categoria',
                y='Valor',
                color='Categoria'
            ).properties(width=600)
            st.altair_chart(alt_chart, use_container_width=True)

            st.header('Despesas por Categoria (Plotly)')
            plotly_chart = px.pie(summary, values='Valor', names='Categoria', title='Distribuição de Despesas')
            st.plotly_chart(plotly_chart)

            st.header('Despesas ao Longo do Tempo')
            time_series = transactions.groupby('Data')['Valor'].sum().reset_index()
            time_series_chart = px.line(time_series, x='Data', y='Valor', title='Despesas Diárias')
            st.plotly_chart(time_series_chart)

            st.header('Despesas por Categoria ao Longo do Tempo (Altair)')
            stacked_bar_chart = alt.Chart(transactions).mark_bar().encode(
                x='yearmonth(Data):O',
                y='sum(Valor):Q',
                color='Categoria'
            ).properties(width=600)
            st.altair_chart(stacked_bar_chart, use_container_width=True)

            st.header('Gráfico de Dispersão (Plotly)')
            scatter_chart = px.scatter(transactions, x='Data', y='Valor', color='Categoria', title='Dispersão de Despesas')
            st.plotly_chart(scatter_chart)

            st.header('Acumulação de Despesas ao Longo do Tempo (Plotly)')
            area_chart = px.area(transactions, x='Data', y='Valor', color='Categoria', title='Acumulação de Despesas')
            st.plotly_chart(area_chart)
        else:
            st.write('Nenhuma transação cadastrada para este mês.')

        st.sidebar.header('Salvar/Carregar Dados')
        if st.sidebar.button('Salvar Dados'):
            transactions = pd.concat(st.session_state['monthly_transactions'].values(), ignore_index=True)
            transactions.to_csv('transacoes.csv', index=False)
            st.sidebar.success('Dados salvos em transacoes.csv')

        if st.sidebar.button('Carregar Dados'):
            transactions = pd.read_csv('transacoes.csv')
            for _, row in transactions.iterrows():
                month = pd.to_datetime(row['Data']).month
                new_transaction = pd.DataFrame({'Data': [row['Data']], 'Categoria': [row['Categoria']], 'Valor': [row['Valor']]})
                if month not in st.session_state['monthly_transactions']:
                    st.session_state['monthly_transactions'][month] = new_transaction
                else:
                    st.session_state['monthly_transactions'][month] = pd.concat([st.session_state['monthly_transactions'][month], new_transaction], ignore_index=True)
            st.sidebar.success('Dados carregados de transacoes.csv')

    def panorama_anual(self):
        st.title("Panorama Anual de Despesas")
        all_transactions = pd.concat(st.session_state['monthly_transactions'].values(), ignore_index=True)
        st.dataframe(all_transactions)
    
        # Gráfico de área para a acumulação de despesas ao longo do ano
        annual_expenses = all_transactions.groupby('Data')['Valor'].sum().cumsum().reset_index()
        annual_expense_chart = px.area(annual_expenses, x='Data', y='Valor', title='Acumulação de Despesas ao Longo do Ano')
        st.plotly_chart(annual_expense_chart)
    
        # Gráfico de dispersão para mostrar a dispersão das despesas
        scatter_chart = px.scatter(all_transactions, x='Data', y='Valor', color='Categoria', title='Dispersão de Despesas ao Longo do Ano')
        st.plotly_chart(scatter_chart)
    
        # Gráfico de barras empilhadas para mostrar a distribuição mensal das despesas
        stacked_bar = alt.Chart(all_transactions).mark_bar().encode(
            x='month(Data):O',
            y='sum(Valor):Q',
            color='Categoria',
            tooltip=['month(Data)', 'Categoria', 'sum(Valor)']
        ).properties(width=600, height=400, title='Despesas Mensais por Categoria')
        st.altair_chart(stacked_bar, use_container_width=True)
    
        st.sidebar.header('Exportar Dados Anuais')
        if st.sidebar.button('Exportar CSV'):
            all_transactions.to_csv('dados_anuais.csv', index=False)
            st.sidebar.success('Dados anuais exportados como dados_anuais.csv')

    def despesas_fixas(self):
        st.title("Despesas Fixas")
        st.dataframe(st.session_state['fixed_expenses'])

        st.sidebar.header('Adicionar Despesa Fixa')
        descricao = st.sidebar.text_input('Descrição')
        valor = st.sidebar.number_input('Valor', min_value=0.0, format="%.2f")

        if st.sidebar.button('Adicionar'):
            new_expense = pd.DataFrame({'Descrição': [descricao], 'Valor': [valor]})
            st.session_state['fixed_expenses'] = pd.concat([st.session_state['fixed_expenses'], new_expense], ignore_index=True)
            st.sidebar.success('Despesa fixa adicionada!')

    def despesas_variaveis(self):
        st.title("Despesas Variáveis")
        st.dataframe(st.session_state['variable_expenses'])

        st.sidebar.header('Adicionar Despesa Variável')
        descricao = st.sidebar.text_input('Descrição')
        valor = st.sidebar.number_input('Valor', min_value=0.0, format="%.2f")

        if st.sidebar.button('Adicionar'):
            new_expense = pd.DataFrame({'Descrição': [descricao], 'Valor': [valor]})
            st.session_state['variable_expenses'] = pd.concat([st.session_state['variable_expenses'], new_expense], ignore_index=True)
            st.sidebar.success('Despesa variável adicionada!')

    def faturas_cartoes(self):
        st.title("Faturas de Cartões de Crédito")
        st.dataframe(st.session_state['credit_card_bills'])

        st.sidebar.header('Adicionar Fatura de Cartão')
        cartao = st.sidebar.text_input('Cartão')
        data_vencimento = st.sidebar.date_input('Data de Vencimento', datetime.today())
        valor = st.sidebar.number_input('Valor', min_value=0.0, format="%.2f")

        if st.sidebar.button('Adicionar'):
            new_bill = pd.DataFrame({'Cartão': [cartao], 'Data de Vencimento': [data_vencimento], 'Valor': [valor]})
            st.session_state['credit_card_bills'] = pd.concat([st.session_state['credit_card_bills'], new_bill], ignore_index=True)
            st.sidebar.success('Fatura de cartão adicionada!')

    def dividas(self):
        st.title("Dívidas")
        st.dataframe(st.session_state['debts'])

        st.sidebar.header('Adicionar Dívida')
        descricao = st.sidebar.text_input('Descrição')
        valor = st.sidebar.number_input('Valor', min_value=0.0, format="%.2f")

        if st.sidebar.button('Adicionar'):
            new_debt = pd.DataFrame({'Descrição': [descricao], 'Valor': [valor]})
            st.session_state['debts'] = pd.concat([st.session_state['debts'], new_debt], ignore_index=True)
            st.sidebar.success('Dívida adicionada!')

    def investimentos(self):
        st.title("Investimentos")
        st.dataframe(st.session_state['investments'])

        st.sidebar.header('Adicionar Investimento')
        descricao = st.sidebar.text_input('Descrição')
        valor = st.sidebar.number_input('Valor', min_value=0.0, format="%.2f")

        if st.sidebar.button('Adicionar'):
            new_investment = pd.DataFrame({'Descrição': [descricao], 'Valor': [valor]})
            st.session_state['investments'] = pd.concat([st.session_state['investments'], new_investment], ignore_index=True)
            st.sidebar.success('Investimento adicionado!')

    def limite_gastos(self):
        st.title("Limite de Gastos por Categorias")
        st.dataframe(st.session_state['spending_limits'])

        st.sidebar.header('Adicionar Limite de Gastos')
        categoria = st.sidebar.text_input('Categoria')
        limite = st.sidebar.number_input('Limite', min_value=0.0, format="%.2f")

        if st.sidebar.button('Adicionar'):
            new_limit = pd.DataFrame({'Categoria': [categoria], 'Limite': [limite]})
            st.session_state['spending_limits'] = pd.concat([st.session_state['spending_limits'], new_limit], ignore_index=True)
            st.sidebar.success('Limite de gastos adicionado!')

    def cartoes_credito(self):
        st.title("Cartões de Crédito")
        st.dataframe(st.session_state['credit_cards'])

        st.sidebar.header('Adicionar Cartão de Crédito')
        cartao = st.sidebar.text_input('Cartão')
        limite = st.sidebar.number_input('Limite', min_value=0.0, format="%.2f")
        data_vencimento = st.sidebar.date_input('Data de Vencimento', datetime.today())
        imagem = st.sidebar.file_uploader("Imagem do Cartão", type=["png", "jpg", "jpeg"])

        if st.sidebar.button('Adicionar'):
            imagem_path = None
            if imagem is not None:
                imagem_path = f"images/{imagem.name}"
                with open(imagem_path, "wb") as f:
                    f.write(imagem.getbuffer())
            new_card = pd.DataFrame({'Cartão': [cartao], 'Limite': [limite], 'Data de Vencimento': [data_vencimento], 'Imagem': [imagem_path]})
            st.session_state['credit_cards'] = pd.concat([st.session_state['credit_cards'], new_card], ignore_index=True)
            st.sidebar.success('Cartão de crédito adicionado!')

    def lista_desejos(self):
        st.title("Lista de Desejos")
        st.dataframe(st.session_state['wishlist'])

        st.sidebar.header('Adicionar Item à Lista de Desejos')
        descricao = st.sidebar.text_input('Descrição')
        categoria = st.sidebar.text_input('Categoria')
        decisao = st.sidebar.selectbox('Decisão', ['Comprar', 'Esperar', 'Descartar'])

        if st.sidebar.button('Adicionar'):
            new_item = pd.DataFrame({'Descrição': [descricao], 'Categoria': [categoria], 'Decisão': [decisao]})
            st.session_state['wishlist'] = pd.concat([st.session_state['wishlist'], new_item], ignore_index=True)
            st.sidebar.success('Item adicionado à lista de desejos!')

    def metas_financeiras(self):
        st.title("Metas Financeiras")
        st.dataframe(st.session_state['financial_goals'])

        st.sidebar.header('Adicionar Meta Financeira')
        descricao = st.sidebar.text_input('Descrição')
        valor_necessario = st.sidebar.number_input('Valor Necessário', min_value=0.0, format="%.2f")
        data = st.sidebar.date_input('Data de Conclusão', datetime.today())
        imagem = st.sidebar.file_uploader("Imagem da Meta", type=["png", "jpg", "jpeg"])

        if st.sidebar.button('Adicionar'):
            imagem_path = None
            if imagem is not None:
                imagem_path = f"images/{imagem.name}"
                with open(imagem_path, "wb") as f:
                    f.write(imagem.getbuffer())
            new_goal = pd.DataFrame({'Descrição': [descricao], 'Valor Necessário': [valor_necessario], 'Data': [data], 'Imagem': [imagem_path]})
            st.session_state['financial_goals'] = pd.concat([st.session_state['financial_goals'], new_goal], ignore_index=True)
            st.sidebar.success('Meta financeira adicionada!')

    def mural_sonhos(self):
        st.title("Mural dos Sonhos")
        st.dataframe(st.session_state['mural_sonhos'])

        st.sidebar.header('Adicionar Item ao Mural dos Sonhos')
        descricao = st.sidebar.text_input('Descrição')
        valor_necessario = st.sidebar.number_input('Valor Necessário', min_value=0.0, format="%.2f")
        data = st.sidebar.date_input('Data de Conclusão', datetime.today())
        imagem = st.sidebar.file_uploader("Imagem do Item", type=["png", "jpg", "jpeg"])

        if st.sidebar.button('Adicionar'):
            imagem_path = None
            if imagem is not None:
                imagem_path = f"images/{imagem.name}"
                with open(imagem_path, "wb") as f:
                    f.write(imagem.getbuffer())
            new_item = pd.DataFrame({'Descrição': [descricao], 'Valor Necessário': [valor_necessario], 'Data': [data], 'Imagem': [imagem_path]})
            st.session_state['mural_sonhos'] = pd.concat([st.session_state['mural_sonhos'], new_item], ignore_index=True)
            st.sidebar.success('Item adicionado ao mural dos sonhos!')

if __name__ == "__main__":
    app = MeuDinheiroOrganizadoApp()
    app.run()
