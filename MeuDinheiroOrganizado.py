import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from datetime import datetime

class MeuDinheiroOrganizadoApp:
    def run(self):
        # Inicializar o estado da sessão para transações mensais e categorias
        if 'monthly_transactions' not in st.session_state:
            st.session_state['monthly_transactions'] = {}
        if 'categories' not in st.session_state:
            st.session_state['categories'] = ['Entrada', 'Mercado', 'Aluguel', 'Utilidades', 'Lazer', 'Outros']

        # Mapeamento de números para nomes dos meses
        month_names = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }

        # Barra lateral para entrada de dados
        st.sidebar.header('Adicionar Transação')
        month = st.sidebar.selectbox('Mês', list(month_names.values()))
        date = st.sidebar.date_input('Data', datetime.today())
        category = st.sidebar.selectbox('Categoria', st.session_state['categories'])
        amount = st.sidebar.number_input('Valor', min_value=0.0, format="%.2f")

        if st.sidebar.button('Adicionar'):
            month_num = list(month_names.keys())[list(month_names.values()).index(month)]
            new_transaction = pd.DataFrame({'Data': [date], 'Categoria': [category], 'Valor': [amount]})
            if month_num not in st.session_state['monthly_transactions']:
                st.session_state['monthly_transactions'][month_num] = new_transaction
            else:
                st.session_state['monthly_transactions'][month_num] = pd.concat([st.session_state['monthly_transactions'][month_num], new_transaction], ignore_index=True)
            st.sidebar.success('Transação adicionada!')

        # Funcionalidade para adicionar nova categoria
        st.sidebar.header('Adicionar Nova Categoria')
        new_category = st.sidebar.text_input('Nova Categoria')
        if st.sidebar.button('Adicionar Categoria'):
            if new_category and new_category not in st.session_state['categories']:
                st.session_state['categories'].append(new_category)
                st.sidebar.success(f'Categoria "{new_category}" adicionada!')
            else:
                st.sidebar.error('Categoria inválida ou já existente.')

        # Funcionalidade de upload de arquivo
        st.sidebar.header('Upload de Arquivo CSV')
        uploaded_file = st.sidebar.file_uploader("Escolha um arquivo CSV", type="csv")

        if uploaded_file is not None:
            st.session_state['transactions'] = pd.read_csv(uploaded_file)
            st.sidebar.success('Arquivo carregado com sucesso!')

        # Página principal
        st.title('Meu Dinheiro Organizado')

        # Exibir transações
        selected_month = st.selectbox('Selecione o Mês', list(month_names.values()))
        selected_month_num = list(month_names.keys())[list(month_names.values()).index(selected_month)]
        if selected_month_num in st.session_state['monthly_transactions']:
            transactions = st.session_state['monthly_transactions'][selected_month_num]
            st.header('Histórico de Transações')
            st.dataframe(transactions)

            # Estatísticas resumidas
            st.header('Estatísticas Resumidas')
            summary = transactions.groupby('Categoria')['Valor'].sum().reset_index()
            st.dataframe(summary)

            # Gráfico de barras Altair
            st.header('Despesas por Categoria (Altair)')
            alt_chart = alt.Chart(summary).mark_bar().encode(
                x='Categoria',
                y='Valor',
                color='Categoria'
            ).properties(width=600)
            st.altair_chart(alt_chart, use_container_width=True)

            # Gráfico de pizza Plotly
            st.header('Despesas por Categoria (Plotly)')
            plotly_chart = px.pie(summary, values='Valor', names='Categoria', title='Distribuição de Despesas')
            st.plotly_chart(plotly_chart)

            # Gráfico de séries temporais
            st.header('Despesas ao Longo do Tempo')
            time_series = transactions.groupby('Data')['Valor'].sum().reset_index()
            time_series_chart = px.line(time_series, x='Data', y='Valor', title='Despesas Diárias')
            st.plotly_chart(time_series_chart)

            # Novo gráfico de barras empilhadas
            st.header('Despesas por Categoria ao Longo do Tempo (Altair)')
            stacked_bar_chart = alt.Chart(transactions).mark_bar().encode(
                x='yearmonth(Data):O',
                y='sum(Valor):Q',
                color='Categoria'
            ).properties(width=600)
            st.altair_chart(stacked_bar_chart, use_container_width=True)

            # Novo gráfico de dispersão (scatter plot)
            st.header('Gráfico de Dispersão (Plotly)')
            scatter_chart = px.scatter(transactions, x='Data', y='Valor', color='Categoria', title='Dispersão de Despesas')
            st.plotly_chart(scatter_chart)

            # Novo gráfico de área
            st.header('Acumulação de Despesas ao Longo do Tempo (Plotly)')
            area_chart = px.area(transactions, x='Data', y='Valor', color='Categoria', title='Acumulação de Despesas')
            st.plotly_chart(area_chart)
        else:
            st.write('Nenhuma transação cadastrada para este mês.')

        # Funcionalidade de salvar e carregar
        st.sidebar.header('Salvar/Carregar Dados')
        if st.sidebar.button('Salvar Dados'):
            transactions = pd.concat(st.session_state['monthly_transactions'].values(), ignore_index=True)
            transactions.to_csv('transacoes.csv', index=False)
            st.sidebar.success('Dados salvos em transacoes.csv')

        if st.sidebar.button('Carregar Dados'):
            transactions = pd.read_csv('transacoes.csv')
            for _, row in transactions.iterrows():
                month = pd.to_datetime(row['Data']).month
                if month not in st.session_state['monthly_transactions']:
                    st.session_state['monthly_transactions'][month] = pd.DataFrame(columns=['Data', 'Categoria', 'Valor'])
                st.session_state['monthly_transactions'][month] = pd.concat([st.session_state['monthly_transactions'][month], pd.DataFrame([row])], ignore_index=True)
            st.sidebar.success('Dados carregados de transacoes.csv')

if __name__ == "__main__":
    app = MeuDinheiroOrganizadoApp()
    app.run()
