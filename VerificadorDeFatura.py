import streamlit as st
import pandas as pd
import pdfplumber
import openai
import re
import matplotlib.pyplot as plt

# Configurar a chave da API do OpenAI
openai.api_key = 'sk-xxxx'

@st.cache_data
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def parse_transactions(text):
    pattern = re.compile(r'(\d{2}/\d{2})\s+(.+?)\s+(\d{1,3}(?:\.\d{3})*,\d{2})')
    matches = pattern.findall(text)
    transactions = [{'Data': match[0], 'Descrição': match[1], 'Valor': float(match[2].replace('.', '').replace(',', '.'))} for match in matches]
    return transactions

def categorize_transactions(transactions):
    categories = {
        'FastFood': ['DRIVE PRESTES MAIA GAR', 'MASTER TEAM FOODS', 'BURGER', 'JERONIMO PAINEIRAS TRA'], 
        'Refeições': ['LANCHONETE'], 
        'Restaurante': ['TBB GESTAO DE RESTAURA'],
        'Cafeteria': ['STARBUCKS', 'Cafe', 'Cafeteria'],
        'Rotisserie': ['ROTISSERIE'],
        'Chocolateria': ['CACAU SHOW'],
        'Mercado': ['PAO DE ACUCAR', 'CARREFOUR', 'PAO DE ACUCAR', 'PALACIO'],
        'SuperMercado': ['PAO DE ACUCAR', 'CARREFOUR','PAO DE ACUCAR', 'PALACIO'],
        'HiperMercado': ['PAO DE ACUCAR', 'CARREFOUR', 'PAO DE ACUCAR', 'PALACIO'],
        'Hortifruti': ['HORTIFRUTI'],
        'Sacolao': ['SETE DIAS SACOLAO LTD'],
        'Frigorifico': ['PAG*CasaDeCarnesOMeu'],
        'Casa de Carnes': ['SWIFT'],
        'Mercado Condominio': ['SMART BREAK'],
        'Shopping': ['AVG - SHOP. FREI CANEC', 'GRAND PLAZA', 'MULTIPLAN', 'VIVA MORUMBI'],
        'Presentes/Brinquedos Sabrina': ['DREAM STORE','PB KIDS', 'RI HAPPY'],
        'Drinks': ['EMPORIO E ADEGA FERREI', 'EMPORIO PERECIVEIS LTD'],
        'E-commerce': ['MERCADOLIVRE'],
        'Farmácias': ['DROGASIL', 'DROGARIA', 'PHARMACIA'],
        'Saúde': ['BEEP SAUDE'],
        'Vestuário': ['PAG*Renner', 'NETSHOES', 'CEA PSA', 'LOJAS RENNER','PAG*LojasRenner', 'VANS SHOPPIN-CT', 'CENTAURO'],
        'Estacionamento': ['EstacionMatti', 'PARK PLACE'],
        'Insumos Escritório/Tech': ['KALUNGA', 'PAPELARIA'],
        'Combustível': ['AUTO POSTO'],
        'Plantas/Paisagismo': ['AbcGarden'],
        'Escolar': ['EDUCANDARIO', 'EDUCANDINHO'],
        'Presentes': ['FLORES'],
        'Insumos Casa': ['LEROY MERLIN', 'CamicadoHousew'],
        'IPVA': ['ZUL IPVA', 'ZUL 3 cartoes'],
        'Assinatura On-line': ['MICROSOFT', 'Google', 'Amazon', 'Apple', 'AWS'],
        'Perfumaria': ['ParFun'],
        'Ingressos On-line': ['SYMPLA'],
        'Odonto': ['ALIG INVISALIG'],
        'Livraria': ['LeituraAbc'],
        'Acessorios Masculinos': ['TON TJ ACESSOR'],
        'Moradia': ['ALUGUEL QUINTOANDAR', 'QUINTOANDAR'],
        'Academia/Gym/Jiujitsu': ['ALLIANCE SAO CAETANO', 'ITALY A ACAD*PAC CENTR'],
        'Hospedagem': ['E-2478772-HOTEL GU06/06', 'Hotel', 'HOTEL'],
        # Adicione mais categorias e padrões conforme necessário
    }
    for transaction in transactions:
        descricao_upper = transaction['Descrição'].upper()
        for category, keywords in categories.items():
            if any(keyword.upper() in descricao_upper for keyword in keywords):
                transaction['Categoria'] = category
                break
        else:
            transaction['Categoria'] = 'Outros'
    return transactions

def analyze_text_with_openai(df):
    category_totals = df.groupby('Categoria')['Valor'].sum().to_dict()
    total_spent = df['Valor'].sum()
    
    insights_request = f"""
    Você é um especialista financeiro. Abaixo estão os dados de uma fatura de cartão de crédito categorizados por tipo de despesa. Analise os dados e forneça insights detalhados sobre os gastos. Dê sugestões específicas para reduzir despesas e melhorar a saúde financeira do usuário.

    Dados da fatura:
    - Totais gastos por categoria: {category_totals}
    - Total gasto no período: R$ {total_spent:.2f}

    Para cada categoria, considere os seguintes pontos:
    1. A razão por trás do nível de gastos nesta categoria.
    2. Sugestões específicas para reduzir gastos nesta categoria.
    3. Recomendações de práticas financeiras saudáveis.

    Por favor, forneça uma análise detalhada e sugestões práticas.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "Você é um especialista financeiro que ajuda as pessoas a entender e melhorar suas finanças pessoais."},
            {"role": "user", "content": insights_request}
        ]
    )
    return response['choices'][0]['message']['content']

def plot_expenses_by_category(df):
    df['Valor'] = df['Valor'].astype(float)
    category_totals = df.groupby('Categoria')['Valor'].sum().sort_values()
    
    fig, ax = plt.subplots()
    category_totals.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_title('Despesas por Categoria', fontsize=14, fontweight='bold')
    ax.set_xlabel('Total Gasto (R$)', fontsize=12)
    ax.set_ylabel('Categoria', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    st.pyplot(fig)

def format_text_extracted(text):
    lines = text.split('\n')
    formatted_text = []
    for line in lines:
        if line.strip():
            formatted_text.append(line.strip())
    return '\n'.join(formatted_text)

def format_analysis_text(text):
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        if line.strip():
            formatted_lines.append(f"<p>{line.strip()}</p>")
    return '\n'.join(formatted_lines)

def chat_with_openai(user_input, df):
    category_totals = df.groupby('Categoria')['Valor'].sum().to_dict()
    total_spent = df['Valor'].sum()
    
    chat_request = f"""
    Dados da fatura:
    - Totais gastos por categoria: {category_totals}
    - Total gasto no período: R$ {total_spent:.2f}

    Usuário: {user_input}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "Você é um especialista financeiro que ajuda as pessoas a entender e melhorar suas finanças pessoais."},
            {"role": "user", "content": chat_request}
        ]
    )
    return response['choices'][0]['message']['content']

def main():
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 5px;
    }
    .stTextArea textarea {
        background-color: #f0f2f6;
        border: 2px solid #4CAF50;
        color: #333;
        font-size: 16px;
    }
    .stDataFrame table {
        border-collapse: collapse;
        width: 100%;
        border: 1px solid #ddd;
    }
    .stDataFrame table th, .stDataFrame table td {
        text-align: left;
        padding: 8px;
    }
    .stDataFrame table tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    .stMarkdown p {
        font-size: 16px;
        line-height: 1.6;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("💳 Análise de Faturas de Cartão de Crédito")
    
    uploaded_file = st.file_uploader("📁 Escolha um arquivo PDF", type="pdf")
    
    if uploaded_file is not None:
        st.write("🛠️ Processando o arquivo...")
        text = extract_text_from_pdf(uploaded_file)
        formatted_text = format_text_extracted(text)
        
        st.subheader("📄 Texto extraído do PDF:")
        st.text_area("Texto Extraído", value=formatted_text, height=300)
        
        st.subheader("🔍 Transações encontradas:")
        transactions = parse_transactions(text)
        transactions = categorize_transactions(transactions)
        df = pd.DataFrame(transactions)
        st.dataframe(df.style.format({"Valor": "R$ {:.2f}"}))

        st.subheader("📊 Totais gastos por categoria:")
        category_totals = df.groupby('Categoria')['Valor'].sum()
        st.dataframe(category_totals.apply(lambda x: f"R$ {x:,.2f}"))

        total_spent = df['Valor'].sum()
        st.write(f"**Total gasto no período:** R$ {total_spent:,.2f}")
        
        st.subheader("📊 Gráfico de Despesas por Categoria:")
        plot_expenses_by_category(df)
        
        st.subheader("🧠 Insights financeiros via Inteligência Artificial (modelo: gpt-4o):")
        analysis = analyze_text_with_openai(df)
        formatted_analysis = format_analysis_text(analysis)
        st.markdown(formatted_analysis, unsafe_allow_html=True)

        st.subheader("💬 Interaja com os dados")
        user_input = st.text_input("Faça uma pergunta sobre seus gastos:")
        if user_input:
            chat_response = chat_with_openai(user_input, df)
            st.markdown(chat_response, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
