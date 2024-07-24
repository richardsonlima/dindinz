import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from datetime import datetime

class MeuDinheiroOrganizadoApp:
    def run(self):
        
        # Inicializar o estado da sessão para transações
        if 'transactions' not in st.session_state:
            st.session_state['transactions'] = pd.DataFrame(columns=['Data', 'Categoria', 'Valor'])
        
        # Barra lateral para entrada de dados
        st.sidebar.header('Adicionar Transação')
        date = st.sidebar.date_input('Data', datetime.today())
        category = st.sidebar.selectbox('Categoria', ['Entrada', 'Mercado', 'Aluguel', 'Utilidades', 'Lazer', 'Outros'])
        amount = st.sidebar.number_input('Valor', min_value=0.0, format="%.2f")
        
        if st.sidebar.button('Adicionar'):
            new_transaction = pd.DataFrame({'Data': [date], 'Categoria': [category], 'Valor': [amount]})
            st.session_state['transactions'] = pd.concat([st.session_state['transactions'], new_transaction], ignore_index=True)
            st.sidebar.success('Transação adicionada!')
        
        # Página principal
        st.title('Meu Dinheiro Organizado')
        
        # Exibir transações
        st.header('Histórico de Transações')
        st.dataframe(st.session_state['transactions'])
        
        # Estatísticas resumidas
        st.header('Estatísticas Resumidas')
        summary = st.session_state['transactions'].groupby('Categoria')['Valor'].sum().reset_index()
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
        time_series = st.session_state['transactions'].groupby('Data')['Valor'].sum().reset_index()
        time_series_chart = px.line(time_series, x='Data', y='Valor', title='Despesas Diárias')
        st.plotly_chart(time_series_chart)
        
        # Funcionalidade de salvar e carregar
        st.sidebar.header('Salvar/Carregar Dados')
        if st.sidebar.button('Salvar Dados'):
            st.session_state['transactions'].to_csv('transacoes.csv', index=False)
            st.sidebar.success('Dados salvos em transacoes.csv')
        
        if st.sidebar.button('Carregar Dados'):
            st.session_state['transactions'] = pd.read_csv('transacoes.csv')
            st.sidebar.success('Dados carregados de transacoes.csv')

if __name__ == "__main__":
    app = MeuDinheiroOrganizadoApp()
    app.run()

